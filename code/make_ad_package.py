"""Build a review-page ad package (sbs-ad-package/1) for any ad of the 120-ad round.

Reads data/round/ads.csv, scenes.csv and findings.jsonl and writes <ad_id>.json, ready for
"Load ad packages" in review/review.html (choose the package together with the ad's video,
downloaded from data/clips_manifest.csv). Findings are printed as the judges wrote them, without
the reviewers' votes; the round's pronunciation findings are not in this release.
Narration lines and captions are not in the release, so the page asks script and pronunciation
on every scene of these ads.

Run from the release root:
  python3 code/make_ad_package.py ad-3eb518b6e3 [more ad ids] [--out DIR] [--video-dir PATH]
--video-dir sets the package's "video" field to PATH/<ad_id>.mp4 (default: the file name only,
matched by name when you load the package with its video).
"""
import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROUND = ROOT / "data" / "round"
FINDING_KEYS = ["finding_id", "ad_id", "scene_id", "axis", "judge", "kind", "description", "location", "time_s",
                "span_start_s", "span_end_s", "evidence_ref", "evidence_photo_sha256"]
JUDGED_AXES = ["product", "scene", "script", "sound"]   # judges shown in the round; pronunciation left out


def build(ad_id, video_dir=None):
    ads = {r["ad_id"]: r for r in csv.DictReader(open(ROUND / "ads.csv", newline=""))}
    if ad_id not in ads:
        raise SystemExit(f"{ad_id} is not an ad of the round (see data/round/ads.csv)")
    ad = ads[ad_id]
    rows = sorted((r for r in csv.DictReader(open(ROUND / "scenes.csv", newline="")) if r["ad_id"] == ad_id),
                  key=lambda r: int(r["scene_index"]))
    scenes, start = [], 0.0
    for r in rows:
        d = float(r["duration_s"])
        scenes.append({"scene_id": r["scene_id"], "scene_index": int(r["scene_index"]), "position": r["position"],
                       "start_s": round(start, 4), "duration_s": round(d, 4), "has_caption": int(r["has_caption"])})
        start += d
    findings = []
    for line in open(ROUND / "findings.jsonl"):
        f = json.loads(line)
        if f["ad_id"] == ad_id:
            findings.append({k: f.get(k) for k in FINDING_KEYS})
    findings.sort(key=lambda f: (f["scene_id"], f["axis"], f["finding_id"]))
    video = f"{ad_id}.mp4" if video_dir is None else f"{video_dir.rstrip('/')}/{ad_id}.mp4"
    return {
        "format": "sbs-ad-package/1",
        "ad_id": ad_id,
        "product_id": ad["product_id"],
        "video": video,
        "duration_s": round(start, 3),
        "judged_axes": JUDGED_AXES,
        "sound_judge_status": ad["sound_judge_status"] or None,
        "axis_notes": {"pronunciation": "The round's pronunciation findings are not in this release."},
        "scenes": scenes,
        "findings": findings,
        "reference_photos": [],
        "text_edits": [],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ad_ids", nargs="+")
    ap.add_argument("--out", default=".", help="folder for the package files")
    ap.add_argument("--video-dir", default=None, help="path written into the package's video field")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for ad_id in a.ad_ids:
        p = build(ad_id, a.video_dir)
        path = out / f"{ad_id}.json"
        path.write_text(json.dumps(p, indent=1, ensure_ascii=False) + "\n")
        print(f"{path}: {len(p['scenes'])} scenes, {len(p['findings'])} findings")


if __name__ == "__main__":
    main()
