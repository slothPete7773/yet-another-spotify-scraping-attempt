from models.models import *
import json

filename = "test_file.json"

with open(filename, "r") as file:
    content = json.load(file)
    record_activities: list[dict] = content["items"]

    # print(record_activities[0].keys())
    model = TrackRecord(**record_activities[0])
    print(model.)
    # print(len(record_activities))
    # print(record_activities[0].keys())
    # a = []
    # a = TrackRecord()
