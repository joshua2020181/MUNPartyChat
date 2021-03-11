from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.conf import settings

from homepage.models import Conference, Committee, Country
from .models import Reso

from docx2python import docx2python
from .Resolution import Resolution
import os

# Create your views here.

@login_required
def delegate(request, confID, page=''):
    context = {
        'user': request.user,
        'conference': Conference.objects.get(conf_id=confID),
    }
    #print(context['user'].username.split('-'))
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
    
    if not page:
        return render(request, 'delegate/delegate.html', context)

    if page == 'upload':
        if request.FILES:
            res = Reso(
                #file_path = confID + '/' + context['committee'].abbr + '/resolutions' if not context['committee'] == 'Committee' else None,
                user=context['user'],
                committee=context['committee'] if not context['committee'] == 'Committee' else None,
                name=request.FILES['uploadedReso'].name,
                resolution_file=request.FILES['uploadedReso'])
            res.save()

            doc = docx2python(os.path.join(settings.MEDIA_ROOT, res.resolution_file.name), html = True)
            #print(doc.text)

            res.resolution = Resolution(doc.text).resolution
        
            context['resolution'] = res

        if request.POST:
            for i in request.POST.keys():
                print(i + ": " + request.POST[i])


    return render(request, f'delegate/{page}.html', context)