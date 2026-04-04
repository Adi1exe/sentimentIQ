import streamlit as st
from datetime import datetime


def init_history():
    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = []


def add_to_history(result: dict):
    init_history()
    entry = {**result, "timestamp": datetime.now().strftime("%H:%M:%S · %d %b %Y")}
    st.session_state.analysis_history.insert(0, entry)
    # Keep max 50 entries
    st.session_state.analysis_history = st.session_state.analysis_history[:50]


def get_history() -> list:
    init_history()
    return st.session_state.analysis_history


def clear_history():
    st.session_state.analysis_history = []


def get_dashboard_stats() -> dict:
    history = get_history()
    if not history:
        return {"total": 0, "positive": 0, "negative": 0, "neutral": 0, "mixed": 0, "avg_score": 0}

    sentiments = [h.get("sentiment", "Neutral") for h in history]
    scores = [h.get("score", 3) for h in history if h.get("score", 0) > 0]

    return {
        "total": len(history),
        "positive": sentiments.count("Positive"),
        "negative": sentiments.count("Negative"),
        "neutral": sentiments.count("Neutral"),
        "mixed": sentiments.count("Mixed"),
        "avg_score": round(sum(scores) / len(scores), 2) if scores else 0,
        "high_urgency": sum(1 for h in history if h.get("urgency") in ["High", "Critical"]),
    }
