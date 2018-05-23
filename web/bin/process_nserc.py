import csv
import sys
import json

from collections import OrderedDict

in_csv = sys.argv[1]
out_json = sys.argv[2]

UNIVERSITY_COLUMN = 4
GRANT_STRUCTURE = OrderedDict([
    ("faculty_name",  1),
    ("university", 4),
    ("application_group", 21),
    ("application_group_fr", 22),
    ("application_area", 23),
    ("application_area_fr", 24),
    ("title", 34),
    ("summary", 36)
])

UOFA = "University of Alberta"

with open(in_csv, 'r', encoding="iso-8859-1") as csv_file, open(out_json, 'w', encoding="utf-8") as json_out:
    in_reader = csv.reader(csv_file)

    out = []
    for row in in_reader:
        if row[UNIVERSITY_COLUMN] == UOFA:
            # grant = [row[i] for i in OUT_FORMAT]
            grant = OrderedDict()
            for header, column in GRANT_STRUCTURE.items():
                grant[header] = row[column]
            out.append(grant)

    json.dump(out, json_out, indent=4)



