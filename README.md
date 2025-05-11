
# 🎵 YouTube Playlist Audio Downloader API

This is a Flask-based API that allows you to download the audio (as MP3) from a YouTube playlist, compress it into a ZIP file, and download it via HTTP. It's built using `yt-dlp`, `ffmpeg`, and `Flask`.

---

## 🔧 Features

- 🎧 Download best-quality audio from any public YouTube playlist
- 💾 Converts audio to `.mp3` format using FFmpeg
- 📦 Zips all audio files and serves the ZIP to the user
- 🌐 Easy-to-use POST endpoint

---

## 🚀 Getting Started

### 🔨 Installation

1. **Clone the repository**

```bash
git clone https://github.com/desmondvidic/YT_Downloader_Render.git
cd YT_Downloader_Render
```

2. **Create a virtual environment (optional but recommended)**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Make sure FFmpeg is installed**

Install FFmpeg (required for MP3 conversion):

```bash
sudo apt install ffmpeg
```

---

### ▶️ Running the App Locally

```bash
python app.py
```

The API will run on `http://localhost:8080`.

---

## 🧪 API Usage

### Endpoint

```
POST /download_playlist
```

### Request Body (JSON)

```json
{
  "playlist_url": "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
}
```

### Response

Returns a `.zip` file containing all audio tracks from the playlist as MP3s.

---

## 🌍 Deploying to Render

1. Push this repo to GitHub.
2. Go to [https://dashboard.render.com](https://dashboard.render.com)
3. Create a new **Web Service**:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Port: `8080`
4. Hit **Deploy**. Done!

---

## ⚠️ Notes

- Private videos will be skipped unless authenticated via cookies.
- FFmpeg is required for audio conversion.
- Large playlists may take time to download and convert.

---

## 📜 License

MIT License
