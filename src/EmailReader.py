from Email import Email
import logging
log = logging.getLogger(__name__)

class EmailReader:
    KEY_WORDS = {
        "subject": "subject", "тема": "subject", "tema": "subject",
        "from": "from", "от кого": "from", "ot kogo": "from",
        "to": "to", "кому": "to", "komu": "to",
        "date": "date", "дата": "date", "data": "date",
    }
    def read(self, file_path):
        subject = ""
        recipient = ""
        source_path = file_path
        body = ""
        sender = ""
        correct = False
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if ":" in line:
                        key = self.KEY_WORDS.get(line[:line.index(":")].strip().lower())
                        if key == "subject":
                            subject = line[line.index(":")+1:].strip()
                        elif key == "from":
                            sender = line[line.index(":")+1:].strip()
                        elif key == "to":
                            recipient = line[line.index(":")+1:].strip()
                        elif key == "date":
                            pass
                        else:
                            raise ValueError("Непредвиденный заголовок письма: " + key)
                    else:
                        body = line + file.read()
                        break
            correct = True
        except ValueError as e:
            log.warning(f"Ошибка для письма: {file_path}: {e}")
        except FileNotFoundError as e:
            log.error(f"Ошибка чтения файла, такого файла не существует: {file_path}: {e}")
        except Exception as e:
            log.error(f"Ошибка чтения файла: {file_path}: {e}")
        finally:
            return Email(recipient, sender, subject, body, source_path, correct)