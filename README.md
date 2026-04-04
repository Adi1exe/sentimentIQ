# 🧠 SentimentIQ — AI-Powered Sentiment Analysis Tool

> Built for **Tophawks AI Internship — Screening Assignment Q5 (Builder Challenge)**

SentimentIQ is a Streamlit app that uses the **Gemini API (Google)** to analyze sentiment in customer feedback, complaints, emails, and business text — returning structured, actionable insights.

---

## 🚀 Features

| Feature | Description |
|---|---|
| **Single Analysis** | Paste any text and get instant sentiment breakdown |
| **Batch Analysis** | Upload a CSV or paste multiple texts for bulk processing |
| **Analytics Dashboard** | Visual charts — sentiment distribution, score spread, urgency |
| **History** | Session-scoped analysis log with CSV export |
| **Structured Output** | Every analysis returns Sentiment, Score, Confidence, Root Issue, Key Themes, Urgency, Draft Response |

---

## 📁 Project Structure

```
sentiment_analyzer/
├── app.py                  # Entry point
├── requirements.txt
├── assets/
│   └── style.css           # Custom dark theme styling
├── pages/
│   ├── single_analysis.py  # Single text analysis page
│   ├── batch_analysis.py   # Batch/CSV analysis page
│   ├── dashboard.py        # Charts & analytics
│   └── history.py          # Session history log
└── utils/
    ├── gemini_api.py        # Gemini API calls + system prompt
    ├── state.py             # Session state / history management
    └── ui_components.py     # Shared UI rendering components
```

---

## ⚙️ Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/Adi1exe/TopHawks-Practical-Screening-Assignment.git
cd TopHawks-Practical-Screening-Assignment
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your API key
Create a `.env` file and add your key:
```bash
cp .env.example .env
GEMINI_API_KEY=your_key_here
```

### 4. Run the app
```bash
streamlit run app.py
```

---

## 🧠 How It Works

Each text input is sent to `gemini-2.5-flash` with a carefully engineered system prompt that forces structured JSON output:

```json
{
  "sentiment": "Negative",
  "score": 2,
  "confidence": 0.91,
  "root_issue": "Late delivery and damaged product",
  "key_themes": ["delivery delay", "product damage", "repeat issue"],
  "urgency": "High",
  "draft_response": "We sincerely apologize for the repeated inconvenience..."
}
```

The system prompt enforces strict JSON-only output with no markdown fences, making parsing reliable across all inputs.

---

## 📊 Sample Output (Batch CSV)

| text | sentiment | score | urgency | root_issue |
|---|---|---|---|---|
| "Delivery was 5 days late..." | Negative | 1 | Critical | Repeated delivery failure |
| "Onboarding was smooth..." | Positive | 5 | Low | Positive onboarding experience |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI**: Google Gemini API (`gemini-2.5-flash`)
- **Data**: Pandas
- **Charts**: Plotly
- **Styling**: Custom CSS (dark theme)

---

## 👤 Author

Built by **Adi** · Final Year AI&DS Student · [GitHub](https://github.com/Adi1exe)