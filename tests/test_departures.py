import binascii
from datetime import datetime
from unittest.mock import patch
from app.api.departures import _binary_search_next_departure, _calculate_min_to_departure, get_departures_data
from app.data_handling.read_data import StopDeparture
def test_time_calculation():
    fake_now = datetime(2026, 9, 3, 7, 0, 0)

    time_str_1 = "7:05:00"
    time_str_2 = "10:38:06"
    time_str_3 = "25:54:06"

    with patch("app.api.departures.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now
        mock_datetime.strptime.side_effect = datetime.strptime
        result = _calculate_min_to_departure(time_str_1)
        assert result == 5

        result_2 = _calculate_min_to_departure(time_str_2)
        assert result_2 == 218

        result_3 = _calculate_min_to_departure(time_str_3)
        assert result_3 == 1134

def test_binary_search():
    fake_now = datetime(2026, 9, 3, 7, 0, 0)

    departures = [StopDeparture(trip_id='100001000007000001', route_id='9011010000100000', line_number='1', arrival_time='06:20:15', departure_time='06:20:15', headsign='Saltö'), StopDeparture(trip_id='100001000019000001', route_id='9011010000100000', line_number='1', arrival_time='07:13:15', departure_time='07:13:15', headsign='Saltö'), StopDeparture(trip_id='100001000021000001', route_id='9011010000100000', line_number='1', arrival_time='07:23:15', departure_time='07:23:15', headsign='Saltö'), StopDeparture(trip_id='100001000023000001', route_id='9011010000100000', line_number='1', arrival_time='07:33:15', departure_time='07:33:15', headsign='Saltö'), StopDeparture(trip_id='100001000027000001', route_id='9011010000100000', line_number='1', arrival_time='07:53:15', departure_time='07:53:15', headsign='Saltö')]

    with patch("app.api.departures.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now
        result = _binary_search_next_departure(departures)

        assert result == 1


#def test_get_departure_data():
#    get_departures_data()
