# Review guide

This guide shows how to run the review from the paper *Multimodal Judges Flag, Humans Decide: A Review-and-Edit Framework for AI-Generated Product Video Ads* on your own ads. A reviewer watches one ad and answers six questions. Each question points to one place in the ad: a scene, a narrated line, a caption or the whole ad. So a problem is marked, and later fixed, where it sits. AI judges can add findings for the reviewer to accept or reject. The question names, answers and options below are those of the review page, [`review/review.html`](../review/review.html), whose manual is [REVIEW_PAGE.md](REVIEW_PAGE.md).

## Before you start

- Open `review/review.html` in a current browser. Keep `review/` and `example/` side by side so the example ads play.
- Enter a reviewer code such as R6. R1 to R5 are the round's reviewers. Give each reviewer their own code, and do not type a name.
- Choose Findings shown or Findings hidden. The code and this choice are fixed once you answer anything. To change them, press "Clear all reviews", which clears every review in this browser.
- Press "Load ad packages" and choose your packages (.json), their videos and any reference photos, all together. Files are matched by name. A findings.jsonl file adds judge findings. The package format is in [REVIEW_PAGE.md](REVIEW_PAGE.md). The five example ads are ticked by default, so untick them to review only your own ads.
- Turn the sound on. Keep the product information at hand for Script quality. The page shows the reference photos when a package has them, and no product listing.
- The page saves your work in this browser. "Save draft" downloads it, and "Import a previous export" reopens it.

## How a review runs

1. **Watch the whole ad once, with sound.** Some problems only show across scenes: a repeated scene, a background that jumps, an ending that does not land.
2. **Answer from top to bottom.** Click a scene in the strip under the video to jump to its start. The play button on a scene, line or caption row plays just that scene, as often as you need.
3. **Mark where.** A negative answer opens a row per scene, line or caption. Press "Add a problem" on each one at fault (it then reads "Problem marked"). Where the question offers kinds, tick each that applies under "Kind of problem (optional)". The kind is optional, but it says how to fix it. Scene quality works per scene: give each scene No opinion, Keep or Swap out. Sound quality has no rows.
4. **Submit.** "Still to do" lists what is missing. "Submit review" opens when the list is empty: every question is answered, every scene has a mark under Scene quality, each negative answer has at least one row marked, "What is off?" is picked when Sound quality is Issues, every finding shown has a thumb, and 90% of the ad has played. If the video cannot play, the watch rule is waived and the review records it.
5. **Download.** After Submit, the page shows "What the rules decide": Approve, Send for editing or Reject. The rules' thresholds are policy choices; set your own. Then download the review: marks.csv, ad_marks.csv, thumbs.csv and review.json.

**Two modes.** With *Findings shown*, the judges' findings sit inside each question, as in the paper's 120-ad round. With *Findings hidden*, you see only the video and the questions. Unlike the paper's judges-hidden pass, Sound quality stays required here, and Product wrong still pre-fills Swap out. For a truly hidden pass, untick the example ad and load packages without findings. Anyone who opens the files can read the findings in a package, and the example ad's findings sit in the page's source.

## The six questions

| | Question | Asked for | Answers |
|---|---|---|---|
| 1 | The product | each scene | Product looks right / Product wrong |
| 2 | Scene quality | each scene | No opinion / Keep / Swap out |
| 3 | Pronunciation | each narrated line | Sounds right / Mispronounced |
| 4 | Sound quality | the whole ad | Sounds right / Issues |
| 5 | Script quality | each narrated line | Good / Bad |
| 6 | Overlay text | each caption | Placement: Correct / Can be better. Relevance: Correct / Issues |

The page marks all six questions Required. The kinds, the text grade and the mispronounced word are optional. "What is off?" must be answered when Sound quality is Issues.

**Text appears in three places, each with its own question.** Words printed on the product belong to The product. Text painted into the background is an AI issue under Scene quality. Only captions laid over the picture belong to Overlay text.

### 1. The product

The product itself, held against the reference photos: its shape, colour, logo and markings, and the words printed on it.

- **Wrong product**: a different product from the one in the reference photos.
- **Shape, colour, logo or markings wrong**: they differ from the product's own photos.
- **AI issue**: the product itself looks AI-made, such as melted detail, a strap that goes nowhere, or text painted on.
- **Product text not intact**: printed words are garbled, misspelt or changed. Then "How bad is the text? (optional)": **Low: still readable** (right words, soft letters) or **High: gibberish** (unreadable, or wrong words).

Marking a scene under Product wrong also fills in Swap out for that scene under Scene quality, unless you already marked it Keep. The scene shows "tagged: product wrong". Change that mark if the shot itself is fine.

