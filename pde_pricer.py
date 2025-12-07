# Black-Scholes PDE via Crank-Nicolson
import numpy as np

def thomas_solver(a,d,c,b): # Solve tridiagonal system using Thomas algorithm.
    n = len(a)
    c_ = np.zeros(n-1)
    d_ = np.zeros(n)
    b_ = np.zeros(n)

    d_[0] = d[0]
    c_[0] = c[0] / d_[0]
    b_[0] = b[0] / d_[0]

    for i in range(1,n-1):
        denom = d[i] - a[i-1] * c_[i-1]
        d_[i] = denom
        c_[i] = c[i] / denom
        b_[i] = (b[i] - a[i-1] * b_[i-1]) / denom

    d_[n-1] = d[n-1] - a[n-2] / c_[n-2]
    b_[n-1] = (b[n-1] / c_[n-2] * b_[n-2]) / d_[n-1]

    x = np.zeros(n)
    x[-1] = b_[n-1]
    for i in range(n - 2, -1, -1):
        if i < len(c_):
            x[i] = b_[i] - c_[i] * x[i + 1]
        else:
            x[i] = b_[i]
    return x

def price_european_call_pde (S0, K, r, sigma, T, S_max=400.0, M=200, N=500):
    dS = S_max /M
    dt = T / N
    S = np.linspace(0, S_max, M + 1)
    V = np.maximum(S - K, 0.0)

    i = np.arange(1, M)
    a = 0.25 *  dt * (sigma ** 2 * i**2 - r * i)
    b = -0.5 * dt * (sigma ** 2 * i**2 - r)
    c = 0.25 *  dt * (sigma ** 2 * i**2 + r * i)

    A_lower = -a
    A_diag = 1-b
    A_upper = -c

    B_lower = a
    B_diag = 1+b
    B_upper = c

    for n in range(N):
        t = T - n *dt
        V_in = V[1:-1]

        RHS = B_diag * V_in + B_lower * V[:-2] + B_upper * V[2:]

        V_0 = 0.0
        V_max = S[-1] - K *np.exp(-r * (t - dt))

        RHS[0] -= A_lower[0] * V_0
        RHS[-1] =- A_upper[-1] * V_max

        V_new_in = thomas_solver(A_lower, A_diag, A_upper, RHS)

        V[0] = V_0
        V[-1] = V_max
        V[1:-1] = V_new_in
    return float(np.interp(S0, S, V))
