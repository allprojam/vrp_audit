"""BTC variance risk premium: existence (C1) vs harvestability (C2).

Implements docs/HYPOTHESIS.md exactly. Reads data/*.csv only -- no network.

    python3 src/vrp.py            # writes runs/vrp.json

Gates are the ones written in the prereg, evaluated as written (I-7).
"""
import csv, json, math, pathlib, statistics as st

ROOT = pathlib.Path(__file__).resolve().parent.parent
H = 30                      # 30-day realized window
COSTS_BP = [0, 5, 10, 20, 40]   # round-trip cost sweep, bps of notional


def load(name):
    with (ROOT / "data" / name).open() as f:
        return {r["date"]: r for r in csv.DictReader(f)}


def estimators(rows, i):
    """Realized vol over the NEXT H days, three ways, annualised.

    CC  = close-to-close std of log returns
    PK  = Parkinson (high/low range)  -- uses intraday extremes, not just closes
    GK  = Garman-Klass (OHLC)         -- the most efficient of the three
    """
    seg = rows[i:i + H]
    if len(seg) < H:
        return None
    cl = [float(r["close"]) for r in seg]
    lr = [math.log(cl[k + 1] / cl[k]) for k in range(len(cl) - 1)]
    cc = st.stdev(lr) * math.sqrt(365)

    pk_num, pk_den = 0.0, 0.0
    gk_num, gk_den = 0.0, 0.0
    for k in range(H - 1):
        hi, lo = float(seg[k]["high"]), float(seg[k]["low"])
        op, c = float(seg[k]["open"]), float(seg[k]["close"])
        if hi <= 0 or lo <= 0:
            continue
        pk_num += math.log(hi / lo) ** 2
        pk_den += 1
        if op > 0 and c > 0:
            gk_num += 0.5 * math.log(hi / lo) ** 2 - (2 * math.log(2) - 1) * math.log(c / op) ** 2
            gk_den += 1
    pk = math.sqrt(pk_num / pk_den / (4 * math.log(2)) * 365) if pk_den else None
    gk = math.sqrt(gk_num / gk_den * 365) if gk_den else None
    return {"cc": cc, "pk": pk, "gk": gk}


def main():
    iv_rows, px_rows = load("btc_dvol_1d.csv"), load("btc_perp_1d.csv")
    days = sorted(set(iv_rows) & set(px_rows))
    series = [px_rows[d] for d in days]

    recs = []
    for i, d in enumerate(days):
        if i + H > len(days):
            break
        e = estimators(series, i)
        if not e:
            continue
        iv = float(iv_rows[d]["close"]) / 100.0      # DVOL is in vol points
        recs.append({"date": d, "iv": iv, **e})

    out = {"n_nominal": len(recs), "n_eff": len(recs) // H, "window": [days[0], days[-1]], "estimators": {}}

    for est in ("cc", "pk", "gk"):
        pairs = [(r["iv"], r[est]) for r in recs if r[est] is not None]
        if not pairs:
            continue
        vrp = [iv - rv for iv, rv in pairs]
        # short-vol P&L per unit variance notional, unit-free
        pnl = [(iv ** 2 - rv ** 2) / iv ** 2 for iv, rv in pairs]
        cum, worst_dd = 0.0, 0.0
        for p in pnl:
            cum += p
            worst_dd = max(worst_dd, (cum - p - (cum - p * 0)) if False else 0.0)
        # drawdown of the cumulative premium path
        peak, mdd = -1e9, 0.0
        c = 0.0
        path = []
        for p in pnl:
            c += p
            path.append(c)
            peak = max(peak, c)
            mdd = max(mdd, peak - c)
        block = {
            "mean_vrp": st.mean(vrp),
            "median_vrp": st.median(vrp),
            "frac_iv_gt_rv": sum(1 for x in vrp if x > 0) / len(vrp),
            "mean_pnl_unit": st.mean(pnl),
            "cum_pnl_unit": path[-1],
            "max_drawdown_unit": mdd,
            "worst_period_pnl": min(pnl),
        }
        # G4: net of round-trip cost c bps -> cost in variance-P&L units, approximated
        # linearly on notional: c bps of notional per round trip
        block["net_mean_pnl_by_cost"] = {c: st.mean(pnl) - c / 1e4 for c in COSTS_BP}
        out["estimators"][est] = block

    # gates, as written in the prereg
    g = {}
    for est in ("cc", "pk", "gk"):
        b = out["estimators"].get(est)
        if not b:
            g[est] = None
            continue
        g[est] = {
            "G1_existence": b["mean_vrp"] > 0 and b["frac_iv_gt_rv"] >= 0.5,
            "G3_tail": b["max_drawdown_unit"] <= 0.5 * max(b["cum_pnl_unit"], 1e-9),
            "G4_cost_20bp": b["net_mean_pnl_by_cost"][20] > 0,
        }
    out["gates"] = g
    out["n_eff_ok"] = out["n_eff"] >= 30

    rp = ROOT / "runs" / "vrp.json"
    rp.parent.mkdir(exist_ok=True)
    rp.write_text(json.dumps(out, indent=1))

    print(f"n nominal {out['n_nominal']}  n_eff {out['n_eff']}  window {out['window']}")
    for est, b in out["estimators"].items():
        print(f"  {est:2s}  mean IV-RV {b['mean_vrp']:+.4f}  IV>RV {100*b['frac_iv_gt_rv']:.1f}%  "
              f"cum P&L {b['cum_pnl_unit']:+.3f}  MaxDD {b['max_drawdown_unit']:.3f}")
    print(f"  gates: {json.dumps(g)}")
    if out["n_eff"] < 30:
        print("  WARNING: n_eff < 30 -- prereg kill condition 4. No conclusion is supported.")


if __name__ == "__main__":
    main()
