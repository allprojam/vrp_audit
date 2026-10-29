"""Fetch BTC DVOL + perpetual OHLC from Deribit into committable CSVs.

Run ONCE. After this, analysis reads data/*.csv with no network, so the study is
reproducible offline (ARCHITECTURE.md data rule).

Verified limits (do not fight them):
  - get_volatility_index_data returns at most 1000 daily points regardless of span.
  - There is no historical bid/ask archive; options snapshots are current-only.

Usage: python3 src/fetch.py
"""
import csv, json, pathlib, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
UA = {"User-Agent": "vrp-audit/1.0"}
BASE = "https://www.deribit.com/api/v2/public"


def get(path, **params):
    q = "&".join(f"{k}={v}" for k, v in params.items())
    req = urllib.request.Request(f"{BASE}/{path}?{q}", headers=UA)
    with urllib.request.urlopen(req, timeout=30) as f:
        return json.loads(f.read().decode())["result"]


def day(ms):
    return time.strftime("%Y-%m-%d", time.gmtime(ms / 1000))


def main():
    DATA.mkdir(exist_ok=True)
    now = int(time.time() * 1000)

    # 1) DVOL -- capped at 1000 points by the API, ask for 3 years to be sure we get all of it
    iv = get("get_volatility_index_data", currency="BTC",
             start_timestamp=now - 1100 * 86400000, end_timestamp=now, resolution="1D")["data"]
    ivp = DATA / "btc_dvol_1d.csv"
    with ivp.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "open", "high", "low", "close"])   # row order verified: [ts, o, h, l, c]
        for r in iv:
            w.writerow([day(r[0]), r[1], r[2], r[3], r[4]])
    print(f"dvol  -> {ivp.relative_to(ROOT)}  {len(iv)} rows  {day(iv[0][0])} .. {day(iv[-1][0])}")

    # 2) perpetual OHLC for realized vol (need high/low for Parkinson & Garman-Klass)
    px = get("get_tradingview_chart_data", instrument_name="BTC-PERPETUAL",
             start_timestamp=now - 1100 * 86400000, end_timestamp=now, resolution="1D")
    ppp = DATA / "btc_perp_1d.csv"
    cols = ["ticks", "open", "high", "low", "close"]
    rows = list(zip(*[px[c] for c in cols]))
    with ppp.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "open", "high", "low", "close"])
        for t, o, h, l, c in rows:
            w.writerow([day(t), o, h, l, c])
    print(f"perp  -> {ppp.relative_to(ROOT)}  {len(rows)} rows  {day(rows[0][0])} .. {day(rows[-1][0])}")

    # 3) current options chain snapshot -- for context on quoted spreads, NOT for backtesting
    b = get("get_book_summary_by_currency", currency="BTC", kind="option")
    live = [x for x in b if x.get("bid_price") and x.get("ask_price")]
    snp = DATA / "btc_options_snapshot.csv"
    with snp.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["instrument", "mark_iv", "bid", "ask", "underlying", "open_interest"])
        for x in sorted(live, key=lambda r: r["instrument_name"]):
            w.writerow([x["instrument_name"], x.get("mark_iv"), x.get("bid_price"),
                        x.get("ask_price"), x.get("underlying_price"), x.get("open_interest")])
    print(f"chain -> {snp.relative_to(ROOT)}  {len(live)} quotable of {len(b)}  (snapshot {day(now)})")


if __name__ == "__main__":
    main()
