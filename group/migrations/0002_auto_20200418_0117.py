# Generated by Django 2.2.11 on 2020-04-18 05:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='voterecord',
            name='vote_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vote',
            name='vote_event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='group.Event'),
        ),
        migrations.AddField(
            model_name='vote',
            name='vote_movie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='group.MovieList'),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='group.Group'),
        ),
        migrations.AddField(
            model_name='usergroup',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movielist',
            name='movie_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.Group'),
        ),
        migrations.AddField(
            model_name='group',
            name='group_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='event_group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='group.Group'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_movie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='group.MovieList'),
        ),
    ]
