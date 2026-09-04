import csv
from pathlib import Path
from app.config import Config
from dataclasses import dataclass


@dataclass(frozen=True)
class StopDeparture:
    trip_id: str
    route_id: str
    line_number: str
    arrival_time: str
    departure_time: str
    headsign: str

with open(Config.STOPS) as file:
    stops = file.read()

def static_read():

    _fetch_static_data()

    # get stop id
    stop_id = _get_stop_id(Config.STOP_NAME)

    if stop_id is None:
        return None  # or return [], depending on your API

    # Resolve trip id -> route_id -> line number ("route_short_name")
    departures = _resolve_departures(stop_id)

    return departures


def _load_stops(file_path: Path) -> list[dict]:
    stops = []
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stops.append(row)
    return stops

def _resolve_departures(stop_id: str) -> list[StopDeparture]:
    trip_to_route = _load_trip_to_route()
    route_to_line = _load_route_to_line()

    departures: list[StopDeparture] = []

    with Config.STOP_TIMES.open("r", encoding="utf-8", newline="",) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["stop_id"] != stop_id:
               continue

            trip_id = row["trip_id"]
            route_id = trip_to_route.get(trip_id)

            if route_id is None:
                continue

            line_number = route_to_line.get(route_id)

            if line_number is None:
                continue

            departures.append(
                StopDeparture(
                    trip_id=trip_id,
                    route_id=route_id,
                    line_number=line_number,
                    arrival_time=row["arrival_time"],
                    departure_time=row["departure_time"],
                    headsign=row["stop_headsign"],
                )
            )

    return departures

def _load_trip_to_route() -> dict[str,str]:
    trip_to_route: dict[str, str] = {}

    with Config.TRIPS.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            trip_to_route[row["trip_id"]] = row["route_id"]

    return trip_to_route

def _load_route_to_line() -> dict[str, str]:
    route_to_line: dict[str,str] = {}

    with Config.ROUTES.open("r", encoding="utf-8", newline="",) as file:
        reader = csv.DictReader(file)

        for row in reader:
            route_to_line[row["route_id"]] = row["route_short_name"]

    return route_to_line


def _get_stop_id(stop_name: str, file_path: Path = Config.STOPS) -> str | None:
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
        (stop for stop in children if stop["platform_code"] == Config.STOP_LETTER),
        None
    )

    if child_a is not None:
        return child_a["stop_id"]

    # 3. Otherwise pick first child
    return children[0]["stop_id"]


def _get_scheduled_stop_time(stop_id):
    pass
    # Based on stop_times.txt get



    # All stop times and convert to HH:MM (Digital clock format)



def _fetch_static_data():
    #TODO: implement this
    pass

    #will do this call
    # https://opendata.samtrafiken.se/gtfs/{operator}/{operator}.zip?key={apikey}
    # where operator = blekinge
    # key from env

    # it gets a zip file

    # unzip the file

    # and overwrite txt files in /data
