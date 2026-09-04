from pathlib import Path


class Config:
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"

    STOP_NAME = "Campus Gräsvik"
    STOP_LETTER = "A"

    STOPS = DATA_DIR / "stops.txt"
    STOP_NAMES = DATA_DIR / "stop_names.txt"
    STOP_LETTERS = DATA_DIR / "stop_letters.txt"
    STOP_TIMES = DATA_DIR / "stop_times.txt"
    TRIPS = DATA_DIR / "trips.txt"
    ROUTES = DATA_DIR / "routes.txt"

    DEPARTURE_ENTRIES = 3
