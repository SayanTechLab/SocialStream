# SocialStream 🎥⚡

SocialStream is an all-in-one social media video and audio extraction web application built with Python Flask and yt-dlp, featuring a modern dark-themed web interface.

## ✨ Features

- **Multi-Platform Support**: Extract video and audio from popular platforms supported by `yt-dlp`.
- **Fast Metadata Fetching**: Instant preview of title, author, thumbnail, and duration.
- **Multiple Quality & Audio Downloads**: Download video (MP4) or audio (MP3) directly.
- **Modern Responsive UI**: Clean, sleek, cyber-dark UI styled with Tailwind CSS and Lucide icons.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/) (recommended for audio conversion and stream remuxing)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SayanTechLab/SocialStream.git
   cd SocialStream
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

```bash
python app.py
```

Open your browser and navigate to `http://localhost:5000`.

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Flask-CORS, yt-dlp
- **Frontend**: HTML5, Tailwind CSS, Lucide Icons, Vanilla JavaScript

## 📄 License

This project is licensed under the MIT License.
