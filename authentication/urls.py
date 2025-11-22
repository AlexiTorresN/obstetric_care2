# authentication/urls.py
"""
URLs de autenticación y dashboards por rol
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    CustomLoginView, 
    custom_logout_view,
    DashboardAdminView,
    DashboardMedicoView,
    DashboardMatronaView,
    DashboardTensView,
)

app_name = 'authentication'

urlpatterns = [
    # ============================================
    # AUTENTICACIÓN
    # ============================================
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout_view, name='logout'), 
    
    # ============================================
    # RECUPERACIÓN DE CONTRASEÑA
    # ============================================
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='authentication/password_reset.html',
             email_template_name='authentication/password_reset_email.html',
             subject_template_name='authentication/password_reset_subject.txt',
             success_url='/password_reset/done/'
         ), 
         name='password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='authentication/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='authentication/password_reset_confirm.html',
             success_url='/reset/done/'
         ), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='authentication/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    
    # ============================================
    # DASHBOARDS POR ROL
    # ============================================
    path('dashboard/admin/', DashboardAdminView.as_view(), name='dashboard_admin'),
    path('dashboard/medico/', DashboardMedicoView.as_view(), name='dashboard_medico'),
    path('dashboard/matrona/', DashboardMatronaView.as_view(), name='dashboard_matrona'),
    path('dashboard/tens/', DashboardTensView.as_view(), name='dashboard_tens'),
]