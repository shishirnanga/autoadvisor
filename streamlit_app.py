import streamlit as st
from parse_csv import analyze_ab_test
from rag_engine import generate_recommendation

st.set_page_config(page_title="AutoAdvisor", layout = "centered")
st.title("AutoAdvisor - A/B Test Strategy Assistant")

st.write("Upload your A/B test CSV and get product insights powered by GPT.")

uploaded_file = st.file_uploader("Upload your A/B test CSV file", type="csv")

if uploaded_file:
    try:
        summary = analyze_ab_test(uploaded_file)
        st.subheader("Experiment Summary")
        st.code(summary)

        if st.button("Generate Recommendations"):
            with st.spinner("Thinking..."):
                insights = generate_recommendation(summary)
                st.subheader("Product Recommendation")
                st.write(insights)
    except Exception as e:
        st.error(f"Error processing file: {e}")