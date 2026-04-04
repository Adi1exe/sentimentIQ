import streamlit as st
import pandas as pd
import json
from utils.gemini_api import analyze_batch
from utils.state import add_to_history
from utils.ui_components import render_result_card, render_page_header

SAMPLE_CSV_CONTENT = """text
"The product is great but shipping was painfully slow. Took 3 weeks!"
"Excellent support team. Resolved my issue within hours. Will recommend."
"Invoice #4521 seems incorrect. We were charged twice for the same item."
"Worst experience ever. The software crashes every time I try to export."
"Pretty average. Nothing special, does the job but nothing more."
"""


def render():
    render_page_header(
        "📂 Batch Analysis",
        "Upload a CSV file or paste multiple texts (one per line) to analyze in bulk."
    )

    tab1, tab2 = st.tabs(["📄 CSV Upload", "📝 Paste Multiple Texts"])

    with tab1:
        st.markdown("Upload a CSV file with a column named **`text`** containing your feedback entries.")

        col1, col2 = st.columns([2, 1])
        with col2:
            st.download_button(
                "⬇ Download Sample CSV",
                data=SAMPLE_CSV_CONTENT,
                file_name="sample_feedback.csv",
                mime="text/csv",
                use_container_width=True
            )

        uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            if "text" not in df.columns:
                st.error("CSV must have a column named `text`.")
                return

            texts = df["text"].dropna().tolist()
            st.info(f"Found **{len(texts)}** entries. Ready to analyze.")

            if st.button(f"Analyze {len(texts)} Entries →", type="primary"):
                _run_batch(texts, df)

    with tab2:
        st.markdown("Paste one feedback entry per line.")
        multi_input = st.text_area(
            "Batch input",
            height=200,
            placeholder="The delivery was late and damaged.\nGreat product, fast shipping!\nCustomer service was unhelpful and rude.",
            label_visibility="collapsed"
        )

        if st.button("Analyze All →", type="primary", key="batch_text_btn"):
            texts = [t.strip() for t in multi_input.strip().splitlines() if t.strip()]
            if not texts:
                st.warning("Please enter at least one line of text.")
                return
            _run_batch(texts)


def _run_batch(texts: list, original_df: pd.DataFrame = None):
    progress = st.progress(0, text="Starting analysis...")
    results = []

    for i, text in enumerate(texts):
        from utils.gemini_api import analyze_single
        try:
            r = analyze_single(text)
        except Exception as e:
            r = {"input_text": text, "sentiment": "Error", "score": 0, "confidence": 0,
                 "root_issue": str(e), "key_themes": [], "urgency": "Low", "draft_response": ""}
        results.append(r)
        add_to_history(r)
        progress.progress((i + 1) / len(texts), text=f"Analyzing {i+1}/{len(texts)}...")

    progress.empty()
    st.success(f"✅ Analyzed {len(results)} entries.")

    # Summary table
    st.markdown("#### Summary Table")
    summary = pd.DataFrame([{
        "Text": r["input_text"][:60] + "..." if len(r["input_text"]) > 60 else r["input_text"],
        "Sentiment": r.get("sentiment", "—"),
        "Score": f"{r.get('score', 0)}/5",
        "Urgency": r.get("urgency", "—"),
        "Root Issue": r.get("root_issue", "—"),
    } for r in results])
    st.dataframe(summary, use_container_width=True)

    # Download results
    full_df = pd.DataFrame([{
        "text": r["input_text"],
        "sentiment": r.get("sentiment"),
        "score": r.get("score"),
        "confidence": r.get("confidence"),
        "root_issue": r.get("root_issue"),
        "urgency": r.get("urgency"),
        "key_themes": ", ".join(r.get("key_themes", [])),
        "draft_response": r.get("draft_response"),
    } for r in results])

    st.download_button(
        "⬇ Download Results CSV",
        data=full_df.to_csv(index=False),
        file_name="sentiment_results.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.markdown("#### Detailed Results")
    for i, result in enumerate(results):
        with st.expander(f"{result.get('sentiment','?')} · {result['input_text'][:70]}..."):
            render_result_card(result, i)
