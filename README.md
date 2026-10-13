# Multimodal Judges Flag, Humans Decide

Data and a review template for checking AI-generated product video ads scene by scene. This is the public release of the WVAQ @ WACV 2027 paper **"Multimodal Judges Flag, Humans Decide: A Review-and-Edit Framework for AI-Generated Product Video Ads"**.

It holds three things: the data from the paper's 120-ad review round, a blind-labeled set for measuring judge accuracy, and a simple template of our review page. Use them to study how the 120 ads were reviewed, to test a product judge, or to run the same review on your own ads.

## What is in it

| Paper contribution | Where it is here |
|---|---|
| Ad review as six questions asked scene by scene (Sec. 3) | [`review/review.html`](review/review.html): a simple, one-file template of our review page, with the six questions, the decision rules, and the judges' findings shown or hidden; [`docs/REVIEW_GUIDE.md`](docs/REVIEW_GUIDE.md): what each question covers and where one ends and the next begins |
| Judges and people review each ad together (Sec. 4) | [`data/round/`](data/round): the 120-ad review round. 562 scenes from 20 products, every reviewer's marks (5 reviewers, 278 reviews), 717 judge findings and the 1,664 votes reviewers gave them |
| Generic scores cannot judge product fidelity (Sec. 6) | [`data/blind_product_set/`](data/blind_product_set): 120 blind-labeled scenes from 35 ads, 29 with a defective product, with every baseline's and judge's score |
| Each confirmed finding becomes a targeted edit (Sec. 5) | Not in this release |

Also included: [`code/reproduce.py`](code/reproduce.py) and [`code/summarize_reviews.py`](code/summarize_reviews.py), the paper's [`supplementary.pdf`](supplementary.pdf), the list of all 802 videos in [`data/clips_manifest.csv`](data/clips_manifest.csv), and five example ads in [`example/`](example): the ad annotated in the paper's Figure 2 and four more from the round, re-encoded at 640x360. They are the only videos in the repository. [`code/make_ad_package.py`](code/make_ad_package.py) builds the review-page package of any of the 120 round ads.

## Read this first: two kinds of labels

> **Round labels are assisted.** Reviewers saw the judges' findings while they marked, and accepting a finding could write it into their marks. Use the round to study the review process: coverage, what people add to the judges, and acceptance. Do not use it as blind ground truth for judge accuracy.
>
> **The blind product set is the part for measuring accuracy.** Its annotators never saw any judge output. Its labels likely under-count wrong scenes, because its four annotator accounts missed subtle defects.

## What the data shows

**The review round (assisted).** Per scene, reviewers mark product, scene (a scene to swap), script, pronunciation, caption placement and caption relevance. The caption axes are asked only where the scene has a caption. Sound is asked once per ad. A scene counts as marked by **any** reviewer when at least one asked reviewer marked it, and by a **majority** when more than half of them did.

- **The product was the main problem.** A majority marked the product wrong on 335 of 562 scenes (59.6%), and any reviewer on 391. A majority marked script, pronunciation, caption or sound problems on under 10% each.
- **The product judge flagged most product problems.** It flagged 396 scenes, including 354 of the 391 marked ones. Reviewers added 37 that it had not flagged (11 by a majority). 729 of the 808 product marks (90.2%) agree with a finding the reviewer accepted.
- **Other axes.** Scene swap: 177 of the 459 scenes asked (153 by a majority). Script: 91 scenes, 17 of them flagged by the script judge. Pronunciation (Figure 4): 53 scenes, 45 judge-flagged and 8 by people only. The pronunciation judge flagged 187 of the 562 scenes, so the chance mark is 33.3%.
- **Acceptance.** Reviewers gave the 717 released findings 1,336 thumbs up and 328 thumbs down. On pronunciation they gave 37 up and 398 down.

**The blind product set.** AUC for finding the defective scenes, where 0.5 is chance:

| deployed clip judge | starting-frame judge | best Qwen3 run | VideoScore2 | DOVER |
|---|---|---|---|---|
| 0.84 | 0.69 | 0.73 | 0.57 | 0.48 |

Generic video-quality scores stay near chance. The clip judge watches the clip with the catalog photos. Its prompt, inputs and model were chosen on these same labels, so its 0.84 is optimistic (see Sec. 6 of the paper and Table S2 of the supplementary). `scores.csv` holds more baselines, among them DINOv2, CLIP, OCR, VideoScore v1.1 and Qwen2.5-VL.

## The review in four steps

