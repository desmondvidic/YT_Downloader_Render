import os
import yt_dlp
import zipfile
from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

# Create a directory to store the downloaded files temporarily
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/download_playlist', methods=['POST'])
def download_playlist():
    # Get the playlist URL from the request body
    playlist_url = request.json.get('playlist_url')
    
    if not playlist_url:
        return jsonify({'error': 'Playlist URL is required'}), 400
    
    # Download videos from the playlist using yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best audio quality
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Convert to mp3
            'preferredquality': '192',  # Set audio quality
        }],
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),  # Save with video title
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])  # Download the playlist
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Create a ZIP file with the downloaded audio files
    zip_filename = 'playlist.zip'
    zip_filepath = os.path.join(DOWNLOAD_DIR, zip_filename)

    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(DOWNLOAD_DIR):
            for filename in filenames:
                if filename.endswith(".mp3"):  # Add only .mp3 files
                    file_path = os.path.join(foldername, filename)
                    zipf.write(file_path, os.path.relpath(file_path, DOWNLOAD_DIR))

    # Return the ZIP file to the user
    return send_file(zip_filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
