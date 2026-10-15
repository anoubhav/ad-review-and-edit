# Review page

How to review an ad, question by question: [REVIEW_GUIDE.md](REVIEW_GUIDE.md).

[`review/review.html`](../review/review.html) is a template of the review protocol in the paper's Sec. 3, in one HTML file. You watch one ad, answer the six questions scene by scene, give each judge finding a thumb up or down, add the problems the judges missed, submit, see what the decision rules make of your answers, and download the review in the formats of [`data/round`](../data/round).

For the overview of the release, see the [README](../README.md). The data files and their columns are documented in [DATA.md](DATA.md).

What it is not:

- It runs no judge. Findings are read from the ad package; for the five example ads they are the findings this release holds for them (the round's pronunciation findings are left out, as under [Exclusions](DATA.md#exclusions)).
- It has no edit tools. The decision after Submit is a preview.
- It is a template of the protocol. The production review portal is a different program, and the page reproduces only the parts of it the paper describes (see [Limits](#limits)).

## Open it

Open `review/review.html` from disk in a current browser. There is nothing to install or build, and the page makes no network request: scripts and styles are inline, and a Content-Security-Policy blocks every other source. The example ads' videos play from [`example/`](../example), so keep the two folders side by side. We tested the page in Google Chrome; Firefox and Safari are untested.

The start screen asks for three things:

1. **Reviewer code.** A pseudonym of the form R followed by digits (default R1). The release uses R1 to R6, so pick another code if you will pool your reviews with `data/round`.
2. **Findings shown or hidden** (see [The two modes](#the-two-modes)).
3. **Ads.** The five example ads, ad packages you load (see [Ad packages](#ad-packages)), or both. "Import a previous export" reopens a review saved from this page.

The reviewer code and the mode are fixed once you answer anything. "Clear all reviews" on the start screen unlocks them.

## The two modes

| page mode | paper condition | what you see |
|---|---|---|
| Findings shown | the 120-ad round (Sec. 4, "Judges and people together") | each question shows its findings at the scene or line they point to, signed "Agent", with kind, description, place on the product, span and a button that jumps the video to the finding. Each needs a thumb: Agree (thumbs up) means the finding is right, Disagree (thumbs down) means it is wrong. A question with findings carries an "Auto-flagged" pill. |
| Findings hidden | close to the judges-hidden pass (Sec. 4 and Supp. B, "The same ads with judges hidden") | the questions and the video only. No finding, flag, marker or thumb is on screen. That pass differed in two ways: sound was optional, with a blank answer counted as no issue, and marking a product wrong did not pre-fill Swap out. The page keeps the round's rules for both. |

For a real judges-hidden pass, give reviewers packages without findings: the example ads' findings sit in the page's source, where anyone who opens the file can read them.

## How a review runs on the page

- **Questions.** Each question starts folded; click its title to open it. Items in the "Still to do" list open their question. Folding is a view setting, kept per ad, and never part of the review.
- **Answers.** Nothing is pre-selected. A negative answer ("Product wrong", "Bad", "Mispronounced", "Can be better", "Issues") opens a row for each scene, line or caption; "Add a problem" marks one, and its secondary options appear under it. Scene quality asks every scene: No opinion, Keep or Swap out. Overlay text asks only scenes with a caption, placement and relevance separately. Pronunciation takes the word that came out wrong. Sound is asked once for the whole ad.
- **Thumbs.** A thumbs up writes the finding into your answers: the negative answer, the scene and the finding's kinds. A note says "Answered for you", with an Undo that takes back only that accept and its thumb, as long as you have not changed those answers since. A thumbs down changes no answer. As in the portal, withdrawing a thumb (click it again) or changing it to a thumbs down never removes an answer; change the answer by hand if you need to.
- **Positive answers.** If you answer "Product looks right" (or another positive answer) after accepting findings on that question, their marks go and a note says so. Their thumbs stay up until you change them.
- **Swap pre-fill.** Marking a scene's product wrong pre-fills Swap out on that scene. The pre-fill counts as a scene mark only once you touch it (a mark or an option on that scene), as in [When a scene counts as marked](DATA.md#when-a-scene-counts-as-marked).
- **Submit.** Submit opens when every required question is answered (all six, as in the round), every finding shown has a thumb, and at least 90% of the ad has played. As in the portal, a jump of more than 2 s between two updates of the video's time counts as a seek, and seeking does not count as playing, so playback faster than about 4x counts little. If the video cannot play, the rule is waived and the review records it. The "Still to do" list under the questions says what is missing, and each item jumps to its question; the line under the video gives the count.
- **Decision.** After Submit the page shows the verdict of the paper's rules (Sec. 3, "From answers to a decision"). Each answer and most secondary options belong to a category (product, shot quality, physics, script, audio, overlay text) with a severity. A category counts toward the decision ("fires") when any of its answers is moderate or severe. Product wrong on any scene, two such categories or two scenes to replace reject the ad. One category, one scene to replace or a swapped weak ending send it for editing. Otherwise the verdict is Approve. The page lists the categories that count and the scenes and lines to fix. These thresholds are policy choices; set your own.
- **Saving.** The page saves your work in the browser's local storage as you go. If the browser blocks storage the page still works, and says so; download before you close it.

## Ad packages

An ad package is one JSON file per ad (`format: "sbs-ad-package/1"`). The example ads' packages are the `DEMO` and `EXTRA_EXAMPLES` constants in the page's script; copy one as a starting point. [`code/make_ad_package.py`](../code/make_ad_package.py) writes the package of any ad of the round (`python3 code/make_ad_package.py <ad_id> --out <folder>`).

| field | meaning |
|---|---|
| `format` | `sbs-ad-package/1` |
| `ad_id`, `product_id` | ids, as in `data/round` (`ad_id` matches `ad-` and ten hex digits) |
| `video` | the video's file name, or a path relative to `review/` |
| `duration_s`, `judged_axes`, `sound_judge_status` | the ad's length; the axes whose findings the package carries (`judge_flagged` is blank for the others); `pass`, `flag` or null |
| `axis_notes` | optional `{axis: text}`, shown on that question when findings are shown. The example ad uses it to say that the round's pronunciation findings are not in this release. |
| `scenes` | `scene_id` (`<ad_id>-s<k>`), `scene_index` (from 1), `position`, `start_s`, `duration_s`, `has_caption`, in play order; `start_s` is the sum of earlier durations |
| `lines`, `captions` | `{scene_id, text}`: the narration line and the caption text per scene. Without `lines`, script and pronunciation ask every scene. |
| `findings` | judge findings in the `findings.jsonl` format (`thumbs` is ignored); a pronunciation finding may carry `word` |
| `reference_photos` | `{label, file}` per photo, `label` as in `evidence_ref` (`hero`, `gallery-1`, ...) |
| `text_edits` | free notes on what was redacted |

"Load ad packages" takes the package files, their videos, any reference photos and a `findings.jsonl` together, and matches them by file name (a `findings.jsonl` adds its findings to the packages with the same `ad_id`). A package that fails the checks (ids, contiguous scenes, findings on known scenes and judged axes) is refused with a message. The queue holds every loaded ad, with its status and previous and next buttons.

The example package takes its scenes from `data/round/scenes.csv` and its findings from `data/round/findings.jsonl`, without votes. It also prints the narration lines and captions of this one ad, as Figure 2 does. In it, the brand name in the line of scene 5 and brand words quoted in four judge descriptions are replaced with `[brand]` and `[brand tagline]`, and the listing text quoted in the script finding with `[listing claim]` and `[listing footnote]`; `text_edits` lists each place. Every finding card says that its text is the model's, and says so again when words were replaced. The four other example ads (`ad-3eb518b6e3`, `ad-b68fbb7151`, `ad-fcb5d2fe86` and `ad-76229af005`) were built by `code/make_ad_package.py`: scenes and findings as in `data/round`, judge descriptions as the judges wrote them, and no narration lines or captions, so the page asks script and pronunciation on every scene of these ads.

## Downloads

After Submit, each ad offers four files, named `<ad_id>.<reviewer>.<kind>`:

| file | lines up with | notes |
|---|---|---|
| `marks.csv` | `data/round/marks.csv`, same header and column meanings | one row per asked scene and axis. `scene_grid_every_scene` is always 1 (the page asks every scene). Pronunciation rows use axis `pronunciation`, with the word in `secondary_options`; the release's pronunciation rows leave `secondary_options` blank, as the word is not released. `judge_flagged` is filled the same way in both modes; thumbs are 0 when findings are hidden. |
| `ad_marks.csv` | `data/round/ad_marks.csv` | the sound answer. The voice and music tags are in the JSON only. |
| `thumbs.csv` | the `thumbs` of `data/round/findings.jsonl`, one row per vote | `reviewer,ad_id,scene_id,finding_id,axis,verdict,applied_to_rubric`; header only when findings are hidden |
| `review.json` | everything | mode, reviewer, the RUBRIC and its version, timestamps (opened, first answer, submitted, and per question the first and last answer), the played intervals, every answer in the portal's key names, your thumbs with times, the decision, the CSV rows, and the state the page needs to reopen the review |

"Save draft" downloads `review.json` before Submit, and "Import a previous export" continues it, on this or another computer. "All submitted reviews in this browser" downloads one `marks.csv`, `ad_marks.csv` and `thumbs.csv` for every submitted ad in the queue.

`applied_to_rubric` means what it means in the release: the accept changed your answers at some point. A second finding that adds nothing is 0. The stamp stays with the thumb when you change it to a thumbs down, as in the portal (22 down votes in `findings.jsonl` carry `true`), and goes when you withdraw the thumb or press Undo.

## Summarize reviews

Run from the release root:

```
python3 code/summarize_reviews.py data/round
python3 code/summarize_reviews.py data/round ~/Downloads/reviews.marks.csv ~/Downloads/reviews.ad_marks.csv
```

[`code/summarize_reviews.py`](../code/summarize_reviews.py) reads any mix of `marks.csv` and `ad_marks.csv` files (or folders of them). Per axis, it prints the units asked, the share marked by any reviewer, the share marked by a majority (more than half of those asked) and the share of marks that came from accepted findings. The definitions are the ones in [DATA.md](DATA.md) and in [`code/reproduce.py`](../code/reproduce.py). On `data/round` it prints the paper's numbers:

```
Files: 1 marks, 1 ad_marks. Reviews: 278. Reviewers: 5.

axis               units asked  marked by any  marked by a majority  marks  from accepted findings
product            562 scenes   391 (69.6%)    335 (59.6%)           808    729 (90.2%)
scene              459 scenes   177 (38.6%)    153 (33.3%)           331    272 (82.2%)
script             562 scenes   91 (16.2%)     33 (5.9%)             117    34 (29.1%)
pronunciation      562 scenes   53 (9.4%)      19 (3.4%)             57     36 (63.2%)
caption_placement  530 scenes   103 (19.4%)    39 (7.4%)             121    0 (0.0%)
caption_relevance  530 scenes   29 (5.5%)      11 (2.1%)             30     0 (0.0%)
sound              120 ads      2 (1.7%)       0 (0.0%)              2      n/a (no judge findings)
```

A row that repeats a reviewer on the same unit is counted once (the last file read wins), so pooled reviews need their own reviewer codes.

## Edit the rubric

The first constant in the page's script, `RUBRIC`, holds the protocol as data, with comments. You can change it in any text editor:

- the order of the questions (the cards and the "Still to do" list follow it);
- their labels, answers, secondary options, hints and help text;
- which questions are required (`preset: 'round'` requires all six; `'default'` requires product and scene and any question a judge flagged);
- the 90% watch rule (`watch_gate`) and the Swap pre-fill (`product_auto_swap`);
- the option order used in exports;
- the decision rules (severities, categories and thresholds).

Reload the page to see the change. Adding or removing a question needs changes to the code, and the row order of `marks.csv` stays the release's. Keep option keys in `option_order`, and change `version`: it is written into every `review.json`.

## Limits

- No judge runs here. Findings for your own ads must be supplied in the `findings.jsonl` format, in the package or a `findings.jsonl` file.
- No edit tools and no decide board (the portal screen where a person can overrule the verdict), so nobody can overrule the verdict on the page.
- The example ads have no catalog photos: the release holds only their hashes. Product findings name the photo they were compared with.
- The page keeps the round's question order (Table 1 and the appendix rubric table). The current portal asks script before pronunciation and moves a flagged middle question first.
- The round's free-text boxes are left out, as the release holds no reviewer text: the comment per product scene, the "another reason" and "why" boxes on scene quality, the notes on sound and script, and the note on a thumbs down.
- Sound uses the labels renamed after the round ("What is off?": Whole voice off, Music off). The round asked "Which part?": The voice, The music.
- You can answer before watching; only Submit waits for 90% of the ad, as in the portal. The paper asks reviewers to watch the whole ad first.
- Other differences from the current portal: it pre-fills Swap only when a run turns it on (the round did, the page always does), and it treats sound as optional (the round required it, as the page does).
- Reviews live in the browser that made them until you download them.
