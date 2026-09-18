from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import traceback
import os
import tempfile

app = Flask(__name__)
CORS(app)


# ============================================================
# ERROR HANDLER
# ============================================================

def get_friendly_error(error):
    """
    Converts yt-dlp errors into user-friendly messages.
    """

    error_text = str(error).lower()

    # YouTube bot / authentication protection
    if (
        "sign in to confirm you're not a bot" in error_text
        or "sign in to confirm you’re not a bot" in error_text
        or "use --cookies-from-browser" in error_text
    ):
        return (
            "YouTube is currently blocking automated extraction for this request. "
            "Please try another public URL later."
        )

    # Private / unavailable content
    if (
        "private video" in error_text
        or "video unavailable" in error_text
        or "this video is private" in error_text
    ):
        return (
            "This media is private or unavailable. "
            "Please use a public media URL that you have permission to download."
        )

    # Invalid URL
    if (
        "unsupported url" in error_text
        or "invalid url" in error_text
    ):
        return "The URL is invalid or this platform is not supported."

    # Login required
    if (
        "login required" in error_text
        or "authentication required" in error_text
        or "sign in" in error_text
    ):
        return (
            "This media requires authentication. "
            "Please try a publicly accessible URL."
        )

    # Requested format problem
    if (
        "requested format is not available" in error_text
        or "no video formats found" in error_text
        or "no formats found" in error_text
    ):
        return (
            "No downloadable media format is currently available for this URL."
        )

    # Generic error
    return "Failed to extract media. The link might be private, invalid, or temporarily unavailable."


# ============================================================
# EXTRACT MEDIA INFORMATION
# ============================================================

def extract_media_data(url):
    """
    Uses yt-dlp to extract metadata and direct media information.
    """

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "format": "best",
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                url,
                download=False
            )

            return {
                "success": True,
                "id": info.get("id"),
                "title": info.get(
                    "title",
                    "Social Media Cut"
                ),
                "uploader": info.get(
                    "uploader",
                    "Creator"
                ),
                "thumbnail": info.get(
                    "thumbnail"
                ),
                "duration": info.get(
                    "duration",
                    0
                ),
                "url": info.get(
                    "url"
                ),
            }

    except Exception as e:

        # Keep the detailed error in Render logs
        print("========================================")
        print("MEDIA EXTRACTION ERROR")
        print("========================================")
        print(traceback.format_exc())
        print("========================================")

        # Send only a safe, friendly message to the website
        return {
            "success": False,
            "error": get_friendly_error(e)
        }


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# FETCH METADATA API
# ============================================================

@app.route("/api/fetch", methods=["POST"])
def fetch_metadata():

    try:

        data = request.get_json(silent=True) or {}

        url = data.get("url", "").strip()

        if not url:
            return jsonify({
                "success": False,
                "error": "Please provide a valid media URL."
            }), 200

        result = extract_media_data(url)

        return jsonify(result), 200

    except Exception as e:

        print("FETCH API ERROR:")
        print(traceback.format_exc())

        return jsonify({
            "success": False,
            "error": "An unexpected server error occurred. Please try again."
        }), 500


# ============================================================
# DOWNLOAD MEDIA API
# ============================================================

@app.route("/api/download")
def download_media():
    """
    Downloads media using yt-dlp and sends the file
    to the user's browser.
    """

    url = request.args.get("url", "").strip()
    ext = request.args.get("ext", "mp4").lower()

    if not url:
        return jsonify({
            "success": False,
            "error": "Missing media URL."
        }), 400

    # Only allow the formats currently supported by the UI
    if ext not in ["mp4", "mp3"]:
        ext = "mp4"

    temp_dir = tempfile.gettempdir()

    # MP4 = best video
    # MP3 = best audio
    ydl_opts = {
        "format": "bestaudio" if ext == "mp3" else "best",

        "outtmpl": os.path.join(
            temp_dir,
            "%(title)s_%(id)s.%(ext)s"
        ),

        "quiet": True,
        "no_warnings": True,
    }

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            # Download the media
            info = ydl.extract_info(
                url,
                download=True
            )

            # Determine downloaded filename
            filename = ydl.prepare_filename(info)

            # Make sure file exists
            if not os.path.exists(filename):
                return jsonify({
                    "success": False,
                    "error": "The media file could not be created."
                }), 500

            # Send file to browser
            return send_file(
                filename,
                as_attachment=True
            )

    except Exception as e:

        # Detailed error remains visible in Render logs
        print("========================================")
        print("MEDIA DOWNLOAD ERROR")
        print("========================================")
        print(traceback.format_exc())
        print("========================================")

        friendly_error = get_friendly_error(e)

        return jsonify({
            "success": False,
            "error": friendly_error
        }), 500


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )