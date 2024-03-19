import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def csv_to_parquet_single_file(csv_file_path, output_file_path, chunksize=100000, sample_rows=None, drop_columns=None):
    chunks = []  # Store chunks in a list

    # Read the CSV in chunks
    for chunk in pd.read_csv(csv_file_path, chunksize=chunksize):
        # If drop_columns is specified, drop the columns from the chunk
        if drop_columns is not None:
            chunk = chunk.drop(columns=drop_columns, errors='ignore')
        chunks.append(chunk)

    # Concatenate all chunks into a single DataFrame
    df = pd.concat(chunks, ignore_index=True)

    # Print the row count before sampling
    print(f"Row count before sampling: {df.shape[0]}")

    # If sample_rows is specified, randomly sample the DataFrame
    if sample_rows is not None and sample_rows < len(df):
        df = df.sample(n=sample_rows)

    # Print the row count after sampling
    print(f"Row count after sampling: {df.shape[0]}")

    # Convert the DataFrame to a PyArrow Table
    table = pa.Table.from_pandas(df)

    # Write the table to a single Parquet file
    pq.write_table(table, output_file_path)

    print(f"Conversion completed. The data has been saved to '{output_file_path}'.")
