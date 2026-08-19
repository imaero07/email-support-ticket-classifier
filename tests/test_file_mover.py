from pathlib import Path
from FileMover import FileMover

def test_move_creates_category_folder(tmp_path, email_factory):
    src = tmp_path / "mail.txt"
    src.write_text("содержимое", encoding="utf-8")
    mover = FileMover(str(tmp_path) + "/")
    email = email_factory(source_path=str(src))
    mover.move_files(email, "HR")
    dst = Path(str(tmp_path) + "/output") / "HR" / "mail.txt"
    assert dst.exists()
    assert dst.read_text(encoding="utf-8") == "содержимое"


def test_move_missing_source(tmp_path, email_factory):
    mover = FileMover(str(tmp_path) + "/")
    email = email_factory(source_path=str(tmp_path / "nope.txt"))
    mover.move_files(email, "Spam")

