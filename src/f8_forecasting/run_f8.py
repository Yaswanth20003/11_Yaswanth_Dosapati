from .data_loader import load_stock_data
from .forecaster import forecast_next_close
from .alert_engine import generate_alerts
from .llm_explainer import explain_forecast

def run_forecast(csv_path, stock):
    df = load_stock_data(csv_path, stock)

    last_row = df.iloc[-1]
    forecast_price = forecast_next_close(df["Close"])

    alerts = generate_alerts(last_row, forecast_price)

    explanation = explain_forecast(
        stock=stock,
        last_close=round(last_row["Close"], 2),
        forecast=forecast_price,
        alerts=alerts
    )

    return {
        "stock": stock,
        "last_close": round(last_row["Close"], 2),
        "forecast_price": forecast_price,
        "alerts": alerts,
        "explanation": explanation
    }
