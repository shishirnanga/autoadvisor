import streamlit as st
from parse_csv import analyze_ab_test
from rag_engine import generate_recommendation
from parse_feedback import parse_feedback
from feedback_engine import generate_feedback_insights
from plot_utils import render_bar_chart

st.set_page_config(page_title="AutoAdvisor", layout="wide")
st.markdown("""
    <style>
        body {
            background-image: url("header_bg.jpg");
            background-size: cover;
            background-attachment: fixed;
        }
        .header-container {
            background: linear-gradient(to right, #f2f7fc, #e0eafc);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }

        .header-container h1 {
            font-size: 2.8rem;
            color: #3366cc;
            margin-bottom: 0.5rem;
        }

        .header-container .subtitle {
            font-size: 1.25rem;
            color: #666;
        }
        .header-container:hover {
            box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 1.05rem;
            font-weight: 500;
            color: #444;
        }
        [data-baseweb="tab-list"] {
            margin-bottom: 1rem;
        }
        /* Inactive tab style */
        [data-baseweb="tab"] {
            background-color: #F0FFFF;
            color: #0000FF;
            border-radius: 6px 6px 0 0;
            padding: 0.75rem 1.2rem;
            margin-right: 0.5rem;
            transition: all 0.3s ease;
            font-weight: 500;
        }

        /* Hover effect */
        [data-baseweb="tab"]:hover {
            background-color: #333333;
            color: #fff;
        }

        /* Active tab style */
        [data-baseweb="tab"][aria-selected="true"] {
            background-color: #4a90e2;
            color: white;
            font-weight: 600;
            box-shadow: 0 -3px 10px rgba(74, 144, 226, 0.4);
        }
        .logo {
            display: flex;
            justify-content: center;
            margin-top: -1rem;
            margin-bottom: 1rem;
        }
        .logo img {
            width: 80px;
            height: auto;
        }
    </style>

    <div class="header-container">
        <h1>AutoAdvisor</h1>
        <div class="subtitle">Your AI-powered product strategy assistant</div>
    </div>
    <div class="logo">
        <img src="logo.jpg" alt="logo">
    </div>
""", unsafe_allow_html=True)



tab1, tab2, tab3 = st.tabs(["A/B Test Analyzer", "Feedback Analyzer", "Dashboard PDF"])



from parse_csv import analyze_ab_test
from plot_utils import render_bar_chart

...

with tab1:
    st.subheader("Upload your A/B test CSV file")
    st.markdown("Upload a CSV with columns like `user_id`, `group`, and metrics such as `conversion_rate` or `avg_time_on_site`.")
    uploaded_file = st.file_uploader("Upload A/B Test CSV", type="csv", key="ab_test")
    st.markdown("")

    if uploaded_file:
        try:
            summary, chart_data, stats = analyze_ab_test(uploaded_file)

            if stats.get("low_data_warning"):
                st.warning("⚠️ Not enough data to run a reliable statistical test.")
            else:
                st.markdown("### Summary Stats")
                st.code(summary)

                p = stats.get("p_value")
                if p is not None:
                    if p < 0.05:
                        st.success(f"The result is statistically significant (p = {p:.4f})")
                    else:
                        st.info(f"The result is NOT statistically significant (p = {p:.4f})")

                metric = st.selectbox("Select a metric to visualize", list(chart_data.keys()))
                fig = render_bar_chart(chart_data, metric)
                if fig:
                    st.pyplot(fig)

                st.markdown("")
                if st.button("Generate Strategy Recommendation", key="ab_button"):
                    with st.spinner("GPT is thinking..."):
                        from rag_engine import generate_recommendation
                        insights = generate_recommendation(summary)
                        st.markdown("### GPT Insights")
                        st.success(insights)
        except Exception as e:
            st.error(f"Error: {e}")


with tab2:
    st.subheader("Upload customer feedback CSV")
    st.markdown("Upload a CSV with a `feedback` column. We'll extract key themes using GPT.")

    feedback_file = st.file_uploader("Upload Feedback CSV", type="csv", key="feedback")
    st.markdown("")

    if feedback_file:
        try:
            feedback_text = parse_feedback(feedback_file)
            st.markdown("### Raw Extracted Feedback")
            st.code(feedback_text[:1000] + "\n..." if len(feedback_text) > 1000 else feedback_text)

            if st.button("Summarize Feedback Insights", key="fb_button"):
                with st.spinner("GPT is reading feedback..."):
                    fb_insights = generate_feedback_insights(feedback_text)
                    st.markdown("### GPT Insights")
                    st.success(fb_insights)
        except Exception as e:
            st.error(f"Error processing feedback file: {e}")


with tab3:
    st.subheader("Upload dashboard screenshot (PDF or image)")
    st.markdown("We'll use OCR to extract text and generate strategy suggestions.")

    pdf_file = st.file_uploader("Upload PDF/Image", type=["pdf", "png", "jpg", "jpeg"], key="pdf")
    st.markdown("")

    if pdf_file:
        try:
            from ingest.parse_pdf import extract_text_from_pdf
            extracted_text = extract_text_from_pdf(pdf_file)
            st.markdown("### Extracted Text")
            st.code(extracted_text[:1000] + "\n..." if len(extracted_text) > 1000 else extracted_text)

            if st.button("Analyze Dashboard Text", key="pdf_button"):
                with st.spinner("GPT is analyzing dashboard..."):
                    insights = generate_recommendation(extracted_text)
                    st.markdown("### GPT Insights")
                    st.success(insights)
        except Exception as e:
            st.error(f"Error processing file: {e}")
