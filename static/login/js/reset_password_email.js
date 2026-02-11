document.addEventListener('DOMContentLoaded', function() {
    const resetForm = document.getElementById('reset-form');
    const emailInput = document.getElementById('email');
    const resetBtn = document.querySelector('.reset-btn');
    
    // Efecto de entrada suave
    setTimeout(() => {
        document.querySelector('.reset-card').style.opacity = '1';
        document.querySelector('.reset-card').style.transform = 'translateY(0)';
    }, 100);
    
    // Animación del logo al hacer hover
    const logo = document.querySelector('.perseo-logo-reset');
    logo.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1) rotate(5deg)';
        this.style.filter = 'drop-shadow(0 0 25px rgba(251, 146, 60, 0.8))';
    });
    
    logo.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1) rotate(0deg)';
        this.style.filter = 'drop-shadow(0 0 20px rgba(251, 146, 60, 0.6))';
    });
    
    // Validación en tiempo real del email
    emailInput.addEventListener('input', function() {
        const email = this.value.trim();
        const isValid = validateEmail(email);
        
        if (email.length > 0) {
            if (isValid) {
                this.style.borderColor = 'rgba(34, 197, 94, 0.5)';
                this.style.boxShadow = '0 0 0 3px rgba(34, 197, 94, 0.15), inset 0 2px 4px rgba(0, 0, 0, 0.1)';
            } else {
                this.style.borderColor = 'rgba(239, 68, 68, 0.5)';
                this.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.15), inset 0 2px 4px rgba(0, 0, 0, 0.1)';
            }
        } else {
            this.style.borderColor = 'rgba(255, 255, 255, 0.15)';
            this.style.boxShadow = 'inset 0 2px 4px rgba(0, 0, 0, 0.1)';
        }
    });

    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

});