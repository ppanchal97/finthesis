from dotenv import load_dotenv
from llama_parse import LlamaParse
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_community.document_loaders import TextLoader

import pickle
import requests
import os
import tempfile
import nest_asyncio
nest_asyncio.apply()


load_dotenv()

llamaparse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

parsing_instructions = """The provided document is an Annual 10K report filed with the Securities and Exchange Commission (SEC).
The 10K provides detailed financial information on the company's financial performance for a specific year.
It includes unaudited financial statements, management discussion and analysis, and other relevant disclosures required by the SEC.
It contains multiple tables, graphs and charts."""

data_to_scrape = [
    {
        "company_name": "comerica",
        "documents_to_parse": [
            {
                "filing_url": "https://app.quotemedia.com/data/downloadFiling?webmasterId=101533&ref=318115331&type=PDF&symbol=CMA&cdn=3ed37db065f231534aa63ebbed69cae0&companyName=Comerica+Incorporated&formType=10-K&dateFiled=2024-02-28",
                "year": 2024,
                "filing_type": "10K"
            },
            {
                "filing_url": "https://app.quotemedia.com/data/downloadFiling?webmasterId=101533&ref=117255384&type=PDF&symbol=CMA&companyName=Comerica+Incorporated&formType=10-K&dateFiled=2023-02-14&CK=28412",
                "year": 2023,
                "filing_type": "10K"
            },
            {
                "filing_url": "https://app.quotemedia.com/data/downloadFiling?webmasterId=101533&ref=116469867&type=PDF&symbol=CMA&companyName=Comerica+Incorporated&formType=10-K&dateFiled=2022-02-16&CK=28412",
                "year": 2022,
                "filing_type": "10K"
            }
        ]
    },
    {
        "company_name": "etsy",
        "documents_to_parse": [
            {
                "filing_url": "https://d18rn0p25nwr6d.cloudfront.net/CIK-0001370637/0fb17b49-062e-454f-b7e7-64158ece22d3.pdf",
                "year": 2024,
                "filing_type": "10K"
            },
            {
                "filing_url": "https://d18rn0p25nwr6d.cloudfront.net/CIK-0001370637/8c7ea579-d065-4550-a295-a65a98eab693.pdf",
                "year": 2023,
                "filing_type": "10K"
            },
            {
                "filing_url": "https://d18rn0p25nwr6d.cloudfront.net/CIK-0001370637/619701ee-f7dc-4baa-9463-4374cfcef85e.pdf",
                "year": 2022,
                "filing_type": "10K"
            }
        ]
    },
    {
        "company_name": "invesco",
        "documents_to_parse": [
            {
                "filing_url": "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000914208/99b9ac5d-22c7-42a0-bc5c-93814ee865db.pdf",
                "year": 2024,
                "filing_type": "10K"
            },
            {
                "filing_url": "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000914208/2b389d43-0fae-4809-af1d-201b18e672b0.pdf",
                "year": 2023,
                "filing_type": "10K"
            },
            {
                "filing_url": "https://d18rn0p25nwr6d.cloudfront.net/CIK-0000914208/ce38bc5d-beb5-4e9a-8280-a41a8edd8a67.pdf",
                "year": 2022,
                "filing_type": "10K"
            }]
    }
]


def read_pdf_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Save PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            tmp.write(response.content)
            tmp_pdf_file = tmp.name  # Capture the file name
        return tmp_pdf_file
    else:
        raise Exception(
            f"Failed to retrieve the PDF. Status code: {response.status_code}")


def load_or_parse_data(file_url, file_name):
    current_directory = os.getcwd()
    pdf_file_path = read_pdf_from_url(file_url)
    output_file = f"{current_directory}/data/parsed_{file_name}.pkl"

    if os.path.exists(output_file):
        # Load the parsed data from the file
        with open(output_file, "rb") as f:
            parsed_data = pickle.load(f)
    else:
        # Parse and store
        parser = LlamaParse(api_key=llamaparse_api_key, result_type="markdown",
                            parsing_instruction=parsing_instructions)
        llama_parse_documents = parser.load_data(pdf_file_path)

        with open(output_file, "wb") as f:
            pickle.dump(llama_parse_documents, f)

        parsed_data = llama_parse_documents

    # Optionally, clean up the temporary PDF file
    os.remove(pdf_file_path)
    print("Parsed Data ✅")

    return parsed_data


def upload_parsed_documents(parsed_pdf_contents, document_metadata):
    markdown_file_location = f"{os.getcwd()}/data/{file_name}.md"

    with open(markdown_file_location, 'a') as f:
        for doc in parsed_pdf_contents:
            f.write(doc.text + '\n')

    loader = TextLoader(markdown_file_location)
    documents = loader.load()
    # Split loaded documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    for doc in docs:
        doc.metadata = document_metadata

    print("Embedded Data ✅")

    # Initialize Embeddings
    embeddings = FastEmbedEmbeddings()

    Qdrant.from_documents(
        documents=docs,
        embedding=embeddings,
        url=qdrant_url,
        collection_name=document_metadata.get("company_name"),
        api_key=qdrant_api_key
    )

    print("Uploaded Vectors to Qdrant ✅")


if __name__ == "__main__":
    for company in data_to_scrape:
        company_name = company["company_name"]
        for document in company["documents_to_parse"]:
            filing_url = document["filing_url"]
            filing_year = document["year"]
            filing_type = document["filing_type"]
            file_name = f"{company_name}_{filing_year}_{filing_type}"

            parsed_pdf_contents = load_or_parse_data(filing_url, file_name)

            # Add metadata
            document_metadata = {
                "company_name": company_name,
                "source": file_name,
                "filing_type": filing_type,
                "filing_year": filing_year
            }

            upload_parsed_documents(parsed_pdf_contents, document_metadata)
