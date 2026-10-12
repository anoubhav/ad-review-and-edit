# Data

This file documents every data file in the release: the ids, each file's columns, how the labels were made, where to get the clips, and what was left out. For the overview, see the [README](../README.md). The review page has its own manual in [REVIEW_PAGE.md](REVIEW_PAGE.md).

## The two parts

1. **The review round** (`data/round/`). 120 generated product video ads (562 scenes, 20 products, 6 ads per product). Reviewers checked every ad scene by scene on each axis of the review guide. They worked in a review tool that showed the judges' findings next to each scene, so they could accept (thumbs up) or reject (thumbs down) each one. The release has every reviewer's per-axis marks and every judge finding with its accept/reject votes. For pronunciation it has the marks, which scenes the judge flagged and the vote counts. The pronunciation findings themselves are not released.
2. **The blind product set** (`data/blind_product_set/`). 120 generated motion scenes from 35 ads; 29 of them have a defective product. The labels are blind: annotators never saw any judge output. The release has those labels and the per-scene scores of every baseline and judge run the paper compares on this set.

> **Labels in the two parts are not the same kind.** Round labels are **assisted**: reviewers saw the judges' findings while they marked. Use them to study the review process: coverage, what people add to the judges, and acceptance. Do not use them as blind ground truth for judge accuracy. The blind product set is the part for measuring accuracy.

## Layout

```
README.md
LICENSE: MIT text, for the code
supplementary.pdf: the paper's supplementary material
docs/DATA.md: this file
docs/REVIEW_GUIDE.md: the reviewer guide (six questions and their boundaries)
docs/REVIEW_PAGE.md: the review page manual
code/reproduce.py
code/summarize_reviews.py
code/make_ad_package.py
review/review.html
example/ad-2438b25fb3.mp4
example/ad-3eb518b6e3.mp4
example/ad-b68fbb7151.mp4
example/ad-fcb5d2fe86.mp4
example/ad-76229af005.mp4
data/round/ads.csv
data/round/scenes.csv
data/round/marks.csv
data/round/ad_marks.csv
data/round/findings.jsonl
data/round/products.csv
data/round/reference_photos.csv
data/blind_product_set/scenes.csv
data/blind_product_set/scores.csv
data/blind_product_set/reference_photos.csv
data/clips_manifest.csv
```

