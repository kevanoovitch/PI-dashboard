

from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).resolve().parent
    PATH_TO_STOPS = BASE_DIR / "data" / "stops.txt"
    PATH_TO_STOP_TIMES = BASE_DIR / "data" / "stop_times.txt"

    STOP_NAME = "Campus Gräsvik"

    # TODO: add a select and view function 
    STOP_LETTER = "A"