from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/users/login_user')
def home(request):
    return render(request, 'index.html', {})