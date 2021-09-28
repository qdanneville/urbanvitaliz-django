# Generated by Django 3.2.3 on 2021-09-27 12:19

from django.db import migrations, models
import urbanvitaliz.apps.survey.models


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0026_auto_20210921_1606"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="attachment",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=urbanvitaliz.apps.survey.models.survey_private_file_path,
            ),
        ),
    ]
