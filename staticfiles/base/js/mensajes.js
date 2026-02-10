document.addEventListener('DOMContentLoaded', function() {
    initializeDjangoMessages();
});

function initializeDjangoMessages() {
    const messagesContainer = document.getElementById('django-messages');
    if (!messagesContainer) return;
    
    // Configurar auto-dismiss para mensajes que lo permiten
    const messages = messagesContainer.querySelectorAll('.django-message');
    messages.forEach((message, index) => {
        const messageId = message.getAttribute('data-message-id');
        const autoDismiss = message.getAttribute('data-auto-dismiss') === 'true';
        
        // Auto-dismiss después de 5 segundos (excepto errores)
        if (autoDismiss) {
            setTimeout(() => {
                dismissMessage(messageId);
            }, 5000 + (index * 500)); // Escalonar el dismiss
        }
        
        // Pausar auto-dismiss en hover
        message.addEventListener('mouseenter', function() {
            const progressBar = this.querySelector('.message-progress');
            if (progressBar) {
                progressBar.style.animationPlayState = 'paused';
            }
        });
        
        message.addEventListener('mouseleave', function() {
            const progressBar = this.querySelector('.message-progress');
            if (progressBar) {
                progressBar.style.animationPlayState = 'running';
            }
        });
    });
}

// Función para cerrar mensaje manualmente
function dismissMessage(messageId) {
    const message = document.querySelector(`[data-message-id="${messageId}"]`);
    if (!message || message.classList.contains('dismissing')) return;
    
    message.classList.add('dismissing');
    
    // Remover después de la animación
    setTimeout(() => {
        if (message.parentNode) {
            message.parentNode.removeChild(message);
            
            // Si no hay más mensajes, remover el container
            const container = document.getElementById('django-messages');
            if (container && container.children.length === 0) {
                container.remove();
            }
        }
    }, 400);
}

// Función para cerrar todos los mensajes
function dismissAllMessages() {
    const messages = document.querySelectorAll('.django-message:not(.dismissing)');
    messages.forEach((message, index) => {
        const messageId = message.getAttribute('data-message-id');
        setTimeout(() => {
            dismissMessage(messageId);
        }, index * 100); // Efecto cascada
    });
}

// Cerrar mensajes con tecla Escape
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        dismissAllMessages();
    }
});
