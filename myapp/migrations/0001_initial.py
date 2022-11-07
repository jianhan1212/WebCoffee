# Generated by Django 4.1 on 2022-10-05 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DetailModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(default='', max_length=100)),
                ('unitprice', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('dtotal', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(default='', max_length=100)),
                ('pprice', models.IntegerField(default=0)),
                ('pimages', models.CharField(default='', max_length=100)),
                ('pdescription', models.TextField(blank=True, default='')),
            ],
        ),
    ]