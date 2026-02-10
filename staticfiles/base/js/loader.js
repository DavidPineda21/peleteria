/* INICIO JS LOADER */

document.addEventListener('DOMContentLoaded', function() {
    const loader = document.getElementById('loader');
    let isNavigatingBack = false;

    // Capturar todos los enlaces que no sean anclas (#) o javascript:void(0)
    document.addEventListener('click', function(e) {
        const target = e.target.closest('a');
        if (loader && target && 
            target.getAttribute('href') && 
            !target.getAttribute('href').startsWith('#') &&
            !target.href.startsWith('javascript:') &&
            !target.hasAttribute('target') &&
            !target.href.includes('indexTablero') &&
            !target.classList.contains('no-loader')) {
            loader.style.display = 'block';
        }
    });

    // Escape para cancelar
    document.addEventListener('keydown', (e) => {
        if (loader && e.key === 'Escape') {
            loader.style.display = 'none';
        }
    });

    // Para formularios
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            if (loader && this.method.toLowerCase() !== 'get') {
                loader.style.display = 'block';
            }
        });
    });

    // Ocultar loader cuando se complete la carga de la página
    window.addEventListener('pageshow', function(event) {
        if (loader) loader.style.display = 'none';
    });

    // Detectar navegación del historial (botón atrás/adelante)
    window.addEventListener('popstate', function() {
        if (loader) loader.style.display = 'none';
        isNavigatingBack = true;
    });

    // Asegurarse de que el loader esté oculto después de cargar la página
    window.addEventListener('load', function() {
        if (loader) loader.style.display = 'none';
    });
});

/* FIN JS LOADER */