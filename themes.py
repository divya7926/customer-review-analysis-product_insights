"""
Lightweight, dependency-free theme tagging for customer reviews.

This intentionally does NOT use a transformer model or topic-modeling
library. The goal of this project is to demonstrate product thinking on
top of a simple ML baseline, not to build the most sophisticated NLP
pipeline. A PM should be able to explain exactly why each review got
tagged the way it did -- a keyword lexicon is transparent and easy to
extend, which matters more here than marginal accuracy gains.

Each theme is a bucket of keywords. A review can match more than one
theme (e.g. "overpriced and slow service" -> Price + Service).
Reviews that match nothing are tagged "Other" so nothing is silently
dropped from the insights view.
"""

from collections import Counter

THEME_KEYWORDS = {
    "Price": [
        "price", "priced", "pricing", "expensive", "cheap", "cost",
        "overpriced", "value", "worth", "affordable",
    ],
    "Service": [
        "service", "staff", "waiter", "waitress", "rude", "friendly",
        "helpful", "support", "attentive", "manager",
    ],
    "Speed / Wait Time": [
        "slow", "fast", "quick", "wait", "waiting", "delay", "delayed",
        "late", "prompt", "took forever",
    ],
    "Quality": [
        "quality", "fresh", "stale", "delicious", "tasty", "bland",
        "bad", "great", "excellent", "amazing", "terrible", "awful",
    ],
    "Experience / Ambience": [
        "atmosphere", "ambience", "ambiance", "clean", "dirty", "noisy",
        "comfortable", "experience", "decor", "vibe",
    ],
}


def get_themes(text: str) -> list[str]:
    """Return the list of themes a single review text matches."""
    text_lower = str(text).lower()
    matched = [
        theme
        for theme, keywords in THEME_KEYWORDS.items()
        if any(keyword in text_lower for keyword in keywords)
    ]
    return matched if matched else ["Other"]


def summarize_themes(reviews: list[str], sentiments: list[str]) -> "list[dict]":
    """
    Given parallel lists of review text and predicted sentiment
    ("Positive"/"Negative"), return theme-level counts sorted by
    negative volume descending -- i.e. the themes most worth a PM's
    attention first.
    """
    negative_counts: Counter = Counter()
    positive_counts: Counter = Counter()

    for text, sentiment in zip(reviews, sentiments):
        for theme in get_themes(text):
            if sentiment == "Negative":
                negative_counts[theme] += 1
            else:
                positive_counts[theme] += 1

    all_themes = set(negative_counts) | set(positive_counts)
    summary = [
        {
            "theme": theme,
            "negative": negative_counts.get(theme, 0),
            "positive": positive_counts.get(theme, 0),
            "total": negative_counts.get(theme, 0) + positive_counts.get(theme, 0),
            "negative_ratio": round(
                negative_counts.get(theme, 0)
                / max(1, negative_counts.get(theme, 0) + positive_counts.get(theme, 0)),
                2,
            ),
        }
        for theme in all_themes
    ]
    return sorted(summary, key=lambda row: row["negative"], reverse=True)
