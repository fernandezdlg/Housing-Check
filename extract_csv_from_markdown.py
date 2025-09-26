"""
CSV Extractor from Markdown File
---------------------------------
This script extracts the life span table from the Markdown file and saves it as a CSV file.
"""

import re
import csv
import os

def extract_csv_from_markdown(markdown_file, csv_output_file):
    """
    Extract the life span table from markdown and save as CSV
    """
    
    # Read the markdown file
    with open(markdown_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find the main table section
    # Look for the table that starts with "| Category | Item/Subitem |"
    table_pattern = r'\| Category \| Item/Subitem.*?\n((?:\|.*?\|\n)+)'
    match = re.search(table_pattern, content, re.DOTALL)
    
    if not match:
        print("Could not find the main table in the markdown file")
        return False
    
    table_content = match.group(1)
    
    # Split into lines and process each row
    lines = table_content.strip().split('\n')
    
    # Header row
    headers = ['Category', 'Item/Subitem', 'Lifespan (Years)', 'Price Type', 'Price (CHF)', 'Unit', 'Notes']
    
    # Process data rows
    csv_data = []
    csv_data.append(headers)
    
    for line in lines:
        if line.strip().startswith('|') and not line.strip().startswith('|---'):
            # Remove leading and trailing |, then split by |
            row_data = [cell.strip() for cell in line.strip()[1:-1].split('|')]
            
            # Skip header separator lines
            if len(row_data) >= 6 and not all('-' in cell for cell in row_data):
                # Ensure we have exactly 7 columns (pad with empty strings if needed)
                while len(row_data) < 7:
                    row_data.append('')
                
                # Take only the first 7 columns
                row_data = row_data[:7]
                
                # Clean up the data
                cleaned_row = []
                for cell in row_data:
                    # Remove extra whitespace and clean up
                    cleaned_cell = cell.strip().replace('  ', ' ')
                    cleaned_row.append(cleaned_cell)
                
                csv_data.append(cleaned_row)
    
    # Write to CSV file
    with open(csv_output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)
    
    print(f"Successfully extracted {len(csv_data)-1} rows to {csv_output_file}")
    return True

def extract_summary_table(markdown_file, summary_csv_file):
    """
    Extract the summary table with category ranges
    """
    
    with open(markdown_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Find the summary table
    summary_pattern = r'\| Category.*?\| Average Lifespan Range \(years\).*?\n((?:\|.*?\|\n)+)'
    match = re.search(summary_pattern, content, re.DOTALL)
    
    if not match:
        print("Could not find the summary table")
        return False
    
    table_content = match.group(1)
    lines = table_content.strip().split('\n')
    
    # Header row
    headers = ['Category', 'Average Lifespan Range (years)']
    
    csv_data = []
    csv_data.append(headers)
    
    for line in lines:
        if line.strip().startswith('|') and not line.strip().startswith('|---'):
            row_data = [cell.strip() for cell in line.strip()[1:-1].split('|')]
            
            if len(row_data) >= 2 and not all('-' in cell for cell in row_data):
                # Take only the first 2 columns
                cleaned_row = [cell.strip() for cell in row_data[:2]]
                csv_data.append(cleaned_row)
    
    # Write to CSV file
    with open(summary_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)
    
    print(f"Successfully extracted summary table with {len(csv_data)-1} rows to {summary_csv_file}")
    return True

def main():
    # File paths
    markdown_file = "Condensed Summary for Life Span.md"
    detailed_csv = "life_span_detailed_table.csv"
    summary_csv = "life_span_summary_table.csv"
    
    # Check if markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Error: {markdown_file} not found!")
        return
    
    print("Extracting tables from markdown file...")
    
    # Extract detailed table
    success1 = extract_csv_from_markdown(markdown_file, detailed_csv)
    
    # Extract summary table
    success2 = extract_summary_table(markdown_file, summary_csv)
    
    if success1:
        print(f"✅ Detailed table saved to: {detailed_csv}")
    
    if success2:
        print(f"✅ Summary table saved to: {summary_csv}")
    
    if success1 or success2:
        print("\n📊 CSV files are ready to be opened in Excel or any spreadsheet application!")
    else:
        print("❌ Failed to extract tables")

if __name__ == "__main__":
    main()