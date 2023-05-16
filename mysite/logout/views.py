from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import logout

# Create your views here.
def trylogout(request):
    logout(request)
    return redirect('main')
    #return HttpResponse("Hello, world. You're at the logout index.")