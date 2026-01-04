# import streamlit as st
# import pandas as pd

# from src.f1_mdna.kpi_calculator import compute_kpis
# from src.f1_mdna.mdna_generator import generate_mdna_groq
# from src.f7_rag.ingest_sec_csv import ingest_sec_filing
# from src.f7_rag.rag_qa import answer_question


# st.set_page_config(
#     page_title="AI Financial Intelligence System",
#     layout="centered"
# )

# st.title("📊 AI-Powered Financial Intelligence System")

# tab1, tab2 = st.tabs(
#     ["📈 Financial Analysis (F1)", "📄 SEC Filing Q&A (F7)"]
# )

# # ======================================================
# # TAB 1 – F1
# # ======================================================
# with tab1:
#     st.subheader("Automated KPI Analysis & MD&A")

#     pl_df = pd.read_csv("data/Annual_P_L_1_final.csv")
#     companies = sorted(pl_df["Name"].dropna().unique())

#     selected_company = st.selectbox(
#         "Select Company (Financial Statements)",
#         companies
#     )

#     if st.button("Generate Financial Analysis"):
#         kpis = compute_kpis(selected_company)

#         col1, col2 = st.columns(2)

#         with col1:
#             st.metric("Revenue Growth YoY (%)", kpis["revenue_growth_yoy_pct"])
#             st.metric("Operating Margin (%)", kpis["operating_margin_pct"])
#             st.metric("ROA (%)", kpis["roa_pct"])

#         with col2:
#             st.metric("Profit Growth YoY (%)", kpis["profit_growth_yoy_pct"])
#             st.metric("ROE (%)", kpis["roe_pct"])
#             st.metric("Debt-to-Equity", kpis["debt_to_equity"])

#         st.metric("Current Ratio", kpis["current_ratio"])

#         st.subheader("📝 AI-Generated MD&A")
#         st.markdown(generate_mdna_groq(kpis))


# # ======================================================
# # TAB 2 – F7 (RAG)
# # ======================================================
# with tab2:
#     st.subheader("SEC Filing Question Answering (RAG)")

#     sec_df = pd.read_csv("data/sec_filings.csv")
#     sec_companies = sorted(sec_df["Company Name"].dropna().unique())

#     selected_sec_company = st.selectbox(
#         "Select Company (SEC Filing)",
#         sec_companies
#     )

#     if st.button("Load SEC Filing"):
#         try:
#             ingest_sec_filing(
#                 csv_path="data/sec_filings.csv",
#                 company_name=selected_sec_company
#             )
#             st.success("SEC filing loaded successfully.")
#         except ValueError as e:
#             st.error(str(e))

#     question = st.text_input(
#         "Ask a question about the SEC filing"
#     )

#     if st.button("Ask Question") and question.strip():
#         answer = answer_question(question)

#         st.subheader("📌 Answer")
#         st.markdown(answer)



import streamlit as st
import pandas as pd

from src.f1_mdna.kpi_calculator import compute_kpis
from src.f1_mdna.mdna_generator import generate_mdna_groq
from src.f7_rag.ingest_sec_csv import ingest_sec_filing
from src.f7_rag.rag_qa import answer_question

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="AI Financial Intelligence System",
    layout="centered"
)

st.title("📊 AI-Powered Financial Intelligence System")

# -------------------------------
# Load data ONCE (global)
# -------------------------------
pl_df = pd.read_csv("data/Annual_P_L_1_final.csv")
financial_companies = sorted(pl_df["Name"].dropna().unique())

sec_df = pd.read_csv("data/sec_filings.csv")

# -------------------------------
# Tabs (NOW 3 TABS)
# -------------------------------
tab1, tab2, tab3 = st.tabs(
    [
        "📈 Financial Analysis",
        "📄 SEC Filing Q&A",
        "🧠 All Integrated Intelligence"
    ]
)

