import os
from flask import Flask, render_template, request, redirect, url_for
import xml.etree.ElementTree as ET
import csv

app = Flask(__name__)

def extract_data_and_generate_csv(folder_path):
    data = []
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    jpeg_files = [f for f in os.listdir(folder_path) if f.endswith('.jpeg')]
    
    for txt_file in txt_files:
        base_name = os.path.splitext(txt_file)[0]
        jpeg_file = f"{base_name}.jpeg"
        if jpeg_file in jpeg_files:
            file_path = os.path.join(folder_path, txt_file)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                try:
                    xml_root = ET.fromstring(content)
                    title = xml_root.findtext('Title')
                    tags = xml_root.findtext('Tags')
                    data.append((jpeg_file, title, tags))
                except ET.ParseError:
                    pass

    csv_file_path = os.path.join(folder_path, 'output.csv')
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Filename', 'Title', 'Keywords'])
        for row in data:
            csv_writer.writerow(row)

    return csv_file_path, data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_folder', methods=['POST'])
def select_folder():
    folder_path = request.form['folder_path']
    return redirect(url_for('show_results', folder_path=folder_path))

@app.route('/results')
def show_results():
    folder_path = request.args.get('folder_path')
    if folder_path:
        csv_file_path, data = extract_data_and_generate_csv(folder_path)
        return render_template('results.html', csv_file_path=csv_file_path, data=data)
    return 'No folder selected', 400

if __name__ == '__main__':
    app.run()