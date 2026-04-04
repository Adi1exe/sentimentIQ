import streamlit as st
import pandas as pd
from utils.state import get_history, get_dashboard_stats
from utils.ui_components import render_page_header, render_stats_row


def render():
    render_page_header(
        "📊 Analytics Dashboard",
        "Visual breakdown of all analyzed texts in this session."
    )

    history = get_history()

    if not history:
        st.info("No analyses yet. Go to **Single Analysis** or **Batch Analysis** to get started.")
        return

    stats = get_dashboard_stats()
    render_stats_row(stats)
    st.markdown("<br>", unsafe_allow_html=True)

    df = pd.DataFrame(history)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Sentiment Distribution")
        sentiment_counts = df["sentiment"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentiment", "Count"]

        colors_map = {
            "Positive": "#22c55e",
            "Negative": "#ef4444",
            "Neutral": "#eab308",
            "Mixed": "#a855f7",
            "Error": "#6b7280",
        }

        try:
            import plotly.express as px
            color_seq = [colors_map.get(s, "#888") for s in sentiment_counts["Sentiment"]]
            fig = px.pie(
                sentiment_counts,
                values="Count",
                names="Sentiment",
                color="Sentiment",
                color_discrete_map=colors_map,
                hole=0.45,
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#ccc",
                legend=dict(font=dict(color="#aaa")),
                margin=dict(t=20, b=20, l=20, r=20),
            )
            st.plotly_chart(fig, use_container_width=True)
        except ImportError:
            st.bar_chart(sentiment_counts.set_index("Sentiment"))

    with col2:
        st.markdown("#### Score Distribution")
        score_counts = df["score"].value_counts().sort_index().reset_index()
        score_counts.columns = ["Score", "Count"]
        score_counts["Score"] = score_counts["Score"].astype(str)

        try:
            import plotly.express as px
            fig2 = px.bar(
                score_counts,
                x="Score",
                y="Count",
                color_discrete_sequence=["#6c63ff"],
            )
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#ccc",
                xaxis=dict(title="Score (1-5)", color="#888"),
                yaxis=dict(title="Count", color="#888"),
                margin=dict(t=20, b=20, l=20, r=20),
            )
            st.plotly_chart(fig2, use_container_width=True)
        except ImportError:
            st.bar_chart(score_counts.set_index("Score"))

    st.markdown("#### Urgency Breakdown")
    urgency_counts = df["urgency"].value_counts().reset_index()
    urgency_counts.columns = ["Urgency", "Count"]
    urgency_colors = {"Low": "#22c55e", "Medium": "#eab308", "High": "#f97316", "Critical": "#ef4444"}

    try:
        import plotly.express as px
        fig3 = px.bar(
            urgency_counts,
            x="Urgency",
            y="Count",
            color="Urgency",
            color_discrete_map=urgency_colors,
        )
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#ccc",
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
        )
        st.plotly_chart(fig3, use_container_width=True)
    except ImportError:
        st.bar_chart(urgency_counts.set_index("Urgency"))
