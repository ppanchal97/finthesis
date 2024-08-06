from utils.gics_classifications import gics_classifications_dict
from utils.financial_metrics import supported_financial_metrics
from utils.db_schema import db_schema

from datetime import datetime

def generate_data_fetching_agent_system_prompt():
    now = datetime.now()
    return f"""
    Select functions that can be used to help answer the user's queries. 
    Don't make assumptions about what values to plug into functions. 
    Be eager to use the functions, even if you have partial information.

    The current date is {now.strftime('%b')} {now.day} {now.year}.
    """

def generate_sanitize_filing_into_markdown_prompt(section_text):
    return f"""
    You have been given markdown text containing a section from a 10K document below:

    markdown text:
    ...
    {section_text}
    ...

    Your task is to:
    1. Appropriately add correct headings e.g., #, ## and ### for titles, sub-titles and paragraphs.
    2. Correct the formatting of any tables that may be irregularly formatted.
    3. Do not make up any numbers.

    Corrected markdown output:    
    """


def generate_execution_steps_prompt(query, stocks_list, required_data_parameters, relevant_financial_performance_figures, relevant_financial_ratios, query_metadata):
    return f"""
    You are an expert financial analyst.

    You are given a financial query.

    Your task is to generate a comprehensive list of steps that a financial analyst would take to completely solve the query.

    You have identified that the query targets the following companies:
    ...
    {stocks_list}
    ...

    You have identified the following data parameters that are important to answer the query:
    ...
    {required_data_parameters}
    ...

    You have identified the following financial performance figures that are important to answer the query:
    ...
    {relevant_financial_performance_figures}
    ...

    You have identified the following financial ratios that are important to answer the query:
    ...
    {relevant_financial_ratios}
    ...

    Here is some additional metadata that you have identified to help you solve the query:
    ...
    {query_metadata}
    ...

    You have access to the following data sources in your own database:
    1. 10K filings
    2. 10Q filings
    3. 8K filings
    4. Earnings Transcripts

    You can search the news for:
    1. Noteworthy events

    You can search APIs for:
    1. Comprehensive Annual Income Statements
    2. Comprehensive Annual Balance Sheets
    3. Comprehensive Annual Cash Flow Statements
    4. Comprehensive Earnings Numbers
    5. End of Day Stock Market Prices for the past 3 years
    6. End of Week Stock Market Prices for the past 3 years
    7. Comprehensive financial information: "marketcapitalization","ebitda","peratio","pegratio","bookvalue","dividendpershare","dividendyield","eps","revenuepersharettm","profitmargin","operatingmarginttm","returnonassetsttm","returnonequityttm","revenuettm","grossprofitttm","dilutedepsttm","quarterlyearningsgrowthyoy","quarterlyrevenuegrowthyoy","trailingpe","forwardpe","pricetosalesratiottm","pricetobookratio","evtorevenue","evtoebitda","beta","52weekhigh","52weeklow","50daymovingaverage","200daymovingaverage","sharesoutstanding","dividenddate","exdividenddate","industrygroup","subindustry"

    Each step dictionary must have the following parameters:
    1. "step_number": an integer denoting the number of the step.
    2. "step_type": the function of the step. Either 'data_retrieval' - a step where you need to lookup data from the data sources above or 'analysis' - a step where you calculate / analyse / perform tasks on data.
    3. "instruction": the actual procedure of the step
    4. "target": an array list of tickers for which the step applies to. Only to be populated with tickers if the step is 'data_retrieval', else set to null. Important when a data_retrieval step needs to be carried out for multiple companies / peer-companies etc.

    Here's an example to help you:
    query:
    ...
    'Compare Invesco's margin compression over the past 2 years with other companies in the capital markets industry?
    ...

    example response:
    ...
    'steps_required_to_complete_query': [{{ "step_number": 1, "step_type": "data_retrieval", "instruction": "Retrieve Data: Use the API to get comprehensive income statements for Invesco (IVZ) for the past 2 years.", "target": ["IVZ"] }}, {{ "step_number": 2, "step_type": "data_retrieval", "instruction": "Retrieve Data: Use the API to get comprehensive income statements for the following peer companies for the past 2 years", "target": ["MS", "BLK", "ICE", "CME", "MSCI", "BK", "NDAQ", "RJF", "TROW", "FDS"] }}, {{ "step_number": 3, "step_type": "analysis", "instruction": "Calculate Financial Ratios: Calculate the gross margin ratio, operating margin ratio, net profit margin, and EBITDA margin for Invesco (IVZ) for the past 2 years using the retrieved income statements.", "target": null }}, {{ "step_number": 4, "step_type": "analysis", "instruction": "Calculate Financial Ratios: Calculate the gross margin ratio, operating margin ratio, net profit margin, and EBITDA margin for the following peer companies in the capital markets industry for the past 2 years using the retrieved income statements.", "target":  null }}, {{ "step_number": 5, "step_type": "analysis", "instruction": "Analyze Trends: Compare the calculated financial ratios for Invesco (IVZ) over the past 2 years to identify any trends in margin compression.", "target": null }}, {{ "step_number": 6, "step_type": "analysis", "instruction": "Analyze Trends: Compare the calculated financial ratios for the following peer companies over the past 2 years to identify any trends in margin compression.", "target": null }}, {{ "step_number": 7, "step_type": "analysis", "instruction": "Perform Comparative Analysis: Compare Invesco's margin compression trends with those of its peer companies to determine how Invesco's performance stacks up against the industry.", "target": null }}, {{ "step_number": 8, "step_type": "data_retrieval", "instruction": "Retrieve Management Discussion and Analysis: Use the 10K filings for Invesco (IVZ) for the past 2 years to gather insights from the Management\u2019s Discussion and Analysis of Financial Condition and Results of Operations section regarding factors affecting margins.", "target": ["IVZ"] }}, {{ "step_number": 9, "step_type": "data_retrieval", "instruction": "Retrieve Management Discussion and Analysis: Use the 10K filings for the following peer companies in the capital markets industry for the past 2 years to gather insights from the Management\u2019s Discussion and Analysis of Financial Condition and Results of Operations section regarding factors affecting margins.", "target": ["MS", "BLK", "ICE", "CME", "MSCI", "BK", "NDAQ", "RJF", "TROW", "FDS"] }}, {{ "step_number": 10, "step_type": "analysis", "instruction": "Perform Sentiment Analysis: Analyze the sentiment of the Management\u2019s Discussion and Analysis of Financial Condition and Results of Operations sections for Invesco (IVZ) and its peer companies to understand the management's outlook on margin compression.", "target": null }}, {{ "step_number": 11, "step_type": "analysis", "instruction": "Compile Report: Summarize the findings from the financial ratio analysis, trend analysis, comparative analysis, and sentiment analysis to provide a comprehensive report on Invesco's margin compression compared to its peers in the capital markets industry.", "target": null }}]
    ...

    If you identify a filing (10K / 10Q / 8K) as part of a step, you must also identify and state the section from the document.

    The sections you have access to in a 10K are:
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

    The sections you have access to in a 8K are:
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

    The sections you have access to in a 10Q are:
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

    You must follow these instructions:
    1. Respond in JSON.
    2. Be granular when defining the list of steps. Use keywords such as 'Perform sentiment analysis for...', 'Get stock prices for...' etc.
    3. You must never include a step to search the internet.
    4. Never assume you have access to information. Always include steps to lookup information whether in an earnings transcript, 10K filing, API etc.
    5. Explicitly state which data source a step needs e.g., 10K / 8K / Earnings transcript / API etc.
    6. Explicitly state the section from the data source that a step needs e.g., Management’s Discussion and Analysis of Financial Condition and Results of Operations from 10K
    7. If you are collecting data on multiple companies, explicitly state the names and symbols of those companies in the step.
    8. Remember that "target" is an array list of tickers for which the step applies to. Only to be populated with tickers if the step is 'data_retrieval', else set to null. Important when a data_retrieval step needs to be carried out for multiple companies / peer-companies etc.

    You are given the following query:
    ...
    {query}
    ...
    """


