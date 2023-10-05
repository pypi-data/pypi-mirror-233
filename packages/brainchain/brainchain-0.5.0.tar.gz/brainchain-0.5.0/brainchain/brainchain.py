import os
import sys
import json
import requests
import tiktoken
from urllib.parse import quote
import aiohttp
from . import SalesIntel, FactCheck

class Brainchain:
    def __init__(self, env: str = "prod", api_key: str = os.environ["BRAINCHAIN_API_KEY"],
                 service_url="https://brainchain--agent.modal.run/", salesintel_api_key=os.environ[
                "SALESINTEL_API_KEY"]):
        self.api_key = api_key
        self.env = env
        self.fact_check_instance = FactCheck(environment=env)
        self.sales_intel_client = SalesIntel(salesintel_api_key)
        self.environments = ["prod", "dev"]
        self.services = {
            "agent": {
                "prod": "https://brainchain--agent.modal.run/",
                "dev": "https://brainchain--agent-dev.modal.run/"
            },
            "agent-service": {
                "agent": "https://brainchain--agent-service.modal.run/agent"
            },
            "prompt-completion-service": {
                "prompting": "https://brainchain--prompt-completion-service.modal.run/prompting",
                "pdf-title": "https://brainchain--prompt-completion-service.modal.run/pdf-title",
                "pdf-authors": "https://brainchain--prompt-completion-service.modal.run/pdf-authors"
            },
            "search": {
                "prod": "https://brainchain--search.modal.run/",
                "dev":  "https://brainchain--search-dev.modal.run/"
            },
            "electrolaser": {
                "prod": "https://brainchain--electrolaser.modal.run/",
                "dev": "https://brainchain--electrolaser-dev.modal.run/"
            },
            "weaviate_ingestion": {
                "ingest": "https://brainchain--weaviate-ingestion-fastapi-app.modal.run/ingest/",
                "query": "https://brainchain--weaviate-ingestion-fastapi-app.modal.run/query/",
                "retrieve": "https://brainchain--weaviate-ingestion-fastapi-app.modal.run/retrieve/",
                "preview": "https://brainchain--weaviate-ingestion-fastapi-app.modal.run/preview/"
            }
        }

    def fact_check(self, statement):
        return self.fact_check_instance.fact_check(statement)

    def search(self, query):
        endpoint = self.services["search"][self.env]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"query": query}
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def search_results(self, query: str, additional_pages: int = 10):
        return self.electrolaser(query, additional_pages=additional_pages)

    def electrolaser(self, query: str, additional_pages: int = 50):
        endpoint = self.services["electrolaser"][self.env]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"query": query, "additional_pages": additional_pages}
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def bullet_point_summarizer(self, content: str, model="gpt-4-32k"):
        enc = tiktoken.encoding_for_model(model)
        endpoint = self.services["prompt-completion-service"]["prompting"]
        system_prompt = f"Write a concise summary of the user input in the form of numbered bullet points. Please output in JSON format, with a key named 'title' (corresponding to a title that you come up with based on the user input), as well as a key named 'description' of the overall text input, and then please have a key called 'bullet_points' which is an array of the bullet point summaries of the content."
        user_prompt = content
        content = content.replace("\n\n", "")
        total_tokens_used = len(enc.encode(content) + enc.encode(system_prompt))
        buffer = 512
        max_tokens = 32768 - (total_tokens_used + buffer)
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"user_prompt": user_prompt, "system_prompt": system_prompt, "backend": "azure", "model": "gpt-4-32k", "max_tokens": max_tokens }
        response = requests.post(endpoint, headers=headers, json=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def prompt(self, 
               user_prompt: str = None, 
               history=[], 
               temperature: float = 0.0,
               top_p: float = 0.0,
               max_tokens: int = 8192,
               system_prompt="You are an autoregressive language model that has been fine-tuned with instruction-tuning and RLHF. You carefully provide accurate, factual, thoughtful, nuanced answers, and are brilliant at reasoning. If you think there might not be a correct answer, you say so. Since you are autoregressive, each token you produce is another opportunity to use computation, therefore you always spend a few sentences explaining background context, assumptions, and step-by-step thinking RFFORE vol trv to answer a guestion", 
               model="gpt-4-32k", 
               backend="azure", 
               presence_penalty=0.0, 
               frequency_penalty=0.0, 
               n: int = 1,
               latest_only: bool = False,
               choices_only: bool = False,
               separator: str = "\n\n"
            ):
        
        endpoint = self.services["prompt-completion-service"]["prompting"]
        headers = {"Authorization": f"Bearer {self.api_key}"}

        # Construct the payload based on the new spec
        payload = {
            "user_prompt": user_prompt,
            "system_prompt": system_prompt,
            "model": model,
            "backend": backend,
            "presence_penalty": float(presence_penalty),
            "frequency_penalty": float(frequency_penalty),
            "top_p": float(top_p),
            "temperature": float(temperature),
            "max_tokens": int(max_tokens),
            "n": int(n),
            "history": history
        }
        
        # Construct the query parameters based on the new spec
        params = {
            "latest_only": latest_only,
            "choices_only": choices_only,
            "separator": separator
        }

        response = requests.post(endpoint, headers=headers, json=payload, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return {}

    def ingest(self, url: str):
        """
        Ingest a document into Weaviate, via URL. For now, this only works with PDFs. URL has to be publicly
        accessible and point directly to the document, e.g. https://www.example.com/document.pdf.

        Note: if you want to monitor the status of your doc's ingestion, look at the Modal logs for the
        "weaviate-ingestion" app.

        :param url: URL of document to ingest.
        """
        endpoint = self.services["weaviate_ingestion"]["ingest"]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {'url': url}
        response = requests.post(endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def preview(self, class_name: str) -> dict:
        """
        Preview a Weaviate class/collection. By default, 3 items are returned (all possible fields in schema are
        returned per item).

        :param class_name: Name of class you want to preview.
        :return: Dictionary containing metadata about the class + an `objects` list containing the items.
        """
        endpoint = self.services["weaviate_ingestion"]["preview"]
        endpoint += class_name
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def query(self, concept: str, fields: str = 'title') -> dict[dict[list[dict[str, str]]]]:
        """
        Query Weaviate IngestDocs collection. By default, only titles are returned. If you want to add fields,
        simply add them as a comma-separated string. For example, fields='title,authors,chunk'.

        Example use:
        ```
        from brainchain import Brainchain
        bc = Brainchain()
        results = bc.query('water', fields='title,authors,chunk')
        ```

        :param concept: Query you want to send to Weaviate.
        :param fields: Fields you want returned from Weaviate.
        :return: Weaviate response.
        """
        endpoint = self.services["weaviate_ingestion"]["query"]
        endpoint += concept

        headers = {"Authorization": f"Bearer {self.api_key}"}
        if fields:
            endpoint += f'?fields={fields}'
            response = requests.get(endpoint, headers=headers)
        else:
            response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def retrieve(self, doc_uuid: str):
        """
        Retrieve a document from Weaviate IngestDocs collection, as stored in Amazon S3, via `doc_uuid`.

        Example use:
        ```
        from brainchain import Brainchain
        bc = Brainchain()
        bc.retrieve(doc_uuid='ed2535defea94c03b1f5bb2e7486bb17')
        >>> 'Congrats, you have downloaded your file locally!'
        ```

        :param doc_uuid: Document UUID as stored in Weaviate.
        """
        endpoint = self.services["weaviate_ingestion"]["retrieve"]
        endpoint += doc_uuid
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def obtain_title(self, text_first_page: str = None):
        endpoint = self.services["prompt-completion-service"]["pdf-title"]
        payload = {}

        if text_first_page:
            payload["document_text"] = text_first_page
    
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(endpoint, headers=headers, json=payload)
        content = response.content.decode('utf-8')
        return json.loads(content)

    def obtain_authors(self, text_first_page: str = None):
        endpoint =  self.services["prompt-completion-service"]["pdf-authors"]
        payload = {}

        if text_first_page:
            payload["document_text"] = text_first_page

        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(endpoint, headers=headers, json=payload)
        content = response.content.decode('utf-8')
        return json.loads(content)

    def summon(self, prompt, agent_type="OAMF", model="gpt-4-32k", backend="azure", max_tokens=8000, temperature=0, top_p=0, presence_penalty=0.0, frequency_penalty=0.0, chat_history: list = []):
        endpoint = self.services["agent-service"]["agent"]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "prompt": prompt,
            "env": self.env,
            "backend": backend,
            "agent_type": agent_type,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "chat_history": chat_history
        }
        response = requests.post(endpoint, headers=headers, json=params)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    async def asummon(self, prompt, agent_type="OAMF", model="gpt-4-32k", backend="azure", max_tokens=8192, temperature=0, top_p=0, top_k=0.0, presence_penalty=0.0, frequency_penalty=0.0, chat_history: list = []):
        endpoint = self.services["agent-service"]["agent"]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "prompt": prompt,
            "env": self.env,
            "agent_type": agent_type,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "chat_history": chat_history
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=headers, json=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    response.raise_for_status()

    def get_company(self, **kwargs):
        return self.sales_intel_client.get_company(**kwargs)

    def get_people(self, **kwargs):
        return self.sales_intel_client.get_people(**kwargs)

    def get_technologies(self, **kwargs):
        return self.sales_intel_client.get_technologies(**kwargs)

    def get_news(self, **kwargs):
        return self.sales_intel_client.get_news(**kwargs)
