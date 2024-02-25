
import os
import sys
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter
from scripts.buysellfx import dfstock

print('4.1) prepping chart and excel export')
# Paths and directory-----------------------------------------------------
current_directory = os.getcwd()

#export to excel----------------------------------------------------------
# Write DataFrame to Excel
excel_path = current_directory+'/03-output/stock.xlsx'
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    dfstock.to_excel(writer, sheet_name='Data', startrow=28, startcol=1)

from openpyxl import load_workbook
from openpyxl.drawing.image import Image

wb = load_workbook(excel_path)
ws = wb['Data']

# Load and insert the image
img = Image(current_directory+'/02-charts/chart.png')

# The cell where you want to insert the image, e.g., A1
ws.add_image(img, 'B2')
ws.sheet_view.showGridLines = False

# Autofit columns for the DataFrame
for col in dataframe_to_rows(dfstock, index=True, header=True):
    for idx, cell in enumerate(col, 1):  
        column_letter = get_column_letter(idx + 1) 
        current_width = ws.column_dimensions[column_letter].width
        content_width = len(str(cell)) * 1.2
        if current_width is None or content_width > current_width:
            ws.column_dimensions[column_letter].width = content_width

# Save the changes to the Excel file
wb.save(excel_path)
wb.close()
print('4.2) excel export completed')