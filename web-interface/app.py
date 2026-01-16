import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Root directory for your SUNY Cybersecurity degree
BASE_DIR = os.path.expanduser("~/Documents/canton-cyber-degree")

@app.route('/')
def index():
    try:
        hierarchy = {}
        # Logic: Explicitly ignore non-academic folders
        ignored_folders = ['venv', 'web-interface', 'scripts', 'templates', '.git', 'archive', 'docs']
        
        for entry in os.listdir(BASE_DIR):
            path = os.path.join(BASE_DIR, entry)
            # Security Audit: Only show folders starting with 'semester-'
            if os.path.isdir(path) and entry.startswith('semester-') and entry not in ignored_folders:
                parts = entry.split('-') 
                if len(parts) >= 4:
                    semester_name = parts[2]
                    year = parts[3]
                    
                    if year not in hierarchy:
                        hierarchy[year] = {}
                    if semester_name not in hierarchy[year]:
                        hierarchy[year][semester_name] = []
                    
                    # Scan for course folders (e.g., CYBR-172)
                    courses = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and not d.startswith('.')]
                    hierarchy[year][semester_name] = sorted(courses)
        
        return render_template('index.html', hierarchy=hierarchy)
    except Exception as e:
        return f"Error loading dashboard: {str(e)}"


@app.route('/get_files/<path:full_path>')
def get_files(full_path):
    # Logic: Scans specifically inside the selected course
    target_path = os.path.join(BASE_DIR, full_path)
    files_data = []
    if os.path.exists(target_path):
        for root, dirs, files in os.walk(target_path):
            for file in files:
                if file == '.DS_Store': continue
                rel_path = os.path.relpath(os.path.join(root, file), target_path)
                files_data.append(rel_path)
    return jsonify(sorted(files_data))

@app.route('/create_folder', methods=['POST'])
def create_folder():
    data = request.json
    folder_name = data.get('folder_name')
    if ".." in folder_name or folder_name.startswith("/"):
        return jsonify({"error": "Security Audit: Invalid path"}), 400
    full_path = os.path.join(BASE_DIR, folder_name)
    os.makedirs(full_path, exist_ok=True)
    return jsonify({"message": f"Created: {folder_name}"})

@app.route('/add_file', methods=['POST'])
def add_file():
    data = request.json
    # Path logic: semester/course/subfolder/filename
    path = os.path.join(BASE_DIR, data['semester'], data['course'], data['folder'], data['filename'])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(f"# {data['filename']}\nCreated via Command Center.")
    return jsonify({"message": "File created successfully"})

@app.route('/read_file/<path:filepath>')
def read_file(filepath):
    path = os.path.join(BASE_DIR, filepath)
    with open(path, 'r') as f:
        return jsonify({"content": f.read()})

@app.route('/save_file', methods=['POST'])
def save_file():
    data = request.json
    path = os.path.join(BASE_DIR, data['filepath'])
    with open(path, 'w') as f:
        f.write(data['content'])
    return jsonify({"message": "Saved successfully"})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
