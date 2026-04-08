
from app.data_handling.read_data import _get_stop_id

def test_get_stop_id_A():

    curr_stop_id = _get_stop_id("Campus Gräsvik")
    id_stop_A = "9022010001927001"

    print(f"Fetched ID: {curr_stop_id}")
    assert curr_stop_id == id_stop_A
    
def test_get_stop_time():
    pass 