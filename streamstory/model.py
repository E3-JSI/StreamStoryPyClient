import requests
import json
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional
import datetime
from streamstory.entities import Model, ModelInfo





# Plan
# 1. classes for configuration
# 2. classes for model




 



class StreamStory:

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key



    def get_models(self) -> list[ModelInfo]:
        headers = {'x-api-key': self.api_key}
        response = requests.get(self.api_url + '/models', headers=headers)
        res_json =  response.json()['models']
        models = [ModelInfo(**model) for model in res_json]
        return models
  
  
    def get_model_by_uuid(self, uuid) -> ModelInfo:
        headers = {'x-api-key': self.api_key}
        response = requests.get(self.api_url + '/models/' + uuid, headers=headers)
        res_json =  response.json()
        model = ModelInfo(**res_json)
        return model

    # def delete_model_by_uuid(self, uuid):
    #     pass

    # def classify_datapoint(self, model_uuid, data):
    #     pass


    # def build_model(self, data, config):
    #     pass


