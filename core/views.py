from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Redirección automática según rol
            if user.groups.filter(name="Administrador").exists():
                return redirect("admin_dashboard")

            if user.groups.filter(name="Médico").exists():
                return redirect("medico_dashboard")

            if user.groups.filter(name="Matrona").exists():
                return redirect("matrona_dashboard")

            if user.groups.filter(name="TENS").exists():
                return redirect("tens_dashboard")

            return redirect("home_public")
        else:
            messages.error(request, "Credenciales inválidas")
    
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def custom_403(request, exception=None):
    return render(request, "403.html", status=403)