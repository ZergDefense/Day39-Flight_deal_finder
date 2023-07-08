import os

from twilio.rest import Client


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def send_sms(self, price, departure_city_name, departure_airport_iata_code, arrival_city_name,
                 arrival_airport_iata_code, outbound_date, inbound_date):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_TOKEN']

        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body=f"Low price alert!\n"
                 f"Only HUF {price} to fly from {departure_city_name}-{departure_airport_iata_code} "
                 f"to {arrival_city_name}-{arrival_airport_iata_code}, "
                 f"from {outbound_date} to {inbound_date}",
            from_=os.environ['TWILIO_FROM_NUMBER'],
            to=os.environ['TWILIO_FROM_NUMBER']
        )
        print(message.status)
