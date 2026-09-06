
from app.data_handling.read_data import _get_stop_id,static_read,_check_avalibility_in_schedule
from unittest.mock import mock_open, patch
from datetime import date


def test_get_stop_id_A():

    curr_stop_id = _get_stop_id("Campus Gräsvik")
    id_stop_A = "9022010001927001"

    print(f"Fetched ID: {curr_stop_id}")
    assert curr_stop_id == id_stop_A

def test_get_stop_time():
    #TODO: implement this
    pass

def test_service_runs_on_monday():
    fake_calendar=(
        "service_id,monday,tuesday,wednesday,thursday,friday,"
        "saturday,sunday,start_date,end_date\n"
        "1,1,0,0,0,0,0,0,20260901,20261130\n"
    )
    with patch(
        "app.data_handling.read_data.Config.CAL",
    ) as mock_calendar_path:
        mock_calendar_path.open = mock_open(read_data=fake_calendar)

        result = _check_avalibility_in_schedule(
            "1",
            date(2026, 9, 7),
            "monday"
        )
    assert result is True

def test_service_runs_on_tuesday():
    fake_calendar=(
        "service_id,monday,tuesday,wednesday,thursday,friday,"
        "saturday,sunday,start_date,end_date\n"
        "1,1,0,0,0,0,0,0,20260901,20261130\n"
    )
    with patch(
        "app.data_handling.read_data.Config.CAL",
    ) as mock_calendar_path:
        mock_calendar_path.open = mock_open(read_data=fake_calendar)

        result = _check_avalibility_in_schedule(
            "1",
            date(2026, 9, 8),
            "tuesday"
        )
    assert result is False
