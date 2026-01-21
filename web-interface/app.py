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
        # Logic: Filter for 'semester-01-Spring-2026' style folders
        if os.path.isdir(path) and entry.startswith('semester-'):
            parts = entry.split('-') 
            if len(parts) >= 4:
                semester_name = parts[2]
                year = parts[3]
                
                if year not in hierarchy:
                    hierarchy[year] = {}
                if semester_name not in hierarchy[year]:
                    hierarchy[year][semester_name] = []
                
                # List course folders inside
                courses = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and not d.startswith('.')]
                hierarchy[year][semester_name] = sorted(courses)
    return hierarchy

@app.route('/')
def index():
    return render_template('index.html', hierarchy=get_hierarchy())

@app.route('/create_academic_tier', methods=['POST'])
def create_academic_tier():
    data = request.json
    year = data.get('year')
    season = data.get('season')
    course = data.get('course') # Optional: if provided, creates a course folder
    
    # Security Audit: Prevent path traversal by stripping slashes
    safe_year = str(year).replace('/', '')
    safe_season = str(season).replace('/', '')
    
    # Folder structure: semester-01-Spring-2026
    sem_folder = f"semester-01-{safe_season}-{safe_year}"
    target_path = os.path.join(BASE_DIR, sem_folder)
    
    try:
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        
        if course:
            course_path = os.path.join(target_path, course.replace('/', ''))
            os.makedirs(course_path, exist_ok=True)
            # Pre-populate standard folders per project rules
            for sub in ['Discussion', 'assignments', 'notes', 'labs']:
                os.makedirs(os.path.join(course_path, sub), exist_ok=True)
        
        return jsonify({"status": "success", "message": f"Updated {sem_folder}"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Existing utility routes (Add your get_files, read_file, save_file logic here)

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
