import streamlit as st
import pandas as pd

from src.f1_mdna.kpi_calculator import compute_kpis
from src.f1_mdna.mdna_generator import generate_mdna_groq
from src.f7_rag.ingest_sec_csv import ingest_sec_filing
from src.f7_rag.rag_qa import answer_question


st.set_page_config(
    page_title="AI Financial Intelligence System",
    layout="centered"
)

st.title("📊 AI-Powered Financial Intelligence System")

tab1, tab2 = st.tabs(
    ["📈 Financial Analysis (F1)", "📄 SEC Filing Q&A (F7)"]
)

# ======================================================
# TAB 1 – F1
# ======================================================
with tab1:
    st.subheader("Automated KPI Analysis & MD&A")

    pl_df = pd.read_csv("data/Annual_P_L_1_final.csv")
    companies = sorted(pl_df["Name"].dropna().unique())

    selected_company = st.selectbox(
        "Select Company (Financial Statements)",
        companies
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
# TAB 2 – F7 (RAG)
# ======================================================
with tab2:
    st.subheader("SEC Filing Question Answering (RAG)")

    sec_df = pd.read_csv("data/sec_filings.csv")
    sec_companies = sorted(sec_df["Company Name"].dropna().unique())

    selected_sec_company = st.selectbox(
        "Select Company (SEC Filing)",
        sec_companies
    )

    if st.button("Load SEC Filing"):
        try:
            ingest_sec_filing(
                csv_path="data/sec_filings.csv",
                company_name=selected_sec_company
            )
            st.success("SEC filing loaded successfully.")
        except ValueError as e:
            st.error(str(e))

    question = st.text_input(
        "Ask a question about the SEC filing"
    )

    if st.button("Ask Question") and question.strip():
        answer = answer_question(question)

        st.subheader("📌 Answer")
        st.markdown(answer)
