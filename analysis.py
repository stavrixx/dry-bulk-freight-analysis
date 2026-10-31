
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("output", exist_ok=True)


def load_bdi(path="data/bdi.csv"):
    df = pd.read_csv(path)
    # Find the date and price columns whatever the site called them
    date_col = next(c for c in df.columns if "date" in c.lower())
    price_col = next(c for c in df.columns if c.lower() in ("price", "close", "last", "value", "bdi"))
    df[date_col] = pd.to_datetime(df[date_col])
    s = (df.set_index(date_col)[price_col]
           .astype(str).str.replace(",", "").astype(float).sort_index())
    return s.resample("MS").mean().rename("bdi")         

def load_iron_ore():
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=PIORECRUSDM"
    try:
        df = pd.read_csv(url)
    except Exception:
        df = pd.read_csv("data/iron_ore.csv")            
    df.columns = ["date", "ore"]
    df["date"] = pd.to_datetime(df["date"])
    df["ore"] = pd.to_numeric(df["ore"], errors="coerce")
    return df.set_index("date")["ore"].dropna()

bdi, ore = load_bdi(), load_iron_ore()
data = pd.concat([bdi, ore], axis=1).dropna()
data = data[data.index >= "2010-09-01"]
data["ln_bdi"], data["ln_ore"] = np.log(data["bdi"]), np.log(data["ore"])
data["d_bdi"], data["d_ore"] = data["ln_bdi"].diff(), data["ln_ore"].diff()   
n_months = len(data)

out = []
out.append(f"Sample: {data.index.min():%b %Y} to {data.index.max():%b %Y} ({n_months} months)\n")


corr_levels = data["ln_bdi"].corr(data["ln_ore"])
corr_changes = data["d_bdi"].corr(data["d_ore"])
out.append(f"Correlation of log LEVELS:   {corr_levels:.2f}  (can be inflated by shared trends)")
out.append(f"Correlation of monthly CHANGES: {corr_changes:.2f}  (the more honest number)\n")


out.append("Correlation of this month's BDI change with iron ore change k months EARLIER:")
lag_rows = []
for k in range(0, 7):
    c = data["d_bdi"].corr(data["d_ore"].shift(k))
    lag_rows.append((k, c))
    out.append(f"  lag {k} months: {c:.2f}")
best = max(lag_rows, key=lambda x: abs(x[1]) if not np.isnan(x[1]) else 0)
out.append(f"Strongest lag: {best[0]} months (corr {best[1]:.2f})\n")


d = data[["d_bdi", "d_ore"]].dropna()
X = np.column_stack([np.ones(len(d)), d["d_ore"].values])
y = d["d_bdi"].values
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
resid = y - X @ beta
r2 = 1 - resid.var() / y.var()
sigma2 = resid @ resid / (len(y) - 2)
se = np.sqrt(np.diag(sigma2 * np.linalg.inv(X.T @ X)))
out.append("OLS: monthly BDI % change = a + b * monthly iron ore % change")
out.append(f"  b = {beta[1]:.2f} (std. err. {se[1]:.2f}, t = {beta[1]/se[1]:.1f}),  R-squared = {r2:.2f}")
out.append("  Interpretation: R-squared is the share of monthly BDI movement iron ore explains.\n")


out.append("Correlation of monthly changes by period (is the relationship stable?):")
for a, b in [("2010", "2014"), ("2015", "2019"), ("2020", "2022"), ("2023", "2030")]:
    sub = data.loc[a:b]
    if len(sub) > 12:
        out.append(f"  {a}-{min(b, str(data.index.max().year))}: {sub['d_bdi'].corr(sub['d_ore']):.2f}  (n={len(sub)})")

open("output/results.txt", "w").write("\n".join(out))
print("\n".join(out))


fig, ax = plt.subplots(figsize=(9, 4.5))
ax.plot(data.index, data["bdi"], color="#1f4e79", label="BDI (monthly avg)")
ax.set_ylabel("BDI")
ax2 = ax.twinx()
ax2.plot(data.index, data["ore"], color="#c55a11", label="Iron ore (USD/t)")
ax2.set_ylabel("Iron ore, USD per tonne")
ax.set_title("Baltic Dry Index vs. iron ore price")
fig.legend(loc="upper left", bbox_to_anchor=(0.1, 0.88))
fig.tight_layout(); fig.savefig("output/levels.png", dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(5.5, 4.5))
ax.scatter(d["d_ore"], d["d_bdi"], s=12, alpha=0.6, color="#1f4e79")
xs = np.linspace(d["d_ore"].min(), d["d_ore"].max(), 50)
ax.plot(xs, beta[0] + beta[1] * xs, color="#c55a11")
ax.set_xlabel("Iron ore monthly % change (log)"); ax.set_ylabel("BDI monthly % change (log)")
ax.set_title(f"Monthly changes, R² = {r2:.2f}")
fig.tight_layout(); fig.savefig("output/scatter.png", dpi=150); plt.close(fig)
