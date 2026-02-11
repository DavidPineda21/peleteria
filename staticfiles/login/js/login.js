// Función para mostrar/ocultar contraseña
function togglePassword() {
    const passwordInput = document.getElementById('contrasena');
    const toggleBtn = document.querySelector('.toggle-password');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleBtn.innerHTML = '🙈';
    } else {
        passwordInput.type = 'password';
        toggleBtn.innerHTML = '👁';
    }
}

// Efectos de entrada suave para el formulario
document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.login-form-container');
    container.style.opacity = '0';
    container.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        container.style.transition = 'all 0.6s ease';
        container.style.opacity = '1';
        container.style.transform = 'translateY(0)';
    }, 100);
    
    // Agregar efecto de hover a los iconos de redes sociales si existen
    const socialIcons = document.querySelectorAll('.social-icon');
    socialIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});
