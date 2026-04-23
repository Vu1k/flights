# Parámetros del viaje
ORIGIN = "LPA"
DESTINATION = "MDE"
DEPARTURE_DATE = "2026-06-27"
RETURN_DATE = "2026-08-07"
ADULTS = 2  # Tus dos hijos

# Rangos para exploración de fechas
OUTBOUND_RANGE = ("2026-06-20", "2026-07-05")
RETURN_RANGE   = ("2026-08-01", "2026-08-15")

# Reglas de Oro (Filtros de Seguridad)
MAX_STOPS = 1
PREFERRED_LAYOVER_AIRPORTS = ["MAD"]  # Prioridad Madrid por idioma y logística
EXCLUDED_TRANSIT_COUNTRIES = ["USA"]  # Evitar trámites de visa
TARGET_PRICE_COP = 13000000           # Precio total ida y vuelta, 2 personas
