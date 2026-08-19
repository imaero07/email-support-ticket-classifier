import pytest

from Email import Email


def test_email_fields_are_lowercased():
    email = Email("USER@X.RU", "Sender@X.RU", "Тема", "ТЕКСТ", "p.txt")
    assert email.recipient == "user@x.ru"
    assert email.sender == "sender@x.ru"
    assert email.subject == "тема"
    assert email.body == "текст"
