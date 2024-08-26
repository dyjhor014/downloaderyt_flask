document.addEventListener('DOMContentLoaded', function() {
    const socket = io('/download');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');

    // Escuchar el evento de progreso
    socket.on('progress', function(data) {
        progressBar.style.width = data.progress;
        progressText.textContent = `Progreso: ${data.progress}`;
    });

    document.getElementById('downloadForm').addEventListener('submit', function(event) {
        event.preventDefault();
        progressBar.style.width = '0%';
        progressText.textContent = 'Progreso: 0%';
        const formData = new FormData(event.target);
        fetch('/download', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                console.log('Descarga iniciada');
            } else {
                alert('Error al descargar el video.');
            }
        });
    });
});