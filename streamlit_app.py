import streamlit as st
from parse_csv import analyze_ab_test
from rag_engine import generate_recommendation
from parse_feedback import parse_feedback
from feedback_engine import generate_feedback_insights
from plot_utils import render_bar_chart

st.set_page_config(page_title="AutoAdvisor", layout="wide")
st.markdown("""
    <style>
        .main {
            background-color: #FFE4C4;
        }
        h1 {
            font-size: 2.5rem;
            color: #222;
        }
        .subtitle {
            font-size: 1.1rem;
            color: #666;
        }
        .stApp {
            padding: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("### 🤖 AutoAdvisor")
st.markdown("<div class='subtitle'>Your AI-powered product strategy assistant</div>", unsafe_allow_html=True)
st.markdown("---")
st.image("logo.png", width=80)  


tab1, tab2, tab3 = st.tabs(["📊 A/B Test Analyzer", "💬 Feedback Analyzer", "📄 Dashboard PDF"])



from parse_csv import analyze_ab_test
from plot_utils import render_bar_chart

...

with tab1:
    st.subheader("📊 Upload your A/B test CSV file")
    st.markdown("Upload a CSV with columns like `user_id`, `group`, and metrics such as `conversion_rate` or `avg_time_on_site`.")
    uploaded_file = st.file_uploader("Upload A/B Test CSV", type="csv", key="ab_test")
    st.markdown("")

    if uploaded_file:
        try:
            summary, chart_data, stats = analyze_ab_test(uploaded_file)

            if stats.get("low_data_warning"):
                st.warning("⚠️ Not enough data to run a reliable statistical test.")
            else:
                st.markdown("### 🧾 Summary Stats")
                st.code(summary)

                p = stats.get("p_value")
                if p is not None:
                    if p < 0.05:
                        st.success(f"🚨 The result is statistically significant (p = {p:.4f})")
                    else:
                        st.info(f"ℹ️ The result is NOT statistically significant (p = {p:.4f})")

                metric = st.selectbox("📈 Select a metric to visualize", list(chart_data.keys()))
                fig = render_bar_chart(chart_data, metric)
                if fig:
                    st.pyplot(fig)

                st.markdown("")
                if st.button("💡 Generate Strategy Recommendation", key="ab_button"):
                    with st.spinner("GPT is thinking..."):
                        from rag_engine import generate_recommendation
                        insights = generate_recommendation(summary)
                        st.markdown("### 🧠 GPT Insights")
                        st.success(insights)
        except Exception as e:
            st.error(f"Error: {e}")


with tab2:
    st.subheader("💬 Upload customer feedback CSV")
    st.markdown("Upload a CSV with a `feedback` column. We'll extract key themes using GPT.")

    feedback_file = st.file_uploader("Upload Feedback CSV", type="csv", key="feedback")
    st.markdown("")

    if feedback_file:
        try:
            feedback_text = parse_feedback(feedback_file)
            st.markdown("### 📚 Raw Extracted Feedback")
            st.code(feedback_text[:1000] + "\n..." if len(feedback_text) > 1000 else feedback_text)

            if st.button("💡 Summarize Feedback Insights", key="fb_button"):
                with st.spinner("GPT is reading feedback..."):
                    fb_insights = generate_feedback_insights(feedback_text)
                    st.markdown("### 🧠 GPT Insights")
                    st.success(fb_insights)
        except Exception as e:
            st.error(f"Error processing feedback file: {e}")


with tab3:
    st.subheader("📄 Upload dashboard screenshot (PDF or image)")
    st.markdown("We'll use OCR to extract text and generate strategy suggestions.")

    pdf_file = st.file_uploader("Upload PDF/Image", type=["pdf", "png", "jpg", "jpeg"], key="pdf")
    st.markdown("")

    if pdf_file:
        try:
            from ingest.parse_pdf import extract_text_from_pdf
            extracted_text = extract_text_from_pdf(pdf_file)
            st.markdown("### 📃 Extracted Text")
            st.code(extracted_text[:1000] + "\n..." if len(extracted_text) > 1000 else extracted_text)

            if st.button("💡 Analyze Dashboard Text", key="pdf_button"):
                with st.spinner("GPT is analyzing dashboard..."):
                    insights = generate_recommendation(extracted_text)
                    st.markdown("### 🧠 GPT Insights")
                    st.success(insights)
        except Exception as e:
            st.error(f"Error processing file: {e}")