# ======================================================
# TAB 1 – F1 (UNCHANGED)
# ======================================================
with tab1:
    st.subheader("Automated KPI Analysis & MD&A")

    selected_company = st.selectbox(
        "Select Company (Financial Statements)",
        financial_companies
    )

    if st.button("Generate Financial Analysis"):
        kpis = compute_kpis(selected_company)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Revenue Growth YoY (%)", kpis["revenue_growth_yoy_pct"])
            st.metric("Operating Margin (%)", kpis["operating_margin_pct"])
            st.metric("ROA (%)", kpis["roa_pct"])

        with col2:
            st.metric("Profit Growth YoY (%)", kpis["profit_growth_yoy_pct"])
            st.metric("ROE (%)", kpis["roe_pct"])
            st.metric("Debt-to-Equity", kpis["debt_to_equity"])

        st.metric("Current Ratio", kpis["current_ratio"])

        st.subheader("📝 AI-Generated MD&A")
        st.markdown(generate_mdna_groq(kpis))

# ======================================================
# TAB 2 – F7 (UNCHANGED)
# ======================================================
with tab2:
    st.subheader("SEC Filing Question Answering (RAG)")

    sec_companies = sorted(sec_df["Company Name"].dropna().unique())

    selected_sec_company = st.selectbox(
        "Select Company (SEC Filing)",
        sec_companies
    )

    if st.button("Load SEC Filing"):
        try:
            ingest_sec_filing(
                csv_path="data/sec_filings.csv",
                company_keyword=selected_sec_company
            )
            st.success("SEC filing loaded successfully.")
        except ValueError as e:
            st.error(str(e))

    question = st.text_input("Ask a question about the SEC filing")

    if st.button("Ask Question") and question.strip():
        answer = answer_question(question)
        st.subheader("📌 Answer")
        st.markdown(answer)

# ======================================================
# TAB 3 – ALL INTEGRATED INTELLIGENCE (NEW)
# ======================================================
with tab3:
    st.header("🧠 All Integrated Financial Intelligence")

    # -------------------------------
    # Company selection (F1 source)
    # -------------------------------
    selected_company = st.selectbox(
        "Select Company",
        financial_companies,
        key="integrated_company"
    )

    # -------------------------------
    # F1 – KPIs
    # -------------------------------
    kpis = compute_kpis(selected_company)

    st.subheader("📊 Key Performance Indicators")

    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue Growth YoY (%)", kpis["revenue_growth_yoy_pct"])
    col2.metric("Profit Growth YoY (%)", kpis["profit_growth_yoy_pct"])
    col3.metric("Operating Margin (%)", kpis["operating_margin_pct"])

    col4, col5, col6 = st.columns(3)
    col4.metric("ROA (%)", kpis["roa_pct"])
    col5.metric("ROE (%)", kpis["roe_pct"])
    col6.metric("Current Ratio", kpis["current_ratio"])

    # -------------------------------
    # MD&A
    # -------------------------------
    st.subheader("📝 Management Discussion & Analysis")
    st.markdown(generate_mdna_groq(kpis))

    # -------------------------------
    # SEC INTEGRATION
    # -------------------------------
    st.subheader("📄 Regulatory Intelligence (SEC Filing Q&A)")

    sec_match = sec_df[
        sec_df["Company Name"].str.contains(
            selected_company, case=False, na=False
        )
    ]

    # Case 1: SEC filing exists
    if not sec_match.empty:
        st.success("SEC filing found for this company.")

        ingest_sec_filing(
            csv_path="data/sec_filings.csv",
            company_keyword=selected_company
        )

        question = st.text_input(
            "Ask a question about the SEC filing",
            key="integrated_sec_q"
        )

        if question:
            with st.spinner("Analyzing SEC filing..."):
                answer = answer_question(question)
            st.markdown("### 📌 Answer")
            st.markdown(answer)

    # Case 2: SEC filing NOT exists
    else:
        st.warning(
            "SEC filing not available for this company. "
            "Please upload an SEC filing (TXT or HTML) to enable regulatory Q&A."
        )

        uploaded_file = st.file_uploader(
            "Upload SEC filing",
            type=["txt", "html"],
            key="integrated_upload"
        )

        if uploaded_file:
            with open("data/sec_filing.txt", "wb") as f:
                f.write(uploaded_file.read())

            st.success("SEC filing uploaded successfully.")

            question = st.text_input(
                "Ask a question about the uploaded filing",
                key="integrated_upload_q"
            )

            if question:
                with st.spinner("Analyzing uploaded SEC filing..."):
                    answer = answer_question(question)
                st.markdown("### 📌 Answer")
                st.markdown(answer)
