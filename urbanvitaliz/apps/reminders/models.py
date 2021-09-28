# encoding: utf-8

"""
Models for reminders

author  : raphael.marvie@beta.gouv.fr, guillaume.libersat@beta.gouv.fr
created : 2021-09-28 12:40:54 CEST
"""


from django.db import models


class MailManager(models.Manager):
    """Manager for mails to send"""

    def get_queryset(self):
        return super().get_queryset().filter(sent=None)


class SentMailManager(models.Manager):
    """Manager for sent mails"""

    def get_queryset(self):
        return super().get_queryset().exclude(sent=None)


class Mail(models.Model):
    """Represents a mail to be sent on a given date"""

    to_send = MailManager()
    sent = SentMailManager()

    recipient = models.CharField(max_length=128)
    subject = models.TextField(default="")
    text = models.TextField(default="")
    html = models.TextField(default="")
    deadline = models.DateField()

    sent = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "mail"
        verbose_name_plural = "mails"

    def __str__(self):
        return f"{self.recipient} {self.deadline}"


# eof