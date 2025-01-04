import pandas as pd
from searchlistapp.models import Productlist  # Adjust import as per your app
from django.shortcuts import render


def homepage(request):

    return render(request, "home.html")


from django.http import JsonResponse
from .models import Productlist


def ajax_search(request):
    query = request.GET.get("q", "")  # Get the query string
    results = []
    if query:
        products = Productlist.objects.filter(
            model__icontains=query
        )  # Filter models containing the query
        results = [
            {"model": product.model, "list_price": str(product.list_price)}
            for product in products
        ]
    return JsonResponse({"results": results})


import json
from django.http import JsonResponse, HttpResponse
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
from django.views.decorators.csrf import csrf_exempt


from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt


import io
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

import json
from django.http import JsonResponse, HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from django.views.decorators.csrf import csrf_exempt
from io import BytesIO

import json
from django.http import HttpResponse, JsonResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt

import json
import pandas as pd
from django.http import HttpResponse, JsonResponse
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def generate_excel(request):
    if request.method == "POST":
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)
            order_data = data.get("order_data", [])

            # Define headings
            headings = [
                "Model",
                "Price",
                "Quantity",
                "Discount (%)",
                "Subtotal",
                "Stock Availability",
            ]

            # Convert order_data to a pandas DataFrame
            df = pd.DataFrame(order_data, columns=headings)

            # Create an in-memory output buffer
            output = BytesIO()

            # Use ExcelWriter to write the DataFrame to an Excel file
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Order Data")

            # Reset the pointer to the start of the buffer
            output.seek(0)

            # Prepare the HTTP response
            response = HttpResponse(
                output,
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = 'attachment; filename="order_data.xlsx"'

            return response

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


# def search_products(request):

#     return render(request, "search_results.html", {"query": query, "results": results})


# def import_productlist_from_csv(csv_path):
#     # Load CSV data
#     data = pd.read_csv(csv_path, skiprows=1, names=["model", "list_price"])

#     # Clean data
#     data = data.dropna()  # Remove rows with missing values
#     data["list_price"] = (
#         data["list_price"]
#         .str.replace(r"[₹,]", "", regex=True)  # Remove currency symbols and commas
#         .str.extract(r"(\d+\.?\d*)")[0]  # Extract numeric values
#     )

#     # Ensure valid numeric conversion
#     data = data.dropna(subset=["list_price"])  # Drop rows where list_price is NaN
#     data["list_price"] = data["list_price"].astype(float)  # Convert to float

#     # Iterate through rows and save to database
#     for _, row in data.iterrows():
#         Productlist.objects.create(model=row["model"], list_price=row["list_price"])

#     print("Data imported successfully.")


# # File path
# csv_path = "C:/Users/DELL/Desktop/SearchApp/searchlist/output.csv"
# import_productlist_from_csv(csv_path)
