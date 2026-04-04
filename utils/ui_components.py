import streamlit as st


SENTIMENT_COLORS = {
    "Positive": "#22c55e",
    "Negative": "#ef4444",
    "Neutral": "#eab308",
    "Mixed": "#a855f7",
    "Error": "#6b7280",
}

URGENCY_COLORS = {
    "Low": "#22c55e",
    "Medium": "#eab308",
    "High": "#f97316",
    "Critical": "#ef4444",
}


def render_result_card(result: dict, index: int = 0):
    sentiment = result.get("sentiment", "Neutral").lower()
    badge_class = f"badge-{sentiment}"
    card_class = f"result-card {sentiment}"

    score = result.get("score", 3)
    confidence = result.get("confidence", 0.0)
    urgency = result.get("urgency", "Low")
    root_issue = result.get("root_issue", "—")
    themes = result.get("key_themes", [])
    draft = result.get("draft_response", "")
    text = result.get("input_text", "")

    urgency_color = URGENCY_COLORS.get(urgency, "#888")
    sentiment_color = SENTIMENT_COLORS.get(result.get("sentiment", "Neutral"), "#888")

    themes_html = "".join(
        f'<span style="background:#1f1f3a;color:#a5b4fc;border-radius:20px;padding:3px 10px;font-size:0.72rem;margin-right:6px;">{t}</span>'
        for t in themes
    )

    st.markdown(f"""
    <div class="{card_class}">
        <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
            <span class="sentiment-badge {badge_class}">{result.get("sentiment","Neutral")}</span>
            <span style="font-size:0.75rem;color:{urgency_color};font-weight:600;">
                ⚡ {urgency} Urgency
            </span>
        </div>

        <div class="original-text">"{text[:300]}{"..." if len(text) > 300 else ""}"</div>

        <div style="margin: 12px 0;">{themes_html}</div>

        <div class="root-issue">🎯 Root Issue: <span>{root_issue}</span></div>

        <div style="margin-top:14px;">
            {_score_bar("Sentiment Score", score, 5, sentiment_color)}
            {_score_bar("Confidence", int(confidence * 5), 5, "#6c63ff")}
        </div>

        <div class="draft-response">
            <div style="font-size:0.72rem;color:#666;margin-bottom:6px;text-transform:uppercase;letter-spacing:1px;">✉ Draft Response</div>
            {draft}
        </div>
    </div>
    """, unsafe_allow_html=True)


def _score_bar(label: str, value: int, max_val: int, color: str) -> str:
    pct = int((value / max_val) * 100)
    return f"""
    <div class="score-row">
        <div class="score-label">{label}</div>
        <div class="score-bar-bg">
            <div class="score-bar-fill" style="width:{pct}%;background:{color};"></div>
        </div>
        <div class="score-val">{value}/{max_val}</div>
    </div>
    """


def render_page_header(title: str, subtitle: str):
    st.markdown(f"""
    <div class="page-header">
        <h2>{title}</h2>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_stats_row(stats: dict):
    cols = st.columns(4)
    items = [
        ("Total Analyzed", stats["total"], "all time"),
        ("Avg Score", f"{stats['avg_score']}/5", "sentiment score"),
        ("Negative", stats["negative"], "need attention"),
        ("High Urgency", stats.get("high_urgency", 0), "flag for review"),
    ]
    for col, (label, value, sub) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">{label}</div>
                <div class="value">{value}</div>
                <div class="sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)
