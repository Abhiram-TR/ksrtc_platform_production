import pandas as pd
import json
import os

def excel_to_json_folder(input_folder, output_file):
    json_data = []
    route_id = 1  # Auto-increment ID for Route
    
    # Iterate through all Excel files in the folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            excel_file = os.path.join(input_folder, filename)
            print(f"Processing file: {filename}")
            
            try:
                xls = pd.ExcelFile(excel_file)
                
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name, header=2)  # Headers in row 3 (0-based index)
                    
                    route_no = sheet_name.strip().upper()
                    
                    for index, row in df.iterrows():
                        try:
                            order_sequence = int(row[0])  # Column A
                            stop_name = str(row[1]).strip()  # Column B
                            stop_latitude = float(row[2])  # Column C
                            stop_longitude = float(row[3])  # Column D
                            fare_stage = str(row[4]).strip().lower() in ['true', '1', 'yes']  # Column E
                        except Exception as e:
                            print(f"Skipping row {index} in {filename} ({sheet_name}) due to error: {e}")
                            continue

                        json_data.append({
                            "model": "bus_route.route",  # Adjust for your Django app
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

            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    # Save JSON to file
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)
    
    print(f"JSON file saved to {output_file}")

# Example usage
input_folder = "route_folder/"  # Replace with your actual folder path
output_file = "routes.json"
excel_to_json_folder(input_folder, output_file)
