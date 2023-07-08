import datetime
import os
import requests


class FlightSearch:
    def __init__(self, home_city: str):
        self.url = "https://api.tequila.kiwi.com/v2/search"
        self.api_key = os.environ["FLIGHT_SEARCH_API_KEY"]
        self.home_city = home_city
        self.currency = "HUF"

    def get_flight_prices(self, destination_city: str):

        search_date_from = datetime.datetime.now().strftime("%d/%m/%Y")
        search_date_to = (datetime.datetime.now() + datetime.timedelta(180)).strftime("%d/%m/%Y")

        headers = {
            "apikey": self.api_key
        }

        parameters = {
            "fly_from": f"city:{self.home_city}",
            "fly_to": f"city:{destination_city}",
            "date_from": search_date_from,
            "date_to": search_date_to,
            "curr": self.currency,
            "max_stopovers": 0

        }

        response = requests.get(url=self.url, params=parameters, headers=headers)
        if response.status_code != 200:
            response.raise_for_status()
            return
        elif len(response.json()['data']) > 0:
            results = {'cityTo': response.json()['data'][0]['cityTo'], 'price': response.json()['data'][0]['price'],
                       'departure': response.json()['data'][0]['local_departure'],
                       'arrival': response.json()['data'][0]['local_arrival']}
            return results
        else:
            return "No results found with such criteria"

    def get_iata_codes(self, city_name: str):
        iata_url = "https://api.tequila.kiwi.com/locations/query"

        headers = {
            "apikey": self.api_key
        }

        parameters = {
            "term": city_name,
            "location_types": "city",
        }

        response = requests.get(url=iata_url, headers=headers, params=parameters)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code
