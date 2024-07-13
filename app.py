from flask import Flask, request, jsonify
import os
import csv

app = Flask(__name__)

# Directory where files will be stored
STORAGE_DIR = '/sid_PV_dir'

# Ensure the storage directory exists
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

@app.route('/')
def home():
    return "Welcome to container 2"

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    file_name = data.get('file')
    product = data.get('product')

    # Check if file name is provided
    if not file_name or not product:
        return jsonify({"file": file_name, "error": "Invalid JSON input."}), 400

    file_path = os.path.join(STORAGE_DIR, file_name)

    # Check if file exists
    if not os.path.exists(file_path):
        return jsonify({"file": file_name, "error": "File not found."}), 404

    try:
        # Calculate the sum at the start of the request processing
        total = 0
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            # Trim whitespaces from headers
            reader.fieldnames = [field.strip() for field in reader.fieldnames]
            print(f"CSV Headers: {reader.fieldnames}")  # Debugging statement
            # Check for required headers in CSV file
            if 'product' not in reader.fieldnames or 'amount' not in reader.fieldnames:
                return jsonify({"file": file_name, "error": "Input file not in CSV format."}), 400
            for row in reader:
                if row['product'] == product:
                    total += int(row['amount'])
        print(f"File: {file_name}, Sum: {total}")  # Output the file name and sum
        # Return the sum along with the file name
        return jsonify({"file": file_name, "sum": total}), 200
    except Exception as e:
        print(f"Exception: {e}")  # Debugging statement
        return jsonify({"file": file_name, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
