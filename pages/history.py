import streamlit as st
from utils.state import get_history, clear_history
from utils.ui_components import render_page_header, SENTIMENT_COLORS


def render():
    render_page_header(
        "🕘 Analysis History",
        "All sentiment analyses from this session, most recent first."
    )

    history = get_history()

    if not history:
        st.info("No history yet. Start analyzing text in **Single Analysis** or **Batch Analysis**.")
        return

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"**{len(history)}** analyses in this session")
    with col2:
        if st.button("🗑 Clear History", use_container_width=True):
            clear_history()
            st.rerun()

    st.markdown("---")

    for entry in history:
        sentiment = entry.get("sentiment", "Neutral")
        color = SENTIMENT_COLORS.get(sentiment, "#888")
        score = entry.get("score", 0)
        urgency = entry.get("urgency", "Low")
        text_preview = entry.get("input_text", "")[:90]
        timestamp = entry.get("timestamp", "")

        st.markdown(f"""
        <div class="history-row">
            <span style="width:10px;height:10px;border-radius:50%;background:{color};display:inline-block;flex-shrink:0;"></span>
            <span style="color:{color};font-weight:600;font-size:0.78rem;width:70px;flex-shrink:0;">{sentiment}</span>
            <span class="history-text">{text_preview}{"..." if len(entry.get("input_text","")) > 90 else ""}</span>
            <span style="color:#a5b4fc;font-size:0.75rem;width:40px;flex-shrink:0;">{score}/5</span>
            <span style="font-size:0.72rem;color:#f97316;width:60px;flex-shrink:0;">{urgency}</span>
            <span class="history-time">{timestamp}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    import pandas as pd
    export_df = pd.DataFrame([{
        "timestamp": e.get("timestamp"),
        "text": e.get("input_text"),
        "sentiment": e.get("sentiment"),
        "score": e.get("score"),
        "urgency": e.get("urgency"),
        "root_issue": e.get("root_issue"),
        "key_themes": ", ".join(e.get("key_themes", [])),
    } for e in history])

    st.download_button(
        "⬇ Export History as CSV",
        data=export_df.to_csv(index=False),
        file_name="sentiment_history.csv",
        mime="text/csv"
    )
