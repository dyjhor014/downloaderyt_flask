import os
from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO, emit
from yt_dlp import YoutubeDL

app = Flask(__name__)
socketio = SocketIO(app)
DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')

    def progress_hook(d):
        if d['status'] == 'downloading':
            progress = d['_percent_str']
            socketio.emit('progress', {'progress': progress}, namespace='/download')
        elif d['status'] == 'finished':
            socketio.emit('progress', {'progress': '100%'}, namespace='/download')

    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'progress_hooks': [progress_hook],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)
            return send_file(video_path, as_attachment=True)
    except Exception as e:
        return f"Error al descargar el video: {e}"

if __name__ == "__main__":
    socketio.run(app, debug=True)