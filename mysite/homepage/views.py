from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def homepage(request):
    return render(request, 'homepage/homepage.html')

def logout(request):
    from django.contrib.auth import logout
    logout(request)
    script = '<script>setTimeout(function () { window.location.href = "/";}, 2000);</script>'
    return HttpResponse('<p style="font-size: 30px;">Logout Completed. Redirecting to homepage.<p>' + script)