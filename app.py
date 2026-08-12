import pickle

import pandas as pd
import streamlit as st

from themes import get_themes, summarize_themes

# ---------------------------------------------------------------------
# Load the trained sentiment model + vectorizer (see model.py)
# ---------------------------------------------------------------------
with open("sentiment_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


def predict_sentiment(text: str) -> str:
    transformed = vectorizer.transform([text])
    prediction = model.predict(transformed)
    return "Positive" if prediction[0] == 1 else "Negative"


st.set_page_config(page_title="Customer Review Analysis", layout="centered")
st.title("Customer Review Analysis")
st.caption(
    "A sentiment baseline plus a product-insights layer: theme tagging "
    "and a roadmap-triage view, so raw reviews turn into decisions, "
    "not just a positive/negative label."
)

page = st.sidebar.radio("Choose a view", ["Single Review", "Product Insights (Batch)"])

# ---------------------------------------------------------------------
# View 1: original single-review sentiment check, now with themes too
# ---------------------------------------------------------------------
if page == "Single Review":
    st.write("### Check one review")
    user_input = st.text_area("Enter your review here:")

    if st.button("Predict"):
        if not user_input.strip():
            st.warning("Enter a review first.")
        else:
            sentiment = predict_sentiment(user_input)
            themes = get_themes(user_input)

            st.write(f"**Predicted Sentiment:** {sentiment}")
            st.write(f"**Detected Theme(s):** {', '.join(themes)}")

# ---------------------------------------------------------------------
# View 2: the product-management-facing view. Upload a batch of
# reviews and get a "what should we fix first" triage table instead
# of reading reviews one by one.
# ---------------------------------------------------------------------
else:
    st.write("### Turn a batch of reviews into a triage list")
    st.write(
        "Upload a CSV/TSV with a `Review` column, or use the bundled "
        "sample dataset. Each review is scored for sentiment and tagged "
        "with a theme, then rolled up so you can see which themes are "
        "driving negative sentiment first."
    )

    uploaded = st.file_uploader("Upload reviews (CSV or TSV)", type=["csv", "tsv"])

    if uploaded is not None:
        sep = "\t" if uploaded.name.endswith(".tsv") else ","
        data = pd.read_csv(uploaded, sep=sep)
    else:
        st.caption("No file uploaded — using the bundled `Restaurant_Reviews.tsv` sample.")
        data = pd.read_csv("Restaurant_Reviews.tsv", delimiter="\t")

    if "Review" not in data.columns:
        st.error("The file needs a `Review` column.")
    else:
        sample_size = st.slider(
            "Number of reviews to analyze (larger = slower on this simple model)",
            min_value=10,
            max_value=min(500, len(data)),
            value=min(200, len(data)),
        )
        sample = data.head(sample_size).copy()

        with st.spinner("Scoring reviews..."):
            sample["Predicted Sentiment"] = sample["Review"].apply(predict_sentiment)
            summary = summarize_themes(
                sample["Review"].tolist(), sample["Predicted Sentiment"].tolist()
            )

        st.write("#### Theme breakdown (sorted by negative volume)")
        summary_df = pd.DataFrame(summary)[
            ["theme", "negative", "positive", "total", "negative_ratio"]
        ]
        st.dataframe(summary_df, use_container_width=True)
        st.bar_chart(summary_df.set_index("theme")[["negative", "positive"]])

        st.write("#### Suggested roadmap candidates")
        top_negative = [row for row in summary if row["negative"] > 0][:3]
        if not top_negative:
            st.write("No negative reviews in this sample — nothing to triage.")
        else:
            for i, row in enumerate(top_negative, start=1):
                st.write(
                    f"{i}. **{row['theme']}** — {row['negative']} negative mentions "
                    f"({int(row['negative_ratio'] * 100)}% of {row['total']} reviews "
                    f"tagged with this theme are negative)"
                )
            st.caption(
                "This ranking is a starting point, not a decision — it should be "
                "validated against ticket volume, revenue impact, and how easy "
                "each fix is, before it becomes an actual roadmap item."
            )

        with st.expander("See raw scored reviews"):
            st.dataframe(
                sample[["Review", "Predicted Sentiment"]], use_container_width=True
            )
