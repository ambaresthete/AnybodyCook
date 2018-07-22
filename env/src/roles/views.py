from django.shortcuts import render, redirect
from .models import Role
from django.contrib.auth import get_user_model

User= get_user_model()

def assign_role(request):
    role = None
    rolename = "cook"
    try:
        if request.user.is_authenticated:
            role = Role.objects.get(user=request.user)
            role.rolename = rolename
            role.save()
            request.session['rolename'] = role.rolename
    except Role.DoesNotExist:
        role = None        
    return redirect("upload:product")
