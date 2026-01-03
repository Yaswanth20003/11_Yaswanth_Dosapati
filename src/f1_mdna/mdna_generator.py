import os
from groq import Groq


def generate_mdna_template(kpis: dict) -> str:
    return f"""
## Management’s Discussion and Analysis (MD&A)

### Performance Overview
{kpis['company']} reported steady performance during the period.
Revenue growth stood at {kpis['revenue_growth_yoy_pct']}%, while profit
growth was {kpis['profit_growth_yoy_pct']}%.

### Profitability & Efficiency
The operating margin was {kpis['operating_margin_pct']}.
Return on Assets (ROA) stood at {kpis['roa_pct']}%, and Return on Equity (ROE)
was {kpis['roe_pct']}%, reflecting overall capital efficiency.

### Financial Position & Risk
The company maintains a current ratio of {kpis['current_ratio']},
with a debt-to-equity ratio of {kpis['debt_to_equity']}.
""".strip()


def generate_mdna_groq(kpis: dict) -> str:
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        prompt = f"""
You are a financial analyst.

Write a professional MD&A in markdown with sections:
- Performance Overview
- Profitability & Efficiency
- Financial Position & Risk

KPIs:
Company: {kpis['company']}
Revenue Growth YoY (%): {kpis['revenue_growth_yoy_pct']}
Profit Growth YoY (%): {kpis['profit_growth_yoy_pct']}
Operating Margin (%): {kpis['operating_margin_pct']}
ROA (%): {kpis['roa_pct']}
ROE (%): {kpis['roe_pct']}
Debt-to-Equity: {kpis['debt_to_equity']}
Current Ratio: {kpis['current_ratio']}

Tone: formal, investor-focused.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return generate_mdna_template(kpis)
