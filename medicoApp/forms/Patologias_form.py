from django import forms
from medicoApp.models import Patologias

class PatologiasForm(forms.ModelForm):
    class Meta:
        model = Patologias
        fields = ['nombre', 'codigo_cie_10', 'descripcion', 'nivel_de_riesgo', 
                'protocolo_seguimiento', 'estado']
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Diabetes Gestacional'
            }),
            'codigo_cie_10': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la patología (opcional)'
            }),
            'nivel_de_riesgo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'protocolo_seguimiento': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Protocolo de seguimiento (opcional)'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        
        labels = {
            'nombre': 'Nombre de la Patología',
            'codigo_cie_10': 'Código CIE-10',
            'descripcion': 'Descripción',
            'nivel_de_riesgo': 'Nivel de Riesgo',
            'protocolo_seguimiento': 'Protocolo de Seguimiento',
            'estado': 'Estado'
        }