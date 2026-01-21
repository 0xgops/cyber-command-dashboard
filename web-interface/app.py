import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Root directory for your SUNY Cybersecurity degree
BASE_DIR = os.path.expanduser("~/Documents/canton-cyber-degree")

@app.route('/')
def index():
    try:
        hierarchy = {}
        # Ignore non-academic system folders
        ignored_folders = ['venv', 'web-interface', 'scripts', 'templates', '.git', 'archive', 'docs']
        
        if not os.path.exists(BASE_DIR):
            return f"Error: Base directory {BASE_DIR} not found."

        for entry in os.listdir(BASE_DIR):
            path = os.path.join(BASE_DIR, entry)
            # Logic: Match 'semester-01-Spring-2026'
            if os.path.isdir(path) and entry.startswith('semester-'):
                parts = entry.split('-') 
                # parts[2] = Spring, parts[3] = 2026
                if len(parts) >= 4:
                    semester_name = parts[2]
                    year = parts[3]
                    
                    if year not in hierarchy:
                        hierarchy[year] = {}
                    if semester_name not in hierarchy[year]:
                        hierarchy[year][semester_name] = []
                    
                    # Scan for course folders inside the semester folder
                    courses = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and not d.startswith('.')]
                    hierarchy[year][semester_name] = sorted(courses)
        
        return render_template('index.html', hierarchy=hierarchy)
    except Exception as e:
        return f"Error loading dashboard: {str(e)}"



if __name__ == '__main__':
    # Force port 5001 to match your dashboard rules
    app.run(debug=True, port=5001, host='0.0.0.0')
