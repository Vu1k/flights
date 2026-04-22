import requests
import os
from dotenv import load_dotenv

load_dotenv()

class SerpFlightProvider:
    def __init__(self):
        self.api_key = os.getenv("SERP_API_KEY")
        self.base_url = "https://serpapi.com/search.json"

    def get_flights(self, origin, destination, date):
        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": date,
            "currency": "COP",
            "hl": "es",
            "api_key": self.api_key
        }
        
        response = requests.get(self.base_url, params=params)
        data = response.json()
        
        # Aquí es donde extraemos la "carne" del JSON
        flights = data.get("best_flights", []) or data.get("other_flights", [])
        insights = data.get("price_insights", {})
        
        return flights, insights, data

# Ejemplo de lo que verías en los insights:
# {
#   "lowest_price": 5100000,
#   "price_level": "high",
#   "typical_price_range": [4200000, 4900000]
# }