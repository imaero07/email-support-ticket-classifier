import logging
import subprocess
import sys
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from EmailReader import EmailReader

log = logging.getLogger(__name__)

EXCLUDED = {"Unknown", "Unclear", "Draft"}


def load_from_output(output_dir):
    texts, labels = [], []
    reader = EmailReader()
    for category_dir in Path(output_dir).iterdir():
        if not category_dir.is_dir() or category_dir.name in EXCLUDED:
            continue
        for path in category_dir.iterdir():
            if not path.is_file():
                continue
            email = reader.read(path)
            text = (email.subject + " " + email.body).strip()
            if text:
                texts.append(text)
                labels.append(category_dir.name)
    return texts, labels


def train(input_dir="../inbox", model_path="../ml_model.joblib", output_dir="../output"):
    if not Path(output_dir).exists():
        log.info("Папка output не найдена — запускаю основную программу...")
        subprocess.run([sys.executable, "main.py", "--input", input_dir, "--output", "../"])
    if not Path(output_dir).exists():
        log.error("Не удалось получить папку output. Запустите основную программу вручную.")
        return

    texts, labels = load_from_output(output_dir)
    log.info(f"Писем для обучения: {len(texts)}, категорий: {len(set(labels))}")
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
        ("tree", DecisionTreeClassifier(random_state=42, max_depth=5)),
    ])
    model.fit(texts, labels)
    joblib.dump(model, model_path)
    log.info(f"Модель обучена и сохранена в {model_path}")
