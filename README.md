# Customer Review Analysis — Product Insights Fork

This is a fork of [iamprashanth238/customer-review-analysis](https://github.com/iamprashanth238/customer-review-analysis),
extended with a product-management-facing "Product Insights" view on
top of the original sentiment classifier. See
[**PRODUCT_CASE_STUDY.md**](./PRODUCT_CASE_STUDY.md) for the full
write-up: the problem framing, the design trade-offs, and what I'd
build next.

## Overview

This project is a **Customer Review Analysis** tool built using Streamlit and various machine learning techniques. The goal is to analyze customer reviews, determine sentiment, and provide insights that can help businesses understand customer feedback better. The tool processes customer review data and classifies them as positive or negative, enabling businesses to gauge overall sentiment quickly.

## Features

- **Sentiment Analysis**: Classify customer reviews as positive or negative.
- **Theme Tagging**: Every review is tagged with a theme (Price, Service, Speed / Wait Time, Quality, Experience) using a transparent keyword lexicon — see `themes.py`.
- **Product Insights (Batch) view**: Upload a CSV/TSV of reviews and get a theme-by-theme breakdown of negative vs. positive mentions, sorted by negative volume, plus a "suggested roadmap candidates" list.
- **Interactive Interface**: Use Streamlit to visualize results in an easy-to-use web application.
- **Data Upload**: Users can upload their own review datasets to analyze.
- **Real-Time Analysis**: Perform real-time sentiment analysis on the input data.

## Installation

To set up and run this project locally, follow these steps:

### Prerequisites

- **Python 3.7+**: Make sure you have Python installed on your system.
- **pip**: Python package installer.
- **virtualenv** (Optional but recommended): To create isolated Python environments.

### Step-by-Step Installation

1. **Clone the Repository**:
   git clone https://github.com/YOUR-USERNAME/customer-review-analysis.git
   cd customer-review-analysis
2. **Create and Activate a Virtual Environment (Optional but recommended)**:
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
3. **Install Dependencies**:
   pip install -r requirements.txt
   If requirements.txt is not provided, you can manually install the necessary libraries:
   pip install streamlit scikit-learn pandas numpy
5. **Run the Application**:
   streamlit run app.py

### Some Outputs:
**Some Negative Reviews**:
![image](https://github.com/user-attachments/assets/796ff45e-e002-406d-a081-30186a9ada90)
![image](https://github.com/user-attachments/assets/ef51ba92-9ebe-4003-9668-3ceec5b9bbd2)

**Some Positive Reviews**:
![image](https://github.com/user-attachments/assets/7d7f1963-861e-452c-bb02-d5889cd8d514)
![image](https://github.com/user-attachments/assets/761b2e42-889b-48f9-9d3f-1d463922a481)

### Sample Dataset
You can use the Restaurant_Reviews.tsv file in this repository as a sample dataset to see how the application works — the "Product Insights (Batch)" view falls back to this file automatically if you don't upload your own.

### Why this fork exists
The original app answers "is this review positive or negative?" This fork pushes one step further and answers "what should we fix first?" — see [PRODUCT_CASE_STUDY.md](./PRODUCT_CASE_STUDY.md) for the reasoning behind every design choice, including why theme tagging is keyword-based instead of a black-box model.

### Deployment
The app can be deployed on any cloud platform like AWS, Heroku, or Streamlit Cloud. To deploy, follow the instructions provided by the respective platforms.

### Contributing
If you want to contribute to this project, you can fix the repository and submit a pull request. Contributions are always welcome!

### Happy Coding...! :)