def generate_identify_metadata_in_query_prompt(query: str):
    now = datetime.now()
    return f"""
    You are an expert financial analyst.

    You are given a financial query.

    Extract important metadata parameters from the query.

    Respond in JSON.

    The key of the response should be metadata.

    The value should be an array list of dictionaries.

    Extract the following parameters:
    1. target_years: a list of years that the query targets.
    2. query_scope: the scope of the financial query. Either broad (multiple companies) or narrow (single company only)
    3. identified_topic: the financial topic covered by the query
    4. query_type: screening or analysis. A screening query aims to only filter stocks e.g., Identify stocks with a PE ratio above 15 or What stocks do you cover in the Information technology industry. An analysis query requires deep analysis on a company or a series of companies.
    The current date is {now.strftime('%b')} {now.day} {now.year}.

    The query you have been given is:
    ...
    {query}
    ...

    Your response:
    """


def generate_identify_data_parameters_prompt(query: str):
    return f"""
    You are an expert financial analyst.

    You have been given a financial query.

    Your task is to identify the most relevant and important financial parameters that you will use to answer the query.

    Extract the following parameters:
    1. required_data_parameters: a comprehensive list of granular financial data parameters that a financial analyst would need to solve the query in 10Ks and earnings transcripts.
    2. relevant_financial_performance_figures: important financial figures related to performance that are relevant to the query in 10Ks and earnings transcripts.
    3. relevant_financial_ratios: important financial ratios that are relevant to the query that could be calculated from 10Ks and earnings transcripts.

    Return the data as JSON.

    For example, given the query:
    ...
    'Rite Aid (RAD) is going bankrupt. Can you identify early warning signs from the last 3 10Ks?'
    ...

    You would return:
    ...
    {{
    'required_data_parameters': [
    'Total liabilities and equity',
    'Cash flow from operations',
    'Net income (loss)',
    'Current ratio',
    'Debt to equity ratio',
    'Revenue trends',
    'Notes on debt restructuring or financial distress'
    ],
    'relevant_financial_performance_figures': [
    {{
    "income_statement_data": [
    "total_revenue",
    "cost_of_goods_sold",
    "gross_profit",
    "operating_expenses",
    "operating_income_or_loss",
    "net_income_or_loss"
    ]
    }},
    {{
    "balance_sheet_data": [
    "current_assets",
    "current_liabilities",
    "long_term_liabilities",
    "equity"
    ]
    }},
    {{
    "cash_flow_statement": [
    "net_cash_provided_by_operating_activities",
    "net_cash_used_in_investing_activities",
    "net_cash_used_in_financing_activities",
    "free_cash_flow"
    ]
    }},
    {{
    "notes_to_financial_statements": [
    "accounting_policies",
    "commitments_and_contingencies",
    "debt_and_credit_arrangements"
    ]
    }},
    {{
    "management_discussion_and_analysis": [
    "executive_overview",
    "financial_condition_and_results_of_operations",
    "liquidity_and_capital_resources"
    ]
    }},
    {{
    "auditor_report": [
    "opinion_on_financial_statements"
    ]
    }}
    ],
    'relevant_financial_ratios': [
    "current_ratio",
    "quick_ratio",
    "debt_to_equity_ratio",
    "interest_coverage_ratio",
    "inventory_turnover_ratio",
    "accounts_receivable_turnover_ratio",
    "gross_margin_ratio",
    "operating_margin_ratio",
    "net_profit_margin",
    "return_on_assets",
    "return_on_equity",
    "free_cash_flow_to_net_income"
    ]
    }}
    ...

    Remember to follow these instructions:
    1. You must be as granular in identifying the required_data_parameters as possible.
    2. Assume you have access to all the data you need.
    3. If you do not think you need certain data points, return an empty list.

    You have been asked the following query:
    ...
    {query}
    ...

    Parameterized query:
    """


