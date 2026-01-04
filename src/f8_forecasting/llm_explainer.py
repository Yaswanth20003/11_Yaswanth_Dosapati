import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def explain_forecast(stock, last_close, forecast, alerts):
    prompt = f"""
You are a financial analyst.

Stock: {stock}
Last Close: {last_close}
Forecasted Next Close: {forecast}

Alerts detected:
{", ".join(alerts) if alerts else "No major alerts"}

Explain the forecast and alerts in simple, professional language.
Do not give investment advice.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
