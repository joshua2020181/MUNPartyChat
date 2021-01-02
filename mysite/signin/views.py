from django.shortcuts import render
from django.http import HttpResponse

from homepage.models import Country, Committee, Conference


# Create your views here.

def signin(request, userType): #usertype is 'delegate', 'admin', or 'chair'
    if userType == 'delegate':
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
            print(request.POST)
            if 'confID' in request.POST:
                try:
                    context['selectedConference'] = Conference.objects.get(conf_id=request.POST['confID'])
                    context['committees'] = context['selectedConference'].committees.all()
                except (KeyError, Conference.DoesNotExist):
                    print("Error: ConfID is wrong")
                    context['errorMsg'] = "Conference ID is incorrect."
                    return render(request, 'signin/delegate.html', context)
            if 'committee' in request.POST:
                context['selectedCommittee'] = Committee.objects.get(id=request.POST['committee'])
                context['countries'] = context['selectedCommittee'].countries.all()
            if 'country' in request.POST:
                context['selectedCountry'] = Country.objects.get(id=request.POST['country'])
            if 'password' in request.POST:
                password = request.POST['password']
                username = context['selectedConference'].conf_id + '-' # ex: CISSMUN2021-GA1-USA
                username += context['selectedCommittee'].abbr + '-'
                username += context['selectedCountry'].abbr
                print('Username: ' + username)
                print('password: ' + password)
                from django.contrib.auth import authenticate
                user = authenticate(username=username, password=password)
                if user is not None:
                    return HttpResponse("<strong>Congrats</strong>")
                else:
                    context['errorMsg'] = "Incorrect Password. Please Try Again"
                    return render(request, 'signin/delegate.html', context)


        print(context) 
        return render(request, 'signin/delegate.html', context)
    return HttpResponse( userType + " signin page")
