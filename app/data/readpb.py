# read_pb_to_json.py
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import json

# read binary file
with open("TripUpdates.pb", "rb") as f:
    data = f.read()

# parse protobuf
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(data)

# convert to dict
feed_dict = MessageToDict(feed)

# save to JSON file
with open("TripUpdates.json", "w") as f:
    json.dump(feed_dict, f, indent=2)

print("Saved to TripUpdates.json ✅")