# core/decorators.py
from django.contrib.auth.decorators import user_passes_test

def role_required(role):
    def validator(user):
        return user.is_authenticated and user.groups.filter(name=role).exists()
    return user_passes_test(validator, login_url='login')
