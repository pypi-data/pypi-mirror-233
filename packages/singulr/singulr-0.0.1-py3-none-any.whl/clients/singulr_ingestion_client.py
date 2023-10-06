# Created by msinghal at 19/09/23
import requests


class Ingestion_Client(object):
    def __init__(self):
        self.injection_endpoint = "http://localhost:8080/api/ingestion/ingest"

    def ingest_payload(self, ingestion_payload):

        try:
            # Make an HTTP POST request to the Java REST endpoint with the data
            response = requests.post(self.injection_endpoint, json=ingestion_payload)  # Use json=data for sending JSON data

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content (JSON, XML, HTML, etc.)
                return response
            else:
                print(f"HTTP POST request failed with status code: {response.status_code}")
                return response

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None


if __name__ == '__main__':
    ic = Ingestion_Client()
    import json
    # with open("simulated_sample.json", "r") as file:
    #     # Parse the JSON content
    #     data = json.load(file)
    # ic.ingest_payload(data)

    with open("b.json", "r") as file:
        # Parse the JSON content
        data = json.load(file)
    ic.ingest_payload(data)
