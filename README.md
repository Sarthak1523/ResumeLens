# 🔍 Resume Lens AI – Resume Job Description Analyzer
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.23%2B-000000?style=for-the-badge)](https://pymupdf.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
An intelligent, lightweight, and privacy-first ATS Resume Analyzer that extracts text from PDF resumes, calculates resume-job alignment scores using TF-IDF and Cosine Similarity, performs skill gap analysis, and provides actionable suggestions.
---
## 🚀 About The Project
**Resume Lens AI** helps job seekers optimize their resumes against specific job descriptions before submitting applications to Applicant Tracking Systems (ATS). 
Unlike cloud-dependent LLM services, Resume Lens AI processes everything **locally and offline** using efficient Natural Language Processing (NLP) techniques, **PyMuPDF**, **Scikit-Learn**, and **Streamlit**.
---
## ✨ Key Features
- **📄 PyMuPDF PDF Text Extraction**: Extracts text instantly from uploaded PDF resumes with exact word counts, page metrics, and layout handling.
- **🧮 TF-IDF & Cosine Similarity Engine**: Converts document text into numerical vector spaces using unigrams and bigrams (`ngram_range=(1,2)`), calculating an accurate ATS match percentage (0% to 100%).
- **🎯 Skill Gap Analysis**: Uses word-boundary regex matching against a taxonomy of 150+ skills across 5 categories to identify **Matched Skills**, **Missing Skills**, and **Extra Skills**.
- **💡 Actionable ATS Recommendations**: Evaluates keyword density, word count, missing high-weight terms, and section headings to generate high-priority and medium-priority optimization tips.
- **🖥️ Streamlit Interactive UI**: Provides score progress meters, visual skill badges, preprocessed text inspectors, and a downloadable text report.
- **⚡ Preloaded Demo Mode**: Includes preloaded sample resume & job description data for fast 1-click demonstration during interviews.
---
## 🛠️ Tech Stack
| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.9+ | Primary application logic |
| **Frontend UI** | Streamlit | Interactive single-page web dashboard |
| **PDF Extraction** | PyMuPDF (`pymupdf`) | Page-by-page text parsing |
| **NLP & ML** | Scikit-Learn | `TfidfVectorizer` & `cosine_similarity` |
| **Data Handling** | NumPy & Pandas | Matrix manipulation & data structuring |
---
## 📂 Project Structure
