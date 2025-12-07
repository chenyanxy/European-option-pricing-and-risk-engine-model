import math

#Parameter
S0 = 100.00
K = 120
r = 0.0414
sigma_input = None
T= 1

# PDE setting
S_max = 4*S0    # upper bound of S in PDE grid
M = 200         # number of price step
N = 500        # number of time step

# Monte carlo setting
MC_paths = 100_000 # Option pricing
VAR_Paths = 100_000 # risk / VaR

# Volatility
Sigma_dist = {
    "type": "truncated_normal",
    "mean": 0.20,
    "std": 0.05,
    "bounds": (0.50, 0.80)
}

#Drift
MU_Scenario = {
    "bear": -0.10,
    "neutral": 0.00,
    "bull": 0.08
}
mu_base = MU_Scenario["neutral"]
dt= 1/252

alpha = 0.95

#Stress parameters
stress_config = {
    "vol_mult": 3.0,
    "jump_prob": 0.02,
    "jump_size": -0.25,
}