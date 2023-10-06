import os
import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path, pdf_path, image_path, product_id, product_name,
             amount_purchase, price_per_unit, total_price):
    """
    This function converts xls file into pdf invoices.
    :param invoices_path:
    :param pdf_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchase:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    filepaths = glob.glob(f'{invoices_path}/*.xlsx')

    for filepath in filepaths:
        # place inside the loop because we wanted to make separate files
        pdf = FPDF(orientation='P', unit='mm', format='a4')
        pdf.add_page()

        # getting the filename and invoice number
        filename = Path(filepath).stem
        invoice_nr = filename.split('-')[0]
        date = filename.split('-')[1]
        # invoice_nr, date = filename.split('-')

        # write the content of the pdf
        pdf.set_font(family='Times', size=16, style='B')
        pdf.cell(w=50, h=8, txt=f"Invoice No. {invoice_nr}", ln=1)

        pdf.set_font(family='Times', size=14, style='B')
        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)

        # extract data from excel and declare pdf setup
        df = pd.read_excel(filepath, sheet_name='Sheet 1')

        # add a header
        headers = df.columns  # get the columns name
        pdf.set_font(family='Times', size=10, style='B')
        pdf.set_text_color(80, 80, 80)
        headers = [i.replace('_', ' ').title() for i in headers]  # format the columns name
        pdf.cell(w=30, h=8, txt=headers[0], border=1)
        pdf.cell(w=70, h=8, txt=headers[1], border=1)
        pdf.cell(w=30, h=8, txt=headers[2], border=1)
        pdf.cell(w=30, h=8, txt=headers[3], border=1)
        pdf.cell(w=30, h=8, txt=headers[4], border=1, ln=1)

        # add rows to the table
        for index, row in df.iterrows():
            pdf.set_font(family='Times', size=10)
            pdf.set_text_color(80,80,80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]), border=1)
            pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[amount_purchase]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]), border=1, ln=1)

        # add total row
        pdf.set_font(family='Times', size=10, style='B')
        pdf.set_text_color(80, 80, 80)
        total = df[total_price].sum()  # adding all the total price
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=70, h=8, txt="Total", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(total), border=1, ln=1)

        # add total sum sentence
        pdf.set_font(family='Times', size=12, style='B')
        pdf.cell(w=30, h=8, txt=f"The total price is {total}", ln=1)

        # add company name and logo
        pdf.set_font(family='Times', size=12, style='B')
        pdf.cell(w=30, h=8, txt="PythonHow")
        pdf.image(image_path, w=10)

        if not os.path.exists(pdf_path):
            os.makedirs(pdf_path)
        # the output is put inside the loop bcs we wanted to make a pdf file each time
        pdf.output(f'{pdf_path}/{filename}.pdf')
