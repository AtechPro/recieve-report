import pandas as pd
import json
import sys
from pathlib import Path

def extract_excel_to_json(excel_file_path, output_file_path=None):
    """
    Extract data from the first worksheet of an Excel file and convert to JSON.
    All values are converted to strings as requested.
    
    Args:
        excel_file_path (str): Path to the Excel file
        output_file_path (str, optional): Path for the output JSON file. 
                                        If None, prints to console
    """
    try:
        # Read the first worksheet of the Excel file
        print(f"Reading Excel file: {excel_file_path}")
        df = pd.read_excel(excel_file_path, sheet_name=0)
        
        # Convert all values to strings
        df = df.astype(str)
        
        # Convert DataFrame to dictionary with records format
        # This creates a list of dictionaries where each row becomes a dictionary
        data = df.to_dict('records')
        
        # Create the final JSON structure
        json_data = {
            "worksheet_name": "Page 1",
            "total_rows": len(data),
            "total_columns": len(df.columns),
            "columns": df.columns.tolist(),
            "data": data
        }
        
        if output_file_path:
            # Save to JSON file
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            print(f"Data extracted and saved to: {output_file_path}")
        else:
            # Print to console
            print(json.dumps(json_data, indent=2, ensure_ascii=False))
            
        return json_data
        
    except FileNotFoundError:
        print(f"Error: File '{excel_file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error reading Excel file: {str(e)}")
        return None

def main():
    """Main function to run the extraction"""
    # Check if a file path was provided as command line argument
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
    else:
        excel_file = "summary_project.xlsx"
    
    # Check if the Excel file exists
    if not Path(excel_file).exists():
        print(f"Error: {excel_file} not found.")
        if len(sys.argv) == 1:
            print("Available files:")
            for file in Path('.').glob('*'):
                print(f"  - {file.name}")
        return
    
    # Extract data and save to JSON file
    output_file = "extracted_data.json"
    result = extract_excel_to_json(excel_file, output_file)
    
    if result:
        print(f"\nExtraction completed successfully!")
        print(f"Total rows extracted: {result['total_rows']}")
        print(f"Total columns: {result['total_columns']}")
        print(f"Columns: {', '.join(result['columns'])}")

if __name__ == "__main__":
    main() 