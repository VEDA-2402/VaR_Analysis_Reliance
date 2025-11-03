"""
VaR calculation for RELIANCE.NS
Methods: Historical, Parametric (Variance‑Covariance), Monte Carlo
Author: < T. VEDA VEDHYA > • Date: 2025‑07‑15
"""

import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# USER SETTINGS
TICKER            = "RELIANCE.NS"
START_DATE        = "2021-01-01"
END_DATE          = "2025-10-01"
PORTFOLIO_VALUE   = 100_000            # ₹
CONFIDENCE_LEVEL  = 0.99
N_MONTE_CARLO     = 10_000


# DOWNLOAD DATA
# auto_adjust=True gives already‑adjusted 'Close' prices

data = yf.download(TICKER,
                   start=START_DATE,
                   end=END_DATE,
                   auto_adjust=True,    # keeps only adjusted Close
                   progress=False)

if data.empty:
    raise ValueError("Yahoo Finance returned no data. Check ticker or dates.")

price = data["Close"]          # already adjusted
returns = price.pct_change().dropna()


# HISTORICAL VaR

var_hist = np.percentile(returns, (1 - CONFIDENCE_LEVEL) * 100)
VaR_hist_value = float(-var_hist * PORTFOLIO_VALUE)


# PARAMETRIC VaR (Variance‑Covariance, Normal assumption)

μ  = returns.mean()
σ  = returns.std()
z  = norm.ppf(1 - CONFIDENCE_LEVEL)    # ≈ ‑1.645 for 95 %
var_param = -(μ + z * σ)
VaR_param_value = float(var_param * PORTFOLIO_VALUE)


# MONTE CARLO VaR

sim_returns = np.random.normal(loc=μ, scale=σ, size=N_MONTE_CARLO)
sim_pnl     = PORTFOLIO_VALUE * sim_returns
VaR_mc_value = float(-np.percentile(sim_pnl, (1 - CONFIDENCE_LEVEL) * 100))


# PRINT RESULTS

print(f"\n— Value at Risk for {TICKER} (1‑day, {int(CONFIDENCE_LEVEL*100)}% c.l.) —")
print(f"Historical VaR   : ₹{VaR_hist_value:,.2f}")
print(f"Parametric VaR   : ₹{VaR_param_value:,.2f}")
print(f"Monte Carlo VaR  : ₹{VaR_mc_value:,.2f}")


# PLOT DISTRIBUTION & VaR THRESHOLD

plt.figure(figsize=(10, 6))
sns.histplot(returns, bins=100, kde=True)
plt.axvline(var_hist, color="red", linestyle="--",
            label=f"Historical VaR ({int(CONFIDENCE_LEVEL*100)}%)")
plt.title(f"Daily Returns Distribution — {TICKER}")
plt.xlabel("Daily Return")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

