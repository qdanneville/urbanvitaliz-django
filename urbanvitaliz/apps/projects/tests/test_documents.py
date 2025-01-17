# encoding: utf-8

"""
Tests for project application

authors: raphael.marvie@beta.gouv.fr, guillaume.libersat@beta.gouv.fr
created: 2022-05-31 10:11:56 CEST
"""


import pytest
from actstream.models import action_object_stream
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from model_bakery import baker
from model_bakery.recipe import Recipe
from urbanvitaliz.utils import login

from .. import models


@pytest.mark.django_db
def test_upload_document_not_available_for_non_logged_users(client):
    project = baker.make(models.Project)
    url = reverse("projects-conversation-upload-file", args=[project.id])
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_upload_document_available_for_project_collaborators(client):
    png = SimpleUploadedFile("img.png", b"file_content", content_type="image/png")
    data = {"description": "this is some content", "the_file": png}

    membership = baker.make(models.ProjectMember, is_owner=True, member__is_staff=False)
    project = baker.make(models.Project, projectmember_set=[membership], status="READY")

    with login(client, user=membership.member):
        url = reverse("projects-conversation-upload-file", args=[project.id])
        response = client.post(url, data=data)

    assert response.status_code == 302

    document = models.Document.objects.all()[0]
    assert document.project == project
    assert document.description == data["description"]
    assert document.uploaded_by == membership.member
    assert document.the_file is not None


@pytest.mark.django_db
def test_upload_document_triggers_notifications(client):
    png = SimpleUploadedFile("img.png", b"file_content", content_type="image/png")
    data = {"description": "this is some content", "the_file": png}

    membership = baker.make(models.ProjectMember, is_owner=True, member__is_staff=False)
    other_membership = baker.make(
        models.ProjectMember, is_owner=False, member__is_staff=False
    )
    project = baker.make(
        models.Project, projectmember_set=[membership, other_membership], status="READY"
    )

    with login(client, user=membership.member):
        url = reverse("projects-conversation-upload-file", args=[project.id])
        response = client.post(url, data=data)

    assert response.status_code == 302

    document = models.Document.objects.all()[0]

    assert action_object_stream(document).count() == 1
    assert membership.member.notifications.count() == 0
    assert other_membership.member.notifications.count() == 1


@pytest.mark.django_db
def test_delete_document_not_available_for_non_logged_users(client):
    project = Recipe(models.Project).make()
    url = reverse("projects-conversation-delete-file", args=[project.id, 1])
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_document_available_for_owner(client):
    membership = baker.make(models.ProjectMember, is_owner=True, member__is_staff=False)
    project = baker.make(models.Project, projectmember_set=[membership], status="READY")
    document = baker.make(
        models.Document, uploaded_by=membership.member, project=project
    )

    with login(client, user=membership.member):
        url = reverse(
            "projects-conversation-delete-file", args=[project.id, document.id]
        )
        response = client.post(url)

    assert response.status_code == 302
    document = models.Document.objects.count() == 0


@pytest.mark.django_db
def test_delete_document_not_available_for_others(client):
    membership = baker.make(models.ProjectMember, is_owner=True, member__is_staff=False)
    project = baker.make(models.Project, projectmember_set=[membership], status="READY")
    document = baker.make(
        models.Document,
        project=project,
        uploaded_by__username="other",
        description="Doc description",
    )

    with login(client, user=membership.member):
        url = reverse(
            "projects-conversation-delete-file", args=[project.id, document.id]
        )
        response = client.post(url)

    assert response.status_code == 403
    document = models.Document.objects.count() == 1
