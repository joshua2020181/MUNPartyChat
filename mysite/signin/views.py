from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse

from homepage.models import Country, Committee, Conference, Chair


# Create your views here.

def signin(request, userType): #usertype is 'delegate', 'admin', or 'chair'
    if userType == 'admin':
        context = {"errorMsg" : None}
        if request.method == 'POST':
            username = ''
            if 'confID' in request.POST:
                try:
                    username += Conference.objects.get(conf_id=request.POST['confID']).conf_id
                except (KeyError, Conference.DoesNotExist):
                    print("Error: ConfID is wrong")
                    context['errorMsg'] = "Conference ID is incorrect."
                    return render(request, 'signin/' + userType + '.html', context)
            if 'adminID' in request.POST:
                username += '-' + request.POST['adminID']
            if 'password' in request.POST:
                from django.contrib.auth import authenticate, login
                user = authenticate(username=username, password=request.POST['password'])
                if user is not None:
                    login(request, user)
                    return redirect(reverse(userType, args = [context['selectedConference'].conf_id]), permanent=True) # ex: CISSMUN2021/admin
                else:
                    context['errorMsg'] = "Incorrect Password."
                    return render(request, 'signin/' + userType + '.html', context)

    if userType == 'delegate' or userType == 'chair':
        print(request.session)
        context = {
            "errorMsg": None,
            "conferences": Conference.objects.all(),
            "committees": None,
            "countries": None,
            "selectedConference": None,
            "selectedCommittee": None,
            "selectedCountry": None,
            }
        if request.method == 'POST':
            if 'confID' in request.POST:
                try:
                    context['selectedConference'] = Conference.objects.get(conf_id=request.POST['confID'])
                    context['committees'] = context['selectedConference'].committees.all()
                except (KeyError, Conference.DoesNotExist):
                    print("Error: ConfID is wrong")
                    context['errorMsg'] = "Conference ID is incorrect."
                    return render(request, 'signin/' + userType + '.html', context)
            if 'committee' in request.POST:
                context['selectedCommittee'] = Committee.objects.get(id=request.POST['committee'])
                if userType == 'delegate':
                    context['countries'] = context['selectedCommittee'].countries.all()
                else: # chair
                    context['countries'] = context['selectedCommittee'].chairs.all()
            if 'country' in request.POST:
                if userType == 'delegate':
                    context['selectedCountry'] = Country.objects.get(id=request.POST['country'])
                else: # chair
                    context['selectedCountry'] = Chair.objects.get(id=request.POST['country'])
            if 'password' in request.POST:
                password = request.POST['password']
                username = context['selectedConference'].conf_id + '-' # ex: CISSMUN2021-GA1-USA
                username += context['selectedCommittee'].abbr + '-'
                if userType == 'delegate':
                    username += context['selectedCountry'].abbr
                else: # chair
                    username += context['selectedCountry'].name
                print('Username: ' + username)
                print('password: ' + password)
                from django.contrib.auth import authenticate, login
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    for k in request.session.keys():
                        print("session key: " + k + "  |  " + request.session[k])
                    return redirect(reverse(userType, args = [context['selectedConference'].conf_id]), permanent=True) # ex: CISSMUN2021/delegate
                else:
                    context['errorMsg'] = "Incorrect Password. Please Try Again"
                    return render(request, 'signin/' + userType + '.html', context)
    return render(request, 'signin/' + userType + '.html', context)
