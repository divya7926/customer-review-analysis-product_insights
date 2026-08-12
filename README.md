# Customer Review Analysis — Product Insights

Built on an open-source sentiment analysis baseline, extended with a
product-management-facing "Product Insights" view. See
[PRODUCT_CASE_STUDY.md](./PRODUCT_CASE_STUDY.md) for the full
write-up: the problem, the design trade-offs, and what I'd build next.

## Overview

A Streamlit tool that analyzes customer reviews, classifies them as
positive or negative, and tags them by theme — turning raw feedback
into a "what should we fix first" view instead of just a sentiment
label.

## Features

- **Sentiment Analysis** — classify reviews as positive or negative
- **Theme Tagging** — tags each review as Price, Service, Speed / Wait Time, Quality, or Experience (`themes.py`)
- **Product Insights (Batch) view** — upload a CSV/TSV and get a theme-by-theme breakdown, sorted by negative volume, plus a "suggested roadmap candidates" list
- **Data Upload** — bring your own review dataset, or use the bundled sample

## Setup

\`\`\`
git clone https://github.com/divya7926/customer-review-analysis-product_insights.git
cd customer-review-analysis-product_insights
pip install -r requirements.txt
streamlit run app.py
\`\`\`

## Sample Dataset

`Restaurant_Reviews.tsv` is included as a demo dataset — the Product
Insights view falls back to it automatically if you don't upload your
own file.

## Why this exists

A basic sentiment tool tells you a review is positive or negative.
This project pushes one step further: it groups reviews by theme and
surfaces which themes are driving the most negative sentiment, so the
output looks like something a PM would actually act on. See
[PRODUCT_CASE_STUDY.md](./PRODUCT_CASE_STUDY.md) for the full
reasoning, including why theme tagging is keyword-based instead of a
black-box model.
