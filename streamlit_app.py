import streamlit as st
from parse_csv import analyze_ab_test
from rag_engine import generate_recommendation
from parse_feedback import parse_feedback
from feedback_engine import generate_feedback_insights
from plot_utils import render_bar_chart

st.set_page_config(page_title="AutoAdvisor", layout="wide")
st.title("AutoAdvisor – Your Product Strategy Copilot")

tab1, tab2, tab3 = st.tabs(["A/B Test", "Feedback", "Dashboard PDF"])


from parse_csv import analyze_ab_test
from plot_utils import render_bar_chart

...

with tab1:
    st.subheader("Upload your A/B test CSV file")
    uploaded_file = st.file_uploader("CSV for A/B test", type="csv", key="ab_test")

    if uploaded_file:
        try:
            summary, chart_data = analyze_ab_test(uploaded_file)
            st.subheader("Experiment Summary")
            st.code(summary)

            metric = st.selectbox("Select metric to visualize", list(chart_data.keys()))
            fig = render_bar_chart(chart_data, metric)
            if fig:
                st.pyplot(fig)

            if st.button("Generate Recommendations", key="ab_button"):
                with st.spinner("Thinking..."):
                    from rag_engine import generate_recommendation
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

with tab3:
    st.subheader("Upload a Dashboard PDF")
    pdf_file = st.file_uploader("PDF report / dashboard", type="pdf")

    if pdf_file:
        if st.button("Analyse PDF"):
            with st.spinner("Extracting & analysing..."):
                from parse_pdf import extract_text_from_pdf
                from pdf_engine import analyse_dashboard

                pdf_text = extract_text_from_pdf(pdf_file)
                if not pdf_text:
                    st.error("No extractable text found in that PDF.")
                else:
                    summary = analyse_dashboard(pdf_text)
                    st.subheader("Dashboard Insights")
                    st.write(summary)
