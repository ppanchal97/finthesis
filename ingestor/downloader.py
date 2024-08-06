from supported_tickers import supported_tickers
import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()


def get_10k_filing_links(ticker: str):
    url = "https://api.sec-api.io"

    payload = json.dumps({
        "query": f"ticker:{ticker} AND formType:\"10-K\"",
        "from": "0",
        "size": "3",
        "sort": [
            {
                "filedAt": {
                    "order": "desc"
                }
            }
        ]
    })
    headers = {
        'Authorization': os.getenv("SEC-API-KEY"),
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    json_res = json.loads(response.text)
    print(f"retrieved {len(json_res['filings'])} filings for ticker {ticker}")

    filings = []
    for filing in json_res['filings'][:3]:
        filing_data = {
            'ticker': filing['ticker'].lower(),
            'filing_url': filing['linkToHtml'],
            'filing_year': filing['filedAt'][0:4],
            'filing_type': "10K"
        }
        print(f"found filing {filing_data}")
        filings.append(filing_data)

    return filings


def download_company_10k_filings(ticker: str):
    filings = get_10k_filing_links(ticker)
    for filing in filings:
        filing_url = filing['filing_url']
        print(f"Processing {filing_url} for ticker {ticker} ⏳")
        file_name = f"{filing['ticker']}_{filing['filing_year']}_{filing['filing_type']}.txt"
        document_text = construct_10k_document(filing_url=filing_url)
        directory_path = f"{os.getcwd()}/data/{ticker.lower()}"
        os.makedirs(directory_path, exist_ok=True)
        with open(os.path.join(directory_path, file_name), 'w') as file:
            file.write(document_text)
        print("TXT file saved successfully ✅")


def construct_10k_document(filing_url: str):
    sections = ["1", "1A", "1B", "1C", "2", "3", "4", "5", "6", "7", "7A",
                "8", "9", "9A", "9B", "9C", "10", "11", "12", "13", "14", "15"]

    filing_text = ""
    for section in sections:
        url = f"https://api.sec-api.io/extractor?url={filing_url}&item={section}&type=text&token={os.getenv('SEC-API-KEY')}"

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        filing_text += response.text

    return filing_text


if __name__ == "__main__":
    for ticker in supported_tickers:
        download_company_10k_filings(ticker=ticker)
