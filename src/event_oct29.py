#!/usr/bin/env python3
"""Oct 29 2026 Binance-hack event snapshot — EXPLORATORY, NOT PRE-REGISTERED.

Writes runs/oct29_event.json. Does NOT touch runs/vrp.json or the e1cc0def lock.

IMPORTANT: this measurement was OBSERVED before any lock (see docs/ADDENDUM_04.md). It is
therefore exploratory and carries the 0.85 prose ceiling. It is NOT a pre-registered result
and must never be reported as one.

Deribit daily bars are 00:00 UTC (verified), not 08:00 UTC.
"""
import csv, json, math, pathlib, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://www.deribit.com/api/v2/public"


def get(path, **kw):
    q = "&".join(f"{k}={v}" for k, v in kw.items())
    r = urllib.request.Request(f"{BASE}/{path}?{q}", headers={"User-Agent": "vrp-audit/1.0"})
    with urllib.request.urlopen(r, timeout=30) as f:
        return json.loads(f.read().decode())["result"]


def main():
    now = int(time.time() * 1000)
    asof = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now / 1000))

    px = get("get_tradingview_chart_data", instrument_name="BTC-PERPETUAL",
             start_timestamp=now - 2 * 86400000, end_timestamp=now, resolution="1D")
    i = len(px["ticks"]) - 1
    O, H, L, C = px["open"][i], px["high"][i], px["low"][i], px["close"][i]
    day = time.strftime("%Y-%m-%d", time.gmtime(px["ticks"][i] / 1000))

    iv = get("get_volatility_index_data", currency="BTC",
             start_timestamp=now - 2 * 86400000, end_timestamp=now, resolution="1D")["data"][-1]

    cc = abs(math.log(C / O)) * math.sqrt(365)                       # V-08: sqrt(365)
    pk = math.sqrt(math.log(H / L) ** 2 / (4 * math.log(2)) * 365)
    gk = math.sqrt((0.5 * math.log(H / L) ** 2
                    - (2 * math.log(2) - 1) * math.log(C / O) ** 2) * 365)

    out = {
        "asof_utc": asof,
        "day": day,
        "bar_closed": False,      # 00:00 UTC close is later than asof
        "exploratory": True,
        "preregistered": False,
        "perp": {"open": O, "high": H, "low": L, "close": C},
        "iv_now": iv[4], "iv_open": iv[1], "iv_high": iv[2], "iv_low": iv[3],
        "iv_change_from_open": (iv[4] - iv[1]) / iv[1],
        "rv_single_day": {"cc": cc, "pk": pk, "gk": gk},
        "intraday_range_pct": (H / L - 1) * 100,
        "utc_daily_move_pct": (C / O - 1) * 100,
        "rv_gt_iv": {"cc": cc > iv[4] / 100, "pk": pk > iv[4] / 100, "gk": gk > iv[4] / 100},
        "cc_vs_gk_ratio": gk / cc,
    }
    rp = ROOT / "runs" / "oct29_event.json"
    rp.write_text(json.dumps(out, indent=1))

    print(f"as-of {asof}  (bar CLOSED: {out['bar_closed']})  EXPLORATORY, not pre-registered")
    print(f"  O={O} H={H} L={L} C={C}")
    print(f"  IV {out['iv_open']:.2f} -> {out['iv_now']:.2f}  ({out['iv_change_from_open']*100:+.1f}%)")
    print(f"  single-day RV:  CC {cc*100:.1f}%   PK {pk*100:.1f}%   GK {gk*100:.1f}%   (IV {out['iv_now']:.1f}%)")
    print(f"  RV>IV:  CC {out['rv_gt_iv']['cc']}   PK {out['rv_gt_iv']['pk']}   GK {out['rv_gt_iv']['gk']}")
    print(f"  intraday range {out['intraday_range_pct']:.2f}%   UTC move {out['utc_daily_move_pct']:+.2f}%")
    print(f"  GK/CC ratio {out['cc_vs_gk_ratio']:.2f}x")
    print(f"  -> {rp.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
