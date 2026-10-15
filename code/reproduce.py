"""Recompute the paper's round counts and blind-set AUCs from this release alone.

    python3 code/reproduce.py            (run from the release root; Python 3 stdlib only)

Round (ASSISTED labels: reviewers saw the judges' findings while marking):
  ad-scene = one ad x one scene x one axis, pooling the reviewers who were asked that scene on that axis;
  any = at least one of them marked it; majority = more than half of them marked it.
  A scene is judge-flagged on an axis when findings.jsonl holds at least one finding for it on that axis.
  Pronunciation findings are not released, so a scene is judge-flagged on pronunciation when its marks.csv rows
  have judge_flagged = 1 (Fig. 4 pronunciation row; chance = judge-flagged scenes / asked scenes).
Judges hidden (60 of the round's ads, marks_judges_hidden.csv): the share of scenes marked product-wrong by each
  reviewer with judges hidden, averaged over the two reviewers, against the round's majority on the same scenes; and
  the reviewer who saw the ads both ways (the reviewer code in both marks files), with findings (marks.csv) and
  without. Shares are exact fractions; percentages are rounded half up.
Blind product set (BLIND labels): Mann-Whitney AUC of each score against label_wrong, ties counted as 0.5.
"""
import csv
import json
import math
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data"


def rows(p):
    with open(p, newline="") as f:
        return list(csv.DictReader(f))


def auc(scores, labels):
    pos = [s for s, y in zip(scores, labels) if y == 1]
    neg = [s for s, y in zip(scores, labels) if y == 0]
    tot = 0.0
    for p in pos:
        for n in neg:
            tot += 1.0 if p > n else 0.5 if p == n else 0.0
    return tot / (len(pos) * len(neg))


def pct(f):
    """Percent of an exact Fraction, rounded half up (57.5 -> 58)."""
    return math.floor(100 * f + Fraction(1, 2))


