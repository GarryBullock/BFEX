import sys
import json

from collections import OrderedDict

in_json = sys.argv[1]
out_json = sys.argv[2]

with open(in_json, 'r') as csv_file, open(out_json, 'w') as json_out:
    data = json.load(csv_file)

    keywords = set()
    for keyword in data["data"]:
        if keyword and len(keyword.split()) > 1 and not keyword.startswith("and "):
            keywords.add(keyword)
            
    data["data"] = list(keywords)
    json.dump(data, json_out, indent=4)