# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

datamanager = DataManager()
flight_search = FlightSearch("BUD")
notification_manager = NotificationManager()

sheet_data = datamanager.get_data()
pprint(sheet_data)

iataCodes = [destination["iataCode"] for destination in sheet_data]

if "" in iataCodes:
    for line in sheet_data:
        if line["iataCode"] == '':
            line["iataCode"] = flight_search.get_iata_codes(line["city"])

    pprint(sheet_data)
    datamanager.update_sheet(sheet_data)

else:
    for destination in sheet_data:
        result = (flight_search.get_flight_prices(destination["iataCode"]))
        if type(result) == dict:
            print(f"{result['cityTo']}: HUF {round(result['price'])}")
            if round(result['price']) < destination["lowestPrice"]:
                try:
                    notification_manager.send_sms(price=round(result['price']), departure_city_name="Budapest",
                                                  departure_airport_iata_code="BUD", arrival_city_name=result['cityTo'],
                                                  arrival_airport_iata_code=destination['iataCode'],
                                                  outbound_date=result['departure'].split("T")[0],
                                                  inbound_date=result['arrival'].split("T")[0])
                except Exception:
                    print(f"Sending SMS failed -> Low price alert!\n"
                          f"Only HUF {int(result['price'])} to fly from Budapest-BUD "
                          f"to {result['cityTo']}-{destination['iataCode']}, "
                          f"from {result['departure'].split('T')[0]} to {result['arrival'].split('T')[0]}\n")
        else:
            print(result)