def main():
    checks = []

    def check(name, got, want, fmt="{}"):
        ok = (round(got, 2) == want) if isinstance(want, float) else (got == want)
        checks.append(ok)
        print(f"  {'OK  ' if ok else 'DIFF'} {name}: {fmt.format(got)} (paper: {want})")

    # ------------------------------------------------------------ round
    ads = rows(D / "round/ads.csv")
    scenes = rows(D / "round/scenes.csv")
    marks = rows(D / "round/marks.csv")
    findings = [json.loads(l) for l in open(D / "round/findings.jsonl")]
    flagged = defaultdict(set)
    for f in findings:
        flagged[f["axis"]].add(f["scene_id"])
    cells = defaultdict(lambda: defaultdict(list))   # axis -> scene -> [marked per asked reviewer]
    for m in marks:
        cells[m["axis"]][m["scene_id"]].append(int(m["marked"]))

    def any_(axis):
        return {s for s, v in cells[axis].items() if any(v)}

    def maj(axis):
        return {s for s, v in cells[axis].items() if sum(v) * 2 > len(v)}

    print("Review round (assisted labels)")
    check("ads", len(ads), 120)
    check("scenes", len(scenes), 562)
    pa, pm, pf = any_("product"), maj("product"), flagged["product"]
    check("product: scenes marked by any reviewer", len(pa), 391)
    check("product: scenes marked by a majority", len(pm), 335)
    check("product: scenes the judge flagged", len(pf), 396)
    check("product: marked (any) scenes the judge flagged", len(pa & pf), 354)
    check("product: people-only scenes, any", len(pa - pf), 37)
    check("product: people-only scenes, majority", len(pm - pf), 11)
    check("scene swap: scenes asked", len(cells["scene"]), 459)
    check("scene swap: marked by any reviewer", len(any_("scene")), 177)
    check("scene swap: marked by a majority", len(maj("scene")), 153)
    sa = any_("script")
    check("script: scenes marked by any reviewer", len(sa), 91)
    check("script: of those, judge-flagged", len(sa & flagged["script"]), 17)

    # pronunciation (Fig. 4): findings are not released; the judge's flag is the judge_flagged column
    pron_flag = {m["scene_id"] for m in marks if m["axis"] == "pronunciation" and m["judge_flagged"] == "1"}
    na, n_asked = any_("pronunciation"), len(cells["pronunciation"])
    check("pronunciation: scenes asked", n_asked, 562)
    check("pronunciation: scenes marked by any reviewer", len(na), 53)
    check("pronunciation: of those, judge-flagged", len(na & pron_flag), 45)
    check("pronunciation: people-only scenes, any", len(na - pron_flag), 8)
    check("pronunciation: scenes the judge flagged (chance)", f"{len(pron_flag)}/{n_asked}", "187/562")
    check("pronunciation: chance, % of scenes", round(100 * len(pron_flag) / n_asked, 1), 33.3, "{:.1f}")

    # ------------------------------------------------------------ the same ads with judges hidden
    hid = rows(D / "round/marks_judges_hidden.csv")
    ads60 = {m["ad_id"] for m in hid}
    print("\nSame ads, judges hidden (marks_judges_hidden.csv)")
    check("ads", len(ads60), 60)
    scenes60 = {s["scene_id"] for s in scenes if s["ad_id"] in ads60}
    check("scenes", len(scenes60), 280)
    asked60 = {s for s in cells["product"] if s in scenes60}
    rmaj = Fraction(len(pm & asked60), len(asked60))
    check(f"product: round majority with findings, {len(pm & asked60)}/{len(asked60)} scenes, %", pct(rmaj), 58)
    alone = defaultdict(list)       # reviewer -> [marked] on product rows with judges hidden
    for m in hid:
        if m["axis"] == "product":
            alone[m["reviewer"]].append(int(m["marked"]))
    shares = {r: Fraction(sum(v), len(v)) for r, v in alone.items()}
    mean = sum(shares.values()) / len(shares)
    parts = ", ".join(f"{r} {sum(alone[r])}/{len(alone[r])}" for r in sorted(shares, key=lambda x: int(x[1:])))
    check(f"product: judges hidden, mean of {len(shares)} reviewers ({parts}), %", pct(mean), 26)
    both = sorted({m["reviewer"] for m in hid} & {m["reviewer"] for m in marks})
    if len(both) != 1:
        check("one reviewer saw the ads both ways", len(both), 1)
    else:
        b = both[0]
        withf = [int(m["marked"]) for m in marks
                 if m["reviewer"] == b and m["axis"] == "product" and m["ad_id"] in ads60]
        k, n = sum(withf), len(withf)
        check(f"product: {b} with findings (marks.csv), {k}/{n} scenes, %", pct(Fraction(k, n)), 57)
        k, n = sum(alone[b]), len(alone[b])
        check(f"product: {b} with judges hidden, {k}/{n} scenes, %", pct(Fraction(k, n)), 19)

    # ------------------------------------------------------------ blind product set
    sc = rows(D / "blind_product_set/scores.csv")
    y = [int(r["label_wrong"]) for r in sc]
    print("\nBlind product set (blind labels)")
    check("scenes", len(sc), 120)
    check("defective scenes", sum(y), 29)
    check("ads", len({r["ad_id"] for r in sc}), 35)

    def a(col):
        return auc([float(r[col]) for r in sc], y)

    check("AUC clip judge (pv2)", a("clip_judge_pv2_wrongness"), 0.84, "{:.4f}")
    check("AUC starting-frame judge (d4)", a("frame_judge_d4_wrongness"), 0.69, "{:.4f}")
    check("AUC DOVER (official fusion)", a("dover_overall_official_wrongness"), 0.48, "{:.4f}")
    check("AUC VideoScore2 (mean of 3)", a("videoscore2_mean_wrongness"), 0.57, "{:.4f}")
    q3 = [c for c in sc[0] if c.startswith(("q35_", "q36_")) and c.endswith("_wrongness") and "seed1" not in c]
    best = max(q3, key=a)
    check(f"AUC best Qwen3.5/3.6 run ({best[:-len('_wrongness')]})", a(best), 0.73, "{:.4f}")

    print("\nAll other score columns (AUC):")
    skip = {"scene_id", "ad_id", "label_wrong"}
    for c in sc[0]:
        if c in skip or c.endswith("_status") or c.endswith("_flag"):
            continue
        print(f"  {c}: {a(c):.4f}")
    print(f"\n{sum(checks)}/{len(checks)} paper numbers reproduced")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
