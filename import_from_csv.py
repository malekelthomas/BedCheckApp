import csv
import os
import django



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BedCheckApp.settings")
django.setup()

with open("client_csv", "r") as csv_f:
    data = csv.reader(csv_f)
    for row in data:
        print(row)