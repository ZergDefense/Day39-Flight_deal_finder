import os
from pprint import pprint
import requests


class DataManager:
    def __init__(self):
        self.url = os.environ['SHEETY_ENDPOINT']
        self.header = {
            "Authorization": f"Bearer {os.environ['TOKEN']}"
        }

    def get_data(self):
        return requests.get(url=self.url, headers=self.header).json()["prices"]

    def update_sheet(self, sheet_data):
        for line in sheet_data:
            request_body = {
                "price": {
                    "iataCode": line["iataCode"]
                }
            }
            response = requests.put(url=f"{self.url}/{line['id']}", headers=self.header, json=request_body).text
            pprint(response)

