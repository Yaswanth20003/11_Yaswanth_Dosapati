def generate_alerts(row, forecast_price):
    alerts = []

    last_close = row["Close"]
    volume = row["Volume"]
    rsi = row["RSI"]
    macd = row["MACD"]

    if forecast_price > last_close and volume > row["Volume"].mean():
        alerts.append("Bullish Momentum")

    if rsi > 70:
        alerts.append("Overbought Condition")

    if rsi < 30:
        alerts.append("Oversold Condition")

    if macd < 0:
        alerts.append("Bearish Signal")

    if abs(forecast_price - last_close) / last_close > 0.03:
        alerts.append("High Volatility")

    return alerts
