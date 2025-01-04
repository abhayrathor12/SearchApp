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


from django.http import JsonResponse, HttpResponse
import pandas as pd
from io import BytesIO
import json
from django.views.decorators.csrf import csrf_exempt


from django.http import JsonResponse, HttpResponse
import pandas as pd
from io import BytesIO
import json
import os
from django.conf import settings

import os
import json
import pandas as pd
from io import BytesIO
from django.http import JsonResponse
from django.conf import settings
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def download_excel(request):
    if request.method == "POST":
        # Parse the JSON data sent from the frontend
        data = json.loads(request.body).get("data", [])

        # Convert the data into a pandas DataFrame
        df = pd.DataFrame(data)

        # Create a BytesIO object to store the Excel file in memory
        output = BytesIO()

        # Create a new workbook and select the active sheet
        wb = Workbook()
        ws = wb.active

        # Write the DataFrame to the worksheet
        for row in dataframe_to_rows(df, index=False, header=True):
            ws.append(row)

        # Style the header with yellow background and borders
        yellow_fill = PatternFill(
            start_color="FFFF00", end_color="FFFF00", fill_type="solid"
        )
        thin_border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin"),
        )

        # Apply styles to header row
        for cell in ws[1]:
            cell.fill = yellow_fill
            cell.border = thin_border

        # Apply borders to all cells
        for row in ws.iter_rows(
            min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column
        ):
            for cell in row:
                cell.border = thin_border

        # Save the workbook to the output BytesIO object
        wb.save(output)

        # Move the cursor to the beginning of the file for sending
        output.seek(0)

        # Create the filename (you can customize this)
        filename = "order_summary.xlsx"
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Save the Excel file temporarily in the media folder
        with open(file_path, "wb") as f:
            f.write(output.read())

        # Return the URL of the file for download
        file_url = os.path.join(settings.MEDIA_URL, filename)

        return JsonResponse({"fileUrl": file_url})

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
