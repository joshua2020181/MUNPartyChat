# Generated by Django 3.1.4 on 2021-02-04 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delegate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reso',
            name='<django.db.models.fields.CharField>_<django.db.models.fields.AutoField>',
        ),
        migrations.AddField(
            model_name='reso',
            name='resolution_file',
            field=models.FileField(blank=True, null=True, upload_to='DEFAULT2021/DEFAULT1/resolutions', verbose_name='Resolution File'),
        ),
    ]
