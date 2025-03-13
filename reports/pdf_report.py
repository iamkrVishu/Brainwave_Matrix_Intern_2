from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf_report(products, sales):
    try:
        file_path = "reports/product_sales_report.pdf"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        pdf = canvas.Canvas(file_path, pagesize=letter)
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(200, 770, "Product & Sales Report")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, 740, "--------------------------------------")

        # Add Product Data
        y = 720
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "Products:")
        pdf.setFont("Helvetica", 10)
        y -= 20
        for product in products:
            pdf.drawString(50, y, f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]}, Qty: {product[3]}, Category: {product[4]}, SKU: {product[5]}, Expiry: {product[6]}")
            y -= 15
            if y < 100:  # Prevent text from overlapping the bottom
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = 750

        # Add Sales Data
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "Sales:")
        pdf.setFont("Helvetica", 10)
        y -= 20
        for sale in sales:
            pdf.drawString(50, y, f"Sale ID: {sale[0]}, Product ID: {sale[1]}, Qty Sold: {sale[2]}, Total Price: {sale[3]}, Sale Date: {sale[4]}")
            y -= 15
            if y < 100:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = 750

        pdf.save()
        print("✅ PDF report generated successfully:", file_path)
        return file_path
    except Exception as e:
        print("❌ Error generating PDF report:", e)
        return None