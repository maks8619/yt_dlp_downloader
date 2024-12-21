from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    quality = data.get('quality', 'best')  # Default to 'best'
    output_path = data.get('output_path', './downloads')  # Default to './downloads'

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    try:
        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'format': map_quality_to_format(quality),
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }] if quality != 'audio' else [],  # Skip conversion for audio
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({'status': 'success', 'message': 'Download complete'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

def map_quality_to_format(quality):
    # Map frontend quality names to yt-dlp format strings
    quality_map = {
        'Best': 'bestvideo+bestaudio/best',
        '1080p': 'bestvideo[height<=1080]+bestaudio/best',
        '720p': 'bestvideo[height<=720]+bestaudio/best',
        '480p': 'bestvideo[height<=480]+bestaudio/best',
        '360p': 'bestvideo[height<=360]+bestaudio/best',
        'Audio Only': 'bestaudio',
    }
    return quality_map.get(quality, 'bestvideo+bestaudio/best')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
