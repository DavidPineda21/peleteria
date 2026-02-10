document.addEventListener('DOMContentLoaded', function() {
    let count = 10;
    let countdownInterval;
    let progressInterval;
    let isActive = true;
    
    const countdownElement = document.getElementById('countdown');
    const progressElement = document.getElementById('progress');
    
    // Efecto de entrada suave para la card
    setTimeout(() => {
        document.querySelector('.error-card').style.opacity = '1';
        document.querySelector('.error-card').style.transform = 'translateY(0)';
    }, 100);
    
    // Animación del logo al hacer hover
    const logo = document.querySelector('.perseo-logo-error');
    if (logo) {
        logo.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) rotate(5deg)';
            this.style.filter = 'drop-shadow(0 0 25px rgba(251, 146, 60, 0.8))';
        });
        
        logo.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
            this.style.filter = 'drop-shadow(0 0 20px rgba(251, 146, 60, 0.6))';
        });
    }
    
    // Función para actualizar el countdown
    function updateCountdown() {
        if (!isActive) return;
        
        count--;
        countdownElement.textContent = count;
        
        if (count <= 0) {
            clearInterval(countdownInterval);
            redirectToHome();
        }
    }
    
    // Función para redireccionar
    function redirectToHome() {
        // Mostrar mensaje de redirección
        const messageSection = document.querySelector('.message-section');
        messageSection.innerHTML = `
            <h2 class="error-message">Redirigiendo...</h2>
            <p class="error-description">Por favor espera un momento.</p>
        `;
        
        // Aquí debes cambiar la URL por la que necesites
        // Para desarrollo local puedes usar:
        setTimeout(() => {
            window.location.href = window.URL_INICIO; // Usar la variable global
        }, 1000);
    }
    
    // Función para redirigir inmediatamente
    window.redirectNow = function() {
        clearInterval(countdownInterval);
        redirectToHome();
    };
    
    // Función para cancelar la redirección
    window.cancelRedirect = function() {
        if (!isActive) return;
        isActive = false;
        clearInterval(countdownInterval);
        
        // Actualizar la interfaz
        const countdownSection = document.querySelector('.countdown-section');
        countdownSection.innerHTML = `
            <div class="countdown-container">
                <span class="countdown-text">Redirección cancelada</span>
            </div>
        `;
        
        // Cambiar los botones
        const actionsSection = document.querySelector('.actions-section');
        actionsSection.innerHTML = `
            <button onclick="goToHome()" class="redirect-btn">
                Ir al inicio
            </button>
            <button onclick="location.reload()" class="cancel-btn">
                Reiniciar
            </button>
        `;
    };
    
    // Función específica para ir al inicio después de cancelar
    window.goToHome = function() {
        redirectToHome();
    };
    
    // Iniciar el countdown
    countdownInterval = setInterval(updateCountdown, 1000);
    
    // Manejar visibilidad de la página
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            // Pausar cuando la página no es visible
            if (countdownInterval) {
                clearInterval(countdownInterval);
            }
        } else {
            // Reanudar cuando la página vuelve a ser visible
            if (isActive && count > 0) {
                countdownInterval = setInterval(updateCountdown, 1000);
            }
        }
    });
    
    // Manejar teclas de acceso rápido
    document.addEventListener('keydown', function(e) {
        if (!isActive) return;
        
        switch(e.key) {
            case 'Enter':
            case ' ':
                e.preventDefault();
                redirectNow();
                break;
            case 'Escape':
                e.preventDefault();
                cancelRedirect();
                break;
        }
    });
});