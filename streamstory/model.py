import requests
import json
import pandas as pd
from streamstory.entities import Model, ModelInfo, BuildModelRequest, Config



class StreamStory:

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key


    def get_models(self) -> list[ModelInfo]:
        headers = {'x-api-key': self.api_key}
        response = requests.get(self.api_url + '/models', headers=headers)

        if response.status_code >= 300:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        
        res_json =  response.json()['models']
        models = [ModelInfo(**model) for model in res_json]
        return models
  
  
    def get_model_by_uuid(self, uuid: str) -> ModelInfo:
        headers = {'x-api-key': self.api_key}
        response = requests.get(self.api_url + '/models/' + uuid, headers=headers)

        if response.status_code >= 300:
            raise Exception(f"Error: {response.status_code} - {response.text}")

        res_json =  response.json()
        model = ModelInfo(**res_json)
        return model

    def delete_model_by_uuid(self, uuid: str) -> None:
        headers = {'x-api-key': self.api_key}
        response = requests.delete(self.api_url + '/models/' + uuid, headers=headers)

        if response.status_code >= 300:
            raise Exception(f"Error: {response.status_code} - {response.text}")


    def build_model(self, build_model_req: BuildModelRequest) -> ModelInfo:
        headers = {'x-api-key': self.api_key}
        json_data = build_model_req.model_dump(mode='json')
        response = requests.post(self.api_url + '/models/build', headers=headers, json=json_data)
        
        if response.status_code >= 300:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        
        return response.json() 


    def classify_datapoint(self, model_uuid, data):
        raise Exception("Not implemented yet")