Video files are not in this repository (see [Clips](#clips) for where to get them), with five exceptions in `example/`: the ad annotated in the paper's Figure 2 and four more ads of the round, the review page's examples.

## Identifiers

All ids are pseudonyms: salted SHA-256, truncated. The salt is not released.

| id | form | meaning |
|---|---|---|
| `product_id` | `prod-xxxxxxxxxx` | one product (round only) |
| `ad_id` | `ad-xxxxxxxxxx` (round), `g1ad-xxxxxxxxxx` (blind set) | one generated ad |
| `scene_id` | `<ad_id>-s<k>` | scene k of that ad, counted from 1 in play order |
| `finding_id` | `f-xxxxxxxxxxxx` | one judge finding |
| `reviewer` | `R1`..`R5` | one round reviewer, numbered by their first submitted review |

## Review round files

### data/round/ads.csv (120 rows)

| column | meaning |
|---|---|
| `ad_id`, `product_id` | ids |
| `n_scenes` | scenes in the ad: 4 or 5 |
| `n_reviews` | submitted reviews of this ad: 1, 2 or 3 |
| `reviewers` | pseudonyms of those reviewers, `;`-separated |
| `sound_judge_status` | whole-ad verdict of the sound judge: `pass` or `flag`. It passed all 120 ads. |
| `ad_video_file`, `ad_video_url`, `ad_video_sha256` | file name of the rendered ad the reviewers watched, with captions and narration; the CDN link to download it; its SHA-256, blank for files we do not hold locally (all 120 rendered ads) |

### data/round/scenes.csv (562 rows)

| column | meaning |
|---|---|
| `scene_id`, `ad_id`, `product_id` | ids |
| `scene_index`, `n_scenes`, `position` | the scene's place in the ad; `position` is `first`, `middle` or `last` |
| `start_s`, `duration_s` | the scene's start and length on the ad timeline, in seconds. `start_s` is the sum of the earlier scenes' durations, which is the timeline the judges' `time_s` uses. |
| `shot_type` | `detail_macro`, `in_use`, `lifestyle`, `model_shot`, or `unset` when the generator recorded none |
| `allow_product_motion` | 1 if the generator was allowed to move the product in this clip |
| `has_caption` | 1 if a caption overlay that draws text is anchored to this scene. Only these scenes are asked the two caption axes. |
| `clip_file`, `clip_url`, `clip_sha256` | release file name of the raw generated scene clip (before overlays); the CDN link to download it; its SHA-256, blank for files we do not hold locally (166 of 562) |

### data/round/marks.csv (7,158 rows)

One row per reviewer × scene × axis that the reviewer was asked about. Scenes a reviewer was not asked do not appear. The 1,297 pronunciation rows come after the rows of the other axes.

| column | meaning |
|---|---|
| `reviewer`, `ad_id`, `scene_id` | who and where |
| `axis` | `product`, `scene` (a scene to swap), `script`, `caption_placement`, `caption_relevance` or `pronunciation` |
| `marked` | 1 if the reviewer marked the scene as having a problem on this axis |
| `secondary_options` | the reviewer's secondary options for the mark, `;`-separated; see [Secondary options](#secondary-options). The caption and pronunciation axes have none. |
| `judge_flagged` | 1 if a judge finding exists for this scene on this axis; blank for the caption axes, which have no judge. For pronunciation, 1 if the pronunciation judge flagged the scene's narrated line (its findings are not in `findings.jsonl`). |
| `thumbs_up`, `thumbs_down` | this reviewer's accept and reject votes on judge findings for this scene and axis |
| `mark_from_accepted_finding` | 1 if the scene is marked, the judge flagged it, and this reviewer accepted at least one of those findings. A 1 means the mark agrees with a finding the reviewer accepted. |
| `scene_grid_every_scene` | 1 if the review was made with the newer scene grid that asks every scene on the scene axis (49 of 278 reviews); see [Caveats](#caveats) |

#### When a scene counts as asked

- **product** and **script:** every scene. Every scene has a narration line.
- **pronunciation:** every scene. The question is asked per scene, about the scene's narrated line. In this round every scene has exactly one narrated line, so a line and a scene are the same unit.
- **caption axes:** scenes with `has_caption = 1`, plus any other scene the reviewer marked anyway.
- **scene:** every scene, except that the older grid did not ask about a scene the reviewer had already marked product-wrong (unless they marked it on the scene axis themselves).

#### When a scene counts as marked

- **product:** answer "wrong", with a row on the scene.
- **scene:** a "swap" row. A swap written automatically by a product-wrong tap does not count unless the reviewer touched it.
- **script:** answer "bad", with a row on the scene.
- **pronunciation:** answer "issues" (Mispronounced), with a row on the scene.
- **caption axes:** answer "issues", with a row on the scene.

#### Pronunciation

As on the other judged axes, reviewers saw the pronunciation judge's findings next to each scene, and accepting one wrote it into their marks. The judge flagged 187 of the 562 scenes. Its verdicts are released only as structured flags: `judge_flagged` and the reviewer's `thumbs_up` / `thumbs_down` counts (37 up and 398 down in all). No finding text is released: no quoted word, judge note or speech-recognizer transcript, and not the word a reviewer marked.

### data/round/ad_marks.csv (278 rows)

Sound is asked once per ad. There is one row per submitted review: `reviewer`, `ad_id`, `axis` (`sound`), `answer` (`ok` or `issues`) and `marked` (1 for `issues`).

### data/round/findings.jsonl (717 lines)

One JSON object per judge finding. Findings appear exactly as the review tool grouped them: the same finding carrying two secondary options appears once, with both options in `kind`.

| field | meaning |
|---|---|
| `finding_id`, `ad_id`, `scene_id` | ids |
| `axis` | `product`, `scene` or `script`. The sound judge raised no findings; the caption axes have no judge. Pronunciation findings are not in this file; which scenes the pronunciation judge flagged is in `marks.csv`. |
| `judge` | `product_clip_judge`, `scene_clip_judge`, `scene_frames_judge` or `script_judge` (see the paper's Sec. 6) |
| `kind` | the judge's secondary option(s), as a list |
| `description` | the judge's own text for the finding (model output) |
| `location` | product findings only: where on the product the judge places the defect (model output) |
| `time_s` | when the finding points, in seconds on the ad timeline; null for script findings |
| `span_start_s`, `span_end_s` | product findings only: the span the judge cited, in seconds within the scene |
| `evidence_ref` | product findings only: which reference image the judge compared against (`hero`, `gallery-N` or `sheet`) |
| `evidence_photo_sha256` | SHA-256 of that image's bytes; it matches a row in `reference_photos.csv` |
| `thumbs` | every vote a reviewer gave this finding: `{reviewer, verdict: "up" or "down", applied_to_rubric}`. `applied_to_rubric` is true when accepting the finding wrote it into that reviewer's marks. |

Counts: 505 product findings, 108 from the scene clip judge, 87 from the scene frames judge, 17 script findings. They carry 1,664 votes.

### data/round/products.csv (20 rows)

`product_id` and `n_ads`. The data files carry no retailer, brand or listing URL for a product, except where a judge description quotes on-product or listing text (see [Privacy](#privacy)). The clips show the products themselves.

### data/round/reference_photos.csv (858 rows)

The reference images the product judge was given for each ad, in its order: `ad_id`, `product_id`, `label` (`hero`, `gallery-1`..`gallery-8` or `sheet`), `kind` and `image_sha256`.

- `kind` is `catalog_photo` for the retailer's photos and `ai_product_sheet` for the product sheet our pipeline generated.
- The hashes are of the bytes downloaded from the same URLs for the paper's analysis after the round. A retailer may have re-encoded a photo since.
- The images themselves are not released.

## Blind product set files

### data/blind_product_set/scenes.csv (120 rows)

| column | meaning |
|---|---|
| `scene_id`, `ad_id`, `scene_index` | ids |
| `duration_s` | length of the raw generated clip, in seconds |
| `has_text_overlay` | 1 if the ad drew a caption over this scene. The clips themselves have no overlay. |
| `label`, `label_wrong` | blind product-fidelity label: `wrong` (1) or `ok` (0) |
| `n_votes`, `n_wrong`, `n_ok`, `n_other` | annotator-account votes on product fidelity |
| `clip_file`, `clip_url`, `clip_sha256` | release file name of the raw generated clip; the CDN link to download it; its SHA-256 (given for all 120) |

### data/blind_product_set/scores.csv (120 rows)

Every score is oriented so that **higher means more likely defective**. Columns ending in `_flag` hold a model's own yes/no verdict, as 1 or 0. The paper's numbers use the columns marked ★.

| column(s) | method |
|---|---|
| `label_wrong` | the blind label (copied from scenes.csv) |
| `dinov2_1_minus_maxcos` | DINOv2 ViT-B/14 CLS embedding. Score = 1 − max cosine between 3 frames of the scene (5%, 50% and 95% of its length) and the ad's catalog photos. |
| `clip_1_minus_maxcos` | the same with CLIP ViT-B/16 (OpenAI) |
| `dinov2_crops_1_minus_maxcos`, `clip_crops_1_minus_maxcos` | the same, with the max also taken over 9 half-size crops per frame (secondary) |
| `ocr_easyocr_mismatch`, `ocr_easyocr_status` | OCR text mismatch with EasyOCR 1.7.1. Score = the mean normalized edit distance from frame tokens to catalog-photo tokens, minimum over frames. `status`: `text`, `no_text` (scored 0) or `no_ref_text` (scored 1). |
| `ocr_tesseract_mismatch`, `ocr_tesseract_status` | the same with Tesseract 5.3.3 (secondary) |
| ★ `clip_judge_pv2_wrongness` | the deployed product clip judge: 100 − fidelity score, with a product that is absent scored 0 |
| ★ `frame_judge_d4_wrongness` | the starting-frame product judge, same score |
| `clip_judge_8frames_wrongness`, `_flag` | the clip judge's prompt, run on 8 frames of the clip as its input (newer model version) |
| ★ `dover_overall_official_wrongness` | DOVER overall score from the official fusion, negated |
| `dover_overall_swapcorrected_wrongness`, `dover_technical_wrongness`, `dover_aesthetic_wrongness` | DOVER's swap-corrected fusion and its two heads, negated (secondary) |
| `videoscore_v11_<aspect>_wrongness` | VideoScore v1.1, negated: the mean of 5 aspects, then each aspect |
| ★ `videoscore2_mean_wrongness` | VideoScore2, negated mean of the 3 soft scores |
| `videoscore2_<aspect>_wrongness` | VideoScore2 aspects, negated |
| `qwen25vl_{7b,32b_awq}_{stills,video}_wrongness`, `_flag` | Qwen2.5-VL 7B and 32B-AWQ, on stills or on native video, given the judge's prompt; same score as the judges |
| ★ `q35_9b_*`, `q36_27b_*` `_wrongness`, `_flag` | Qwen3.5-9B and Qwen3.6-27B-FP8 on 8 frames (`frames8`) or video, with thinking `on` or `off`. The best of the 8 runs (`q36_27b_frames8_off`) is the paper's "best Qwen3" number. |
| `q35_9b_{frames8,video}_on_seed1_*` | repeats with seed 1, used only to check variance; they are not reported runs |

### data/blind_product_set/reference_photos.csv (247 rows)

`ad_id`, `label` (`hero` or `gallery-N`), `kind` and `image_sha256` for the catalog photos the embedding and OCR baselines compared against. Hashes only; the images are not released.

## data/clips_manifest.csv (802 rows)

Every video file the release refers to: `file`, `set` (`round` or `blind_product_set`), `kind` (`rendered_ad` or `scene_clip`), `sha256` (given for the 516 files we hold locally, blank for the other 286), `url` (the CDN link to download the file) and `bytes` (the file's size as the CDN reports it).

## Clips

The 120 rendered round ads, the 562 round scene clips and the 120 blind-set clips are hosted on a CDN.

- To get a file, download it from the `url` column of `clips_manifest.csv`. The same link is in the `ad_video_url` or `clip_url` column next to each ad or scene.
- Save it under the name in the `file` column so it matches the tables.
- `bytes` gives each file's size.
- `sha256` gives a checksum for the 516 files we hold a local copy of (all 120 blind-set clips and 396 round scene clips), so you can check your download against it. It is blank for the other 286 files (the 120 rendered ads and 166 round scene clips). For those, compare the size with `bytes`.

## How the labels were made

**Review round (assisted).**

- Five reviewers took part. 78 ads were reviewed by three of them, 2 by two and 40 by one, for 278 submitted reviews.
- The tool ran in "badge" mode on all 120 ads: each judge finding appeared next to its scene, and reviewers were asked to accept or reject each finding.
- Accepting a finding could write it into the reviewer's marks, so a mark and an accepted finding are not independent evidence.
- Pooled labels in `reproduce.py`: **any** means at least one asked reviewer marked the scene; **majority** means more than half of them did.

**Blind product set (blind).**

- The clips were rated in a separate annotation round. Annotators never saw judge output.
- Each scene's label is the majority of the annotator accounts that rated it. Ties ("splits", 26 scenes) were dropped, as were scenes that were not motion clips.
- 5 of the 120 scenes rest on a single account's vote (see `n_votes`).
- The paper's caveat (Tab. S4): the four annotator accounts missed subtle defects, so these labels likely under-count wrong scenes.

## Secondary options

- **product:** `wrong_product`, `wrong_form` (shape or markings differ), `product_ai` (the product looks AI-made), `product_text_broken` (on-product text is garbled), with `text_low` / `text_high` grading how bad the broken text is.
- **scene:** `ai_look`, `underwhelming`, `background_change`, `impossible_motion`, `weak_ending`.
- **script:** `unsupported_claim`, `awkward_phrasing`.

Reviewers and judges choose from the same lists.

## Example ads (Figure 2 and four more)

[`example/ad-2438b25fb3.mp4`](../example/ad-2438b25fb3.mp4) (15 s, 640x360) is the ad the paper annotates scene by scene in Figure 2. Its rows in this release use the same id: `ads.csv`, `scenes.csv` (scenes `ad-2438b25fb3-s1` to `-s5`), `marks.csv` and `findings.jsonl` hold every reviewer mark and judge finding shown in the figure.

Four more ads of the round, `ad-3eb518b6e3`, `ad-b68fbb7151`, `ad-fcb5d2fe86` and `ad-76229af005`, are the review page's other examples, re-encoded the same way (15 s, 640x360). Their rows use the same ids.

## Privacy

- **Reviewers.** They appear only as R1..R5. No names, e-mail addresses, account ids or roles are included.
- **Annotators.** Blind-set annotators appear only as vote counts.
- **Free text.** No text written by a person is included: no reviewer notes, no reasons for thumbs-down votes, no comments. The only free text is model output (the judges' `description` and `location`). Pronunciation is released as flags and counts only, with no word, note or transcript.
- **Internal data.** The clip links are the public addresses of the files on our CDN; their paths contain our internal asset ids, which carry no personal data. No other internal ids, private storage paths or signed links are included, and a scan run at build time checks the data files for them.
- **Products.** In the data files they appear as a pseudonym and the SHA-256 of each reference image. The clips show the products themselves. No retailer, listing URL, catalog photo or listing text (titles, descriptions, features) is included, except where a judge description quotes listing text, as many script findings do. The review page replaces the quote in its one script finding with `[listing claim]` and `[listing footnote]`.
- **Example ads.** `example/ad-2438b25fb3.mp4` is the rendered ad shown in the paper's Figure 2, and the four other files in `example/` are ads of the round, each as reviewers watched it, re-encoded at 640x360. Unlike the figure, they are not blurred: they show the products, their packaging and, in some, generated people.

## Exclusions

- **Pronunciation finding text.** The pronunciation judge's findings (the quoted word, the judge's note and the recognizer transcript) and the word a reviewer marked. The axis itself is in `marks.csv`, as flags and counts.
- **Catalog photos and listing text.** Hashes only, as above.
- **Free text written by reviewers.**
- **Script lines, caption words and generation prompts.** They are not needed for any number in the paper. The one exception is the example ad: [`review/review.html`](../review/review.html) prints its five narration lines and four captions, as Figure 2 does, with the brand name replaced by `[brand]`.
- **One ruling on a human flag**, which is not a judge finding.

## Caveats

- **Scene-axis denominator.** Until a late tool change, the scene grid did not ask about a scene the reviewer had already marked product-wrong. On those reviews (`scene_grid_every_scene = 0`), such a scene is on the scene axis only if the reviewer marked it there. Rates computed on the 49 newer reviews alone are an unbiased check.
- **No sound or caption findings.** The sound judge raised no findings. The caption axes have no judge, so every caption mark comes from a person.
- **Timelines.** `time_s` is on the ad timeline. `span_*` values are within the scene. For 508 of the 510 product flags behind the 505 product findings, `time_s` equals the scene's `start_s` + `span_start_s`.

## Reproduce

Run from the release root:

```
python3 code/reproduce.py
```

`code/reproduce.py` recomputes the paper's round counts and blind-set AUCs from these files alone. It needs Python 3 and the standard library only, and runs in a few seconds. It prints each paper number next to the value recomputed from the release, and exits non-zero if any differs.

- **Round:** 562 scenes; 120 ads; product scenes marked by any reviewer 391, by a majority 335; judge-flagged 396; 354 of the 391 flagged; people-only 37 (any) and 11 (majority); scene swap 177 of 459 asked (any), 153 (majority); script 17 of 91.
- **Pronunciation (Figure 4):** 53 scenes marked by any reviewer, 45 of them judge-flagged and 8 people-only; the judge flagged 187 of the 562 scenes, so the chance mark is 33.3%.
- **Blind set AUCs:** clip judge 0.84, frame judge 0.69, DOVER 0.48, VideoScore2 0.57, best Qwen3 0.73.

For per-axis counts of the round, or of reviews you made with the review page, use `code/summarize_reviews.py` (see [REVIEW_PAGE.md](REVIEW_PAGE.md#summarize-reviews)).
