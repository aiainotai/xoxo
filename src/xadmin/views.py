from django.shortcuts import render

# Create your views here.

def admindash(request):
    return render(request, 'backend/based/main.html')
