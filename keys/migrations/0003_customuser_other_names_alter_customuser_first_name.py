# Generated by Django 5.0.6 on 2024-06-08 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0002_accesskey_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='other_names',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]