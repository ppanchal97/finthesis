import requests
import os
import json

from typing import Tuple, Dict

#######################################################################################################################
# 1. Functions have an agnostic arguments dict passed in to prevent complex if/else logic at the service layer
# 2. OpenAPI tool specifications, however, have granular argument definitions to let LLM know the correct signature
#######################################################################################################################


def get_sec_filing_links_for_year(ticker: str, document_type: str, year: int) -> Tuple[int, Dict]:
    url = "https://api.sec-api.io"
    payload = json.dumps({
        "query": f"ticker:{ticker} AND formType:\"{document_type}\" AND filedAt:[{year}-01-01 TO {year}-12-31]"
    })
    headers = {
        'Authorization': f"{os.environ.get('SEC_API_KEY')}",
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    filings = data.get("filings")
    filing_count = data['total']['value']
    return filing_count, filings


def get_10k_filing_section(function_args: dict):
    # 1. get 10K document url based on ticker and year params
    ticker = function_args.get('ticker')
    year = function_args.get('year')
    section = function_args.get('section')
    print(f"Executing get_10k_filing_section for ticker: {ticker}, year: {year}, section: {section}")
    document_type = "10-K"
    filing_count, filings = get_sec_filing_links_for_year(
        ticker, document_type, year)
    if filing_count > 0:
        # filter filings
        annual_filing = filings[0]
        document_link = annual_filing.get('linkToHtml')
        # 2. get section for document
        url = f"https://api.sec-api.io/extractor?url={document_link}&item={section}&type=text&token={os.environ.get('SEC_API_KEY')}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        section_text = response.text
        return section_text
    else:
        print(f"10K filing section not found for for ticker: {ticker}, year: {year}, section: {section}")
        return ""


def get_10q_filing_section(function_args: dict):
    # 1. get 10Q document url based on ticker and year params
    ticker = function_args.get('ticker')
    year = function_args.get('year')
    section = function_args.get('section')
    print(f"Executing get_10q_filing_section for ticker: {ticker}, year: {year}, section: {section}")
    document_type = "10-Q"
    filing_count, filings = get_sec_filing_links_for_year(
        ticker, document_type, year)
    if filing_count > 0:
        # filter filings
        annual_filing = filings[0]
        document_link = annual_filing.get('linkToHtml')
    
        # 2. get section for document
        url = f"https://api.sec-api.io/extractor?url={document_link}&item={section}&type=text&token={os.environ.get('SEC_API_KEY')}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        section_text = response.text
        return section_text
    else:
        print(f"10Q filing section not found for for ticker: {ticker}, year: {year}, section: {section}")
        return ""

def get_8k_filing_section(function_args: dict):
    # 1. get 10Q document url based on ticker and year params
    ticker = function_args.get('ticker')
    year = function_args.get('year')
    section = function_args.get('section')
    print(f"Executing get_8k_filing_section for ticker: {ticker}, year: {year}, section: {section}")
    document_type = "8-K"
    filing_count, filings = get_sec_filing_links_for_year(ticker, document_type, year)
    if filing_count > 0:
        # filter filings
        annual_filing = filings[0]
        document_link = annual_filing.get('linkToHtml')
    
        # 2. get section for document
        url = f"https://api.sec-api.io/extractor?url={document_link}&item={section}&type=text&token={os.environ.get('SEC_API_KEY')}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        section_text = response.text
        return section_text
    else:
        print(f"8K filing section not found for for ticker: {ticker}, year: {year}, section: {section}")
        return ""

def get_annual_income_statement_for_company(function_args: dict):
    ticker = function_args.get('ticker')
    year = function_args.get('year')
    print(f"Executing get_annual_income_statement_for_company for ticker {ticker} and year {year}")
    url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={ticker}&apikey={os.environ.get('ALPHA_VANTAGE_API_KEY')}"
    r = requests.get(url)
    data = r.json()
    extracted_data = []
    # extract annual reports
    for report in data.get('annualReports'):
        if str(year) in report.get('fiscalDateEnding'):
            extracted_data.append({"annual_report": report})

    # extract quarterly reports
    for report in data.get('quarterlyReports'):
        if str(year) in report.get('fiscalDateEnding'):
            extracted_data.append({"quarterly_report": report})

    return extracted_data

def get_annual_balance_sheet_for_company(function_args: dict):
    ticker = function_args.get('ticker')
    year = function_args.get('year')
    print(f"Executing get_annual_balance_sheet_for_company for ticker {ticker} and year {year}")
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={ticker}&apikey={os.environ.get('ALPHA_VANTAGE_API_KEY')}"
    r = requests.get(url)
    data = r.json()
    extracted_data = []
    # extract annual reports
    for report in data.get('annualReports'):
        if str(year) in report.get('fiscalDateEnding'):
            extracted_data.append({"annual_report": report})

    # extract quarterly reports
    for report in data.get('quarterlyReports'):
        if str(year) in report.get('fiscalDateEnding'):
            extracted_data.append({"quarterly_report": report})

    return extracted_data


def get_annual_cash_flow_for_company(function_args: dict):
    ticker = function_args.get('ticker')
    year = function_args.get('year')
    print(f"Executing get_annual_cash_flow_for_company for ticker {ticker} and year {year}")
    url = f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={ticker}&apikey={os.environ.get('ALPHA_VANTAGE_API_KEY')}"
    r = requests.get(url)
    data = r.json()
    extracted_data = []
    # extract annual reports
    for report in data.get('annualReports'):
        if str(year) in report.get('fiscalDateEnding'):
            extracted_data.append({"annual_report": report})

    # extract quarterly reports
    for report in data.get('quarterlyReports'):
        if str(year) in report.get('fiscalDateEnding'):
            extracted_data.append({"quarterly_report": report})

    return extracted_data

def get_annual_earnings_numbers_for_company(function_args: dict):
    ticker = function_args.get('ticker')
    year = function_args.get('year')
    print(f"Executing get_annual_earnings_numbers_for_company for ticker {ticker} and year {year}")
    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={ticker}&apikey={os.environ.get('ALPHA_VANTAGE_API_KEY')}"
    r = requests.get(url)
    data = r.json()
    extracted_data = []
    # extract annual earnings
    for report in data.get('annualEarnings'):
        if str(year) in report.get('fiscalDateEnding'):
            extracted_data.append({"annual_earnings": report})

    # extract quarterly earnings
    for report in data.get('quarterlyEarnings'):
        if str(year) in report.get('fiscalDateEnding'):
            extracted_data.append({"quarterly_earnings": report})

    return extracted_data

def get_annual_earnings_transcripts(function_args: dict):
    ticker = function_args.get('ticker')
    year = function_args.get('year')
    print(
        f"Executing get_annual_earnings_transcripts for ticker {ticker} for year {year}")
    url = f"https://financialmodelingprep.com/api/v4/batch_earning_call_transcript/{ticker}?year={year}&apikey={os.environ.get('FMP_API_KEY')}"
    r = requests.get(url)
    data = r.json()
    return data

def filter_stock_data(stock_quotes, start_date, end_date):
    filtered_data = []

    for date, data in stock_quotes.items():
        if start_date <= date <= end_date:
            stock_data = {'date': date, 'close': data['4. close']}
            filtered_data.append(stock_data)

    return filtered_data

def get_end_of_day_stock_prices_for_ticker_given_date_range(function_args: dict):
    ticker = function_args.get('ticker')
    start_date = function_args.get('start_date')
    end_date = function_args.get('end_date')
    print(f"Executing get_end_of_day_stock_prices_for_ticker_given_date_range for ticker {ticker} from start date {start_date} to end date {end_date}")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={ticker}&outputsize=full&apikey={os.environ.get('ALPHA_VANTAGE_API_KEY')}"
    r = requests.get(url)
    data = r.json()
    stock_quotes = data.get('Time Series (Daily)')
    filtered_data = filter_stock_data(stock_quotes, start_date, end_date)

    return filtered_data

def get_end_of_week_stock_prices_for_ticker_given_date_range(function_args: dict):
    ticker = function_args.get('ticker')
    start_date = function_args.get('start_date')
    end_date = function_args.get('end_date')
    print(f"Executing get_end_of_week_stock_prices_for_ticker_given_date_range for ticker {ticker} from start date {start_date} to end date {end_date}")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol={ticker}&outputsize=full&apikey={os.environ.get('ALPHA_VANTAGE_API_KEY')}"
    r = requests.get(url)
    data = r.json()
    stock_quotes = data.get('Time Series (Daily)')
    filtered_data = filter_stock_data(stock_quotes, start_date, end_date)

    return filtered_data

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_10k_filing_section",
            "description": "Get a section from the annual 10K filings for a particular company given it's stock ticker, year and document section",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol for which the annual 10K filings are to be retrieved"
                    },
                    "year": {
                        "type": "integer",
                        "description": "The target year for which the annual 10K filings are to be retrieved"
                    },
                    "section": {
                        "type": "string",
                        "description": f"""
                        The section of the 10K filing that is to be retrieved. Interpret the section description and return only the section number from the list given:
                        1 - Business
                        1A - Risk Factors
                        1B - Unresolved Staff Comments
                        1C - Cybersecurity
                        2 - Properties
                        3 - Legal Proceedings
                        4 - Mine Safety Disclosures
                        5 - Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities
                        6 - Selected Financial Data (prior to February 2021)
                        7 - Management’s Discussion and Analysis of Financial Condition and Results of Operations
                        7A - Quantitative and Qualitative Disclosures about Market Risk
                        8 - Financial Statements and Supplementary Data
                        9 - Changes in and Disagreements with Accountants on Accounting and Financial Disclosure
                        9A - Controls and Procedures
                        9B - Other Information
                        10 - Directors, Executive Officers and Corporate Governance
                        11 - Executive Compensation
                        12 - Security Ownership of Certain Beneficial Owners and Management and Related Stockholder Matters
                        13 - Certain Relationships and Related Transactions, and Director Independence
                        14 - Principal Accountant Fees and Services
                        15 - Exhibits and Financial Statement Schedules
                        """
                    }
                },
                "required": ["ticker", "year", "section"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_10q_filing_section",
            "description": "Get a section from the quarterly 10Q filings for a particular company given it's stock ticker, year and document section",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol for which the quarterly 10Q filings are to be retrieved"
                    },
                    "year": {
                        "type": "integer",
                        "description": "The target year for which the quarterly 10Q filings are to be retrieved"
                    },
                    "section": {
                        "type": "string",
                        "description": f"""
                        The section of the 10Q filing that is to be retrieved. Interpret the section description and return only the section title from the list given:
                        part1item1: Financial Statements
                        part1item2: Management’s Discussion and Analysis of Financial Condition and Results of Operations
                        part1item3: Quantitative and Qualitative Disclosures About Market Risk
                        part1item4: Controls and Procedures
                        part2item1: Legal Proceedings
                        part2item1a: Risk Factors
                        part2item2: Unregistered Sales of Equity Securities and Use of Proceeds
                        part2item3: Defaults Upon Senior Securities
                        part2item4: Mine Safety Disclosures
                        part2item5: Other Information
                        part2item6: Exhibits
                        """
                    }
                },
                "required": ["ticker", "year", "section"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_8k_filing_section",
            "description": "Get a section from an 8K filing for a particular company given it's stock ticker, year and document section",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol for which the 8K filings are to be retrieved"
                    },
                    "year": {
                        "type": "integer",
                        "description": "The target year for which the 8K filings are to be retrieved"
                    },
                    "section": {
                        "type": "string",
                        "description": f"""
                        1-1: Entry into a Material Definitive Agreement
                        1-2: Termination of a Material Definitive Agreement
                        1-3: Bankruptcy or Receivership
                        1-4: Mine Safety - Reporting of Shutdowns and Patterns of Violations
                        1-5: Material Cybersecurity Incidents (introduced in 2023)
                        2-1: Completion of Acquisition or Disposition of Assets
                        2-2: Results of Operations and Financial Condition
                        2-3: Creation of a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement of a Registrant
                        2-4: Triggering Events That Accelerate or Increase a Direct Financial Obligation or an Obligation under an Off-Balance Sheet Arrangement
                        2-5: Cost Associated with Exit or Disposal Activities
                        2-6: Material Impairments
                        3-1: Notice of Delisting or Failure to Satisfy a Continued Listing Rule or Standard; Transfer of Listing
                        3-2: Unregistered Sales of Equity Securities
                        3-3: Material Modifications to Rights of Security Holders
                        4-1: Changes in Registrant's Certifying Accountant
                        4-2: Non-Reliance on Previously Issued Financial Statements or a Related Audit Report or Completed Interim Review
                        5-1: Changes in Control of Registrant
                        5-2: Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers: Compensatory Arrangements of Certain Officers
                        5-3: Amendments to Articles of Incorporation or Bylaws; Change in Fiscal Year
                        5-4: Temporary Suspension of Trading Under Registrant's Employee Benefit Plans
                        5-5: Amendments to the Registrant's Code of Ethics, or Waiver of a Provision of the Code of Ethics
                        5-6: Change in Shell Company Status
                        5-7: Submission of Matters to a Vote of Security Holders
                        5-8: Shareholder Nominations Pursuant to Exchange Act Rule 14a-11
                        6-1: ABS Informational and Computational Material
                        6-2: Change of Servicer or Trustee
                        6-3: Change in Credit Enhancement or Other External Support
                        6-4: Failure to Make a Required Distribution
                        6-5: Securities Act Updating Disclosure
                        6-6: Static Pool
                        6-10: Alternative Filings of Asset-Backed Issuers
                        7-1: Regulation FD Disclosure
                        8-1: Other Events
                        9-1: Financial Statements and Exhibits
                        """
                    }
                },
                "required": ["ticker", "year", "section"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_annual_income_statement_for_company",
            "description": "Get comprehensive annual and quarterly income statement data for a company given it's stock ticker and a year",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol for which income statement data is to be retrieved"
                    },
                    "year": {
                        "type": "integer",
                        "description": "The target year for which the annual income statement is to be retrieved"
                    },
                },
                "required": ["ticker", "year"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_annual_balance_sheet_for_company",
            "description": "Get comprehensive annual and quarterly balance sheet data for a company given it's stock ticker and a year",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol for which balance sheet data is to be retrieved"
                    },
                    "year": {
                        "type": "integer",
                        "description": "The target year for which the annual balance sheet is to be retrieved"
                    },
                },
                "required": ["ticker", "year"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_annual_cash_flow_for_company",
            "description": "Get comprehensive annual and quarterly cash flow data for a company given it's stock ticker and a year",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol for which cash flow statement data is to be retrieved"
                    },
                    "year": {
                        "type": "integer",
                        "description": "The target year for which the cash flow statement is to be retrieved"
                    },
                },
                "required": ["ticker", "year"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_annual_earnings_numbers_for_company",
            "description": "Get comprehensive annual and quarterly earnings data for a company given it's stock ticker and a year",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol for which earnings data is to be retrieved"
                    },
                    "year": {
                        "type": "integer",
                        "description": "The target year for which the earnings data is to be retrieved"
                    },
                },
                "required": ["ticker", "year"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_annual_earnings_transcripts",
            "description": "Get earnings transcripts for a full financial year for a company given its stock ticker and target year",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol for which earnings transcripts are to be retrieved"
                    },
                    "year": {
                        "type": "integer",
                        "description": "The target year for which earnings transcripts are desired"
                    }
                },
                "required": ["ticker", "year"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_end_of_day_stock_prices_for_ticker_given_date_range",
            "description": "Get end of day stock price movements for a company in a range of dates given its stock ticker, a start_date and an end_date",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol for which detailed price movements since IPO are to be retrieved"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "The starting date in the format yyyy-mm-dd from which the stock prices are to be retrieved for example 2024-06-27"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "The end date in the format yyyy-mm-dd from which the stock prices are to be retrieved for example 2024-07-02"
                    }
                },
                "required": ["ticker", "start_date", "end_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_end_of_week_stock_prices_for_ticker_given_date_range",
            "description": "Get end of week stock price movements for a company in a range of dates given its stock ticker, a start_date and an end_date",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The stock ticker symbol for which detailed price movements since IPO are to be retrieved"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "The starting date in the format yyyy-mm-dd from which the stock prices are to be retrieved for example 2024-06-27"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "The end date in the format yyyy-mm-dd from which the stock prices are to be retrieved for example 2024-07-02"
                    }
                },
                "required": ["ticker", "start_date", "end_date"]
            }
        }
    },
]

available_functions_dict = {
    "get_10k_filing_section": get_10k_filing_section,
    "get_10q_filing_section": get_10q_filing_section,
    "get_8k_filing_section": get_8k_filing_section,
    "get_annual_income_statement_for_company": get_annual_income_statement_for_company,
    "get_annual_balance_sheet_for_company": get_annual_balance_sheet_for_company,
    "get_annual_cash_flow_for_company": get_annual_cash_flow_for_company,
    "get_annual_earnings_numbers_for_company": get_annual_earnings_numbers_for_company,
    "get_annual_earnings_transcripts": get_annual_earnings_transcripts,
    "get_end_of_day_stock_prices_for_ticker_given_date_range": get_end_of_day_stock_prices_for_ticker_given_date_range,
    "get_end_of_week_stock_prices_for_ticker_given_date_range": get_end_of_week_stock_prices_for_ticker_given_date_range
}
