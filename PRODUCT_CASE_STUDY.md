# Product Case Study: From Sentiment Score to Roadmap Signal

*Written from a product management lens, on top of an open-source sentiment
analysis baseline ([original project](https://github.com/iamprashanth238/customer-review-analysis)).*

## 1. The problem

Most sentiment tools stop at a label: "this review is positive" or
"negative." That's an ML output, not a product decision. A PM reading
1,000 reviews doesn't need to know the *split* — they need to know
**what to fix first**, and how confident to be about that ranking.

That gap — sentiment score to roadmap signal — is what this project
adds on top of the base classifier.

## 2. Target user

A product manager (or a small team without a dedicated data/insights
function) who has a pile of raw customer reviews and 15 minutes to
decide what to raise in the next planning meeting.

## 3. What was added on top of the base repo

The original project (linked above) trains a Naive Bayes classifier on
a restaurant-reviews dataset and predicts positive/negative for one
review at a time. I kept that baseline and added:

- **Theme tagging** (`themes.py`): a transparent, keyword-based
  classifier that buckets each review into Price, Service, Speed /
  Wait Time, Quality, or Experience — deliberately *not* a black-box
  topic model, so every tag is explainable in one sentence.
- **A batch "Product Insights" view**: upload a CSV/TSV of reviews and
  get a theme-level breakdown of negative vs. positive mentions,
  sorted by negative volume, plus a "suggested roadmap candidates"
  list — the top 3 themes driving negative sentiment.
- **An explicit caveat** on that ranking (see §5) so it's used as a
  starting point for triage, not treated as a finished prioritization.

## 4. Why keyword tagging instead of a fancier model

I considered using an LLM or embedding-based clustering for theme
extraction. I chose a keyword lexicon instead, for a product reason,
not a technical limitation:

- **Explainability beats accuracy here.** If a PM asks "why is this
  review tagged Service?", the answer needs to be one sentence, not a
  black-box embedding distance. That trust matters more than a few
  points of precision at this stage.
- **It's editable by a non-engineer.** The keyword lists in
  `themes.py` are a plain dictionary — anyone on the team can extend
  them without touching a model.
- **It fails predictably.** A review that matches nothing falls into
  an explicit "Other" bucket instead of being silently misclassified
  into the nearest cluster.

The trade-off: it will miss sarcasm, implied themes, and phrasing it
hasn't seen. That's a known and acceptable limitation for a v1 — see
"What I'd do next."

## 5. Known limitations (stated on purpose)

- **Sentiment model, not just the theme layer, is a simple baseline.**
  It's a Naive Bayes classifier trained on ~1,000 restaurant reviews —
  it will not generalize well to, say, app-store reviews about a
  content-recommendation product without retraining on in-domain data.
- **The "roadmap candidates" list is a triage aid, not a decision.**
  It ranks by negative volume alone. A real prioritization needs to
  weight this against ticket volume, revenue impact, and fix
  difficulty — the app says this explicitly rather than implying
  false precision.
- **Small sample sizes are noisy.** A theme with 2 negative mentions
  out of 3 total reviews shows a 67% negative ratio that looks
  alarming but isn't statistically meaningful. This is flagged, not
  solved, in this version.

## 6. Success metrics, if this were a real product

- **Precision of theme tags** against a small human-labeled sample
  (target: spot-check 50 reviews, >80% agreement before trusting the
  triage list).
- **Time-to-insight**: minutes from "reviews land" to "themes
  surfaced," compared to a PM reading them manually.
- **Adoption**: whether PMs actually reference the triage list in
  planning, vs. ignoring it — the real test of whether this is useful
  or just a demo.

## 7. What I'd do next

1. Retrain the sentiment model on a dataset closer to the target
   domain (app reviews, not restaurant reviews).
2. Add a lightweight feedback loop — let a PM mark a theme tag as
   wrong, and use that to grow the keyword lexicon over time.
3. Weight the roadmap-candidates ranking by review recency and
   (if available) user segment, not just raw negative count.
4. Handle multi-language reviews — the keyword approach currently
   only works in English.
