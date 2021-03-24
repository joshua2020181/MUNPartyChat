from django.db import models
from django.contrib.auth.models import User
from homepage.models import Committee, Conference
# Create your models here.


class Reso(models.Model):

    id = models.AutoField(primary_key=True) # explicitly defined to be used later
    def reso_default():
        return {
            "header": { "forum": "",
                        "questionOf": "",
                        "submittedBy": "",
                        "committee": "",
                        },
            "preambles": [],
            "clauses": [{ "number": 0,
                            "clause": "",
                            "subClauses": [{
                                    "number": 'a',
                                    "subClause": "",
                                    "subSubClauses": [{
                                            "number": 'i',
                                            "subSubClause": "",
                                        }],
                                }],
                        }],
        }

    resolution = models.JSONField(default=reso_default)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    
    def file_path(instance, filename):
        try:
            pth = Conference.objects.get(committees__id=instance.committee.id).conf_id
            pth += '/' + instance.committee.abbr + '/resolutions/' + filename
            return pth
        except:
            return 'DEFAULT2021/DEFAULT1/resolutions/' + filename 


    
    name = models.CharField(max_length=30, default='default_reso_name') # user's name of the file ex: "GA1_resolution_1"
    resolution_file = models.FileField(upload_to=file_path, verbose_name='Resolution File', null=True, blank=True)
    


    def __str__(self):
        if self.resolution_file.name:
            return "Reso at: " + str(self.resolution_file.name)
        return "Reso obj with no file attatched. ID: " + str(self.id)
