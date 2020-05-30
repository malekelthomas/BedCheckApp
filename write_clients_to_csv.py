import csv
import os
import django



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BedCheckApp.settings")
django.setup()

from bedcheck.models import Client

clients = Client.objects.all()

with open("client_csv", "w") as csv_f:
    writer = csv.writer(csv_f)
    for i in clients:
        writer.writerow([i.first_name, i.last_name, i.cares_id, i.room_num, i.bed, i.signature, i.image, i.lp_on])
    csv_f.close()



