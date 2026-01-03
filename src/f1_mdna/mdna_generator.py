import os
from groq import Groq


def generate_mdna_template(kpis: dict) -> str:
    """
    Deterministic fallback MD&A (no LLM)
    """
    return f"""
Management’s Discussion and Analysis (MD&A)

{kpis['company']} reported stable financial performance during the period.
Revenue growth stood at {kpis['revenue_growth_pct']}%, while profit growth
was recorded at {kpis['profit_growth_pct']}%.

The company maintained an operating margin of {kpis['operating_margin_pct']}%,
reflecting disciplined cost management and operational efficiency.

From a financial position perspective, total assets stood at
₹{kpis['total_assets']} crore, with total debt of ₹{kpis['total_debt']} crore.
Liquidity remains comfortable, supported by a current ratio of
{kpis['current_ratio']}.

Overall, the company demonstrates a balanced capital structure and
stable operating fundamentals.
""".strip()


def generate_mdna_groq(kpis: dict) -> str:
    """
    LLM-powered MD&A generation using Groq
    Falls back to template if API fails
    """
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        prompt = f"""
You are a financial analyst.

Write a professional Management’s Discussion & Analysis (MD&A)
based on the following KPIs:

Company: {kpis['company']}
Revenue Growth (%): {kpis['revenue_growth_pct']}
Profit Growth (%): {kpis['profit_growth_pct']}
Operating Margin (%): {kpis['operating_margin_pct']}
Total Assets: {kpis['total_assets']}
Total Debt: {kpis['total_debt']}
Current Ratio: {kpis['current_ratio']}

Tone: formal, analytical, investor-focused.
Length: one concise paragraph.
"""

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )

        return completion.choices[0].message.content.strip()

    except Exception:
        return generate_mdna_template(kpis)
