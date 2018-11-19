from django.shortcuts import render


def upro(request):
    return render(request,"upro/user.html",{})
