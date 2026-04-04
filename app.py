import streamlit as st

st.set_page_config(
    page_title="SentimentIQ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from pages import single_analysis, batch_analysis, history, dashboard

PAGES = {
    "🔍 Single Analysis": single_analysis,
    "📂 Batch Analysis": batch_analysis,
    "📊 Dashboard": dashboard,
    "🕘 History": history,
}

st.sidebar.markdown("""
<div class="sidebar-header">
    <h1>🧠 SentimentIQ</h1>
    <p>AI-powered sentiment analysis for business text</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
selection = st.sidebar.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div class="sidebar-footer">
    <small>Built by ADITYA DOLAS · Tophawks Assignment Q5</small>
</div>
""", unsafe_allow_html=True)

page = PAGES[selection]
page.render()
