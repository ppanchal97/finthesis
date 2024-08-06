import json
from openai import OpenAI
import prompts
from database import companies

openai_client = OpenAI(
    api_key="api-key")

def chat_completion(chat_history, model, temperature, response_format):
    response = openai_client.chat.completions.create(
        model=model,
        response_format={"type": response_format},
        messages=chat_history,
        temperature=temperature
    )
    if response:
        res_string = response.choices[0].message.content
        return res_string
    else:
        return None

if __name__ == "__main__":
    # Initialize the JSON file with an empty array
    with open('refactored_companies.json', 'w') as file:
        file.write('[\n')  # Start of JSON array

    for company in companies:
        filtered_company_object = {
            "Symbol": company["Symbol"],
            "AssetType": company["AssetType"],
            "Name": company["Name"],
            "Description": company["Description"],
            "CIK": company["CIK"],
            "Exchange": company["Exchange"],
            "Currency": company["Currency"],
            "Country": company["Country"],
            "Sector": company["Sector"],
            "Industry": company["Industry"],
            "Address": company["Address"],
        }
        system_prompt = prompts.re_classify_company_with_gics_taxonomy(filtered_company_object)
        chat_history = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "..."}
        ]
        response = chat_completion(
            chat_history=chat_history,
            model="gpt-4o",
            temperature=0,
            response_format="json_object",
        )
        if response:
            json_response = json.loads(response)
            company_overview = json_response.get("company_overview")
            company["Sector"] = company_overview["sector"]
            company["IndustryGroup"] = company_overview["industry_group"]
            company["Industry"] = company_overview["industry"]
            company["SubIndustry"] = company_overview["sub_industry"]

            # Write the updated company to the JSON file
            with open('refactored_companies.json', 'a') as file:
                file.write(json.dumps(company, indent=4) + ',\n')  # Append company to JSON array

            print(f"Processed {company['Symbol']}")

    # Correct the trailing comma and close the JSON array
    with open('refactored_companies.json', 'rb+') as file:
        file.seek(-2, 2)  # Seek to the second last byte
        file.truncate()  # Remove the last comma
        file.write(b'\n]')  # Close the JSON array

    print("Data written to refactored_companies.json successfully.")
