import csv
from datetime import date, datetime, timedelta
from pathlib import Path
from sys import exception
from app.config import Config
from dataclasses import dataclass
import logging

logger = logging.getLogger()

@dataclass(frozen=True)
class StopDeparture:
    trip_id: str
    route_id: str
    line_number: str
    arrival_time: str
    departure_time: str
    departure_DT: datetime
    headsign: str

with open(Config.STOPS) as file:
    stops = file.read()

def static_read():


    logger.info("Doing a static read")

    _fetch_static_data()

    # get stop id
    stop_id = _get_stop_id(Config.STOP_NAME)

    logger.debug("stop_id: %s", stop_id)

    if stop_id is None:
        return []  # or return [], depending on your API

    # Resolve trip id -> route_id -> line number ("route_short_name")

    today = datetime.now().date()
    departures = []

    for offset in (-1,0,1):
        service_date=today + timedelta(days=offset)
        departures.extend(_resolve_departures(stop_id,service_date))

    return departures


def _load_stops(file_path: Path) -> list[dict]:
    stops = []
    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stops.append(row)
    return stops

def _resolve_departures(stop_id: str, service_date: date) -> list[StopDeparture]:
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

            hours, minutes, seconds = map(int,row["departure_time"].split(":"))
            departure_datetime = datetime.combine(service_date,datetime.min.time()) + timedelta(
                hours = hours,
                minutes=minutes,
               seconds=seconds,
            )

            # Check availibilty of trip

            if (_check_date_availability(trip_id, service_date) is True):

                departures.append(
                    StopDeparture(
                        trip_id=trip_id,
                        route_id=route_id,
                        line_number=line_number,
                        arrival_time=row["arrival_time"],
                        departure_time=row["departure_time"],
                        departure_DT= departure_datetime,
                        headsign=row["stop_headsign"],
                    )
                )

    return departures

def _check_date_availability(trip_id, service_date: date) -> bool:

    service_id = _get_service_id(trip_id)


    weekday = service_date.strftime("%A").lower()

    # Check if it runs today in calendar.txt

    is_planned = _check_avalibility_in_schedule(service_id,service_date,weekday)


    # Check for exceptions in calendar_dates.txt
    has_exceptions = _check_schedule_exceptions(service_id,service_date)

    if has_exceptions is not None:
        #There is an exception and it's value dictates if it runs or not
        return has_exceptions

    return is_planned

def _get_service_id(trip_id) -> str:

    result = ""

    with Config.TRIPS.open(
        "r",
        encoding="utf=8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["trip_id"] == trip_id:
                return row["service_id"]

    return result

def _check_schedule_exceptions(service_id, today_date) -> bool | None:

    with Config.CAL_DATES.open(
        "r",
        encoding="utf=8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["service_id"] != service_id:
                continue

            date_dt = datetime.strptime(row["date"], "%Y%m%d").date()
            if date_dt == today_date and row["service_id"] == service_id:
                if row["exception_type"] == "1":
                    #Exception it does run today
                    logger.debug("This trip had exception: %s", row["exception_type"])
                    return True
                if row["exception_type"] == "2":
                    #Exception it does not run today
                    logger.debug("This trip had exception: %s", row["exception_type"])
                    return False


        #No exception found use regular schedule
        logger.debug("This trip had no exceptions")
        return None

def _check_avalibility_in_schedule(service_id, today_date, weekday) -> bool:

    # Open calendar_dates.txt and look for 0 or 1 on todays date.

    with Config.CAL.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:

            # check if todays date is in start-end range
            start_date = datetime.strptime(row["start_date"], "%Y%m%d").date()
            end_date = datetime.strptime(row["end_date"], "%Y%m%d").date()

            if(today_date >=start_date and today_date <= end_date):
                # Check if it runs on today's weekday
                if (row[weekday] == "1"):
                    # it runs today
                    logger.debug("this service id %s ran today %s", service_id,today_date)
                    return True
                else:
                    logger.debug("this service id %s did not run today %s", service_id,today_date)
                    return False

            else:
                logger.error("Todays out of range of calendar.txt! Stale data maybe?")
                return False

    return False

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
