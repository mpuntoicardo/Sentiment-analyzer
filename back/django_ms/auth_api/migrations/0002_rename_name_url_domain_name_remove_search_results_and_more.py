# Generated by Django 5.0.4 on 2024-04-10 16:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='name',
            new_name='domain_name',
        ),
        migrations.RemoveField(
            model_name='search',
            name='results',
        ),
        migrations.AddField(
            model_name='search',
            name='result_id',
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='search',
            name='is_favorite',
            field=models.ForeignKey(default='Null', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='favorite_searches', to=settings.AUTH_USER_MODEL),
        ),
    ]
