from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class CustomLoginForm(AuthenticationForm):
    """
    Formulario personalizado de login que acepta RUT o username
    """
    username = forms.CharField(
        label='Usuario o RUT',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su usuario o RUT',
            'autofocus': True,
            'autocomplete': 'username'
        })
    )
    
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'autocomplete': 'current-password'
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            # Intentar autenticar con username o RUT
            self.user_cache = authenticate(
                self.request, 
                username=username, 
                password=password
            )
            
            if self.user_cache is None:
                # Si falla, intentar normalizar como RUT
                from utilidad.rut_validator import normalizar_rut
                try:
                    username_normalizado = normalizar_rut(username)
                    self.user_cache = authenticate(
                        self.request,
                        username=username_normalizado,
                        password=password
                    )
                except:
                    pass
            
            if self.user_cache is None:
                raise ValidationError(
                    'Usuario o contraseña incorrectos. Por favor, verifique sus credenciales.',
                    code='invalid_login',
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data
    
    def confirm_login_allowed(self, user):
        """
        Verificar que el usuario puede hacer login
        """
        if not user.is_active:
            raise ValidationError(
                'Esta cuenta está desactivada. Contacte al administrador.',
                code='inactive',
            )