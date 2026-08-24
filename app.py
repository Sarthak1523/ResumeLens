import streamlit as st
import os
import sys
import pandas as pd

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.pdf_parser import extract_text_from_pdf
from utils.nlp_processor import calculate_tf_idf_similarity, preprocess_text
from utils.skill_extractor import analyze_skill_gap
from utils.suggestion_engine import generate_resume_suggestions
from sample_data.sample_resume_data import SAMPLE_RESUME_TEXT, SAMPLE_JD_TEXT

# Streamlit Page Configuration
st.set_page_config(
    page_title="Resume Lens AI – Resume JD Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished UI
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #555555;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 8px;
        padding: 1.2rem;
        border-left: 5px solid #1E88E5;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .skill-badge-matched {
        display: inline-block;
        background-color: #E8F5E9;
        color: #2E7D32;
        border: 1px solid #A5D6A7;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.88rem;
        font-weight: 600;
        margin: 3px;
    }
    .skill-badge-missing {
        display: inline-block;
        background-color: #FFEBEE;
        color: #C62828;
        border: 1px solid #EF9A9A;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.88rem;
        font-weight: 600;
        margin: 3px;
    }
    .skill-badge-extra {
        display: inline-block;
        background-color: #E3F2FD;
        color: #1565C0;
        border: 1px solid #90CAF9;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.88rem;
        font-weight: 600;
        margin: 3px;
    }
    .alert-high {
        background-color: #FFF3E0;
        border-left: 4px solid #EF6C00;
        padding: 10px 15px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    .alert-positive {
        background-color: #E8F5E9;
        border-left: 4px solid #2E7D32;
        padding: 10px 15px;
        border-radius: 4px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Header Section
    st.markdown('<div class="main-title">🔍 Resume Lens AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Automated Resume Job Description Analyzer | Powered by PyMuPDF, Scikit-Learn & NLP</div>', unsafe_allow_html=True)
    
    st.sidebar.header("⚙️ Control Panel")
    
    # Selection of input mode
    input_mode = st.sidebar.radio(
        "Choose Input Method:",
        ["Upload PDF Resume", "Paste Resume Text", "⚡ Load Preloaded Demo Data"],
        index=2
    )

    resume_text = ""
    pdf_metadata = {}
    
    # 1. Handling Input Methods
    if input_mode == "Upload PDF Resume":
        uploaded_file = st.sidebar.file_uploader("Upload PDF Resume", type=["pdf"])
        if uploaded_file is not None:
            try:
                resume_text, pdf_metadata = extract_text_from_pdf(uploaded_file)
                st.sidebar.success(f"✅ Extracted {pdf_metadata.get('total_words', 0)} words across {pdf_metadata.get('page_count', 0)} page(s).")
            except Exception as e:
                st.sidebar.error(f"Error parsing PDF: {e}")
        else:
            st.info("👈 Please upload a PDF resume using the sidebar control panel.")

    elif input_mode == "Paste Resume Text":
        resume_text = st.sidebar.text_area("Paste Candidate Resume Text:", height=200)

    else: # Preloaded Demo Data
        st.sidebar.success("Loaded preloaded sample resume & job description!")
        resume_text = SAMPLE_RESUME_TEXT

    # 2. Job Description Input
    if input_mode == "⚡ Load Preloaded Demo Data":
        jd_text = st.sidebar.text_area("Job Description:", value=SAMPLE_JD_TEXT, height=220)
    else:
        jd_text = st.sidebar.text_area("Paste Job Description:", height=200)

    # Action Button
    analyze_btn = st.sidebar.button("🚀 Analyze Resume & Job Description", type="primary", use_container_width=True)

    # Automatically analyze if demo mode is active or user clicked analyze button
    if analyze_btn or (input_mode == "⚡ Load Preloaded Demo Data" and resume_text and jd_text):
        if not resume_text.strip():
            st.warning("Please provide resume content to begin analysis.")
            return
        if not jd_text.strip():
            st.warning("Please provide a job description to calculate match score.")
            return

        with st.spinner("Processing text, running TF-IDF vectorizer & extracting skills..."):
            # Compute similarity metrics
            tfidf_results = calculate_tf_idf_similarity(resume_text, jd_text)
            
            # Analyze skill gap
            skill_gap_results = analyze_skill_gap(resume_text, jd_text)
            
            # Generate actionable suggestions
            suggestions = generate_resume_suggestions(resume_text, jd_text, tfidf_results, skill_gap_results)

        match_score = tfidf_results["match_percentage"]
        matched_count = skill_gap_results["matched_skills_count"]
        missing_count = skill_gap_results["missing_skills_count"]
        word_count = len(resume_text.split())

        # Top Executive Metric Summary Row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="🎯 ATS Match Score", value=f"{match_score}%")
        with col2:
            st.metric(label="✅ Matched Skills", value=f"{matched_count} skills")
        with col3:
            st.metric(label="⚠️ Missing Skills", value=f"{missing_count} skills")
        with col4:
            st.metric(label="📄 Resume Word Count", value=f"{word_count} words")

        st.divider()

        # Detailed Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Match Score & Keywords", 
            "🎯 Skill Gap Analysis", 
            "💡 ATS Suggestions", 
            "📝 Extracted Content"
        ])

        # TAB 1: Match Score & Keywords
        with tab1:
            st.subheader("ATS Match Score Breakdown")
            
            # Visual Progress Bar
            st.progress(min(int(match_score), 100))
            
            if match_score >= 75:
                st.success("🟢 **High Match**: Candidate profile is strongly aligned with this job description.")
            elif match_score >= 50:
                st.warning("🟡 **Moderate Match**: Candidate has solid core qualifications but is missing key job keywords.")
            else:
                st.error("🔴 **Low Match**: Resume requires optimization to align with target role requirements.")

            st.markdown("---")
            kcol1, kcol2 = st.columns(2)
            
            with kcol1:
                st.markdown("##### 🟢 Top Matching TF-IDF Keywords")
                top_matches = tfidf_results["top_matching_keywords"]
                if top_matches:
                    for kw in top_matches:
                        st.markdown(f"- **{kw}**")
                else:
                    st.write("No direct TF-IDF keyword overlap found.")

            with kcol2:
                st.markdown("##### 🔴 High-Weight Job Terms Missing in Resume")
                missing_kw = tfidf_results["missing_top_keywords"]
                if missing_kw:
                    for kw in missing_kw:
                        st.markdown(f"- <span style='color:red;'>{kw}</span>", unsafe_allow_html=True)
                else:
                    st.write("No critical missing terms detected.")

        # TAB 2: Skill Gap Analysis
        with tab2:
            st.subheader("Skill Gap & Taxonomy Analysis")
            
            st.markdown(f"**Skill Match Coverage:** `{matched_count} matched` out of `{skill_gap_results['total_jd_skills_count']} skills` required in Job Description.")
            
            st.markdown("---")
            st.markdown("### 🟢 Matched Skills (Found in both Resume & Job Description)")
            matched_skills = skill_gap_results["matched_skills"]
            if matched_skills:
                badges_html = "".join([f'<span class="skill-badge-matched">✓ {skill.upper()}</span>' for skill in matched_skills])
                st.markdown(badges_html, unsafe_allow_html=True)
            else:
                st.info("No matching skills detected from taxonomy.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🔴 Missing Skills (Required in Job Description, Missing in Resume)")
            missing_skills = skill_gap_results["missing_skills"]
            if missing_skills:
                badges_html = "".join([f'<span class="skill-badge-missing">✗ {skill.upper()}</span>' for skill in missing_skills])
                st.markdown(badges_html, unsafe_allow_html=True)
            else:
                st.success("Great job! No major missing skills identified from the taxonomy.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🔵 Additional Candidate Skills (Present in Resume, Not in JD)")
            extra_skills = skill_gap_results["extra_skills"]
            if extra_skills:
                badges_html = "".join([f'<span class="skill-badge-extra">+ {skill.upper()}</span>' for skill in extra_skills])
                st.markdown(badges_html, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 📂 Categorized Resume Skills Breakdown")
            cat_skills = skill_gap_results["resume_skills_by_category"]
            if cat_skills:
                for cat, s_list in cat_skills.items():
                    st.markdown(f"**{cat}:** {', '.join([s.title() for s in s_list])}")

        # TAB 3: ATS Suggestions
        with tab3:
            st.subheader("Personalized Recommendations for Resume Improvement")

            st.markdown("#### 🚨 High Priority Actions")
            if suggestions["high_priority"]:
                for item in suggestions["high_priority"]:
                    st.markdown(f"""
                    <div class="alert-high">
                        <strong>{item['title']}</strong><br>
                        {item['detail']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("No critical issues found.")

            st.markdown("#### 💡 Optimization & Formatting Tips")
            if suggestions["medium_priority"]:
                for item in suggestions["medium_priority"]:
                    st.info(f"**{item['title']}**: {item['detail']}")
            else:
                st.write("No medium priority optimizations needed.")

            st.markdown("#### ✅ Strengths & Positive Signals")
            if suggestions["positive_feedback"]:
                for item in suggestions["positive_feedback"]:
                    st.markdown(f"""
                    <div class="alert-positive">
                        <strong>{item['title']}</strong><br>
                        {item['detail']}
                    </div>
                    """, unsafe_allow_html=True)

        # TAB 4: Extracted Content Inspector
        with tab4:
            st.subheader("Extracted Content & Preprocessing Inspector")
            
            pcol1, pcol2 = st.columns(2)
            with pcol1:
                st.markdown("##### Extracted Resume Text")
                st.text_area("Raw Text extracted via PyMuPDF:", value=resume_text, height=350, disabled=True)
            
            with pcol2:
                st.markdown("##### Cleaned & Tokenized Text (NLP Preprocessed)")
                cleaned_res = preprocess_text(resume_text)
                st.text_area("Preprocessed Resume Tokens:", value=cleaned_res, height=350, disabled=True)

        # Sidebar Download Summary Report
        st.sidebar.markdown("---")
        report_text = f"""==================================================
RESUME LENS AI - ANALYTICS REPORT
==================================================
ATS Match Score: {match_score}%
Matched Skills ({matched_count}): {', '.join(matched_skills)}
Missing Skills ({missing_count}): {', '.join(missing_skills)}
Resume Word Count: {word_count}

RECOMMENDED ACTIONS:
"""
        for item in suggestions["high_priority"]:
            report_text += f"\n- [HIGH PRIORITY] {item['title']}: {item['detail']}"
        for item in suggestions["medium_priority"]:
            report_text += f"\n- [OPTIMIZATION] {item['title']}: {item['detail']}"

        st.sidebar.download_button(
            label="📥 Download Analysis Report",
            data=report_text,
            file_name="resume_match_report.txt",
            mime="text/plain",
            use_container_width=True
        )


if __name__ == "__main__":
    main()
