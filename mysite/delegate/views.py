from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from homepage.models import Conference, Committee, Country

# Create your views here.

@login_required
def delegate(request, confID):
    context = {
        'user': request.user,
        'conference': Conference.objects.get(conf_id=confID),
    }
    print(context['user'].username.split('-'))
    if Group.objects.get(name='delegates') not in request.user.groups.all():
        if not request.user.is_staff:
            return redirect('/')
        context['alerts'] = []
        context['alerts'].append('Staff account. Things may not work.')

    try:
        context['committee'] = context['conference'].committees.get(abbr=context['user'].username.split('-')[1])
        context['country'] = context['committee'].countries.get(abbr=context['user'].username.split('-')[2])
        
    except:
        context['committee'] = "Committee"
        context['country'] = 'Country'
    
    return render(request, 'delegate/delegate.html', context)