# main.py
import numpy as np
from config import (
    S0, K, r, sigma_input, T,
    S_max, M, N,
    MC_paths, VAR_Paths,
    Sigma_dist, MU_Scenario,
    mu_base, dt, alpha,
    stress_config
)
from utils_uncertainty import sample_sigma, get_input_or_estimate
from pde_pricer import price_european_call_pde
from mc_pricer import price_european_call_mc
from risk_engine import (
    greek_delta, greek_gamma, greek_vega,
    mc_var_gbm, scenario_var_table
)

def main():
    print("=== Realistic Option & Risk Engine ===\n")

    # Resolve / sample volatility (subjective / uncertain)
    sigma = get_input_or_estimate(
        sigma_input,
        estimator_fn=lambda: sample_sigma(Sigma_dist),
        name="sigma"
    )
    print(f"Using volatility (sigma): {sigma:.4f} (sampled from truncated normal)")

    # Price option via PDE (structural model)
    pde_price = price_european_call_pde(
        S0, K, r, sigma, T,
        S_max=S_max, M=M, N=N
    )
    print(f"\nPDE call price: {pde_price:.4f}")

    # Price option via Monte Carlo (model check)
    mc_price, mc_err = price_european_call_mc(
        S0, K, r, sigma, T, n_paths=MC_paths
    )
    ci_low = mc_price - 1.96 * mc_err
    ci_high = mc_price + 1.96 * mc_err
    print(f"MC call price:  {mc_price:.4f}  (95% CI: [{ci_low:.4f}, {ci_high:.4f}])")

    # Greeks from PDE (using same structural model)
    print("\nGreeks from PDE (finite differences):")
    delta = greek_delta(S0, K, r, sigma, T, S_max=S_max, M=M, N=N)
    gamma = greek_gamma(S0, K, r, sigma, T, S_max=S_max, M=M, N=N)
    vega = greek_vega(S0, K, r, sigma, T, S_max=S_max, M=M, N=N)
    print(f"Delta: {delta:.4f}")
    print(f"Gamma: {gamma:.6f}")
    print(f"Vega : {vega:.4f}")

    # 1-day VaR on underlying in "neutral" drift view
    print("\n1-day VaR on 1 share (neutral drift view):")
    var_neutral = mc_var_gbm(
        S0, mu_base, sigma, dt, alpha=alpha, n_paths=VAR_Paths,
        vol_mult=1.0,
        jump_prob=0.0,
        jump_size=0.0
    )
    print(f"{int(alpha * 100)}% 1-day VaR (normal regime): {var_neutral:.4f}")

    var_neutral_stress = mc_var_gbm(
        S0, mu_base, sigma, dt, alpha=alpha, n_paths=VAR_Paths,
        vol_mult=stress_config["vol_mult"],
        jump_prob=stress_config["jump_prob"],
        jump_size=stress_config["jump_size"]
    )
    print(f"{int(alpha * 100)}% 1-day VaR (stressed regime): {var_neutral_stress:.4f}")

    # Subjective drift scenarios (bear/neutral/bull) with and without stress
    print("\nScenario VaR table (subjective drift + stress):")
    rows = scenario_var_table(
        S0, sigma, dt, alpha, VAR_Paths, MU_Scenario, stress_config
    )
    for row in rows:
        print(
            f"Scenario: {row['scenario']:7s} | "
            f"mu={row['mu']:+.2%} | "
            f"Var_normal={row['Var_normal']:.4f} | "
            f"Var_stress={row['Var_stress']:.4f}"
        )

    #Parameter-uncertainty pricing band (sigma sampled many times)
    print("\nParameter uncertainty band on PDE price (sampling sigma):")
    n_sigma_samples = 50
    prices = []
    sigmas = []
    for _ in range(n_sigma_samples):
        s_sample = sample_sigma(Sigma_dist)
        p = price_european_call_pde(S0, K, r, s_sample, T, S_max=S_max, M=M, N=N)
        prices.append(p)
        sigmas.append(s_sample)

    prices = np.array(prices)
    sigmas = np.array(sigmas)
    print(f"Sigma mean: {sigmas.mean():.4f}, std: {sigmas.std(ddof=1):.4f}")
    print(
        f"PDE price mean: {prices.mean():.4f}, "
        f"5%: {np.quantile(prices, 0.05):.4f}, "
        f"95%: {np.quantile(prices, 0.95):.4f}"
    )

    print("\nDone.")

if __name__ == "__main__":
    main()