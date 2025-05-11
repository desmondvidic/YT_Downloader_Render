import os
import yt_dlp
import zipfile
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS  # 👈 Import CORS

app = Flask(__name__)
CORS(app)

# Create a directory to store the downloaded files temporarily
DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.route('/download_playlist', methods=['POST'])
def download_playlist():
    playlist_url = request.json.get('playlist_url')
    
    if not playlist_url:
        return jsonify({'error': 'Playlist URL is required'}), 400
    
    # First, extract playlist info to get the title
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info_dict = ydl.extract_info(playlist_url, download=False)
            playlist_title = info_dict.get('title', 'playlist')
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve playlist info: {str(e)}'}), 500

    # Sanitize the title to use as filename
    safe_title = "".join(c if c.isalnum() or c in " ._-" else "_" for c in playlist_title)
    zip_filename = f'{safe_title}.zip'
    zip_filepath = os.path.join(DOWNLOAD_DIR, zip_filename)

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

    # Create the ZIP file with downloaded audio files
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for foldername, subfolders, filenames in os.walk(DOWNLOAD_DIR):
            for filename in filenames:
                if filename.endswith(".mp3"):
                    file_path = os.path.join(foldername, filename)
                    zipf.write(file_path, os.path.relpath(file_path, DOWNLOAD_DIR))

    return send_file(zip_filepath, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
