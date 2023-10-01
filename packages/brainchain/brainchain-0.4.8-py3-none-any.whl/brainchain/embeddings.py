import requests
from typing import Dict, Union, List, Any

class TextEmbeddingClient:
    def __init__(self, model: str = "gte-base", env: str = "prod"):
        if env == "prod":
            if model == "gte-base":
                self.base_url = "https://brainchain--embedding-service-gte-b.modal.run"
            else:
                raise Exception("Invalid model: only gte-base is supported at this time.")
        

    def is_live(self) -> bool:
        response = requests.get(f"{self.base_url}/.well-known/live")
        return response.status_code == 204

    def is_ready(self) -> bool:
        response = requests.get(f"{self.base_url}/.well-known/ready")
        return response.status_code == 204

    def get_meta(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/meta")
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()

    def embed_text(self, text: str, vectors_only: bool = True, split_text_over_512: bool = True) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        max_text_length = 512
        idx = 0
        if split_text_over_512:
            text_chunks = []
            while idx < len(text):
                text_chunks.append(text[idx:idx+max_text_length])
                idx += max_text_length
            text = text_chunks
            text_embedding_map = {}
            for chunk in text:
                payload = {"text": chunk}
                response = requests.post(f"{self.base_url}/vectors", json=payload)
                response_data = response.json()
                text_embedding_map[response_data["text"]] = response_data["vector"]
            if vectors_only:
                return list(text_embedding_map.values())
            else:
                return text_embedding_map
        else:
            payload = {"text": text}
            response = requests.post(f"{self.base_url}/vectors", json=payload)
            response.raise_for_status()
            response_data = response.json()
            if vectors_only:
                return response_data["vector"]
            else:
                return response_data