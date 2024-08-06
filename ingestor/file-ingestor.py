from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain_community.document_loaders import TextLoader
from supported_tickers import supported_tickers

import concurrent.futures
import os
import nest_asyncio
import re
nest_asyncio.apply()


load_dotenv()

llamaparse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

base_directory = f"{os.getcwd()}/data"

parsing_instructions = """The provided document is an Annual 10K report filed with the Securities and Exchange Commission (SEC).
The 10K provides detailed financial information on the company's financial performance for a specific year.
It includes unaudited financial statements, management discussion and analysis, and other relevant disclosures required by the SEC.
It contains multiple tables, graphs and charts."""

current_directory = os.getcwd()


def upload_parsed_documents(file_path, document_metadata):
    loader = TextLoader(file_path)
    documents = loader.load()
    # Split loaded documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    for doc in docs:
        doc.metadata = document_metadata

    print(
        f"Embedded Data for file {document_metadata.get('ticker')}_{document_metadata.get('filing_year')}_{document_metadata.get('filing_type')}✅")

    # Initialize Embeddings
    embeddings = FastEmbedEmbeddings()

    Qdrant.from_documents(
        documents=docs,
        embedding=embeddings,
        url=qdrant_url,
        collection_name=document_metadata.get("ticker"),
        api_key=qdrant_api_key
    )

    print(
        f"Uploaded Vectors to Qdrant file {document_metadata.get('ticker')}_{document_metadata.get('filing_year')}_{document_metadata.get('filing_type')} ✅")

    return True


def handle_ticker(ticker):
    ticker = ticker.lower()
    directory_path = os.path.join(base_directory, ticker)
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        # find all .txt files in the ticker directory
        for file_name in os.listdir(directory_path):
            if file_name.endswith(".txt"):
                print(f"Processing {file_name}")
                file_path = os.path.join(directory_path, file_name)
                # for each file, parse it and upload vectors to Qdrant
                pattern = r'_(\d{4})_'
                match = re.search(pattern, file_name)
                if match:
                    filing_year = match.group(1)

                # Add metadata
                document_metadata = {
                    "ticker": ticker,
                    "source": file_name,
                    "filing_type": "10-K",
                    "filing_year": filing_year if filing_year else "not_found"
                }

                upload_parsed_documents(file_path, document_metadata)

    else:
        print(f"\nDirectory {ticker} does not exist.")

    return True


if __name__ == "__main__":
    # Use ThreadPoolExecutor to process tickers in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(
            handle_ticker, ticker): ticker for ticker in supported_tickers}
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(
                    f"Error processing company: {e}")

    print("Completed Vectorization ✅")
