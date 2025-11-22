from django.shortcuts import redirect
from django.urls import reverse

class Require2FAMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            if request.user.is_superuser or \
               request.user.groups.filter(name="Administrador").exists():

                # Verificar si tiene 2FA activo
                if not request.user.is_verified():  
                    return redirect(reverse("two_factor:setup"))

        return self.get_response(request)
