import os
import yt_dlp
import zipfile
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Directory setup
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/download_playlist', methods=['POST'])
def download_playlist():
    playlist_url = request.json.get('playlist_url')
    if not playlist_url:
        return jsonify({'error': 'Playlist URL is required'}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    zip_filename = 'playlist.zip'
    zip_filepath = os.path.join(DOWNLOAD_DIR, zip_filename)

    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename in os.listdir(DOWNLOAD_DIR):
            if filename.endswith('.mp3'):
                file_path = os.path.join(DOWNLOAD_DIR, filename)
                zipf.write(file_path, filename)

    return send_file(zip_filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
