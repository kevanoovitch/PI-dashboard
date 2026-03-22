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
    return mock_data
