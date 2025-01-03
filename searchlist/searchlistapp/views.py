import pandas as pd
from searchlistapp.models import Productlist  # Adjust import as per your app


def import_productlist_from_csv(csv_path):
    # Load CSV data
    data = pd.read_csv(csv_path, skiprows=1, names=["model", "list_price"])

    # Clean data
    data = data.dropna()  # Remove rows with missing values
    data["list_price"] = (
        data["list_price"]
        .str.replace(r"[₹,]", "", regex=True)  # Remove currency symbols and commas
        .str.extract(r"(\d+\.?\d*)")[0]  # Extract numeric values
    )

    # Ensure valid numeric conversion
    data = data.dropna(subset=["list_price"])  # Drop rows where list_price is NaN
    data["list_price"] = data["list_price"].astype(float)  # Convert to float

    # Iterate through rows and save to database
    for _, row in data.iterrows():
        Productlist.objects.create(model=row["model"], list_price=row["list_price"])

    print("Data imported successfully.")


# File path
csv_path = "C:/Users/ADMIN/Desktop/search/searchlist/output.csv"
import_productlist_from_csv(csv_path)
