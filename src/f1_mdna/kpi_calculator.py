import pandas as pd

PL_PATH = "data/Annual_P_L_1_final.csv"
BS_PATH = "data/Balance_Sheet_final.csv"


def compute_kpis(company_name: str) -> dict:
    pl = pd.read_csv(PL_PATH)
    bs = pd.read_csv(BS_PATH)

    pl_row = pl[pl["Name"] == company_name].iloc[0]
    bs_row = bs[bs["Name"] == company_name].iloc[0]

    # -----------------------------
    # YoY Growth (proxy using trailing data)
    # -----------------------------
    prev_12m_sales = pl_row.get("Sales preceding 12months")
    if pd.notna(prev_12m_sales) and prev_12m_sales > 0:
        revenue_yoy = ((pl_row["Sales"] - prev_12m_sales) / prev_12m_sales) * 100
    else:
        revenue_yoy = "NA"

    prev_12m_profit = pl_row.get("Net profit preceding 12months")
    if pd.notna(prev_12m_profit) and prev_12m_profit > 0:
        profit_yoy = ((pl_row["Net profit"] - prev_12m_profit) / prev_12m_profit) * 100
    else:
        profit_yoy = "NA"

    # -----------------------------
    # Liquidity
    # -----------------------------
    if bs_row["Current liabilities"] > 0:
        current_ratio = bs_row["Current assets"] / bs_row["Current liabilities"]
    else:
        current_ratio = "NA"

    # -----------------------------
    # Profitability & Risk
    # -----------------------------
    roa = (
        (pl_row["Net profit"] / bs_row["Total Assets"]) * 100
        if bs_row["Total Assets"] > 0 else "NA"
    )

    roe = (
        (pl_row["Net profit"] / bs_row["Equity capital"]) * 100
        if bs_row["Equity capital"] > 0 else "NA"
    )

    debt_to_equity = (
        bs_row["Debt"] / bs_row["Equity capital"]
        if bs_row["Equity capital"] > 0 else "NA"
    )

    return {
        "company": company_name,

        "revenue_growth_yoy_pct": round(revenue_yoy, 2) if revenue_yoy != "NA" else "NA",
        "profit_growth_yoy_pct": round(profit_yoy, 2) if profit_yoy != "NA" else "NA",

        "operating_margin_pct": round(float(pl_row["OPM"]), 2),
        "roa_pct": round(roa, 2) if roa != "NA" else "NA",
        "roe_pct": round(roe, 2) if roe != "NA" else "NA",
        "debt_to_equity": round(debt_to_equity, 2) if debt_to_equity != "NA" else "NA",
        "current_ratio": round(current_ratio, 2) if current_ratio != "NA" else "NA",

        "total_assets": round(float(bs_row["Total Assets"]), 2),
        "total_debt": round(float(bs_row["Debt"]), 2),
    }
