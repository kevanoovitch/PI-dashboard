
import logging
from datetime import datetime, timedelta

from app.config import Config
from app.data_handling.read_data import static_read

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

def _binary_search_next_departure(departures):

    # Find the departure nearest to the current time using gtfs_minutes
    now = datetime.now()

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
