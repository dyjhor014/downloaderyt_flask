document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('downloadForm');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        // Reiniciar barra de progreso y texto
        progressBar.style.width = '0%';
        progressText.textContent = 'Progreso: 0%';

        const formData = new FormData(form);
        fetch('/download', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                checkProgress();  // Inicia la verificación de progreso
            } else {
                alert('Error al descargar el video.');
            }
        });
    });

    function checkProgress() {
        fetch('/progress')
            .then(response => response.json())
            .then(data => {
                if (data.status === 'downloading') {
                    progressBar.style.width = data.progress;
                    progressText.textContent = `Progreso: ${data.progress}`;
                    setTimeout(checkProgress, 1000);  // Repetir después de 1 segundo
                } else if (data.status === 'finished') {
                    progressBar.style.width = '100%';
                    progressText.textContent = 'Descarga completada!';
                }
            });
    }
});