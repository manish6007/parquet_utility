import argparse
import pandas as pd
import pyarrow.parquet as pq

def segregate_column(df, column_name, new_column_names, delimiter='@'):
    # Split the column
    split_df = df[column_name].str.split(delimiter, expand=True)
    
    # Assign new column names
    for i, new_name in enumerate(new_column_names):
        if i < len(split_df.columns):
            df.loc[:, new_name] = split_df[i]
    
    return df

def parquet_to_csv(parquet_file, output_csv, columns, filter_condition, segregate_columns):
    # Read the Parquet file
    table = pq.read_table(parquet_file, columns=columns)
    df = table.to_pandas()

    # Apply the filter condition if provided
    if filter_condition:
        df = df.query(filter_condition)

    # Create a copy of the filtered DataFrame to avoid SettingWithCopyWarning
    df = df.copy()

    # Segregate specified columns
    for col, new_names in segregate_columns.items():
        df = segregate_column(df, col, new_names, delimiter='@')

    # Write to CSV
    df.to_csv(output_csv, index=False)
    print(f"CSV file created: {output_csv}")

def parse_segregate_arg(arg):
    parts = arg.split(':')
    column = parts[0]
    new_names = parts[1].split(',') if len(parts) > 1 else []
    return column, new_names

def main():
    parser = argparse.ArgumentParser(description="Convert Parquet file to CSV with specified columns, filter, and custom field segregation.")
    parser.add_argument("parquet_file", help="Path to the input Parquet file")
    parser.add_argument("output_csv", help="Path to the output CSV file")
    parser.add_argument("--columns", nargs='+', help="Columns to fetch (space-separated)")
    parser.add_argument("--filter", help="Filter condition (e.g., 'last_name==\"Freeman\"')")
    parser.add_argument("--segregate", nargs='+', help="Columns to segregate with new names (e.g., 'email:user,domain')")

    args = parser.parse_args()

    segregate_columns = {}
    if args.segregate:
        for seg in args.segregate:
            col, new_names = parse_segregate_arg(seg)
            segregate_columns[col] = new_names

    parquet_to_csv(args.parquet_file, args.output_csv, args.columns, args.filter, segregate_columns)

if __name__ == "__main__":
    main()