# Generated by Django 3.2.19 on 2023-06-20 13:40

from django.db import migrations, models
import urbanvitaliz.apps.training.models


class Migration(migrations.Migration):
    dependencies = [
        ("training", "0005_auto_20230620_1419"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="challengedefinition",
            managers=[
                (
                    "objects",
                    urbanvitaliz.apps.training.models.ChallengeDefinitionOnSiteManager(),
                ),
            ],
        ),
        migrations.AddField(
            model_name="challenge",
            name="started_on",
            field=models.DateTimeField(
                default=None, null=True, verbose_name="Date de démarrage"
            ),
        ),
    ]