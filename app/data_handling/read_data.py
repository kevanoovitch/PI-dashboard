import csv 
from app.config import Config



PATH_TO_STOPS = Config.PATH_TO_STOPS
STOP_NAME = Config.STOP_NAME
STOP_LETTER = Config.STOP_LETTER



def static_read():
    # will do big things 
    pass

    _fetch_static_data()

    # get stop id 
    _get_stop_id(STOP_NAME)

    # get stop times / "schedule for a stop"

    # trip_id "line nr id"

def _load_stops(file_path: str) -> list[dict]:
    stops = []
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader: 
            stops.append(row)
    return stops


def _get_stop_id(stop_name: str, file_path: str = PATH_TO_STOPS) -> str | None:
    stops = _load_stops(file_path)

    #1. Find the parent stop by name
    parent = next(
        (
            stop for stop in stops
            if stop["stop_name"] == stop_name
            and stop["location_type"] == "1"
            and stop["parent_station"] == ""
        ),
        None
    )

    if parent is None: 
        return None 
    
    parent_id = parent["stop_id"]

    #2. Find children of that parent stop
    children = [
        stop for stop in stops
        if stop["parent_station"] == parent_id
    ]

    if not children: 
        # no children exist
        return parent_id 
    
    child_a = next(
        (stop for stop in children if stop["platform_code"] == STOP_LETTER),
        None
    )

    if child_a is not None: 
        return child_a["stop_id"]

    # 3. Otherwise pick first child
    return children[0]["stop_id"]
    
def _fetch_static_data():
    #TODO: implement this

    #will do this call 
    # https://opendata.samtrafiken.se/gtfs/{operator}/{operator}.zip?key={apikey}
    # where operator = blekinge
    # key from env

    # it gets a zip file 

    # unzip the file

    # and overwrite txt files in /data
    pass 

