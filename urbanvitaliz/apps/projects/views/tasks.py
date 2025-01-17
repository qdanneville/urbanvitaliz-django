# encoding: utf-8

"""
Views for projects application

author  : raphael.marvie@beta.gouv.fr,guillaume.libersat@beta.gouv.fr
created : 2021-05-26 15:56:20 CEST
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from urbanvitaliz.apps.reminders import api
from urbanvitaliz.apps.reminders import models as reminders_models
from urbanvitaliz.apps.resources import models as resources
from urbanvitaliz.apps.survey import models as survey_models
from urbanvitaliz.utils import (
    check_if_switchtender,
    is_staff_or_403,
    is_switchtender_or_403,
)

from .. import models, signals
from ..forms import (
    CreateActionsFromResourcesForm,
    CreateActionWithoutResourceForm,
    CreateActionWithResourceForm,
    PushTypeActionForm,
    RemindTaskForm,
    RsvpTaskFollowupForm,
    TaskFollowupForm,
    TaskRecommendationForm,
    UpdateTaskFollowupForm,
    UpdateTaskForm,
)
from ..utils import (
    can_manage_or_403,
    create_reminder,
    get_active_project_id,
    remove_reminder,
)


@login_required
def visit_task(request, task_id):
    """Visit the content of a task"""
    task = get_object_or_404(models.Task, site=request.site, pk=task_id)
    can_manage_or_403(task.project, request.user, allow_draft=True)
    is_switchtender = check_if_switchtender(request.user)

    if not task.visited and not is_switchtender:
        task.visited = True
        task.save()

        signals.action_visited.send(
            sender=visit_task, task=task, project=task.project, user=request.user
        )

    if task.resource:
        return redirect(reverse("resources-resource-detail", args=[task.resource.pk]))

    return redirect(reverse("projects-project-detail-actions", args=[task.project_id]))


@login_required
def toggle_done_task(request, task_id):
    """Mark task as done for a project"""
    task = get_object_or_404(models.Task, site=request.site, pk=task_id)
    can_manage_or_403(task.project, request.user)

    if request.method == "POST":
        if task.open:
            task.status = models.Task.DONE

            # NOTE should we remove all the reminders?
            api.remove_reminder_email(task)
            signals.action_done.send(
                sender=toggle_done_task,
                task=task,
                project=task.project,
                user=request.user,
            )
        else:
            task.status = models.Task.PROPOSED

            signals.action_undone.send(
                sender=toggle_done_task,
                task=task,
                project=task.project,
                user=request.user,
            )
        task.save()

    return redirect(reverse("projects-project-detail-actions", args=[task.project_id]))


@login_required
def refuse_task(request, task_id):
    """Mark task refused for a project (user not interested)"""
    task = get_object_or_404(models.Task, site=request.site, pk=task_id)
    can_manage_or_403(task.project, request.user)

    if request.method == "POST":
        task.status = models.Task.NOT_INTERESTED
        task.save()
        api.remove_reminder_email(task)
        signals.action_not_interested.send(
            sender=refuse_task, task=task, project=task.project, user=request.user
        )

    return redirect(reverse("projects-project-detail-actions", args=[task.project_id]))


@login_required
def already_done_task(request, task_id):
    """Mark task refused for a project"""
    task = get_object_or_404(models.Task, site=request.site, pk=task_id)
    can_manage_or_403(task.project, request.user)

    if request.method == "POST":
        task.status = models.Task.ALREADY_DONE
        task.save()
        api.remove_reminder_email(task)
        signals.action_already_done.send(
            sender=already_done_task, task=task, project=task.project, user=request.user
        )

    return redirect(reverse("projects-project-detail-actions", args=[task.project_id]))


@login_required
def sort_task(request, task_id, order):
    """Update an existing task for a project"""
    task = get_object_or_404(models.Task, site=request.site, pk=task_id)
    can_manage_or_403(task.project, request.user)

    if order == "up":
        task.up()
    elif order == "down":
        task.down()
    else:
        return HttpResponseForbidden()

    task.save()

    return redirect(
        reverse("projects-project-detail-actions", args=[task.project_id])
        + f"#action-{task.id}"
    )


@login_required
def update_task(request, task_id=None):
    """Update an existing task for a project"""
    task = get_object_or_404(models.Task, site=request.site, pk=task_id)
    can_manage_or_403(task.project, request.user)

    was_public = task.public

    if request.method == "POST":
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.updated_on = timezone.now()
            instance.save()
            instance.project.updated_on = instance.updated_on
            instance.project.save()
            api.remove_reminder_email(
                task, recipient=request.user.email, origin=api.models.Reminder.STAFF
            )

            # If we are going public, notify
            if was_public is False and instance.public is True:
                signals.action_created.send(
                    sender=update_task,
                    task=instance,
                    project=instance.project,
                    user=request.user,
                )

            return redirect(
                reverse("projects-project-detail-actions", args=[task.project_id])
                + f"#action-{task.id}"
            )
    else:
        form = UpdateTaskForm(instance=task)
    return render(request, "projects/project/task_update.html", locals())


########
# Task Recommendation
########


@login_required
def task_recommendation_create(request):
    """Create a new task recommendation for a project"""
    is_staff_or_403(request.user)

    if request.method == "POST":
        form = TaskRecommendationForm(request.POST)
        if form.is_valid():
            reco = form.save(commit=False)
            reco.site = request.site
            reco.save()

            return redirect(reverse("projects-task-recommendation-list"))
    else:
        form = TaskRecommendationForm()
    return render(request, "projects/tasks/recommendation_create.html", locals())


@login_required
def task_recommendation_update(request, recommendation_id):
    """Update a task recommendation"""
    is_staff_or_403(request.user)

    recommendation = get_object_or_404(
        models.TaskRecommendation, site=request.site, pk=recommendation_id
    )

    if request.method == "POST":
        form = TaskRecommendationForm(request.POST, instance=recommendation)
        if form.is_valid():
            form.save()
            return redirect(reverse("projects-task-recommendation-list"))
    else:
        form = TaskRecommendationForm(instance=recommendation)

    return render(request, "projects/tasks/recommendation_update.html", locals())


@login_required
def task_recommendation_list(request):
    """List task recommendations for a project"""
    is_staff_or_403(request.user)

    recommendations = models.TaskRecommendation.on_site.all()

    return render(request, "projects/tasks/recommendation_list.html", locals())


@login_required
def presuggest_task(request, project_id):
    """Suggest tasks"""
    is_switchtender_or_403(request.user)

    project = get_object_or_404(models.Project, sites=request.site, pk=project_id)

    try:
        survey = survey_models.Survey.on_site.get(pk=1)  # XXX Hardcoded survey ID
        session, created = survey_models.Session.objects.get_or_create(
            project=project, survey=survey
        )
    except survey_models.Survey.DoesNotExist:
        session = None

    tasks = []

    if session:
        session_signals = session.signals

        for recommandation in models.TaskRecommendation.on_site.all():
            if not project.commune:
                continue

            if recommandation.departments.all().count() > 0:
                if not (
                    project.commune.department.code
                    in recommandation.departments.values_list("code", flat=True)
                ):
                    continue

            reco_tags = set(
                recommandation.condition_tags.values_list("name", flat=True)
            )
            if reco_tags.issubset(session_signals):
                tasks.append(
                    models.Task(
                        id=0,
                        project=project,
                        resource=recommandation.resource,
                        intent=recommandation.text,
                    )
                )

    return render(request, "projects/project/task_suggest.html", locals())


@login_required
def delete_task(request, task_id=None):
    """Delete a task from a project"""
    is_switchtender_or_403(request.user)
    task = get_object_or_404(models.Task, site=request.site, pk=task_id)
    if request.method == "POST":
        task.deleted = timezone.now()
        task.save()

    next_url = reverse("projects-project-detail-actions", args=[task.project_id])
    return redirect(next_url)


@login_required
def remind_task(request, task_id=None):
    """Set a reminder for a task"""
    task = get_object_or_404(models.Task, site=request.site, pk=task_id)

    membership = task.project.projectmember_set.filter(is_owner=True).first()
    if not membership:
        raise Http404

    if request.method == "POST":
        form = RemindTaskForm(request.POST)
        if form.is_valid():
            days = form.cleaned_data.get("days")
            days = days or 6 * 7  # 6 weeks is default

            if create_reminder(
                days, task, membership.member, origin=api.models.Reminder.SELF
            ):
                messages.success(
                    request,
                    "Une alarme a bien été programmée dans {0} jours.".format(days),
                )
            else:
                messages.error(
                    request,
                    "Impossible de programmer l'alarme : cet utilisateur n'existe pas.",
                )
        else:
            messages.error(
                request, "Impossible de programmer l'alarme : données invalides."
            )

    return redirect(reverse("projects-project-detail-actions", args=[task.project_id]))


@login_required
def remind_task_delete(request, task_id=None):
    """Delete a reminder for a task"""
    task = get_object_or_404(models.Task, site=request.site, pk=task_id)

    if request.method == "POST":
        api.remove_reminder_email(task)

    return redirect(reverse("projects-project-detail-actions", args=[task.project_id]))


@login_required
def followup_task(request, task_id=None):
    """Create a new followup for task"""
    task = get_object_or_404(models.Task, site=request.site, pk=task_id)
    can_manage_or_403(task.project, request.user)
    if request.method == "POST":
        form = TaskFollowupForm(request.POST)
        if form.is_valid():
            followup = form.save(commit=False)
            followup.task = task
            followup.who = request.user

            followup.save()

            if followup.status in (
                models.Task.ALREADY_DONE,
                models.Task.NOT_INTERESTED,
            ):
                remove_reminder(task, task.project.owner)
            else:
                # Create or reset 6 weeks reminder
                create_reminder(
                    7 * 6,
                    task,
                    task.project.owner,
                    origin=reminders_models.Reminder.SYSTEM,
                )

    return redirect(reverse("projects-project-detail-actions", args=[task.project.id]))


@login_required
def followup_task_update(request, followup_id=None):
    """Update a followup for task"""
    followup = get_object_or_404(
        models.TaskFollowup, task__site=request.site, pk=followup_id
    )

    if followup.who != request.user:
        return HttpResponseForbidden()

    form = UpdateTaskFollowupForm(
        request.POST or request.GET or None, instance=followup
    )
    if request.method == "POST":
        if form.is_valid():
            followup = form.save()

            return redirect(
                reverse(
                    "projects-project-detail-actions", args=[followup.task.project.id]
                )
                + f"#action-{followup.task.id}"
            )
    return render(request, "projects/task/task_followup_update.html", locals())


def rsvp_followup_task(request, rsvp_id=None, status=None):
    """Manage the user task followup from her rsvp email.
    Triggered when a user clicks on a rsvp link
    """
    try:
        rsvp = models.TaskFollowupRsvp.objects.get(uuid=rsvp_id)
    except models.TaskFollowupRsvp.DoesNotExist:
        return render(request, "projects/task/rsvp_followup_invalid.html", locals())

    task = rsvp.task

    rsvp_signals = [
        models.Task.INPROGRESS,
        models.Task.DONE,
        models.Task.ALREADY_DONE,
        models.Task.NOT_INTERESTED,
        models.Task.BLOCKED,
    ]

    if status not in rsvp_signals:
        raise Http404()

    if request.method == "POST":
        form = RsvpTaskFollowupForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get("comment", "")
            followup = models.TaskFollowup(
                status=status, comment=comment, task=task, who=rsvp.user
            )
            followup.save()

            rsvp.delete()  # we are done with this use only once object

            # Reminder update
            if task.status in [models.Task.INPROGRESS, models.Task.BLOCKED]:
                create_reminder(
                    7 * 6, task, request.user, origin=reminders_models.Reminder.SYSTEM
                )
            else:
                api.remove_reminder_email(task)

            return render(request, "projects/task/rsvp_followup_thanks.html", locals())
    else:
        form = RsvpTaskFollowupForm()
    return render(request, "projects/task/rsvp_followup_confirm.html", locals())


########################################################################
# push resource to project
########################################################################


@login_required
def create_action(request, project_id=None):
    """Create action for given project"""
    project = get_object_or_404(models.Project, sites=request.site, pk=project_id)

    can_manage_or_403(project, request.user)

    if request.method == "POST":
        # Pick a different form for better data handling based
        # on the 'push_type' attribute
        type_form = PushTypeActionForm(request.POST)

        type_form.is_valid()

        push_type = type_form.cleaned_data.get("push_type")

        try:
            push_form_type = {
                "noresource": CreateActionWithoutResourceForm,
                "single": CreateActionWithResourceForm,
                "multiple": CreateActionsFromResourcesForm,
            }[push_type]
        except KeyError:
            return render(request, "projects/project/task_create.html", locals())

        form = push_form_type(request.POST)
        if form.is_valid():
            if push_type == "multiple":
                for resource in form.cleaned_data.get("resources", []):
                    public = form.cleaned_data.get("public", False)
                    action = models.Task.on_site.create(
                        project=project,
                        site=request.site,
                        resource=resource,
                        intent=resource.title,
                        created_by=request.user,
                        public=public,
                    )
                    action.top()

                    # Notify other switchtenders
                    signals.action_created.send(
                        sender=create_action,
                        task=action,
                        project=project,
                        user=request.user,
                    )

            else:
                action = form.save(commit=False)
                action.project = project
                action.site = request.site
                action.created_by = request.user
                action.save()
                action.top()

                # Notify other switchtenders
                signals.action_created.send(
                    sender=create_action,
                    task=action,
                    project=project,
                    user=request.user,
                )

            next_url = reverse("projects-project-detail-actions", args=[project.id])
            return redirect(next_url + f"#action-{action.id}")
    else:
        form = PushTypeActionForm()

    return render(request, "projects/project/task_create.html", locals())


@login_required
def create_resource_action_for_current_project(request, resource_id=None):
    """Create action for given resource to project stored in session"""
    is_switchtender_or_403(request.user)
    project_id = get_active_project_id(request)
    resource = get_object_or_404(resources.Resource, sites=request.site, pk=resource_id)
    project = get_object_or_404(models.Project, sites=request.site, pk=project_id)

    next_url = reverse("projects-project-create-action", args=[project.id])
    next_url += f"?resource={resource.id}"
    return redirect(next_url)
