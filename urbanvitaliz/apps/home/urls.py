# encoding: utf-8

"""
Urls for projects application

authors: raphael.marvie@beta.gouv.fr,guillaume.libersat@beta.gouv.fr
created: 2021-05-26 15:54:25 CEST
"""


from django.urls import path

from . import views

urlpatterns = [
    path(r"", views.HomePageView.as_view(), name="home"),
    path(r"login-redirect", views.LoginRedirectView.as_view(), name="login-redirect"),
    path(r"stats", views.StatisticsView.as_view(), name="statistics"),
    path(r"methodologie", views.MethodologyPageView.as_view(), name="methodology"),
    path(
        r"acteurs-locaux",
        views.RegionalActorsPageView.as_view(),
        name="regional-actors",
    ),
    path(r"qui-sommes-nous", views.WhoWeArePageView.as_view(), name="whoweare"),
    path(r"nous-suivre", views.FollowUsPageView.as_view(), name="followus"),
    path(r"contact/", views.contact, name="home-contact"),
    path(r"setup-password/", views.setup_password, name="home-user-setup-password"),
]

# eof
