

from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).resolve().parent
    PATH_TO_STOPS = BASE_DIR / "data" / "stops.txt"

    STOP_NAME = "Campus Gräsvik"

    # TODO: add a select and view function 
    STOP_LETTER = "A"