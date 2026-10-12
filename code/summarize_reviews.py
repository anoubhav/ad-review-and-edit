"""Summarize review marks per axis: the release's round, or reviews downloaded from review/review.html.

    python3 code/summarize_reviews.py data/round
    python3 code/summarize_reviews.py reviews.marks.csv reviews.ad_marks.csv
    python3 code/summarize_reviews.py data/round my_reviews/      (pool several sources)

Each argument is a marks.csv or ad_marks.csv file, or a folder holding files whose names end in
marks.csv or ad_marks.csv. Python 3 standard library only.

Definitions are the ones in docs/DATA.md and code/reproduce.py:
  unit      one scene on one axis (one ad for sound); a unit is asked when a marks row exists for it
  any       at least one reviewer who was asked marked the unit
  majority  more than half of the reviewers who were asked marked it
  from accepted findings   the share of marks (marked = 1 rows) with mark_from_accepted_finding = 1
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

AXES = ["product", "scene", "script", "pronunciation", "caption_placement", "caption_relevance"]


def find_files(args):
    marks, ad_marks = [], []
    for a in args:
        p = Path(a)
        files = sorted(p.iterdir()) if p.is_dir() else [p]
        for f in files:
            if not f.is_file():
                continue
            if f.name.endswith("ad_marks.csv"):
                ad_marks.append(f)
            elif f.name.endswith("marks.csv"):
                marks.append(f)
            elif not p.is_dir():
                sys.exit(f"not a marks.csv or ad_marks.csv file: {f}")
    return marks, ad_marks


def read_rows(files, key):
    """Rows keyed so that the same reviewer's row on the same unit is counted once (the last file wins)."""
    out, dup = {}, 0
    for f in files:
        with open(f, newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                k = key(r)
                dup += k in out
                out[k] = r
    return list(out.values()), dup


def pct(n, d):
    return f"{n} ({100.0 * n / d:.1f}%)" if d else "0 (n/a)"


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    marks_files, ad_files = find_files(argv)
    if not marks_files and not ad_files:
        sys.exit("no marks.csv or ad_marks.csv files found")
    marks, dup_m = read_rows(marks_files, lambda r: (r["reviewer"], r["scene_id"], r["axis"]))
    ad_marks, dup_a = read_rows(ad_files, lambda r: (r["reviewer"], r["ad_id"], r["axis"]))

    cells = defaultdict(lambda: defaultdict(list))   # axis -> unit -> [marked per asked reviewer]
    n_marks, n_accepted = defaultdict(int), defaultdict(int)
    for r in marks:
        m = int(r["marked"])
        cells[r["axis"]][r["scene_id"]].append(m)
        if m:
            n_marks[r["axis"]] += 1
            n_accepted[r["axis"]] += r.get("mark_from_accepted_finding") == "1"
    for r in ad_marks:
        m = int(r["marked"] or 0)
        cells[r["axis"]][r["ad_id"]].append(m)
        n_marks[r["axis"]] += m

    reviews = {(r["reviewer"], r["ad_id"]) for r in marks} | {(r["reviewer"], r["ad_id"]) for r in ad_marks}
    print(f"Files: {len(marks_files)} marks, {len(ad_files)} ad_marks. Reviews: {len(reviews)}. "
          f"Reviewers: {len({r for r, _ in reviews})}.")
    if dup_m or dup_a:
        print(f"Note: {dup_m + dup_a} rows repeat a reviewer on the same unit; the last file read was kept.")
    print()
    head = ("axis", "units asked", "marked by any", "marked by a majority", "marks", "from accepted findings")
    rows = []
    for axis in AXES + sorted(a for a in cells if a not in AXES):
        units = cells.get(axis)
        if not units:
            continue
        n = len(units)
        any_ = sum(1 for v in units.values() if any(v))
        maj = sum(1 for v in units.values() if sum(v) * 2 > len(v))
        unit_word = ("ad" if n == 1 else "ads") if axis == "sound" else ("scene" if n == 1 else "scenes")
        acc = "n/a (no judge findings)" if axis == "sound" else pct(n_accepted[axis], n_marks[axis])
        rows.append((axis, f"{n} {unit_word}", pct(any_, n), pct(maj, n), str(n_marks[axis]), acc))
    widths = [max(len(x[i]) for x in rows + [head]) for i in range(len(head))]
    for line in [head] + rows:
        print("  ".join(c.ljust(w) for c, w in zip(line, widths)).rstrip())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
