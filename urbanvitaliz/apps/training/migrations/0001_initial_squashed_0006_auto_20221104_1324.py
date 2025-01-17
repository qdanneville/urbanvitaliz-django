# Generated by Django 3.2.16 on 2022-11-04 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('training', '0001_initial'), ('training', '0002_alter_challengedefinition_next_challenge'), ('training', '0003_challenge_acquired_on'), ('training', '0004_auto_20221104_1209'), ('training', '0005_auto_20221104_1240'), ('training', '0006_auto_20221104_1324')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChallengeDefinition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
                ('next_challenge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='training.challengedefinition')),
                ('code', models.SlugField(default='2022-11-04 11:40:17.709206+00:00', max_length=128, unique=True)),
                ('icon_name', models.CharField(blank=True, max_length=25, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acquired', models.BooleanField(default=False)),
                ('name', models.CharField(blank=True, max_length=128)),
                ('description', models.TextField(blank=True, null=True)),
                ('challenge_definition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.challengedefinition')),
                ('next_challenge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='training.challenge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_challenges', to=settings.AUTH_USER_MODEL)),
                ('acquired_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name="Date d'acquisition")),
            ],
        ),
        migrations.AlterModelManagers(
            name='challenge',
            managers=[
                ('acquired_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='description',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='name',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='next_challenge',
        ),
    ]
