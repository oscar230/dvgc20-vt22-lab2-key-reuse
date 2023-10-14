import json

with open("crib_drag_results.json", "r") as infile:
    data = json.load(infile)

print(data)
