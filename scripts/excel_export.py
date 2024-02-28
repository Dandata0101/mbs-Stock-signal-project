import os
import glob
import pandas as pd
from openpyxl import load_workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.utils import get_column_letter


def filter_date_range(df):
    """Filter the DataFrame to include data from Jan 1, 2020, to the present, retaining the 'Date' column."""
    start_date = pd.to_datetime('2020-01-01').date()  # Use a date for comparison
    # Ensure 'Date' column is in the correct format and filter out the epoch date if present
    if 'Date' in df.columns:
        # Convert 'Date' column to datetime and coerce errors to NaT
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
        # Create a mask to filter out rows with 'Date' at or before the Unix epoch
        mask = df['Date'] > pd.Timestamp('1970-01-01').date()
        # Apply the mask to filter the DataFrame
        df = df[mask]
        # Set 'Date' column as index
        df = df.set_index('Date')
        # Filter based on date range
        filtered_df = df[df.index >= start_date]
    else:
        raise ValueError("DataFrame must have a 'Date' column.")
    return filtered_df


def export_df_to_excel_with_chart(df=None, tickerSymbol=None, output_directory='03-output', 
                                  chart_path='static/images/chart.png'):
    print('4.1) Prepping chart and excel export')

    df=filter_date_range(df)
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
