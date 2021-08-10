# encoding: utf-8

"""
Tests for survey application

authors: raphael.marvie@beta.gouv.fr, guillaume.libersat@beta.gouv.fr
created: 2021-06-27 12:06:10 CEST
"""

import pytest

from model_bakery.recipe import Recipe

from .. import models


########################################################################
# Session
########################################################################


@pytest.mark.django_db
def test_session_next_question_if_none():
    survey = Recipe(models.Survey).make()
    Recipe(models.QuestionSet, survey=survey).make()
    Recipe(models.QuestionSet, survey=survey).make()

    session = Recipe(models.Session, survey=survey).make()

    next_q = session.next_question()
    assert next_q is None


@pytest.mark.django_db
def test_session_next_question_returns_first_a_default():
    survey = Recipe(models.Survey).make()
    qs = Recipe(models.QuestionSet, survey=survey).make()
    q1 = Recipe(models.Question, text="Q1", question_set=qs).make()

    session = Recipe(models.Session, survey=survey).make()
    next_q = session.next_question()

    assert next_q == q1


@pytest.mark.django_db
def test_session_next_question_with_priority():
    survey = Recipe(models.Survey).make()
    qs = Recipe(models.QuestionSet, survey=survey).make()
    Recipe(models.Question, priority=10, text="Q1", question_set=qs).make()
    q2 = Recipe(models.Question, priority=100, text="Q2", question_set=qs).make()

    session = Recipe(models.Session, survey=survey).make()
    next_q = session.next_question()

    assert next_q == q2


#
# next question


@pytest.mark.django_db
def test_session_next_question_skips_answered_ones():
    survey = Recipe(models.Survey).make()
    qs = Recipe(models.QuestionSet, survey=survey).make()
    q1 = Recipe(models.Question, text="Q1", question_set=qs).make()
    q2 = Recipe(models.Question, text="Q2", question_set=qs).make()
    q3 = Recipe(models.Question, text="Q3", question_set=qs).make()

    session = Recipe(models.Session, survey=survey).make()

    # Answer Q2, meaning it should be skipped
    Recipe(models.Answer, session=session, question=q2).make()

    assert session.next_question(q1) == q3


@pytest.mark.django_db
def test_session_next_question_skips_untriggered_question():
    survey = Recipe(models.Survey).make()
    qs = Recipe(models.QuestionSet, survey=survey).make()
    q1 = Recipe(models.Question, text="Q1", question_set=qs).make()
    Recipe(
        models.Question, text="Q2", precondition="oscar-mike", question_set=qs
    ).make()
    q3 = Recipe(models.Question, text="Q3", question_set=qs).make()

    session = Recipe(models.Session, survey=survey).make()

    assert session.next_question(q1) == q3


#
# previous question


@pytest.mark.django_db
def test_session_previous_question_skips_answered_ones():
    survey = Recipe(models.Survey).make()
    qs = Recipe(models.QuestionSet, survey=survey).make()
    q1 = Recipe(models.Question, text="Q1", question_set=qs).make()
    q2 = Recipe(models.Question, text="Q2", question_set=qs).make()
    q3 = Recipe(models.Question, text="Q3", question_set=qs).make()

    session = Recipe(models.Session, survey=survey).make()

    # Answer Q2, meaning it should be skipped
    Recipe(models.Answer, session=session, question=q2).make()

    assert session.previous_question(q3) == q1


@pytest.mark.django_db
def test_session_previous_question_skips_untriggered_question():
    survey = Recipe(models.Survey).make()
    qs = Recipe(models.QuestionSet, survey=survey).make()
    q1 = Recipe(models.Question, text="Q1", question_set=qs).make()
    Recipe(
        models.Question, text="Q2", precondition="oscar-mike", question_set=qs
    ).make()
    q3 = Recipe(models.Question, text="Q3", question_set=qs).make()

    session = Recipe(models.Session, survey=survey).make()

    assert session.previous_question(q3) == q1


#
# use of question signals

@pytest.mark.django_db
def test_session_signals_union():
    session = Recipe(models.Session).make()

    signals = ["charlie-mike, pan, pan", "tango-yankee"]
    answers = []
    for signal in signals:
        answers.append(Recipe(models.Answer, session=session, signals=signal).make())

    # Check that each signal from the answers are found in the session
    for answer in answers:
        for tag in answer.tags:
            assert tag.name in session.signals


########################################################################
# Question Sets
########################################################################


@pytest.mark.django_db
def test_question_set_next():
    survey = Recipe(models.Survey).make()
    qs1 = Recipe(models.QuestionSet, survey=survey).make()
    qs2 = Recipe(models.QuestionSet, survey=survey).make()

    assert qs2 == qs1.next()
    assert qs2.next() is None


@pytest.mark.django_db
def test_question_set_previous():
    survey = Recipe(models.Survey).make()
    qs1 = Recipe(models.QuestionSet, survey=survey).make()
    qs2 = Recipe(models.QuestionSet, survey=survey).make()

    assert qs1 == qs2.previous()
    assert qs1.previous() is None


########################################################################
# Questions
########################################################################


@pytest.mark.django_db
def test_question_next_question():
    survey = Recipe(models.Survey).make()
    qs = Recipe(models.QuestionSet, survey=survey).make()
    q1 = Recipe(models.Question, priority=0, text="Q1", question_set=qs).make()
    q2 = Recipe(models.Question, priority=0, text="Q2", question_set=qs).make()

    assert q2 == q1.next()
    assert q2.next() is None


@pytest.mark.django_db
def test_question_next_question_with_priority():
    survey = Recipe(models.Survey).make()
    qs = Recipe(models.QuestionSet, survey=survey).make()
    q1 = Recipe(models.Question, text="Q1", priority=300, question_set=qs).make()
    q2 = Recipe(models.Question, text="Q2", question_set=qs).make()
    q3 = Recipe(models.Question, text="Q2", priority=200, question_set=qs).make()

    assert q1.next() == q3
    assert q3.next() == q2


@pytest.mark.django_db
def test_question_previous_question():
    survey = Recipe(models.Survey).make()
    qs = Recipe(models.QuestionSet, survey=survey).make()
    q1 = Recipe(models.Question, priority=0, text="Q1", question_set=qs).make()
    q2 = Recipe(models.Question, priority=0, text="Q2", question_set=qs).make()

    assert q1 == q2.previous()
    assert q1.previous() is None


@pytest.mark.django_db
def test_question_precondition_succeeds():
    session = Recipe(models.Session).make()

    signal = "gamma"

    Recipe(models.Answer, session=session, signals=signal).make()

    q = Recipe(models.Question, precondition=signal, text="Q-with-precondition").make()

    assert q.check_precondition(session) is True


@pytest.mark.django_db
def test_question_precondition_fails():
    session = Recipe(models.Session).make()

    q = Recipe(models.Question, precondition="gamma", text="Q-with-precondition").make()

    assert q.check_precondition(session) is False