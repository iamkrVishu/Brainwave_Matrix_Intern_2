import pandas as pd
import os

def generate_excel_report(products, sales):
    try:
        file_path = "reports/product_sales_report.xlsx"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Debug: Print products to verify column structure
        print("Products Data from DB:", products)

        # Corrected column names (8 columns instead of 7)
        product_columns = ['ID', 'Name', 'Price', 'Quantity', 'Category', 'SKU', 'Expiry Date', 'Reorder Level']

        # Convert product data to DataFrame
        product_df = pd.DataFrame(products, columns=product_columns)

        # Convert sales data to DataFrame
        sales_df = pd.DataFrame(sales, columns=['Sale ID', 'Product ID', 'Quantity Sold', 'Total Price', 'Sale Date'])

        # Create Excel Writer & Save Sheets
        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            product_df.to_excel(writer, sheet_name="Products", index=False)
            sales_df.to_excel(writer, sheet_name="Sales", index=False)

        print("✅ Excel report generated successfully:", file_path)
        return file_path

    except Exception as e:
        print("❌ Error generating Excel report:", e)
        return None