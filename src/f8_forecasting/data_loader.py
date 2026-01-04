import pandas as pd

def load_stock_data(csv_path, stock):
    df = pd.read_csv(csv_path)

    df = df[df["Stock"] == stock].copy()

    # Robust date parsing (handles mixed formats)
    df["Date"] = pd.to_datetime(
        df["Date"],
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )

    # Drop any rows where date could not be parsed
    df = df.dropna(subset=["Date"])

    df.sort_values("Date", inplace=True)

    return df
