from statsmodels.tsa.arima.model import ARIMA

def forecast_next_close(close_series):
    model = ARIMA(close_series, order=(5,1,0))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=1)
    return round(float(forecast.iloc[0]), 2)
