import pandas as pd
import json
import os

def excel_to_json(excel_file, output_file):
    # Load the Excel file
    xls = pd.ExcelFile(excel_file)
    
    json_data = []
    route_id = 1  # Auto-increment ID for Route
    
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=2)  # Headers in row 3 (0-based index)
        
        # Extract route name from cell I1
        route_no = sheet_name.strip().upper()        
        # Iterate through each row starting from index 3 (A4 in Excel -> index 3 in Pandas)
        for index, row in df.iterrows():
            try:
                order_sequence = int(row[0])  # Column A (order_sequence)
                stop_name = str(row[1]).strip()  # Column B (stop_name)
                stop_latitude = float(row[2])  # Column C (latitude)
                stop_longitude = float(row[3])  # Column D (longitude)
                fare_stage = str(row[4]).strip().lower() in ['true', '1', 'yes']  # Column E (fare_stage)
            except Exception as e:
                print(f"Skipping row {index} due to error: {e}")
                continue  # Skip rows with missing/invalid data

            json_data.append({
                "model": "bus_route.route",  # Change "app_name" to your Django app name
                "pk": route_id,
                "fields": {
                    "route_no": route_no,
                    "order_sequence": order_sequence,
                    "stop_name": stop_name,
                    "stop_latitude": stop_latitude,
                    "stop_longitude": stop_longitude,
                    "fare_stage": fare_stage
                }
            })
            route_id += 1
    
    # Save JSON to file
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)
    
    print(f"JSON file saved to {output_file}")

# Example usage
excel_file = "route_data.xlsx"  # Replace with the actual Excel file name
output_file = "routes.json"
excel_to_json(excel_file, output_file)