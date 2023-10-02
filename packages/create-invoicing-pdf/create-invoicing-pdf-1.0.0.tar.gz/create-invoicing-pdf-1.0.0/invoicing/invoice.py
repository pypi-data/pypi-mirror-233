import os
import pandas as pd
import glob
from pathlib import Path
from fpdf import FPDF


def generate(invoices_path, pdfs_path, image_path, product_id, product_name,
             amount_purchased, price_per_unit, total_price):
    """
    This function convert invoice Excel file in to pdf invoice file.
    :param invoices_path:
    :param pdfs_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    filepaths = glob.glob(f"invoices_path/*.xlsx")
    for filepath in filepaths:
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        filename = Path(filepath).stem
        invoice_nr = filename.split("-")[0]
        invoice_date = filename.split("-")[1]
        pdf.set_font(family="Times", style="B", size=16)
        pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", align="L")
        pdf.ln()
        pdf.cell(w=50, h=8, txt=f"Date:{invoice_date}", align="L", ln=1)
        df = pd.read_excel(filepath, sheet_name="Sheet 1")
        column = list(df.columns)
        column = [item.replace("_", " ").title() for item in column]
        pdf.set_font(family="Times", size=10, style="B")
        # pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=column[0], border=1)
        pdf.cell(w=65, h=8, txt=column[1], border=1)
        pdf.cell(w=33, h=8, txt=column[2], border=1)
        pdf.cell(w=30, h=8, txt=column[3], border=1)
        pdf.cell(w=25, h=8, txt=column[4], border=1, ln=1)
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=65, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=33, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=25, h=8, txt=str(row[total_price]), border=1, ln=1)
        total_amount = df[total_price].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=65, h=8, txt="", border=1)
        pdf.cell(w=33, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=25, h=8, txt=str(total_amount), border=1, ln=1)

        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=10, txt=f"The total price is INR {total_amount}.", ln=1)

        pdf.set_font(family="Times", size=13, style="B")
        pdf.cell(w=25, h=8, txt="Python How")
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")
