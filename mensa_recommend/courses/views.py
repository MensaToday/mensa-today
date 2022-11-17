from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mensa_recommend.source.data_collection.learnweb import run


def learnweb_login(request):

    if request.method == "POST":
        ziv_id = request.POST['username']
        ziv_password = request.POST['password']
        current_user = request.user

        run.delay(ziv_id, ziv_password, current_user.id)

    return render(request, 'learnweb_login.html', {})
