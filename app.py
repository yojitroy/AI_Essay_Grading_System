import streamlit as st

from src.essay_analyzer import analyze_essay
from src.visualizations import create_radar_chart

from src.database import (
    create_database,
    save_essay,
    get_all_records,
    get_previous_essays
)

from src.analytics import (
    create_score_distribution,
    create_student_performance,
    create_metric_summary,
    create_score_pie_chart,
    create_plagiarism_chart,
    create_top_students
)

from src.report_generator import generate_pdf
from src.utils import ensure_reports_folder


# =================================================
# INIT (SAFE)
# =================================================
create_database()
ensure_reports_folder()


# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="AI Essay Grading System",
    page_icon="📝",
    layout="wide"
)


# =================================================
# SIMPLE CSS (UNCHANGED STYLE)
# =================================================
st.markdown("""
<style>

.big-title {
    font-size: 35px;
    font-weight: bold;
    text-align: center;
}

.subtitle {
    text-align:center;
    color:#94A3B8;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)


# =================================================
# SIDEBAR
# =================================================
st.sidebar.title("🔎 Navigation")

page = st.sidebar.radio(
    "Select Page",
    ["Essay Evaluation","Analytics Dashboard","Student History","About Project"]
)


# =================================================
# HEADER
# =================================================
st.markdown("""
<div class='big-title'>
📝 Automated Essay & Assignment Grading System
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='subtitle'>
Intelligent Essay Assessment using NLP, Machine Learning and Data Visualization
</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")


# =================================================
# SAFE RESULT HELPER (IMPORTANT)
# =================================================
def safe(result, key, default="N/A"):
    return result.get(key, default) if isinstance(result, dict) else default


# =================================================
# ESSAY EVALUATION PAGE
# =================================================
if page == "Essay Evaluation":

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Essay Input")
        essay_text = st.text_area("Paste Essay", height=300)

    with col2:
        st.subheader("Student Information")
        student_name = st.text_input("Student Name")
        essay_topic = st.text_input("Essay Topic")
        grade_level = st.selectbox(
            "Grade Level",
            ["School","Undergraduate","Postgraduate"]
        )

    if st.button("🚀 Analyze"):

        if not essay_text.strip():
            st.warning("Please enter an essay.")
            st.stop()

        if not essay_topic.strip():
            st.warning("Please enter an essay topic.")
            st.stop()

        try:
            previous_essays = get_previous_essays()

            result = analyze_essay(
                essay_text,
                essay_topic,
                previous_essays
            )

            save_essay(
                student_name,
                essay_topic,
                grade_level,
                essay_text,
                result
            )

            st.success("Essay analyzed successfully!")

        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            st.stop()


        # =================================================
        # ANALYSIS RESULTS
        # =================================================
        st.subheader("📊 Analysis Result")

        c1, c2, c3, c4, c5, c6 = st.columns(6)

        with c1: st.metric("Grammar", safe(result,"grammar_score"))
        with c2: st.metric("Vocabulary", safe(result,"vocabulary_score"))
        with c3: st.metric("Readability", safe(result,"readability_score"))
        with c4: st.metric("ML Score", safe(result,"ml_score"))
        with c5: st.metric("Topic", safe(result,"topic_score"))
        with c6: st.metric("Plagiarism %", safe(result,"plagiarism_score"))

        st.divider()


        # =================================================
        # RADAR CHART (SAFE)
        # =================================================
        chart_col, details_col = st.columns([2, 1])

        with chart_col:
            st.subheader("📈 Performance Radar Chart")

            try:
                fig = create_radar_chart(result)
                st.plotly_chart(fig, use_container_width=True)
            except:
                st.info("Radar chart unavailable")

        with details_col:
            st.subheader("📋 Essay Statistics")

            st.info(f"Words: {safe(result,'word_count')}")
            st.info(f"Sentences: {safe(result,'sentence_count')}")
            st.info(f"ML Score: {safe(result,'ml_score')}")
            st.info(f"Topic Relevance: {safe(result,'topic_score')}")
            st.info(f"Plagiarism: {safe(result,'plagiarism_score')}%")
            st.info(f"Final Score: {safe(result,'overall_score')}")


        st.divider()


        # =================================================
        # FINAL SCORE
        # =================================================
        st.subheader("🏆 Final Composite Score")

        st.metric(
            "Overall Essay Score",
            safe(result,"overall_score")
        )


        # =================================================
        # FEEDBACK (SAFE)
        # =================================================
        st.subheader("💡 AI Feedback")

        feedback_list = result.get("feedback", []) if isinstance(result, dict) else []

        if feedback_list:
            for item in feedback_list:
                st.success(item)
        else:
            st.info("No feedback generated.")


        # =================================================
        # PLAGIARISM STATUS
        # =================================================
        plagiarism = safe(result, "plagiarism_score", 0)

        if isinstance(plagiarism, (int, float)):
            if plagiarism < 20:
                st.success("✅ Original Content")
            elif plagiarism < 50:
                st.warning("⚠ Moderate Similarity Detected")
            else:
                st.error("❌ High Similarity Detected")


        st.divider()


        # =================================================
        # PDF GENERATION (SAFE)
        # =================================================
        try:
            pdf_file = (
                f"reports/"
                f"{student_name.replace(' ', '_')}_report.pdf"
            )

            generate_pdf(
                student_name,
                essay_topic,
                result,
                pdf_file
            )

            st.success("PDF Report Generated Successfully!")

            with open(pdf_file, "rb") as pdf:
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf,
                    file_name=f"{student_name}_report.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"PDF generation failed: {str(e)}")


# =================================================
# ANALYTICS DASHBOARD
# =================================================
elif page == "Analytics Dashboard":

    st.header(
        "📊 Analytics Dashboard"
    )
    df = get_all_records()

    if len(df) > 0:
        metrics = create_metric_summary(df)
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Total Essays",
                metrics["total_essays"]
            )

        with c2:
            st.metric(
                "Average Score",
                metrics["average_score"]
            )

        with c3:
            st.metric(
                "Highest Score",
                metrics["highest_score"]
            )

        with c4:
            st.metric(
                "Lowest Score",
                metrics["lowest_score"]
            )

        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(
                "📈 Score Distribution"
            )

            st.plotly_chart(
                create_score_distribution(df),
                use_container_width=True
            )

        with col2:
            st.subheader(
                "🥧 Performance Categories"
            )

            st.plotly_chart(
                create_score_pie_chart(df),
                use_container_width=True
            )

        st.divider()
        col3, col4 = st.columns(2)

        with col3:
            st.subheader(
                "🏆 Top Students"
            )

            st.plotly_chart(
                create_top_students(df),
                use_container_width=True
            )

        with col4:
            st.subheader(
                "📊 Student Performance"
            )

            st.plotly_chart(
                create_student_performance(df),
                use_container_width=True
            )

        st.divider()

        st.subheader(
            "🔍 Plagiarism vs Performance"
        )

        st.plotly_chart(
            create_plagiarism_chart(df),
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "📄 Recent Records"
        )

        st.dataframe(
            df.tail(20),
            use_container_width=True
        )

    else:

        st.info(
            "No records available."
        )


# =================================================
# STUDENT HISTORY
# =================================================
elif page == "Student History":

    st.header("📁 Student History")

    df = get_all_records()

    if df is not None and len(df) > 0:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records available.")


# =================================================
# ABOUT PROJECT
# =================================================
elif page == "About Project":

    st.header("ℹ️ About Project")

    st.write("""
### Automated Essay & Assignment Grading System

Technologies Used:
- Python
- Streamlit
- SQLite
- NLP (NLTK, TextBlob)
- Sentence Transformers
- Scikit-learn
- Plotly
- ReportLab

Features:
- Essay Scoring Engine
- Grammar & Vocabulary Analysis
- Semantic Similarity
- Plagiarism Detection
- Radar Visualization
- PDF Report Generation
- Student Analytics Dashboard
""")