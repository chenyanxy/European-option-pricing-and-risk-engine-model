#Risk engine
import numpy as np
from pde_pricer import price_european_call_pde
from mc_pricer import simulate_gbm_terminal

# Greek from PDE

def greek_delta(S0, K, r, sigma, T, h=1e-2, **pde_kwargs): # Finite Delta
    V_plus = price_european_call_pde(S0 + h, K, r, sigma, T,**pde_kwargs)
    V_0 = price_european_call_pde(S0, K, r, sigma, T,**pde_kwargs)
    V_minus = price_european_call_pde(S0 - h, K, r, sigma,T, **pde_kwargs)
    return(V_plus - V_minus) / (2*h)

def greek_gamma(S0, K, r, sigma, T, h=1e-2, **pde_kwargs): # Finite Gamma
    V_plus = price_european_call_pde(S0 + h, K, r, sigma, T, **pde_kwargs)
    V_0 = price_european_call_pde(S0, K, r, sigma, T, **pde_kwargs)
    V_minus = price_european_call_pde(S0 - h, K, r, sigma,T, **pde_kwargs)
    return (V_plus - 2 * V_0 + V_minus) / (h**2)

def greek_vega(S0, K, r, sigma, T, h=1e-3, **pde_kwargs):
    V_plus = price_european_call_pde(S0, K, r, sigma + h, T, **pde_kwargs)
    V_minus = price_european_call_pde(S0, K, r, sigma - h,T, **pde_kwargs)
    return(V_plus - V_minus) / (2*h)

#VaR engine
def mc_var_gbm(
        S0, mu, sigma, dt, alpha=0.95, n_paths=100_000,
        vol_mult=1.0, jump_prob=0.0, jump_size=0.0
):
    ST = simulate_gbm_terminal(
        S0, mu, sigma, dt, n_paths,
        vol_mult=vol_mult, jump_prob=jump_prob, jump_size=jump_size,
    )
    pnl = ST - S0
    loss = -pnl
    var = np.quantile(loss, alpha)
    return float(var)

def scenario_var_table(S0, sigma, dt, alpha, n_paths, mu_scenarios, stress_config):
    rows = []
    for label, mu in mu_scenarios.items():
        var_normal = mc_var_gbm( #Normal regime
            S0, mu, sigma, dt, alpha=alpha, n_paths=n_paths,
            vol_mult=1.0,
            jump_prob=0.0,
            jump_size=0.0
        )
        var_stress = mc_var_gbm( # Stressed regime VaR
            S0, mu, sigma, dt, alpha=alpha, n_paths=n_paths,
            vol_mult=stress_config["vol_mult"],
            jump_prob=stress_config["jump_prob"],
            jump_size=stress_config["jump_size"]
        )

        rows.append({
            "scenario": label,
            "mu": mu,
            "Var_normal":var_normal,
            "Var_stress":var_stress,
        })
    return rows