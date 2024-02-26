import os
import glob
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter

def export_df_to_excel_with_chart(df=None, tickerSymbol=None, output_directory='03-output', chart_path='static/images/chart.png'):
 
    print('4.1) Prepping chart and excel export')
    current_directory = os.getcwd()
    directory_path = os.path.join(current_directory, output_directory)
    pattern = os.path.join(directory_path, '*stock*.xlsx')

    # Find all files matching the pattern and delete them
    excel_files = glob.glob(pattern)
    for file_path in excel_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f'4.2 Deleted: {file_path}')

    # Export to Excel
    excel_path = os.path.join(directory_path, f'{tickerSymbol}_stock.xlsx')
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Data', startrow=28, startcol=1)

    # Load workbook and worksheet
    wb = load_workbook(excel_path)
    ws = wb['Data']

    # Load and insert the image
    img = Image(os.path.join(current_directory, chart_path))
    ws.add_image(img, 'B2')
    ws.sheet_view.showGridLines = False

    # Autofit columns for the DataFrame
    for col in dataframe_to_rows(df, index=True, header=True):
        for idx, cell in enumerate(col, 1):
            column_letter = get_column_letter(idx + 1)
            current_width = ws.column_dimensions[column_letter].width
            content_width = len(str(cell)) * 1.2
            if current_width is None or content_width > current_width:
                ws.column_dimensions[column_letter].width = content_width

    # Save the changes to the Excel file
    wb.save(excel_path)
    wb.close()
    print('4.3) Excel export completed')
    print('')
