# partosApp/forms/documentos_forms.py
"""
Formularios para Documentos del Parto
CORREGIDO: Usar registro_recien_nacido en lugar de registro_parto
"""
from django import forms
from recienNacidoApp.models import DocumentosParto, RegistroRecienNacido  # ✅ Importación corregida


class DocumentosPartoForm(forms.ModelForm):
    """
    Formulario completo para documentos del parto
    """
    class Meta:
        model = DocumentosParto
        fields = [
            'registro_recien_nacido',  # ✅ Campo corregido
            # Ley Dominga
            'recuerdos_entregados',
            # Placenta
            'retira_placenta',
            'estampado_placenta',
            # Registro Civil
            'folio_valido',
            'folios_nulos',
            # Manejo del Dolor
            'manejo_dolor_no_farmacologico',
        ]
        widgets = {
            'registro_recien_nacido': forms.Select(attrs={  # ✅ Corregido
                'class': 'form-select',
                'required': True
            }),
            # Ley Dominga
            'recuerdos_entregados': forms.Textarea(attrs={  # ✅ Cambiado a Textarea
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej: Huella, foto, mechas de cabello'
            }),
            # Placenta
            'retira_placenta': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'estampado_placenta': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            # Registro Civil
            'folio_valido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de folio'
            }),
            'folios_nulos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Folios anulados (si aplica)'
            }),
            # Manejo del Dolor
            'manejo_dolor_no_farmacologico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa los métodos no farmacológicos utilizados'
            }),
        }
        labels = {
            'registro_recien_nacido': 'Registro de Recién Nacido',  # ✅ Corregido
            'recuerdos_entregados': 'Recuerdos Entregados (Ley N° 21.372 Dominga)',
            'retira_placenta': '¿Retira Placenta?',
            'estampado_placenta': '¿Estampado de Placenta?',
            'folio_valido': 'Folio Válido Registro Civil',
            'folios_nulos': 'Folios Nulos',
            'manejo_dolor_no_farmacologico': 'Manejo del Dolor No Farmacológico',
        }
        help_texts = {
            'recuerdos_entregados': 'Lista de recuerdos entregados según Ley N° 21.372',
            'folio_valido': 'Número de folio del certificado de nacimiento',
        }
    
    def __init__(self, *args, **kwargs):
        # Permitir pasar el registro_recien_nacido como parámetro
        registro_rn = kwargs.pop('registro_rn', None)
        super().__init__(*args, **kwargs)
        
        # Si se pasa registro_rn, preseleccionarlo y ocultarlo
        if registro_rn:
            self.fields['registro_recien_nacido'].initial = registro_rn
            self.fields['registro_recien_nacido'].widget = forms.HiddenInput()
        
        # Filtrar solo registros de RN
        self.fields['registro_recien_nacido'].queryset = RegistroRecienNacido.objects.select_related(
            'registro_parto__ficha__paciente__persona'
        )
        
        # Todos los campos son opcionales excepto registro_recien_nacido
        for field_name in self.fields:
            if field_name != 'registro_recien_nacido':
                self.fields[field_name].required = False


class LeyDomingaForm(forms.ModelForm):
    """
    Formulario solo para Ley Dominga
    """
    class Meta:
        model = DocumentosParto
        fields = [
            'recuerdos_entregados',
        ]
        widgets = {
            'recuerdos_entregados': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Lista de recuerdos entregados'
            }),
        }
        labels = {
            'recuerdos_entregados': 'Recuerdos Entregados',
        }


class PlacentaForm(forms.ModelForm):
    """
    Formulario solo para información de placenta
    """
    class Meta:
        model = DocumentosParto
        fields = [
            'retira_placenta',
            'estampado_placenta',
        ]
        widgets = {
            'retira_placenta': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'estampado_placenta': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'retira_placenta': 'La familia retira la placenta',
            'estampado_placenta': 'Se realizó estampado de placenta',
        }


class RegistroCivilForm(forms.ModelForm):
    """
    Formulario solo para Registro Civil
    """
    class Meta:
        model = DocumentosParto
        fields = [
            'folio_valido',
            'folios_nulos',
        ]
        widgets = {
            'folio_valido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 7787343'
            }),
            'folios_nulos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Folios anulados (separados por coma)'
            }),
        }
        labels = {
            'folio_valido': 'Folio Válido',
            'folios_nulos': 'Folios Nulos',
        }