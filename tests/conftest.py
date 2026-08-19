import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

import pytest
from Email import Email
from Classifier import Classifier
from EmailReader import EmailReader


def make_email(subject="", body="", recipient="user@company.ru",
               sender="user@company.ru", source_path="test.txt", correct=True):
    return Email(recipient, sender, subject, body, source_path, correct)


@pytest.fixture
def email_factory():
    return make_email


@pytest.fixture
def classifier():
    return Classifier()


@pytest.fixture
def reader():
    return EmailReader()


@pytest.fixture
def sample_file(tmp_path):
    def _make(text, name="mail.txt"):
        path = tmp_path / name
        path.write_text(text, encoding="utf-8")
        return path
    return _make
