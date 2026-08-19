import pytest


VALID_EMAIL = """От кого: ivan@company.ru
Кому: support@company.ru
Дата: 01.06.2026
Тема: Запрос доступа

Прошу выдать доступ к корпоративному порталу.
Спасибо.
"""


def test_read_valid_email(reader, sample_file):
    path = sample_file(VALID_EMAIL)
    email = reader.read(path)
    assert email.correct is True
    assert email.sender == "ivan@company.ru"
    assert email.recipient == "support@company.ru"
    assert email.subject == "запрос доступа"
    assert "прошу выдать доступ" in email.body


def test_read_missing_file_marks_incorrect(reader, tmp_path):
    path = tmp_path / "nope.txt"
    email = reader.read(path)
    assert email.correct is False


def test_read_empty_file(reader, sample_file):
    path = sample_file("")
    email = reader.read(path)
    assert email.subject == ""
    assert email.body == ""
    assert email.recipient == ""


def test_read_unknown_header_format(reader, sample_file):
    text = "Заголовок: текст\n\nТело письма."
    path = sample_file(text)
    email = reader.read(path)
    assert email.correct is False


@pytest.mark.parametrize("header", ["От кого", "From", "Ot kogo"])
def test_read_sender_different(reader, sample_file, header):
    text = f"{header}: someone@company.ru\nКому: me@company.ru\nТема: test\n\nтело"
    path = sample_file(text)
    email = reader.read(path)
    assert email.correct is True
    assert email.sender == "someone@company.ru"
