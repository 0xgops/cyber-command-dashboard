import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Root directory configuration
BASE_DIR = os.path.expanduser("~/Documents/canton-cyber-degree")

def get_hierarchy():
    hierarchy = {}
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    for entry in os.listdir(BASE_DIR):
        path = os.path.join(BASE_DIR, entry)
        if os.path.isdir(path) and entry.startswith('semester-'):
            parts = entry.split('-') 
            if len(parts) >= 4:
                semester_name = parts[2]
                year = parts[3]
                if year not in hierarchy:
                    hierarchy[year] = {}
                if semester_name not in hierarchy[year]:
                    hierarchy[year][semester_name] = []
                courses = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and not d.startswith('.')]
                hierarchy[year][semester_name] = sorted(courses)
    return hierarchy

@app.route('/')
def index():
    return render_template('index.html', hierarchy=get_hierarchy())

@app.route('/create_file', methods=['POST'])
def create_file():
    data = request.json
    filepath = data.get('filepath')
    # Security Audit: Prevent directory traversal
    if ".." in filepath or filepath.startswith("/"):
        return jsonify({"error": "Unauthorized"}), 403
    
    path = os.path.join(BASE_DIR, filepath)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, 'w') as f:
                f.write("") # Create empty file
            return jsonify({"status": "success", "message": f"Created {filepath}"})
        else:
            return jsonify({"status": "error", "message": "File already exists"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/get_files/<path:full_path>')
def get_files(full_path):
    if ".." in full_path or full_path.startswith("/"):
        return jsonify({"error": "Invalid path"}), 400
    target_path = os.path.join(BASE_DIR, full_path)
    files_data = []
    if os.path.exists(target_path):
        for root, dirs, files in os.walk(target_path):
            for file in files:
                if file.startswith('.') or file == 'venv' or file == '__pycache__':
                    continue
                rel_path = os.path.relpath(os.path.join(root, file), target_path)
                files_data.append(rel_path)
        return jsonify(sorted(files_data))
    return jsonify({"error": "Path not found"}), 404

@app.route('/read_file/<path:filepath>')
def read_file(filepath):
    if ".." in filepath: return jsonify({"error": "Unauthorized"}), 403
    path = os.path.join(BASE_DIR, filepath)
    try:
        with open(path, 'r') as f:
            return jsonify({"content": f.read()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save_file', methods=['POST'])
def save_file():
    data = request.json
    if ".." in data['filepath']: return jsonify({"error": "Unauthorized"}), 403
    path = os.path.join(BASE_DIR, data['filepath'])
    try:
        with open(path, 'w') as f:
            f.write(data['content'])
        return jsonify({"message": "Saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
