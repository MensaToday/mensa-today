from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mensa_recommend.source.data_collection.learnweb import LearnWebCollector, run
from celery.result import AsyncResult


def learnweb_login(request):

    if request.method == "POST":

        # check if request parameters were provided
        if 'username' in request.POST and 'password' in request.POST:

            # get request parameters
            ziv_id = request.POST['username']
            ziv_password = request.POST['password']
            current_user = request.user

            # Check if provided login data is correct
            session_id = LearnWebCollector(ziv_id, ziv_password,
                                           current_user).get_session_id()

            if session_id == False:

                # If data is not correct send user feedback
                print("Daten falsch...")
            else:

                # Id data is correct then crawling can be started
                run.delay(ziv_id, ziv_password, current_user.id)

    return render(request, 'learnweb_login.html', {})