1. **Generate.** A pipeline makes a short video ad from a product's data.
2. **Review.** A reviewer answers six questions scene by scene: product, scene quality, pronunciation, sound, script and captions. AI judges place their findings inside the questions. The reviewer accepts or rejects each finding and adds the problems the judges missed.
3. **Decide.** Rules turn the answers into Approve, Send for editing or Reject and list the scenes and lines to fix. The queue puts the ads with the fewest and lightest issues first, since a catalog needs only a few usable ads per product. Set the rules by what each fix costs your team: re-voicing one line is cheaper than swapping a shot.
4. **Edit.** A confirmed issue opens the edit tool for its own scene or line. The new cut goes back to review.

The template covers Review and a preview of Decide. It shows the judge findings that come with each ad, and it has no edit tools. The production review portal is a different program, and the template reproduces only the parts of it the paper describes.

## Start here

**Open the review template.** Open [`review/review.html`](review/review.html) from disk in a current browser. Keep `review/` and `example/` side by side so the five example ads play. There is nothing to install or build, and the page makes no network request. We tested it in Google Chrome; Firefox and Safari are untested.

- **Reviewer code.** The release uses R1 to R5, so pick another code if you will pool your reviews with `data/round`.
- **Findings shown or hidden.** Findings shown matches the 120-ad round. Findings hidden is close to the paper's judges-hidden pass.
- **Questions.** Each of the six questions starts folded; open one by its title.
- **More of the round.** `python3 code/make_ad_package.py <ad_id>` writes the package of any round ad. Load it with that ad's video from `data/clips_manifest.csv`.
- **Your own ads.** The page runs no judge. Supply judge findings in the `findings.jsonl` format, inside an ad package or as a separate `findings.jsonl` file.
- **After Submit.** The page shows Approve, Send for editing or Reject as a preview only. Its thresholds are policy choices; set your own. You then download the review in the formats of `data/round`.

Ad packages, downloads and how to edit the rubric are in [docs/REVIEW_PAGE.md](docs/REVIEW_PAGE.md).

**Reproduce the paper's numbers.** Run from the release root:

```
python3 code/reproduce.py
python3 code/summarize_reviews.py data/round
```

They need Python 3 and its standard library only. `reproduce.py` recomputes the paper's round counts and blind-set AUCs from these files alone. It prints each one next to the paper's value and exits non-zero if any differs. `summarize_reviews.py` prints per-axis counts for the round or for your own reviews.

**Get the videos.** Download each video from the `url` column of `data/clips_manifest.csv` and save it under the name in the `file` column. Check it against `sha256` where given (516 of the 802 files), or else against `bytes`. See [Clips](docs/DATA.md#clips).

## Documentation

- [docs/DATA.md](docs/DATA.md): every data file and column, the ids, how the labels were made, the clips, privacy, exclusions and caveats.
- [docs/REVIEW_GUIDE.md](docs/REVIEW_GUIDE.md): the reviewer guide, with the six questions, their answers and the boundaries between them.
- [docs/REVIEW_PAGE.md](docs/REVIEW_PAGE.md): the full manual of the review page and `summarize_reviews.py`.

## Privacy

- All ids are pseudonyms. Reviewers appear only as R1..R5, and blind-set annotators only as vote counts.
- The clip links are the public addresses of the files on our CDN; their paths contain our internal asset ids, which carry no personal data.
- No text written by a person is included. The only free text is model output from the judges.
- Pronunciation is released as flags and counts only, with no word, note or transcript.
- In the data files, products appear as a pseudonym and the hashes of their reference images. The clips show the products themselves. No retailer, listing URL, catalog photo or listing text is included, except where a judge description quotes listing text.
- The example ads are not blurred: they show the products, their packaging and, in some, generated people.

The full statements are under [Privacy](docs/DATA.md#privacy) and [Exclusions](docs/DATA.md#exclusions).

## License

- Code (`code/` and the review page `review/review.html`): MIT, see [`LICENSE`](LICENSE).
- Data (`data/`), documentation (this README, the files in `docs/` and `supplementary.pdf`) and images and video (`example/`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The products shown in the clips and the example ads, the catalog photos behind the reference-photo hashes, and any listing text quoted in judge descriptions are third-party content that these licenses do not cover.

## Citation

Authors: Anoubhav Agarwaal, Sukesh Perla, Karthikeyan Mohanraj, Susmita Ghose (Anoki Inc.)

```
@misc{agarwaal2027judgesflag,
  title  = {Multimodal Judges Flag, Humans Decide: A Review-and-Edit Framework for AI-Generated Product Video Ads},
  author = {Agarwaal, Anoubhav and Perla, Sukesh and Mohanraj, Karthikeyan and Ghose, Susmita},
  year   = {2027},
  note   = {Submitted to the WVAQ workshop at WACV 2027}
}
```
