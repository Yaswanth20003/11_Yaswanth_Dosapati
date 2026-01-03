import pandas as pd
import requests
from bs4 import BeautifulSoup


def ingest_sec_filing(
    csv_path="data/sec_filings.csv",
    company_name=None,
):
    df = pd.read_csv(csv_path)

    # Keep only real filings (ignore exhibits)
    df = df[
        df["Form Type"].isin(["10-K", "8-K"])
        & (~df["Description"].str.contains("EX-", na=False))
    ]

    # Exact match instead of contains
    company_rows = df[df["Company Name"] == company_name]

    if company_rows.empty:
        raise ValueError(
            f"No valid 10-K or 8-K filing found for company: {company_name}"
        )

    # Take the most recent filing
    row = company_rows.sort_values("Filed At", ascending=False).iloc[0]

    filing_url = row["Filing URL"]
    print("Fetching:", filing_url)

    response = requests.get(
        filing_url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    with open("data/sec_filing.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("Saved SEC filing to data/sec_filing.txt")
