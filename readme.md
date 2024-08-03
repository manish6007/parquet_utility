# Parquet to CSV Converter

This Python script converts Parquet files to CSV format with additional features like column filtering, row filtering, and email segregation.

## Features

- Convert Parquet files to CSV
- Select specific columns to include in the output
- Apply filters to rows
- Segregate email addresses into username and domain

## Requirements

- Python 3.6+
- pandas
- pyarrow

Install the required packages using:

```
pip install pandas pyarrow
```

## Usage

```
python parquet_to_csv.py <parquet_file> <output_csv> [options]
```

### Arguments

- `parquet_file`: Path to the input Parquet file
- `output_csv`: Path to the output CSV file

### Options

- `--columns`: Columns to fetch (space-separated)
- `--filter`: Filter condition (e.g., 'last_name=="Freeman"')
- `--segregate`: Columns to segregate with new names (e.g., 'email:user,domain')

## Examples

1. Basic conversion:
   ```
   python parquet_to_csv.py input.parquet output.csv
   ```

2. Select specific columns:
   ```
   python parquet_to_csv.py input.parquet output.csv --columns first_name last_name email
   ```

3. Apply a filter:
   ```
   python parquet_to_csv.py input.parquet output.csv --filter "last_name=='Freeman'"
   ```

4. Segregate email column:
   ```
   python parquet_to_csv.py input.parquet output.csv --segregate "email:user,domain"
   ```

5. Combine all options:
   ```
   python parquet_to_csv.py input.parquet output.csv --columns first_name last_name email --filter "last_name=='Freeman'" --segregate "email:user,domain"
   ```

## Output

The script will create a CSV file with the specified columns. If email segregation is used, it will add new columns for the segregated parts while keeping the original email column intact.

For example, with email segregation, the output CSV might have these columns:
```
first_name, last_name, email, user, domain
```

Where:
- `email` is the original email address (e.g., "abc@gmail.com")
- `user` is the part of the email before the '@' (e.g., "abc")
- `domain` is the part of the email after the '@' (e.g., "gmail.com")

## Note

This script is designed for basic Parquet to CSV conversion with some additional features. For more complex transformations or large-scale data processing, consider using more robust ETL tools or frameworks.