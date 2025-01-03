import csv
from searchlistapp.models import Productlist

# Path to the CSV file
file_path = "C:/Users/ADMIN/Desktop/searchingapp/searchprice/price.PDF"

# Open and process the file
with open(file_path, "r", encoding="utf-8") as file:
    reader = csv.reader(file)

    for row in reader:
        model_name = row[0]  # First column
        price = (
            row[1].replace("₹", "").replace(",", "").replace('"', "").strip()
        )  # Clean price field

        # Save the data in the database
        Productlist.objects.create(model_name=model_name, price=float(price))
