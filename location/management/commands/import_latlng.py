import csv
from django.core.management.base import BaseCommand
from location.models import County, SubCounty, Ward

class Command(BaseCommand):
    help = "Import latitude and longitude for counties, subcounties, and wards"

    def handle(self, *args, **kwargs):
        with open(r"E:\list of counties, constituencies, and wards.csv", newline='', encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                lat = row.get("latitude")
                lng = row.get("longitude")

                if row.get("county_name"):
                    County.objects.filter(
                        name__iexact=row["county_name"].strip()
                    ).update(latitude=lat, longitude=lng)

                if row.get("subcounty_name"):
                    SubCounty.objects.filter(
                        name__iexact=row["subcounty_name"].strip()
                    ).update(latitude=lat, longitude=lng)

                if row.get("ward_name"):
                    Ward.objects.filter(
                        name__iexact=row["ward_name"].strip()
                    ).update(latitude=lat, longitude=lng)

        self.stdout.write(self.style.SUCCESS("Latitude & Longitude imported successfully"))
