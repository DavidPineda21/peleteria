/* INICIO JS SELECT2 Y SELECT3 */ 
    $(document).ready(function() {
        $('.select2').select2({
        width: '100%'
        });
        $('.select3').select2({
            ajax: {
                url: 'ajax/equipment/',
                dataType: 'json',
                delay: 1000,
                data: function (params) {
                    const fieldName = $(this).data('field-name');
                    return {
                        q: params.term, // Search term
                        field_name: fieldName
                    };
                },
                processResults: function (data) {
                    return {
                        results: data.results
                    };
                },
                cache: true
            },
            minimumInputLength: 0, // Minimum number of characters before AJAX is triggered
        });

            // Añadir el valor seleccionado como una opción en el select2
        $('.select3').each(function() {
            const selectedValue = $(this).val();
            if (selectedValue) {
                const selectedText = $(this).find('option:selected').text();
                $(this).append(new Option(selectedText, selectedValue, true, true));
            }
        });
    
        // Prevent AJAX on open until user types something
        $('.select3').on('select3:open', function(e) {
            if ($('.select3-search__field').val() === '') {
                e.preventDefault(); // Prevent AJAX call if input is empty
            }
        });
    
        // Optional: Clear input state when an option is selected
        $('.select3').on('select3:select', function(e) {
            $('.select3-search__field').val(''); // Clear input after selection
        });
    });
    

        document.addEventListener("DOMContentLoaded", function () {
            const form = document.querySelector("form");
            if (form) {
                const submitBtn = form.querySelector("button[type='submit'], input[type='submit']");
                if (submitBtn) {
                    form.addEventListener("submit", function () {
                        submitBtn.disabled = true;
                        submitBtn.innerText = "Enviando..."; // Opcional
                    });
                }
            }
        });


/* FIN JS SELECT2 Y SELECT3 */ 

/* INICIO JS EXPANDIR CELDA */

// Mejorado: solo aplica a celdas con contenido que desborda
document.querySelectorAll('td').forEach(cell => {
    cell.addEventListener('click', () => {
        cell.classList.toggle('expanded');
    });
});

/* FIN JS EXPANDIR CELDA */