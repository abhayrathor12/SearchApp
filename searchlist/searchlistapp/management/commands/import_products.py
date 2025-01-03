import csv
from django.core.management.base import BaseCommand
from searchlistapp.models import (
    Productlist,
)  # Replace `your_app` with the name of your app


class Command(BaseCommand):
    help = "Import products from a CSV file into the Productlist model"

    def handle(self, *args, **kwargs):
        csv_file = "C:/Users/ADMIN/Desktop/searchingapp/searchprice/price.PDF"  # Replace with the path to your CSV file

        try:
            with open(csv_file, mode="r", encoding="ISO-8859-1") as file:
                reader = csv.DictReader(file)
                print("Headers found:", reader.fieldnames)  # Debugging headers

                for row in reader:
                    model = row["Model"].strip() if "Model" in row else None
                    list_price = (
                        row["List Price"].replace("₹", "").replace(",", "").strip()
                        if "List Price" in row
                        else None
                    )

                    if model:  # Skip rows where the model is blank
                        Productlist.objects.create(
                            model=model,
                            list_price=float(list_price),
                        )
                        self.stdout.write(f"Added {model} with price {list_price}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))

        self.stdout.write(self.style.SUCCESS("Product import completed!"))
