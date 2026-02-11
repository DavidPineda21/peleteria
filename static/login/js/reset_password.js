document.addEventListener('DOMContentLoaded', function() {
    const resetForm = document.getElementById('reset-form');
    const emailInput = document.getElementById('email');
    const tokenInput = document.getElementById('token'); // Cambiado de 'code' a 'token'
    const newPasswordInput = document.getElementById('newPassword');
    const confirmPasswordInput = document.getElementById('confirmPassword');

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
    
    // Función para mostrar/ocultar contraseña
    window.togglePassword = function(fieldId) {
        const field = document.getElementById(fieldId);
        const button = field.parentNode.querySelector('.toggle-password');
        
        if (field.type === 'password') {
            field.type = 'text';
            button.textContent = '🙈';
        } else {
            field.type = 'password';
            button.textContent = '👁';
        }
    }
    
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
            resetInputStyle(this);
        }
    });
    
    // Validación del token (solo números, máximo 6 dígitos)
    tokenInput.addEventListener('input', function() {
        // Solo permitir números
        this.value = this.value.replace(/[^0-9]/g, '');
        
        const token = this.value;
        if (token.length > 0) {
            if (token.length === 6) {
                this.style.borderColor = 'rgba(34, 197, 94, 0.5)';
                this.style.boxShadow = '0 0 0 3px rgba(34, 197, 94, 0.15), inset 0 2px 4px rgba(0, 0, 0, 0.1)';
            } else {
                this.style.borderColor = 'rgba(251, 146, 60, 0.5)';
                this.style.boxShadow = '0 0 0 3px rgba(251, 146, 60, 0.15), inset 0 2px 4px rgba(0, 0, 0, 0.1)';
            }
        } else {
            resetInputStyle(this);
        }
    });
    
    // Validación de contraseña nueva
    newPasswordInput.addEventListener('input', function() {
        const password = this.value;

        // Actualizar indicadores de requisitos
        updatePasswordRequirements(password, 'newPassword-requirements');
        
        if (password.length > 0) {
            if (ivalidatePassword(password)) {
                this.style.borderColor = 'rgba(34, 197, 94, 0.5)';
                this.style.boxShadow = '0 0 0 3px rgba(34, 197, 94, 0.15), inset 0 2px 4px rgba(0, 0, 0, 0.1)';
            } else {
                this.style.borderColor = 'rgba(239, 68, 68, 0.5)';
                this.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.15), inset 0 2px 4px rgba(0, 0, 0, 0.1)';
            }
        } else {
            resetInputStyle(this);
        }
        
        // Validar confirmación de contraseña si ya tiene contenido
        if (confirmPasswordInput.value.length > 0) {
            validatePasswordConfirmation();
        }
    });
    
    // Validación de confirmación de contraseña
    confirmPasswordInput.addEventListener('input', validatePasswordConfirmation);
    
    function validatePasswordConfirmation() {
        const password = newPasswordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        
        if (confirmPassword.length > 0) {
            if (password === confirmPassword) {
                confirmPasswordInput.style.borderColor = 'rgba(34, 197, 94, 0.5)';
                confirmPasswordInput.style.boxShadow = '0 0 0 3px rgba(34, 197, 94, 0.15), inset 0 2px 4px rgba(0, 0, 0, 0.1)';
            } else {
                confirmPasswordInput.style.borderColor = 'rgba(239, 68, 68, 0.5)';
                confirmPasswordInput.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.15), inset 0 2px 4px rgba(0, 0, 0, 0.1)';
            }
        } else {
            resetInputStyle(confirmPasswordInput);
        }
    }
    
    function resetInputStyle(input) {
        input.style.borderColor = 'rgba(255, 255, 255, 0.15)';
        input.style.boxShadow = 'inset 0 2px 4px rgba(0, 0, 0, 0.1)';
    }

    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    function validatePassword(password) {
        // Al menos 8 caracteres, al menos una mayúscula, una minúscula y un número
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
        return passwordRegex.test(password);
    }

    // Función para actualizar indicadores de requisitos
    function updatePasswordRequirements(password, requirementsId) {
        const requirementsDiv = document.getElementById(requirementsId);
        if (!requirementsDiv) return;

        const hasLength = password.length >= 8;
        const hasUpper = /[A-Z]/.test(password);
        const hasLower = /[a-z]/.test(password);
        const hasNumber = /\d/.test(password);

        // Mostrar u ocultar indicadores
        if (password.length > 0) {
            requirementsDiv.classList.add('show');
        } else {
            requirementsDiv.classList.remove('show');
        }

        // Actualizar cada requisito
        const lengthReq = requirementsDiv.querySelector('#req-length-reset');
        const upperReq = requirementsDiv.querySelector('#req-uppercase-reset');
        const lowerReq = requirementsDiv.querySelector('#req-lowercase-reset');
        const numberReq = requirementsDiv.querySelector('#req-number-reset');

        // Función para actualizar un requisito individual
        function updateRequirement(element, isValid) {
            if (element) {
                const icon = element.querySelector('.req-icon');
                if (isValid) {
                    element.classList.add('valid');
                    if (icon) icon.textContent = '✅';
                } else {
                    element.classList.remove('valid');
                    if (icon) icon.textContent = '❌';
                }
            }
        }

        updateRequirement(lengthReq, hasLength);
        updateRequirement(upperReq, hasUpper);
        updateRequirement(lowerReq, hasLower);
        updateRequirement(numberReq, hasNumber);
    }

});