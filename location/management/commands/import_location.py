import csv
from django.core.management.base import BaseCommand
from location.models import County, SubCounty, Ward

class Command(BaseCommand):
    help = "Import Kenya counties, constituencies (as subcounties) and wards"

    def handle(self, *args, **kwargs):
        with open(
            r'E:\list of counties, constituencies, and wards.csv',
            newline='',
            encoding='utf-8'
        ) as csvfile:

            reader = csv.DictReader(csvfile)

            self.stdout.write(f"CSV Headers detected: {reader.fieldnames}")

            for row in reader:
                county_name = row['County'].strip()
                subcounty_name = row['Constituency_name'].strip()
                ward_name = row['Ward'].strip()

                county, _ = County.objects.get_or_create(
                    name=county_name
                )

                subcounty, _ = SubCounty.objects.get_or_create(
                    name=subcounty_name,
                    county=county
                )

                Ward.objects.get_or_create(
                    name=ward_name,
                    subcounty=subcounty
                )

        self.stdout.write(
            self.style.SUCCESS("Counties, constituencies, and wards imported successfully")
        )
