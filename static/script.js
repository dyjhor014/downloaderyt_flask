var videoIndex = 0;
var videoPlayer = document.getElementById('videoPlayer');

function playNextVideo() {
    if (videoIndex < playlist.length) {
        videoPlayer.src = playlist[videoIndex];
        videoPlayer.play();
        videoIndex++;
    } else {
        // Si la lista de reproducción está vacía, hacer una redirección al backend para eliminar el primer video y recargar
        window.location.href = "/next_video";
    }
}

// Reproducir el siguiente video cuando el actual termine
videoPlayer.addEventListener('ended', playNextVideo);

// Comenzar la reproducción
if (playlist.length > 0) {
    playNextVideo();
}