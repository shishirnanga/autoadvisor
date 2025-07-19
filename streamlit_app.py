import streamlit as st
from parse_csv import analyze_ab_test
from rag_engine import generate_recommendation
from parse_feedback import parse_feedback
from feedback_engine import generate_feedback_insights

st.set_page_config(page_title="AutoAdvisor", layout="wide")
st.title("AutoAdvisor – Your Product Strategy Copilot")

tab1, tab2 = st.tabs(["A/B Test Analyzer", "Feedback Analyzer"])

with tab1:
    st.subheader("Upload your A/B test CSV file")
    uploaded_file = st.file_uploader("CSV for A/B test", type="csv", key="ab_test")

    if uploaded_file:
        try:
            summary = analyze_ab_test(uploaded_file)
            st.subheader("Experiment Summary")
            st.code(summary)

            if st.button("Generate Recommendations", key="ab_button"):
                with st.spinner("Thinking..."):
                    insights = generate_recommendation(summary)
                    st.subheader("Product Recommendation")
                    st.write(insights)
        except Exception as e:
            st.error(f"Error processing file: {e}")

with tab2:
    st.subheader("Upload Customer Feedback (CSV format)")
    feedback_file = st.file_uploader("CSV with a 'feedback' column", type="csv", key="feedback")

    if feedback_file:
        try:
            feedback_text = parse_feedback(feedback_file)
            if st.button("Analyze Feedback", key="feedback_button"):
                with st.spinner("Analyzing..."):
                    result = generate_feedback_insights(feedback_text)
                    st.subheader("Key Insights & Suggestions")
                    st.write(result)
        except Exception as e:
            st.error(f"Error processing feedback file: {e}")
