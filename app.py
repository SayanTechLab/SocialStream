from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import traceback
import os
import tempfile

app = Flask(__name__)
CORS(app)

def extract_media_data(url):
    """Uses yt-dlp to extract metadata and direct video streams."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'format': 'best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                "success": True,
                "id": info.get('id'),
                "title": info.get('title', 'Social Media Cut'),
                "uploader": info.get('uploader', 'Creator'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration', 0),
                "url": info.get('url'),
            }
    except Exception as e:
        print(traceback.format_exc())
        return {
            "success": False,
            "error": "Failed to extract media. The link might be private or invalid."
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/fetch', methods=['POST'])
def fetch_metadata():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({"success": False, "error": "Please provide a valid media URL."}), 200

    result = extract_media_data(url)
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 200

@app.route('/api/download')
def download_media():
    """Securely downloads the media locally via yt-dlp and serves it to the browser."""
    url = request.args.get('url')
    ext = request.args.get('ext', 'mp4')

    if not url:
        return "Missing URL", 400

    temp_dir = tempfile.gettempdir()
    
    # Use 'best' for MP4 video and 'bestaudio' for Audio extracts
    ydl_opts = {
        'format': 'bestaudio' if ext == 'mp3' else 'best',
        'outtmpl': os.path.join(temp_dir, '%(title)s_%(id)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download the file to the OS temp directory
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Send the completed file to the user's browser download manager
            return send_file(filename, as_attachment=True)
            
    except Exception as e:
        print(traceback.format_exc())
        return f"Download Failed: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)