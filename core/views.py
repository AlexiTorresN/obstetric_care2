from django.shortcuts import render
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages

# ============================================
# VISTAS DE LOGIN/LOGOUT MOVIDAS A authentication/
# ============================================
# def login_view(request):
#     """DEPRECADO: Usar authentication.views.CustomLoginView"""
#     pass

# def logout_view(request):
#     """DEPRECADO: Usar authentication.views.CustomLogoutView"""
#     pass

# ============================================
# VISTA DE ERROR 403
# ============================================
def custom_403(request, exception=None):
    """Handler personalizado para errores 403 Forbidden"""
    return render(request, "403.html", status=403)