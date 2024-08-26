document.addEventListener('DOMContentLoaded', function() {
    const socket = io.connect('http://' + document.domain + ':' + location.port + '/');

    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');

    // Escuchar el evento de progreso (opcional, en caso de que haya alguna preparación antes de la redirección)
    socket.on('progress', function(data) {
        console.log(`Progreso recibido: ${data.progress}`);
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
            if (response.redirected) {
                // Si hay una redirección, navegar automáticamente al enlace de descarga
                window.location.href = response.url;
            } else {
                alert('Error al obtener el enlace de descarga.');
            }
        }).catch(error => {
            console.error('Error durante la solicitud:', error);
            alert('Ocurrió un error durante la solicitud.');
        });
    });
});
