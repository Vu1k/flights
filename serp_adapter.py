import requests
import os
from dotenv import load_dotenv

load_dotenv()

class SerpFlightProvider:
    def __init__(self):
        self.api_key = os.getenv("SERP_API_KEY")
        self.base_url = "https://serpapi.com/search.json"

    def get_flights(self, origin, destination, date, return_date=None, adults=1):
        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": date,
            "type": "1" if return_date else "2",
            "adults": adults,
            "currency": "COP",
            "hl": "es",
            "deep_search": "true",
            "api_key": self.api_key
        }
        if return_date:
            params["return_date"] = return_date
        
        response = requests.get(self.base_url, params=params)
        data = response.json()
        
        # Aquí es donde extraemos la "carne" del JSON
        flights = data.get("best_flights", []) or data.get("other_flights", [])
        insights = data.get("price_insights", {})
        
        return flights, insights, data

    def get_return_flights(self, origin, destination, return_date, adults=1):
        params = {
            "engine": "google_flights",
            "departure_id": destination,
            "arrival_id": origin,
            "outbound_date": return_date,
            "type": "2",
            "adults": adults,
            "currency": "COP",
            "hl": "es",
            "deep_search": "true",
            "api_key": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data.get("best_flights", []) or data.get("other_flights", []), {}, data

# Ejemplo de lo que verías en los insights:
# {
#   "lowest_price": 5100000,
#   "price_level": "high",
#   "typical_price_range": [4200000, 4900000]
# }