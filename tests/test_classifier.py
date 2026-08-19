import pytest


@pytest.mark.parametrize("subject, body, expected", [
    ("Запрос доступа", "Прошу выдать доступ к корпоративной почте", "Access"),
    ("Отпуск", "Согласовать отпуск с 1 июня", "HR"),
    ("Счёт на оплату", "Передать в бухгалтерию счёт №67", "Finance"),
    ("Ошибка 500", "Сервис не отвечает, сбой после обновления", "Tech"),
    ("Договор", "Направляем документ во вложении, ознакомьтесь", "Docs"),
    ("Жалоба клиента", "Клиент не может зарегистрироваться, кнопка не работает", "Client"),
    ("Newsletter", "Корпоративный дайджест, не отвечайте на это письмо", "Auto"),
])
def test_classify_basic_categories(classifier, email_factory, subject, body, expected):
    email = email_factory(subject=subject, body=body)
    assert classifier.classify(email) == expected


def test_classify_spam(classifier, email_factory):
    email = email_factory(
        subject="Поздравляем, вы выиграли приз",
        body="Только сегодня скидка 90%, перейдите по ссылке",
    )
    assert classifier.classify(email) == "Spam"


def test_classify_urgent_priority(classifier, email_factory):
    email = email_factory(
        subject="URGENT",
        body="Срочно, работа полностью остановлена, эскалация",
    )
    assert classifier.classify(email) == "Urgent"


def test_classify_repeat(classifier, email_factory):
    email = email_factory(
        subject="Напоминание",
        body="Обращаемся повторно, повторно направляю запрос",
    )
    assert classifier.classify(email) == "Repeat"


def test_no_reply_sender_goes_to_auto(classifier, email_factory):
    email = email_factory(
        subject="тема",
        body="текст",
        sender="no-reply@service.com",
    )
    assert classifier.classify(email) == "Auto"


def test_empty_email_is_draft(classifier, email_factory):
    email = email_factory(subject="", body="", recipient="")
    assert classifier.classify(email) == "Draft"


def test_incorrect_email_is_unknown(classifier, email_factory):
    email = email_factory(subject="что угодно", body="что угодно", correct=False)
    assert classifier.classify(email) == "Unknown"


def test_no_matches_is_unclear(classifier, email_factory):
    email = email_factory(
        subject="Привет",
        body="Просто пишу поздороваться, без особой темы.",
    )
    assert classifier.classify(email) == "Unclear"


def test_single_match_is_unclear(classifier, email_factory):
    email = email_factory(subject="reminder", body="ничего важного")
    assert classifier.classify(email) == "Unclear"


def test_body_has_more_weight_than_subject(classifier, email_factory):
    email = email_factory(
        subject="отпуск",
        body="счёт на оплату, передать в бухгалтерию",
    )
    assert classifier.classify(email) == "Finance"
