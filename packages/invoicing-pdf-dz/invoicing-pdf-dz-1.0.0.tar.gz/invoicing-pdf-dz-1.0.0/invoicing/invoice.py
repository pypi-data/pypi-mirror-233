import os

import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path, pdf_path, image_path, product_id, product_name,
             amount_purchased, price_per_unit, total_price):
    """
    This function converts invoice Excel files into PDF invoices.
    :param invoices_path:
    :param pdf_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """

    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:

        # creating the pdf object
        pdf = FPDF(orientation="P", unit="mm", format="A4")

        # adding a page
        pdf.add_page()

        # getting the file name
        filename = Path(filepath).stem[:5]
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt="Invoice nr.{}".format(filename), ln=1)

        # getting the date
        current_date = Path(filepath).stem[6:]
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt="Date: {}".format(current_date), ln=1)

        # reading the excel file
        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        # adding headers
        columns = list(df.columns)
        columns = [column.replace("_", " ").title() for column in columns]
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=str(columns[0]), border=1)
        pdf.cell(w=65, h=8, txt=str(columns[1]), border=1)
        pdf.cell(w=35, h=8, txt=str(columns[2]), border=1)
        pdf.cell(w=30, h=8, txt=str(columns[3]), border=1)
        pdf.cell(w=30, h=8, txt=str(columns[4]), border=1, ln=1)

        # adding rows
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=65, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=35, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        # add cell with total sum
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=65, h=8, txt="", border=1)
        pdf.cell(w=35, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(df[total_price].sum()), border=1, ln=1)

        # add total sum sentence
        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=8, txt="The total price is {}".format(df[total_price].sum()), ln=1)

        # add company name and logo
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=25, h=8, txt="PythonHow")
        pdf.image(image_path, w=10)

        # Create the pdf path and folder if it does not exist
        if not os.path.exists(pdf_path):
            os.mkdir(pdf_path)

        # outputting the pdf
        pdf.output(f"{pdf_path}/{filename}.pdf")
