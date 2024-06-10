from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json['rows']
    results = {}
    format = request.json['format']

    for item in data:
        parameter_name = item['parameterName']
        start_value = float(item['startValue'])
        min_value = float(item['minValue'])
        param_type = item['type']
        start = item['start']
        end = item['end']

        if param_type == 'Intraday':
            start_time = datetime.strptime(start, '%H:%M')
            end_time = datetime.strptime(end, '%H:%M')
            current_time = start_time
            while current_time <= end_time:
                value = random.uniform(min_value, start_value)
                timestamp = current_time.strftime('%H:%M')
                if timestamp not in results:
                    results[timestamp] = {}
                results[timestamp][parameter_name] = value
                current_time += timedelta(hours=1)
        else:
            start_date = datetime.strptime(start, '%Y-%m-%d')
            end_date = datetime.strptime(end, '%Y-%m-%d')
            current_date = start_date
            while current_date <= end_date:
                value = random.uniform(min_value, start_value)
                date = current_date.strftime('%Y-%m-%d')
                if date not in results:
                    results[date] = {}
                results[date][parameter_name] = value
                current_date += timedelta(days=1)

    # Convert the results dictionary to a DataFrame
    df = pd.DataFrame.from_dict(results, orient='index').sort_index()

    # Save DataFrame to a CSV file
    df.to_csv('generated_data.csv', index_label='Timestamp/Date')

    def XLSXconversion():
        csv_file = 'generated_data.csv'
        df = pd.read_csv(csv_file)

        # Save as XLSX file
        xlsx_file = 'DataInXlsx.xlsx'
        df.to_excel(xlsx_file, index=False)

    def Xmlconversion():
        # Load CSV file
        csv_file = 'generated_data.csv'
        df = pd.read_csv(csv_file)

        # Create XML structure
        root = ET.Element('root')
        for i, row in df.iterrows():
            item = ET.SubElement(root, 'item')
            for field in row.index:
                field_element = ET.SubElement(item, field)
                field_element.text = str(row[field])

        # Save as XML file
        tree = ET.ElementTree(root)
        xml_file = 'GeneratedXMLFile.xml'
        tree.write(xml_file)

    def Jsonconversion():
        csv_file = 'generated_data.csv'
        df = pd.read_csv(csv_file)
        json_file = 'GeneratedJsonFile.json'
        df.to_json(json_file, orient='records', lines=True)

    def PlainTextConversion():
        csv_file = 'generated_data.csv'
        with open(csv_file, 'r') as file:
            csv_content = file.read()
        txt_file = 'GeneratedDataTextFile.txt'
        with open(txt_file, 'w') as file:
            file.write(csv_content)

    if format == "XLSX":
        XLSXconversion()
    
    if format == "XML":
        Xmlconversion()

    if format == "Text":
        PlainTextConversion()

    if format == "JSON":
        Jsonconversion()

    return jsonify(results), 200

if __name__ == '__main__':
    app.run(debug=True)
