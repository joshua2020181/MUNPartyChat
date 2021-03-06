# Generated by Django 3.1.4 on 2020-12-30 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('abbr', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ['abbr'],
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('abbr', models.CharField(max_length=10)),
                ('committees', models.ManyToManyField(to='homepage.Committee')),
            ],
            options={
                'ordering': ['abbr'],
            },
        ),
    ]
