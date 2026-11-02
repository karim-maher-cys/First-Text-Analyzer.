# SentinEL — Privacy-First Text Analyzer

SentinEL is a Streamlit application that combines **Personally Identifiable Information (PII) detection and anonymization** with **sentiment analysis**. It is designed to demonstrate a privacy-aware text-analysis workflow for individual text samples and CSV datasets.

## Features

### 1. Single Text Inspector
- Enter or paste a text sample.
- Detect potential PII entities with Microsoft Presidio.
- Review detected entities, confidence scores, and their positions in the text.
- Anonymize detected entities before running sentiment classification.
- Display the sentiment label and model confidence.

### 2. Batch CSV Sanitizer
- Upload a CSV file.
- Select the column containing text to inspect.
- Choose how many rows from the beginning of the file to process.
- Anonymize detected PII in the selected text column.
- Run sentiment analysis on the anonymized text.
- View sentiment and detected-entity charts.
- Download the processed output as a CSV file.

## Technology Stack

- **Python** — application logic
- **Streamlit** — interactive web interface
- **Microsoft Presidio** — PII analysis and anonymization
- **Hugging Face Transformers** — sentiment-analysis pipeline
- **DistilBERT (SST-2)** — pretrained sentiment model
- **Pandas** — CSV handling and tabular results

## How the Workflow Works

1. The application receives text from the user or a selected CSV column.
2. Presidio analyzes the text for supported PII entities using English-language analysis.
3. The anonymizer replaces entities detected by Presidio.
4. The sentiment model classifies the anonymized text as `POSITIVE` or `NEGATIVE`.
5. For CSV input, the application displays summary charts and allows the processed results to be downloaded.

## Project Structure

```text
SentinEL/
├── app.py
├── README.md
└── requirements.txt
```

## Installation

### Prerequisites
- Python 3.9 or later (a compatible Python version for the installed package releases is required).
- `pip`
- An internet connection for installing packages and downloading the NLP/sentiment models on first use.

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/SentinEL.git
cd SentinEL
```

Replace `YOUR-USERNAME` with your GitHub username and adjust the repository name if needed.

### 2. Create and activate a virtual environment

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install the spaCy English model

Presidio's default NLP engine configuration commonly uses the `en_core_web_lg` model. Install it with:

```bash
python -m spacy download en_core_web_lg
```

If your Presidio installation is configured to use a different spaCy model, install the model specified by that configuration.

### 5. Run the application

```bash
streamlit run app.py
```

Streamlit will print a local address (usually `http://localhost:8501`) that you can open in your browser.

## Model Information

The application uses:

```text
distilbert-base-uncased-finetuned-sst-2-english
```

This is an English sentiment-classification model fine-tuned on SST-2. In this app, the output is presented as either `POSITIVE` or `NEGATIVE`; the application does not provide a neutral class.

The first run may take longer because the required model files are downloaded and initialized.

## Important Privacy and Usage Notes

- **Anonymization is not encryption.** The app replaces entities detected by Presidio; it does not encrypt the original text.
- **PII detection is not guaranteed to be complete.** Detection depends on Presidio recognizers, language support, configuration, and the confidence threshold. Review results before relying on them.
- **The sentiment model is English-focused.** Results on other languages, mixed-language text, slang, or domain-specific content may be unreliable.
- **This is a demonstration project, not a certified security or compliance solution.** Do not use it as the sole protection for sensitive, regulated, or production data.
- The application code runs the Presidio and sentiment workflows in the app process. However, the interface imports Google Fonts from an external service and loads the confetti JavaScript library from jsDelivr. Therefore, do not describe the complete application as fully offline or as making zero external network requests.
- In the CSV workflow, the app processes the first `N` rows selected by the user and drops the selected input text column from the downloadable output. Other CSV columns are retained.

## Current Scope and Limitations

- PII analysis is called with `language="en"`.
- Sentiment classification returns the model's positive/negative labels.
- The CSV interface processes a user-selected text column.
- The app is intended for experimentation, learning, and demonstration.

## Acknowledgements

This project uses the open-source work of:
- [Streamlit](https://streamlit.io/)
- [Microsoft Presidio](https://microsoft.github.io/presidio/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Pandas](https://pandas.pydata.org/)
- [spaCy](https://spacy.io/)

---

**SentinEL — Privacy-aware text analysis with PII anonymization and sentiment classification.**
