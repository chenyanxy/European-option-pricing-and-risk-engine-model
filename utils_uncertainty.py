import numpy as np
from scipy.stats import truncnorm

def sample_sigma(dist, n_samples = 1):
    if dist["type"] != "truncated_normal":
        raise NotImplementedError(f"Only 'truncated_normal' is implemented, got {dist['type']}")

    mean = dist["mean"]
    std = dist["std"]
    lower, upper = dist["bounds"]

    #Truncnorm bounds
    a = (lower - mean) / std
    b = (upper - mean) / std

    #Sample from truncnorm
    samples = truncnorm.rvs(a, b, loc=mean, scale=std, size=n_samples)

    #Return single float
    return float(samples[0]) if n_samples == 1 else samples

def get_input_or_estimate(value, estimator_fn=None, name="parameter"):
    if value is not None:
        return value
    if estimator_fn is not None:
        return estimator_fn()
    raise ValueError(f"No estimator provided for {name}.")

