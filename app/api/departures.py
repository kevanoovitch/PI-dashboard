
from datetime import date, datetime, timedelta
from doctest import debug
from venv import logger
from app.data_handling.read_data import static_read
from app.config import Config
import logging


"""
Docstring for app.api.departure

My get departure api which should return the data
line number
destination
departure time
platform/departure stop

Optionals:
minutes until departure
status (on time / delayed)

ex 1:
linje 1: Saltö, 4 min från Campus Gräsvik

or something like this
| Linje | Dst | Time |
---
| 1     | Saltö | 4 min |
---

"""

mock_data = [
    {
        "line": "1",
        "destination": "Saltö",
        "minutes_to_departure": "4",
        "station": "Campus Gräsvik"
    },
    {
        "line": "1",
        "destination": "Saltö",
        "minutes_to_departure": "14",
        "station": "Campus Gräsvik"
    },
    {
        "line": "1",
        "destination": "Saltö",
        "minutes_to_departure": "24",
        "station": "Campus Gräsvik"
    }

]

logger = logging.getLogger()

def get_departures_data():

    clean_data = []
    # convert a list of departures objects into correct json structure
    departures = static_read()

    departures.sort(
        key=lambda departure: departure.departure_DT)


    next_departure_idx = _binary_search_next_departure(departures)

    if next_departure_idx == -1:
        logger.error("not departures found")
        return []
    # loop through amount of entries to be persented


    logger.info("Parsing departure data from static read")

    picked_entries_arr = departures[next_departure_idx:next_departure_idx+Config.DEPARTURE_ENTRIES]

    for entry in picked_entries_arr:

        minutes_to_departure = _calculate_min_to_departure(entry.departure_DT)

        display_time = (
            f"{minutes_to_departure} min"
            if minutes_to_departure < 60
            else entry.departure_DT.strftime("%H:%M")
        )

        day_label = (
            "Tomorrow"
            if entry.departure_DT.date() == datetime.now().date() + timedelta(days=1)
            else ""
        )

        parsed_entry = {
            "line": entry.line_number,
            "destination": entry.headsign,
            "minutes_to_departure": minutes_to_departure,
            "station": Config.STOP_NAME,
            "display_time" : display_time,
            "day_label" : day_label,
        }

        clean_data.append(parsed_entry)

        logger.debug(
            "Parsed departure: %s",
            parsed_entry,
        )

        # Convert each entry into one json block
    return clean_data

#FIXME: remove derelict function
def _gtfs_seconds(time_str: str) -> int:
    hours, minutes, seconds = map(int, time_str.split(":"))
    return hours * 3600 + minutes * 60 + seconds

def _binary_search_next_departure(departures):

    # Find the departure nearest to the current time using gtfs_minutes
    now = datetime.now()
    now_seconds = (
        now.hour * 3600
        + now.minute * 60
        + now.second
    )

    low_idx = 0
    high_idx = len(departures)-1


    result = -1
    while low_idx <= high_idx:
        mid_idx = low_idx+(high_idx-low_idx) //2

        if departures[mid_idx].departure_DT >= now:
            # This could be the next departure
            # OR maybe there is an earlier departure
            result = mid_idx
            high_idx = mid_idx - 1
        else:
            # This departure has already passed
            low_idx = mid_idx + 1

    return result

def _calculate_min_to_departure(departure_dt: datetime) -> int:
    difference = departure_dt - datetime.now()
    return int(difference.total_seconds()/60)
