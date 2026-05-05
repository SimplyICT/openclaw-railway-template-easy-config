import os
import subprocess
from flask import Flask, request, jsonify, send_from_directory

from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app) # Enable CORS for all routes

# Serve static files
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    try:
        data = request.json
        site_name = data.get('site_name', 'Benowa ELC')
        # Use simple date string for the report search
        import datetime
        target_date = data.get('date', datetime.datetime.now().strftime("%Y-%m-%d"))
        
        print(f"Starting Magic Report Chain for {site_name} on {target_date}")

        # 1. Run Reporter to get .md (using current workspace python)
        subprocess.run(['python3', '/data/workspace/reporter.py', site_name, target_date], check=True)
        
        md_file = f"report_{site_name.replace(' ', '_')}_{target_date}.md"
        docx_file = f"report_{site_name.replace(' ', '_')}_{target_date}.docx"

        # 2. Convert MD to DOCX
        if os.path.exists('/data/workspace/md_to_docx.py'):
            subprocess.run(['python3', '/data/workspace/md_to_docx.py', md_file], check=True)

        # 3. Upload to SharePoint
        if os.path.exists('/data/workspace/sp_upload.py'):
            # Note: sp_upload.py currently has hardcoded filename. 
            # We might want to edit it to accept the filename as arg in the future.
            subprocess.run(['python3', '/data/workspace/sp_upload.py'], check=True)
            return jsonify({"status": "success", "message": f"Report generated and uploaded!"})
        else:
            return jsonify({"status": "error", "message": "sp_upload.py missing."})

    except subprocess.CalledProcessError as e:
        return jsonify({"status": "error", "message": f"Process failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
