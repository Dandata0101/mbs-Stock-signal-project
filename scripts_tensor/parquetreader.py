import os
import pandas as pd
import pyarrow.parquet as pq

def read_parquet_file(parquet_file_path):

    # Read the Parquet file into a PyArrow Table
    table = pq.read_table(parquet_file_path)
    
    # Convert the PyArrow Table to a Pandas DataFrame
    df = table.to_pandas()
    
    # Return the DataFrame and its data types
    return df