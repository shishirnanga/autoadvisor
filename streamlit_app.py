import streamlit as st
from parse_csv import analyze_ab_test
from rag_engine import generate_recommendation
from parse_feedback import parse_feedback
from feedback_engine import generate_feedback_insights
from plot_utils import render_bar_chart
import streamlit.components.v1 as components
from ingest.parse_pdf import extract_text_from_pdf

st.set_page_config(page_title="AutoAdvisor", layout="wide")
st.markdown("""
    <style>
        /* Smooth content animation */
        .block-container {
            animation: fadeSlideUp 0.5s ease;
        }

        @keyframes fadeSlideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Header styling */
        .header-container {
            background: linear-gradient(to right, #e3f2fd, #e0f7fa);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }

        .header-container h1 {
            font-size: 2.8rem;
            margin: 0;
            color: #1e88e5;
        }

        .header-container .subtitle {
            font-size: 1.2rem;
            color: #555;
            margin-top: 0.5rem;
        }

        /* Tab header style */
        .stTabs [data-baseweb="tab"] {
            font-size: 1.1rem;
            color: #444;
            background-color: transparent;
            border-radius: 8px 8px 0 0;
            padding: 0.75rem 1.2rem;
            margin-right: 0.5rem;
            transition: all 0.3s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: #e3f2fd;
            color: #1e88e5;
            box-shadow: 0 2px 6px rgba(30, 136, 229, 0.2);
        }

        .stTabs [aria-selected="true"] {
            background-color: #bbdefb;
            color: #0d47a1;
            font-weight: bold;
            box-shadow: 0 -2px 8px rgba(0,0,0,0.1);
        }

        /* Card-style container */
        .st-emotion-cache-1y4p8pa {
            background-color: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(5px);
            border-radius: 15px;
            padding: 1.2rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
    </style>

    <div class="header-container">
        <h1>AutoAdvisor</h1>
        <div class="subtitle">Your AI-powered product strategy assistant</div>
    </div>
""", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs(["A/B Test Analyzer", "Feedback Analyzer", "Dashboard PDF"])

from parse_csv import analyze_ab_test
from plot_utils import render_bar_chart


with tab1:
    st.subheader("📊 Upload your A/B test CSV file")
    st.markdown("Upload a CSV with columns like `user_id`, `group`, and metrics such as `conversion_rate` or `avg_time_on_site`.")
    uploaded_file = st.file_uploader("Upload A/B Test CSV", type="csv", key="ab_test")

    if uploaded_file:
        try:
            summary, chart_data, stats = analyze_ab_test(uploaded_file)

            if stats.get("low_data_warning"):
                st.warning("⚠️ Not enough data to run a reliable statistical test.")
            else:
                with st.expander("📋 Summary Stats"):
                    st.code(summary)

                p = stats.get("p_value")
                if p is not None:
                    with st.expander("📌 P-Value Explanation"):
                        st.markdown("The **p-value** tells you if the observed difference between A and B is likely due to chance. If `p < 0.05`, it's considered statistically significant.")

                    if p < 0.05:
                        st.success(f"🎉 Statistically significant difference (p = {p:.4f})")
                        st.balloons()
                    else:
                        st.info(f"Not statistically significant (p = {p:.4f})")

                metric = st.selectbox("Select a metric to visualize", list(chart_data.keys()))
                fig = render_bar_chart(chart_data, metric)

                with st.expander("📈 View Bar Chart"):
                    if fig:
                        st.pyplot(fig)

                if st.button("💡 Generate Strategy Recommendation", key="ab_button"):
                    with st.spinner("🧠 GPT is thinking through the results..."):
                        insights = generate_recommendation(summary)
                        st.markdown("### 🧠 GPT Insights")
                        st.success(insights)
        except Exception as e:
            st.error(f"Error: {e}")



with tab2:
    st.subheader("💬 Upload customer feedback CSV")
    st.markdown("Upload a CSV with a `feedback` column. We'll extract key themes using GPT and summarize what users are saying.")

    feedback_file = st.file_uploader("Upload Feedback CSV", type="csv", key="feedback")

    if feedback_file:
        try:
            feedback_text = parse_feedback(feedback_file)

            with st.expander("📚 Raw Extracted Feedback"):
                st.code(feedback_text[:1000] + "\n..." if len(feedback_text) > 1000 else feedback_text)

            if st.button("💡 Summarize Feedback Insights", key="fb_button"):
                with st.spinner("🧠 GPT is reading your customers' voices..."):
                    fb_insights = generate_feedback_insights(feedback_text)
                    st.markdown("### 🧠 GPT Feedback Summary")
                    with st.expander("🔍 Key Themes & Sentiments"):
                        st.success(fb_insights)
        except Exception as e:
            st.error(f"Error processing feedback file: {e}")



with tab3:
    st.subheader("📄 Upload dashboard screenshot (PDF or image)")
    st.markdown("We'll extract text using OCR and suggest strategic takeaways.")

    pdf_file = st.file_uploader("Upload PDF/Image", type=["pdf", "png", "jpg", "jpeg"], key="pdf")

    if pdf_file:
        try:
            from ingest.parse_pdf import extract_text_from_pdf
            extracted_text = extract_text_from_pdf(pdf_file)

            with st.expander("📃 Extracted Dashboard Text"):
                st.code(extracted_text[:1000] + "\n..." if len(extracted_text) > 1000 else extracted_text)

            if st.button("💡 Analyze Dashboard Text", key="pdf_button"):
                with st.spinner("📊 GPT is reviewing dashboard trends..."):
                    insights = generate_recommendation(extracted_text)
                    st.markdown("### 🧠 GPT Dashboard Insights")
                    st.success(insights)
        except Exception as e:
            st.error(f"Error processing file: {e}")

