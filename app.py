import os
from flask import Flask, render_template, request, send_file, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
progress = {'status': '', 'progress': '0%'}  # Reiniciar progreso

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    global progress
    progress = {'status': '', 'progress': '0%'}  # Reiniciar progreso

    url = request.form.get('url')
    
    def progress_hook(d):
        if d['status'] == 'downloading':
            progress['status'] = 'downloading'
            progress['progress'] = d['_percent_str']
        elif d['status'] == 'finished':
            progress['status'] = 'finished'
            progress['progress'] = '100%'

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

@app.route('/progress', methods=['GET'])
def get_progress():
    return jsonify(progress)

if __name__ == "__main__":
    app.run(debug=True)
