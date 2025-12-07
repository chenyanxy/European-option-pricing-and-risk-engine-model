import numpy as np

def simulate_gbm_terminal(
        S0, mu, sigma, dt, n_paths,
        vol_mult=1.0, jump_prob=0.0, jump_size=0.0
):
    sigma_stress = sigma * vol_mult
    Z = np.random.normal(size=n_paths)
    ST = S0 * np.exp(
        (mu - 0.5 * sigma_stress**2) * dt + sigma_stress * np.sqrt(dt) * Z

    )

    if jump_prob > 0.0 and jump_size != 0.0:
        jumps = np.random.normal(n_paths) < jump_prob
        ST[jumps] *= (1.0 + jump_size)

    return ST

def price_european_call_mc(S0, K, r, sigma, T, n_paths=100_00, antithetic=True): # Risk-neutral Monte Carlo pricing of European call
    if antithetic:
        n_half = n_paths // 2
        Z = np.random.normal(size=n_half)
        Z = np.concatenate([Z, -Z])
    else:
        Z = np.random.normal(size=n_paths)

    ST= S0 * np.exp((r-0.5*sigma**2) * T + sigma * np.sqrt(T) * Z)
    payoff = np.maximum(ST - K, 0.0)

    disc_factor = np.exp(-r * T)
    price = disc_factor * np.mean(payoff)
    stderr = disc_factor * np.std(payoff, ddof=1) /np.sqrt(len(payoff))
    return float(price), float(stderr)

