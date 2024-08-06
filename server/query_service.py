import prompts
import json
import utils.enums as enums

from data_fetching_agent import tools, available_functions_dict

DB_SEARCH_LIMIT = 5

class QueryService:
    def __init__(self, openai_client, db_client):
        self.openai_client = openai_client
        self.db_client = db_client

    async def chat_completion(self, chat_history, model, temperature=None, response_format=None, tools=None, tool_choice=None):
        if tools and tool_choice:
            response = self.openai_client.chat.completions.create(
            model=model,
            messages=chat_history,
            tools=tools,
            tool_choice=tool_choice
            )
            
            if response:
                response_message = response.choices[0].message
                return response_message
        else:
            response = self.openai_client.chat.completions.create(
                model=model,
                response_format={"type": response_format},
                messages=chat_history,
                temperature=temperature
            )
            if response:
                res_string = response.choices[0].message.content
                return res_string

    async def check_explicit_company_names_in_query(self, query):
        system_prompt = prompts.extract_company_names_from_query(query)
        chat_history = [
            {"role": "system",
                "content": system_prompt},
            {"role": "user", "content": f"..."}
        ]
        response = await self.chat_completion(
            chat_history=chat_history,
            model="gpt-4o",
            temperature=0,
            response_format="json_object",
        )
        if response:
            json_response = json.loads(response)
            stocks_list = json_response.get('companies')
            return stocks_list

    async def extract_gics_classifications_in_query(self, query):
        system_prompt = prompts.extract_gics_classifications_from_query(query)
        chat_history = [
            {"role": "system",
                "content": system_prompt},
            {"role": "user", "content": "..."}
        ]
        response = await self.chat_completion(
            chat_history=chat_history,
            model="gpt-4o",
            temperature=0.5,
            response_format="json_object",
        )
        if response:
            json_response = json.loads(response)
            gics_classification_list = json_response.get(
                'gics_classifications')
            print(f"Detected GICS Taxonomy: {gics_classification_list}")
            return gics_classification_list

    async def filter_companies_by_financial_metrics_in_query(self, query):
        system_prompt = prompts.extract_financial_metrics_from_query(query)
        chat_history = [
            {"role": "system",
                "content": system_prompt},
            {"role": "user", "content": f"..."}
        ]
        response = await self.chat_completion(
            chat_history=chat_history,
            model="gpt-4o",
            temperature=0,
            response_format="json_object",
        )
        if response:
            json_response = json.loads(response)
            financial_metrics_list = json_response.get('financial_metrics')
            return financial_metrics_list

    def find_most_granular_classification(self, classifications):
        hierarchy = {
            "sector": 1,
            "industry_group": 2,
            "industry": 3,
            "sub_industry": 4
        }

        most_granular = None
        max_level = 0

        for classification in classifications:
            for key in classification:
                if key in hierarchy and hierarchy[key] > max_level:
                    most_granular = classification
                    max_level = hierarchy[key]

        return most_granular

    async def convert_filter_params_into_db_query(self, filter_params_list):
        system_prompt = prompts.generate_convert_filter_params_into_query_prompt(
            filter_params_list)
        chat_history = [
            {"role": "system",
                "content": system_prompt},
            {"role": "user", "content": f"..."}
        ]
        response = await self.chat_completion(
            chat_history=chat_history,
            model="gpt-4o",
            temperature=0,
            response_format="json_object",
        )
        if response:
            json_response = json.loads(response)
            db_query = json_response.get('db_query')
            return db_query

    async def filter_stocks_from_query(self, query):
        stocks_list = []
        db_filter_list = []
        # 1. check for presence of explicit names
        explicit_company_names_in_query = await self.check_explicit_company_names_in_query(
            query)
        if len(explicit_company_names_in_query) > 0:
            print(f"Found explicit stocks in query: {explicit_company_names_in_query}")
            stocks_list.extend(explicit_company_names_in_query)
        # 2. check for presence of GICS classifications
        gics_classifications_list = await self.extract_gics_classifications_in_query(query)
        if len(gics_classifications_list) > 0:
            # lookup companies based on most granular classification
            most_granular_classification = self.find_most_granular_classification(
                gics_classifications_list)
            db_filter_list.append(most_granular_classification)

        # 3. check for presence of financial metrics
        financial_metrics_filter_list = await self.filter_companies_by_financial_metrics_in_query(query)
        # 4. Convert into db query
        db_filter_list.extend(financial_metrics_filter_list)
        db_filter_query = await self.convert_filter_params_into_db_query(db_filter_list)
        # 5. Execute query - searching only once
        print(f"Executing db query {db_filter_query}")
        if db_filter_query:
            cursor = self.db_client['companies'].find(db_filter_query, {'name': 1, 'symbol': 1, '_id': 0}).limit(DB_SEARCH_LIMIT)
            result = await cursor.to_list(length=None)
            existing_symbols = {stock['symbol'] for stock in stocks_list}
            for item in result:
                if item['symbol'] not in existing_symbols:
                    stocks_list.append(item)
                    existing_symbols.add(item['symbol'])
        return stocks_list

    async def build_data_parameters_list(self, query):
        system_prompt = prompts.generate_identify_data_parameters_prompt(query)
        chat_history = [
            {"role": "system",
                "content": system_prompt},
            {"role": "user", "content": f"..."}
        ]
        response = await self.chat_completion(
            chat_history=chat_history,
            model="gpt-4o",
            temperature=0,
            response_format="json_object",
        )
        if response:
            json_response = json.loads(response)
            return json_response

    async def get_query_metadata(self, query):
        system_prompt = prompts.generate_identify_metadata_in_query_prompt(
            query)
        chat_history = [
            {"role": "system",
                "content": system_prompt},
            {"role": "user", "content": f"..."}
        ]
        response = await self.chat_completion(
            chat_history=chat_history,
            model="gpt-4o",
            temperature=0,
            response_format="json_object",
        )
        if response:
            json_response = json.loads(response)
            metadata = json_response.get('metadata')
            return metadata

    async def build_query_execution_steps(self, query, stocks_list, required_data_parameters, relevant_financial_performance_figures, relevant_financial_ratios, query_metadata):
        system_prompt = prompts.generate_execution_steps_prompt(
            query, stocks_list, required_data_parameters, relevant_financial_performance_figures, relevant_financial_ratios, query_metadata)
        chat_history = [
            {"role": "system",
                "content": system_prompt},
            {"role": "user", "content": f"..."}
        ]
        response = await self.chat_completion(
            chat_history=chat_history,
            model="gpt-4o",
            temperature=0,
            response_format="json_object",
        )
        if response:
            json_response = json.loads(response)
            execution_steps = json_response.get(
                'steps_required_to_complete_query')
            return execution_steps

    async def fetch_identified_stocks(self, identified_stocks):
        # Query db for companies with symbols in identified stocks
        symbols = [stock.symbol for stock in identified_stocks]
        cursor = self.db_client['companies'].find({'symbol': {'$in': symbols}})

        results = []
        async for document in cursor:
            results.append(document)
        
        # TODO: filter results to exclude sensitive and irrelevant fields e.g., _id etc.
        for company in results:
            del company['_id']
        return results

    async def parameterize_query(self, query: str):
        # 1. Identify stocks in focus through filtering
        stocks_list = await self.filter_stocks_from_query(query)
        print(f"Retrieved {len(stocks_list)} stocks")

        # 2. Identify important data parameters
        data_params = await self.build_data_parameters_list(query)
        required_data_parameters = data_params.get('required_data_parameters')
        relevant_financial_performance_figures = data_params.get(
            'relevant_financial_performance_figures')
        relevant_financial_ratios = data_params.get(
            'relevant_financial_ratios')

        # 3. Identify important metadata
        query_metadata = await self.get_query_metadata(query)
        # TODO: decide how to handle screening only queries and analysis queries differently through query_type metadata parameter

        # 4. Identify execution steps - pass all params to generate better steps
        execution_steps = await self.build_query_execution_steps(query, stocks_list, required_data_parameters, relevant_financial_performance_figures, relevant_financial_ratios, query_metadata)
        with open('execution_steps.json', 'w') as file:
            json.dump(execution_steps, file, indent=4)

        return {"identified_stocks": stocks_list, "execution_steps": execution_steps, 
                "required_data_parameters": required_data_parameters, "relevant_financial_performance_figures": relevant_financial_performance_figures, 
                "relevant_financial_ratios": relevant_financial_ratios, "query_metadata": query_metadata, "query": query}
    

    async def identify_data_fetching_agent_tools(self, execution_step):
        user_message = f"""
        Instruction: {execution_step.instruction},
        Target Companies: {execution_step.target}
        """
        messages = []
        messages.append(
            {"role": "system", "content": prompts.generate_data_fetching_agent_system_prompt()})
        messages.append(
            {"role": "user", "content": user_message})
        response = await self.chat_completion(
            model="gpt-4o",
            chat_history=messages,
            tools=tools,
            tool_choice="auto"
        )
        identified_tools = response.tool_calls
        return identified_tools
    
    async def retrieve_data_for_step(self, execution_step):
        # 1. Initiate step data_bank
        data_bank = []
        # 2. Identify tools
        identified_tools = await self.identify_data_fetching_agent_tools(execution_step)
        # 3. Run tools
        for tool in identified_tools:
            function_name = tool.function.name
            function_to_call = available_functions_dict[function_name]
            function_args = json.loads(tool.function.arguments)        
            print(f"executing function: {function_name}. using arguments: {function_args}")
            res = function_to_call(function_args)
            # Sanitize outputs

            # Append into step's data bank
            data_bank.append({f"{function_name}_for_{function_args.get('ticker')}" :res})

        # 4. return
        return data_bank

    async def execute_analysis_step(self, execution_step):
        # 1. Identify Data Points from Data Bank Needed to Execute Step
        # 2. Run step on identified data points
        # 3. Return
        raise NotImplementedError()
    
    async def execute_query(self, query_execution_data: dict):
        # 1. Create a data_bank and analysis_bank
        data_bank = []
        analysis_bank = []
        
        # 2. Fetch the company objects containing key financial info for each company in identified stocks
        identified_stocks_instances_data = await self.fetch_identified_stocks(query_execution_data.identified_stocks)
        data_bank.append({"important_data_for_each_company_in_query": identified_stocks_instances_data})

        # 3. Iterate over execution steps
        for execution_step in query_execution_data.execution_steps:
            if execution_step.step_type == enums.ExecutionStepType.DATA_RETRIEVAL.value:
                # handle data retrieval step
                data_fetched_for_step = await self.retrieve_data_for_step(execution_step)
                data_bank.extend(data_fetched_for_step)
            elif execution_step.step_type == enums.ExecutionStepType.ANALYSIS.value:
                # handle analysis step
                analysis_for_step = await self.execute_analysis_step(execution_step)
                analysis_bank.extend(analysis_for_step)
        
        with open('data_bank.py', 'w') as file:
            json.dump(data_bank, file, indent=4)