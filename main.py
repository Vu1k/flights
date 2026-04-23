from config import (ORIGIN, DESTINATION, DEPARTURE_DATE, RETURN_DATE, ADULTS,
                    MAX_STOPS, PREFERRED_LAYOVER_AIRPORTS, TARGET_PRICE_COP)
from serp_adapter import SerpFlightProvider


def filter_flights(flights):
    results = []
    for f in flights:
        layovers = [l["id"] for l in f.get("layovers", [])]
        if len(layovers) > MAX_STOPS:
            continue
        if any(airport not in PREFERRED_LAYOVER_AIRPORTS for airport in layovers):
            continue
        results.append(f)
    return results


def print_legs(legs):
    for leg in legs:
        dep = leg["departure_airport"]
        arr = leg["arrival_airport"]
        print(f"   {leg['flight_number']:10} {dep['id']}→{arr['id']}  {dep['time']}  ({leg['airline']})")


if __name__ == "__main__":
    provider = SerpFlightProvider()

    # IDA
    raw_flights, insights, _ = provider.get_flights(ORIGIN, DESTINATION, DEPARTURE_DATE, RETURN_DATE, ADULTS)
    valid_outbound = filter_flights(raw_flights)

    # REGRESO
    raw_return, _, _ = provider.get_return_flights(ORIGIN, DESTINATION, RETURN_DATE, ADULTS)
    valid_return = filter_flights(raw_return)

    print(f"--- Informe de Vuelos {ORIGIN} ↔ {DESTINATION} ---")
    if insights:
        print(f"Precio más bajo: {insights.get('lowest_price'):,} COP")
        print(f"Rango típico: {insights.get('typical_price_range')} COP\n")

    if not valid_outbound:
        print("No hay vuelos de IDA que cumplan los filtros.")
    else:
        for f in valid_outbound:
            price = f.get("price", 0)
            status = "COMPRAR AHORA" if price <= TARGET_PRICE_COP else "MONITOREAR"
            diff = price - TARGET_PRICE_COP
            print(f"\n[{status}] {price:,} COP (diff: {diff:+,})")
            print(f"   Duración: {f.get('total_duration')} min")
            print(f"   IDA ({DEPARTURE_DATE})")
            print_legs(f.get("flights", []))

    print(f"\n   REGRESO ({RETURN_DATE})")
    if not valid_return:
        print("   No hay vuelos de regreso que cumplan los filtros.")
    else:
        for f in valid_return[:2]:  # mostrar los 2 mejores
            print_legs(f.get("flights", []))

    print(f"\n   Buscar: https://www.google.com/travel/flights?q=vuelos+{ORIGIN}+{DESTINATION}+{DEPARTURE_DATE}+regreso+{RETURN_DATE}")
