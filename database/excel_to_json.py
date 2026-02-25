import pandas as pd
import json
import os

def excel_to_json(excel_file, output_file=None):
    """
    Convert Excel file to JSON format.
    
    Args:
        excel_file (str): Path to the Excel file
        output_file (str, optional): Path to the output JSON file. 
                                   If not provided, will use the same name as input with .json extension
    """
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)
        
        # Convert DataFrame to list of dictionaries (one per row)
        data = df.to_dict(orient='records')
        
        # Determine output file name if not provided
        if output_file is None:
            output_file = os.path.splitext(excel_file)[0] + '.json'
        
        # Write to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully converted {excel_file} to {output_file}")
        return True
        
    except Exception as e:
        print(f"Error converting file: {str(e)}")
        return False

if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all Excel files in the same directory
    excel_files = [f for f in os.listdir(script_dir) 
                  if f.endswith(('.xlsx', '.xls'))]
    
    if not excel_files:
        print("No Excel files found in the current directory.")
    else:
        for excel_file in excel_files:
            excel_path = os.path.join(script_dir, excel_file)
            excel_to_json(excel_path)
