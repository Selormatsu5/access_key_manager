# Generated by Django 5.0.6 on 2024-06-14 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0005_alter_accesskey_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesskey',
            name='key',
            field=models.CharField(default='', max_length=16, unique=True),
        ),
    ]
