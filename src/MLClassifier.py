import logging
from pathlib import Path

import joblib

log = logging.getLogger(__name__)

class MLClassifier:
    def __init__(self, model_path="ml_model.joblib"):
        self.model = None
        try:
            self.model = joblib.load(Path(model_path))
            log.info(f"ML модель загружена из {model_path}")
        except FileNotFoundError:
            log.error(f"Файл модели {model_path} не найден")
        except Exception as e:
            log.error(f"Не удалось загрузить модель: {e}")

    def classify(self, email):
        if not email.correct:
            return "Unknown"
        if email.recipient == "":
            return "Draft"
        text = (email.subject + " " + email.body).strip()
        if not text or self.model is None:
            return "Unclear"
        try:
            return str(self.model.predict([text])[0])
        except Exception as e:
            log.error(f"Ошибка предсказания: {e}")
            return "Unclear"