def generate_convert_filter_params_into_query_prompt(filter_params_list: list):
    return f"""
    You have been given a list of database filter parameters and their values.

    Convert the list of parameters into a single legal mongoDB query.

    Respond in JSON.

    The key should be "db_query".

    The value should be a legal and valid MongoDB query.

    The collection you are querying has the following schema:
    ...
    {db_schema}
    ...

    Here's an example query of filter parameters to help you:
    ...
    [{{"industry": "banks"}}, {{"marketcapitalization": "greater than $10b"}},
        {{"peratio": "between 5 and 10"}}]
    ...

    And here is what you would respond with:
    ...
    {{"db_query": {{
        "industry": "banks",
        "marketcapitalization": {{"$gt": 10000000000}},
        "peratio": {{"$gte": 5, "$lte": 10}}
    }}}}
    ...

    Here is the list of filter parameters you have been given:
    ...
    {filter_params_list}
    ...

    Legal MongoDB query:
    """


def extract_financial_metrics_from_query(query: str):
    return f"""You are given a financial query.
    You are given a financial query.

    Extract all supported financial metrics from the query.

    Return your answer as an array list of dictionaries.

    The keys of the dictionaries should be the financial metrics that you have identified.

    The values should be the constraints that the user needs for the metric.

    Respond in JSON.

    The metrics that you should search for are:
    ...
    {supported_financial_metrics}
    ...

    For example in the query:
    ...
    "Find companies in the consumer technology industry with a PE ratio greater than 25 likely to transition from transactional to SaaS model, similar to ADSK and F5"
    ...

    You would return:
    ...
    {{
    "financial_metrics": [{{"peratio": "greater than 25"}}]
    }}
    ...

    Here's another example with multiple financial metrics in the query:
    ...
    "Over the past year, identify stocks that have lost more than 80% of their value within 6 months, that have a market capitalization of greater than $5b and a price to book ratio of at-leat 10  → Look for news that explain the losses."
    ...

    You would return:
    ...
    {{
    "financial_metrics": [{{"marketcapitalization": "greater than $5b"}}, {{"pricetobook": "greater than 10"}}]
    }}
    ...

    Follow these instructions:
    1. Never extract stock price metrics
    2. Only search for the metrics provided above.
    3. If the query does not mention a range e.g., greater than / less than / between, ignore the metric
    4. Only use the terms greater-than, less-than and between for values

    The query you have been given is:
    ...
    {query}
    ...

    Extracted financial metrics:
    """


