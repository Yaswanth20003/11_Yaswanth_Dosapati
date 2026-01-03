import pandas as pd
from mdna_generator import generate_mdna_groq

PL_PATH = "data/Annual_P_L_1_final.csv"
BS_PATH = "data/Balance_Sheet_final.csv"


def load_data():
    """
    Load Profit & Loss and Balance Sheet data
    """
    pl = pd.read_csv(PL_PATH)
    bs = pd.read_csv(BS_PATH)
    return pl, bs


def compute_kpis(company_name: str) -> dict:
    """
    Compute key financial KPIs for a given company
    """
    pl, bs = load_data()

    pl_row = pl[pl["Name"] == company_name].iloc[0]
    bs_row = bs[bs["Name"] == company_name].iloc[0]

    revenue_growth = (
        (pl_row["Sales"] - pl_row["Sales last year"])
        / pl_row["Sales last year"]
        if pl_row["Sales last year"] != 0 else 0
    ) * 100

    profit_growth = (
        (pl_row["Net profit"] - pl_row["Net Profit last year"])
        / pl_row["Net Profit last year"]
        if pl_row["Net Profit last year"] != 0 else 0
    ) * 100

    current_ratio = (
        bs_row["Current assets"] / bs_row["Current liabilities"]
        if bs_row["Current liabilities"] != 0 else None
    )

    kpis = {
        "company": company_name,
        "revenue_growth_pct": round(float(revenue_growth), 2),
        "profit_growth_pct": round(float(profit_growth), 2),
        "operating_margin_pct": round(float(pl_row["OPM"]), 2),
        "total_assets": round(float(bs_row["Total Assets"]), 2),
        "total_debt": round(float(bs_row["Debt"]), 2),
        "current_ratio": round(float(current_ratio), 2) if current_ratio else None,
        "market_cap": round(float(pl_row["Market Capitalization"]), 2),
    }

    return kpis


if __name__ == "__main__":
    company = "20 Microns"  # change company name here
    kpis = compute_kpis(company)

    print("\n=== KEY PERFORMANCE INDICATORS (KPIs) ===\n")
    for key, value in kpis.items():
        print(f"{key}: {value}")

    print("\n=== AI-GENERATED MD&A ===\n")
    print(generate_mdna_groq(kpis))
