# AutoAdvisor — LLM Product Strategy Assistant
Turns dashboards, A/B results, and user feedback into concise next-step recommendations.

## Why
PMs drown in data; AutoAdvisor summarizes signals and proposes actions in seconds.

## What it does
- Feedback clustering & themes
- A/B test parser with key metrics
- Dashboard Q&A (CSV/PDF/text ingestion)
- Streamlit UI for interactive exploration

## Stack
Python • Streamlit • RAG (FAISS/Chroma) • OpenAI API • pandas • scikit-learn

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