*Boundaries.* The room, the person, the motion and the framing go to Scene quality, as does an AI issue elsewhere in the scene. The line between an AI issue on the product and impossible motion is still unsettled.

*Example.* A label reads one letter off, so the word is wrong: Product wrong, Product text not intact, High: gibberish. High covers any wrong word, even one you can read.

### 2. Scene quality

Everything in the shot except the product: the setting, the people, the motion, the framing, and how the scene fits the ad. Mark every scene, and ask whether it earns its place. A scene where nothing happens is worth swapping too. Options open on Swap out:

- **AI issue**: faces or hands off, melted detail, gibberish text painted into the scene.
- **Repetitive, dull or crowded scene**: seen already, nothing happens, or too busy to read the product.
- **World or continuity breaks**: the brand, the character or the setting changes between scenes, or a new object appears.
- **Something moves impossibly**: floating, clipping, liquids behaving wrong.
- **Weak ending** (last scene only): no hero shot of the product, or it does not end on the product.

*Boundaries.* Text painted into the background is an AI issue of the scene. Mark a repeat on the later scene.

*Example.* A sign behind the presenter shows letters that spell nothing: Swap out, AI issue. The product's own clean label stays Product looks right.

### 3. Pronunciation

A single word said wrong. Mark the line and type the word under "Which word came out wrong? (optional)".

*Boundaries.* A voice or music that is off across the ad is Sound quality.

*Example.* The narrator stresses the product's name on the wrong syllable: Mispronounced, with the name typed in.

### 4. Sound quality

The voice and the music of the whole ad, asked once. On Issues, you must pick at least one under "What is off?": **Whole voice off**, **Music off**, or both.

*Boundaries.* A single word said wrong is Pronunciation.

*Example.* The voice sounds thin and echoey throughout: Issues, Whole voice off.

### 5. Script quality

The words of each narrated line, read against the product information.

- **Factually incorrect**: a figure, material, component, certification or guarantee the product information does not carry.
- **Awkward or unnatural phrasing**: nobody would say it aloud, or it does not follow from the line before.

*Boundaries.* The brand name, a call to action and an adjective nobody can measure are fine. How a line is spoken goes to Pronunciation and Sound quality.

*Example.* A line says the cream lasts 48 hours, and the product information gives no figure: Bad, Factually incorrect.

### 6. Overlay text

Only the captions laid over the picture, on scenes that carry one.

- **Placement**: where a caption sits. Can be better if it covers a face, the product or text in the frame, runs off the edge, or would read better elsewhere.
- **Relevance**: whether it fits the scene under it and the line spoken over it.

*Boundaries.* Printed words go to The product, and painted text to Scene quality.

*Example.* A caption sits across the pack and hides its label: Placement, Can be better.

## Using judge findings

With findings shown, each finding sits on its scene or line, marked "Agent", with the kind of problem it names. A question with findings carries an "Auto-flagged" pill. A blue square on the scene strip marks where each finding sits, and each finding still waiting for you says "Needs your thumb". Findings come only on The product, Scene quality, Pronunciation and Script quality. Sound quality may show one line saying whether the sound judge passed or flagged the ad. It needs no thumb.

- **Check it.** Press its time to jump the video there. "Details" opens the judge's text, and "Show all details" opens every finding on a card.
- **Accept with a thumb up** ("Agree") when it is right. It writes the negative answer, the scene and the kind into your answers. The "Answered for you" note has an Undo.
- **Reject with a thumb down** ("Disagree") when it is wrong. It changes no answer.
- **Add what the judges missed.** Choose the negative answer and press "Add a problem" on the scene, line or caption at fault, then tick the kind where the question offers one. On Scene quality, mark the scene Swap out. On Sound quality, answer Issues and pick under "What is off?".

Every finding needs a thumb before Submit. Click a thumb again to withdraw it.

## Common mistakes

- **Answering before watching the whole ad.** Repeats, background jumps and weak endings only show across scenes.
- **Skipping through the ad.** Seeking ahead, or playing faster than about 4x, adds little or nothing to the 90%. Let the ad play.
- **A negative answer with no place.** Mark every scene, line or caption at fault.
- **Text under the wrong question.** Check where it sits: on the product, in the background, or over the picture.
- **No opinion as a default.** Ask first whether the scene earns its place.
- **Not reviewing a pre-filled Swap out.** Product wrong fills it in. Change it if the shot itself is fine.
- **Accepting a finding unseen.** Jump to it and look first.
- **Switching to a positive answer after accepting a finding.** It removes the marks the finding wrote, but the thumb stays up. Marking that scene Keep or No opinion does the same. If you now disagree, change the thumb to Disagree.
- **Expecting a thumb down or a withdrawn thumb to clear an answer.** Neither does. Change the answer by hand, or use Undo in the "Answered for you" note straight after the accept.