def extract_gics_classifications_from_query(query):
    return f"""
    You are given a financial query.

    Extract Global Industry Classification Standard (GICS) classifications that are explicitly present in the query.

    Return your answer as an array list of dictionaries.

    The keys of the dictionaries can be "sector", "industry_group", "industry", or "sub_industry".

    The values should be the GICS classifications that you have explicitly identified.

    Respond in JSON.

    Here's an example to help you:
    Query:
    ...
    Over the past year, identify midcap Industrial stocks that gained more than 20% within a week → Look for news and filings that explain the gain = catalysts → Identify leading indicators → Find stocks that match these indicators (from the same universe of midcap Industrials)
    ...

    Your response:
    {{
    "gics_classifications": [{{"sector": "industrials"}}]
    }}

    Explanation:
    The query contained the phrase "industrial stocks" which maps to the GICS industrials sector.

    Here's another example:
    Query:
    ...
    For several quarters before SVB failed (in 1Q of 2023), the company was reporting declines in its tangible book value caused by unrealized losses on securities due to rising rates. The market ignored that because earnings continued to grow in this period.  Find consumer banks whose TBV has been deteriorating despite increasing earnings.
    ...

    Your response:
    {{
    "gics_classifications": [{{"sector": "financials"}}, {{"industry_group": "financial_services"}}, {{"industry": "consumer_finance"}}, {{"sub_industry": "consumer_finance"}}]
    }}

    Explanation:
    The query contained the phrase "consumer finance" which maps to the GICS financials sector, financial_services industry group, consumer_finance industry and consumer_finance sub_industry.

    Here's another example:
    Query:
    ...
    "Did Invesco experience margin compression over the past 2 years?"
    ...
    Your response:
    {{
    "gics_classifications": []
    }}

    Explanation:
    The query does not contain any phrases containing explicit GICS classifications.

    The entire list of GICS classifications is below:
    ...
    {gics_classifications_dict}
    ...

     You must follow these instructions:
    1. Use values from the taxonomy shown above
    2. If you cannot explicitly find a particular classification e.g., sub_industry / industry, do not include the key-value pair in the array-list
    3. If no GICS classifications are explicitly present, return an empty list.
    4. Do not generate GICS classifications for tickers in the query.
    The query you have been given is:
    {query}
    """


def extract_company_names_from_query(query: str):
    return f"""
    You are given a financial query.

    Extract any company names that the query addresses.

    Return your answer as an array list of stock tickers.

    Respond in JSON.

    The key of the array list should be 'companies'.

    If you find no companies, return an empty array list.

    Here's an example to help you:

    Query:
    ...
    Over the past year, identify midcap Industrial stocks that gained more than 20% within a week → Look for news and filings that explain the gain = catalysts → Identify leading indicators → Find stocks that match these indicators (from the same universe of midcap Industrials)
    ...

    Your response:
    {{
        "companies": []
    }}

    Here's another example:
    Query:
    ...
    RiteAid and BestBuy went bankrupt. Can you show me a trend of discussions about liquidity issues in their filings and earnings transcripts?  Then, find companies exhibiting a similar trend.
    ...

    Your response:
    {{
        "companies": [{{"name": "rite aid corp", "symbol": "radcq"}}, {{"name": "best buy co inc", "symbol": "bby"}}]
    }}

    You must follow these instructions:
    1. Only use the keys 'name' and 'symbol'.
    2. Lowercase all of the strings in your output.

    You are given the following query:
    ...
    {query}
    ...

    Your response:
    """


def re_classify_company_with_gics_taxonomy(filtered_company_object: dict):
    return f"""
    You are an expert financial analyst.

    You are analyzing the company overview for a stock in your portfolio.

    The sector / industry_group / industry / sub_industry values are not accurate.

    Your task is to accurately infer and add values for the parameters above using the GICS taxonomy.

    Return your response as json with the key "company_overview".

    Here is the GICS Taxonomy to help you classify the company you are looking at:

    ...
    {gics_classifications_dict}
    ...

    And here is the company that you are currently looking to re-classify:

    ...
    {filtered_company_object}
    ...

    Remember to add key value pairs for the parameters: sector / industry-group / industry / sub-industry

    Return only the parameters: sector / industry-group / industry / sub-industry

    Updated company object:
    """
