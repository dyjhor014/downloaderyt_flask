from flask import Flask, render_template, request, redirect, url_for
from yt_dlp import YoutubeDL

app = Flask(__name__)

def get_video_url(youtube_url):
    """
    Función para extraer la URL directa del video utilizando yt-dlp.
    """
    ydl_opts = {
        'format': 'best',  # Formato de mejor calidad disponible
        'noplaylist': True  # No descargar listas de reproducción, solo el video
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        video_url = info_dict.get('url', None)
        return video_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        video_url = get_video_url(youtube_url)
        if video_url:
            return redirect(url_for('play_video', video_url=video_url))
        else:
            return "Error al extraer la URL del video.", 400
    return render_template('index.html')

@app.route('/play')
def play_video():
    video_url = request.args.get('video_url')
    if not video_url:
        return "No se proporcionó una URL de video.", 400
    return render_template('play.html', video_url=video_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)