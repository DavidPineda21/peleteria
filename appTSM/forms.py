from django import forms
from django.forms.widgets import DateInput
import unicodedata

from .models import clsProductos



# Definir el formulario de activosTi
class frmProductos(forms.ModelForm):
    imagenes = forms.FileField(
        label='Imagenes del producto',
        required=False
    )

    tipoproducto = forms.ChoiceField(
        choices=[('', 'Seleccione una opción'),
                 ('TELA', 'TELA'),
                 ('SUELA', 'SUELA')
                 ],
        label='Tipo de Producto',
        widget=forms.Select(attrs={'class': 'select2'})
    )
    color = forms.ChoiceField(
        choices=[('', 'Seleccione una opción'),
                 ('NEGRO', 'NEGRO'),
                 ('ROJO', 'ROJO'),
                 ('BLANCO', 'BLANCO')
                 ],
        label='Color',
        widget=forms.Select(attrs={'class': 'select2'})
    )
    precioxm = forms.ChoiceField(
        choices=[('', 'Seleccione una opción'),
                 ('SI', 'SI'),
                 ('NO', 'NO')
                 ],
        label='Precio por metro',
        widget=forms.Select(attrs={'class': 'select2'})
    )

    class Meta:
        model = clsProductos
        fields = [
            'tipoproducto',
            'nombre',
            'color',
            'descripcion',
            'precio',
            'precioxm',
            'stock',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Procesar cada campo del formulario
        for field in cleaned_data:
            if isinstance(cleaned_data[field], str):
                # Convertir a mayúsculas
                value_upper = cleaned_data[field].upper()
                # Eliminar tildes
                cleaned_data[field] = ''.join(
                    char for char in unicodedata.normalize('NFD', value_upper)
                    if unicodedata.category(char) != 'Mn'
                )
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si es edición (hay instancia), deshabilita el campo
        # if self.instance and self.instance.pk:
        #     self.fields['serialactivoti'].disabled = True