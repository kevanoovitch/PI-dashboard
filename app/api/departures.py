
from datetime import date, datetime, timedelta
from tkinter.constants import N
from app.data_handling.read_data import static_read
from app.config import Config

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
def get_departures_data():
    #FIXME:return mock_data

    # convert a list of departures objects into correct json structure
    departures = static_read()

    next_departure = _binary_search_next_departure(departures)
    # loop through amount of entries to be persented
    for entry in range(Config.DEPARTURE_ENTRIES):
        # look for the next entries in line
        pass

        # Convert each entry into one json block

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

        departure_seconds = _gtfs_seconds(departures[mid_idx].departure_time)

        if departure_seconds >= now_seconds:
            # This could be the next departure
            # OR maybe there is an earlier departure
            result = mid_idx
            high_idx = mid_idx - 1
        else:
            # This departure has already passed
            low_idx = mid_idx + 1

    return result

def _calculate_min_to_departure(departure_time: str) -> int:

    now = datetime.now()

    hours, minutes, seconds = map(int, departure_time.split(":"))

    # in order to handle times such as 25:24:11 (ie 01:24:11)
    midnight = now.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    departure = midnight + timedelta(
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )

    difference = departure - now
    return int(difference.total_seconds()/60)
