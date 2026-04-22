from config import (ORIGIN, DESTINATION, DEPARTURE_DATE,
                    MAX_STOPS, PREFERRED_LAYOVER_AIRPORTS, TARGET_PRICE_COP)
from serp_adapter import SerpFlightProvider

def filter_and_analyze(flights):
    results = []
    for f in flights:
        legs = f.get("flights", [])
        layovers = [leg["arrival_airport"]["id"] for leg in legs[:-1]]

        # Reglas de seguridad: máx 1 escala, solo en aeropuertos preferidos
        if len(layovers) > MAX_STOPS:
            continue
        if any(airport not in PREFERRED_LAYOVER_AIRPORTS for airport in layovers):
            continue

        price = f.get("price", 0)
        results.append({
            "flight": f,
            "status": "COMPRAR AHORA" if price <= TARGET_PRICE_COP else "MONITOREAR",
            "diff": price - TARGET_PRICE_COP
        })
    return results

if __name__ == "__main__":
    provider = SerpFlightProvider()
    raw_flights, insights, data_raw = provider.get_flights(ORIGIN, DESTINATION, DEPARTURE_DATE)

    print(f"--- Informe de Vuelos {ORIGIN} -> {DESTINATION} ({DEPARTURE_DATE}) ---")

    if insights:
        print(f"Precio más bajo disponible: {insights.get('lowest_price')} COP")
        print(f"Rango típico: {insights.get('typical_price_range')} COP\n")

    import json; print(json.dumps(data_raw, indent=2, ensure_ascii=False))

    valid_options = filter_and_analyze(raw_flights)

    if not valid_options:
        print("No hay vuelos que cumplan los filtros de seguridad.")
    else:
        for opt in valid_options:
            f = opt["flight"]
            airline = f["flights"][0].get("airline", "Desconocida")
            duration = f.get("total_duration", "N/A")
            print(f"[{opt['status']}] {airline} - {f['price']} COP (diff: {opt['diff']:+,})")
            print(f"   Duración total: {duration} min")
