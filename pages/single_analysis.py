import streamlit as st
from utils.openai_api import analyze_single
from utils.state import add_to_history, get_dashboard_stats
from utils.ui_components import render_result_card, render_page_header, render_stats_row

EXAMPLE_TEXTS = [
    "Your delivery was 5 days late and the product arrived completely damaged. This is the third time this has happened and I'm done with your service.",
    "The onboarding experience was smooth and the support team was incredibly helpful. We saw ROI within the first month — very impressed!",
    "The product itself is decent but the pricing is too high for what you get. Customer support takes too long to respond.",
    "Just checking in on our invoice from last week. Haven't received any update yet.",
]


def render():
    render_page_header(
        "🔍 Single Text Analysis",
        "Paste any customer feedback, email, review, or complaint and get instant structured sentiment insights."
    )

    stats = get_dashboard_stats()
    if stats["total"] > 0:
        render_stats_row(stats)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("#### Input Text")

    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        example_pick = st.selectbox("Load an example", ["— choose —"] + [f"Example {i+1}" for i in range(len(EXAMPLE_TEXTS))], label_visibility="collapsed")

    with col1:
        default_text = ""
        if example_pick != "— choose —":
            idx = int(example_pick.split(" ")[1]) - 1
            default_text = EXAMPLE_TEXTS[idx]

        user_input = st.text_area(
            "Text input",
            value=default_text,
            height=160,
            placeholder="Paste customer feedback, complaint, email, or review here...",
            label_visibility="collapsed"
        )

    col_btn, col_clear = st.columns([1, 5])
    with col_btn:
        analyze_clicked = st.button("Analyze →", type="primary", use_container_width=True)

    if analyze_clicked:
        if not user_input.strip():
            st.warning("Please enter some text to analyze.")
            return

        with st.spinner("Analyzing sentiment..."):
            result = analyze_single(user_input.strip())
            add_to_history(result)

        st.markdown("---")
        st.markdown("#### Result")
        render_result_card(result)

        with st.expander("📋 Raw JSON Output"):
            import json
            st.code(json.dumps({k: v for k, v in result.items() if k != "input_text"}, indent=2), language="json")
