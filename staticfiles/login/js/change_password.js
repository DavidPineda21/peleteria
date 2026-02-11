document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const currentPasswordInput = document.getElementById('current-password');
    const newPasswordInput = document.getElementById('new-password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const changePasswordBtn = document.getElementById('change-password-btn');

    // Efecto de entrada suave
    setTimeout(() => {
        document.querySelector('.change-card').style.opacity = '1';
        document.querySelector('.change-card').style.transform = 'translateY(0)';
    }, 100);
    
    // Animación del logo al hacer hover
    const logo = document.querySelector('.perseo-logo-change');
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

    // Función para mostrar/ocultar contraseña (igual que en reset_password.js)
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

    // Función para resetear estilo de input (igual que en reset_password.js)
    function resetInputStyle(input) {
        input.style.borderColor = 'rgba(255, 255, 255, 0.15)';
        input.style.boxShadow = 'inset 0 2px 4px rgba(0, 0, 0, 0.1)';
    }

    // Función para aplicar estilo de éxito
    function setSuccessStyle(input) {
        input.style.borderColor = 'rgba(34, 197, 94, 0.5)';
        input.style.boxShadow = '0 0 0 3px rgba(34, 197, 94, 0.15), inset 0 2px 4px rgba(0, 0, 0, 0.1)';
    }

    // Función para aplicar estilo de error
    function setErrorStyle(input) {
        input.style.borderColor = 'rgba(239, 68, 68, 0.5)';
        input.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.15), inset 0 2px 4px rgba(0, 0, 0, 0.1)';
    }

    // Función para validar contraseña (mejorada para aceptar más caracteres especiales)
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
        const lengthReq = requirementsDiv.querySelector('#req-length');
        const upperReq = requirementsDiv.querySelector('#req-uppercase');
        const lowerReq = requirementsDiv.querySelector('#req-lowercase');
        const numberReq = requirementsDiv.querySelector('#req-number');

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

    // Validación de contraseña actual (sin validación de fuerza, solo que no esté vacía)
    currentPasswordInput.addEventListener('input', function() {
        const password = this.value;

        if (password.length > 0) {
            // Solo verificar que no esté vacía, sin validar la fuerza
            setSuccessStyle(this);
        } else {
            resetInputStyle(this);
        }
        validateForm();
    });

    // Validación de nueva contraseña (igual que en reset_password.js)
    newPasswordInput.addEventListener('input', function() {
        const password = this.value;

        // Actualizar indicadores de requisitos
        updatePasswordRequirements(password, 'new-password-requirements');

        if (password.length > 0) {
            if (validatePassword(password)) {
                setSuccessStyle(this);
            } else {
                setErrorStyle(this);
            }
        } else {
            resetInputStyle(this);
        }
        
        // Validar confirmación de contraseña si ya tiene contenido
        if (confirmPasswordInput.value.length > 0) {
            validatePasswordConfirmation();
        }
        validateForm();
    });

    // Validación de confirmación de contraseña (igual que en reset_password.js)
    confirmPasswordInput.addEventListener('input', validatePasswordConfirmation);

    function validatePasswordConfirmation() {
        const password = newPasswordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        
        if (confirmPassword.length > 0) {
            if (password === confirmPassword) {
                setSuccessStyle(confirmPasswordInput);
            } else {
                setErrorStyle(confirmPasswordInput);
            }
        } else {
            resetInputStyle(confirmPasswordInput);
        }
        validateForm();
    }

    // Función para validar todo el formulario
    function validateForm() {
        const currentPassword = currentPasswordInput.value;
        const newPassword = newPasswordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        
        const isCurrentValid = currentPassword.length > 0; // Solo verificar que no esté vacía
        const isNewValid = newPassword.length > 0 && validatePassword(newPassword) && newPassword !== currentPassword;
        const isConfirmValid = confirmPassword.length > 0 && confirmPassword === newPassword;
        
        const isFormValid = isCurrentValid && isNewValid && isConfirmValid;
        
        // Habilitar/deshabilitar botón
        if (changePasswordBtn) {
            changePasswordBtn.disabled = !isFormValid;
            if (isFormValid) {
                changePasswordBtn.style.opacity = '1';
                changePasswordBtn.style.cursor = 'pointer';
            } else {
                changePasswordBtn.style.opacity = '0.6';
                changePasswordBtn.style.cursor = 'not-allowed';
            }
        }
        
        return isFormValid;
    }

    // Inicializar estado del formulario
    validateForm();

    // Mejorar UX: focus automático en el primer campo
    if (currentPasswordInput) {
        currentPasswordInput.focus();
    }
});