# encoding: utf-8

"""
Forms for projects application

author  : raphael.marvie@beta.gouv.fr,guillaume.libersat@beta.gouv.fr
created : 2021-12-14 10:36:20 CEST
"""

from django import forms
from markdownx.fields import MarkdownxFormField

from . import models

##################################################
# Notes
##################################################


class NoteForm(forms.ModelForm):
    """Form new project note creation"""

    class Meta:
        model = models.Note
        fields = ["content", "tags"]

    content = MarkdownxFormField()


class StaffNoteForm(NoteForm):
    class Meta:
        model = models.Note
        fields = ["content", "tags", "public"]


##################################################
# Tasks
##################################################


class TaskRecommendationForm(forms.ModelForm):
    """Form new task recommendation creation"""

    class Meta:
        model = models.TaskRecommendation
        fields = ["condition", "resource", "text", "departments"]


class TaskFollowupForm(forms.ModelForm):
    """Create a new followup for a task"""

    class Meta:
        model = models.TaskFollowup
        fields = ["comment"]


class RsvpTaskFollowupForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, required=False)


class ResourceTaskForm(forms.ModelForm):
    """Create and task for push resource"""

    notify_email = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = models.Task
        fields = ["intent", "content", "contact", "notify_email"]


class CreateTaskForm(forms.ModelForm):
    """Form new project task creation"""

    content = MarkdownxFormField(required=False)

    notify_email = forms.BooleanField(initial=False, required=False)

    class Meta:
        model = models.Task
        fields = [
            "intent",
            "content",
            "tags",
            "public",
            "priority",
            "deadline",
            "resource",
            "contact",
            "done",
            "notify_email",
        ]


class UpdateTaskForm(forms.ModelForm):
    """Form for task update"""

    content = MarkdownxFormField(required=False)

    class Meta:
        model = models.Task
        fields = [
            "intent",
            "content",
            "tags",
            "public",
            "priority",
            "deadline",
            "resource",
            "contact",
            "done",
        ]


class RemindTaskForm(forms.Form):
    """Remind task after X days"""

    days = forms.IntegerField(min_value=0, required=False, initial=42)


##################################################
# Project
##################################################
class ProjectForm(forms.ModelForm):
    """Form for updating the base information of a project"""

    postcode = forms.CharField(max_length=5, required=False, label="Code Postal")
    publish_to_cartofriches = forms.BooleanField(
        label="Publication sur cartofriches", disabled=True, required=False
    )

    class Meta:
        model = models.Project
        fields = [
            "email",
            "first_name",
            "last_name",
            "org_name",
            "phone",
            "name",
            "postcode",
            "location",
            "description",
            "switchtender",
            "publish_to_cartofriches",
        ]


class OnboardingForm(forms.ModelForm):
    """Form for onboarding a new local authority"""

    postcode = forms.CharField(max_length=5, required=False, label="Code Postal")

    impediment_kinds = forms.MultipleChoiceField(
        choices=[
            (
                "Méthode à suivre, guidage sur les prochaines étapes et questions à se poser",
                "Méthode à suivre, guidage sur les prochaines étapes et questions à se poser",
            ),
            (
                "Définition du projet de réhabilitation",
                "Définition du projet de réhabilitation",
            ),
            (
                "Accompagnement, conseil et compétences techniques avant travaux",
                "Accompagnement, conseil et compétences techniques avant travaux",
            ),
            ("Financement pour des études", "Financement pour des études"),
            ("Financement des travaux", "Financement des travaux"),
            (
                "Propriété de la friche, acquisition, contact avec le propriétaire",
                "Propriété de la friche, acquisition, contact avec le propriétaire",
            ),
            ("Autre", "Autre (précisez en commentaire)"),
        ],
        required=True,
        label="Quels sont les besoins et points de blocage?",
    )

    class Meta:
        model = models.Project
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "org_name",
            "name",
            "location",
            "description",
            "impediments",
            "publish_to_cartofriches",
        ]