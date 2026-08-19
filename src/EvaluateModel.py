from pathlib import Path
import csv
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import accuracy_score, f1_score
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline


from EmailReader import EmailReader


INBOX_DIR = Path("../inbox")
LABELS_FILE = Path("../labels.csv")
EXCLUDED_LABELS = {"Unknown", "Unclear", "Draft"}


def load_labeled_emails():
    reader = EmailReader()

    texts = []
    labels = []

    with open(LABELS_FILE, newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file)

        for row in rows:
            path = INBOX_DIR / row["filename"]
            if row["true_label"] in EXCLUDED_LABELS:
                continue

            if not path.exists():
                print(f"Skipping missing file: {path}")
                continue

            email = reader.read(path)

            if not email.correct:
                continue

            text = (email.subject + " " + email.body).strip()

            if not text:
                continue

            texts.append(text)
            labels.append(row["true_label"])

    return texts, labels


def build_model():
    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=1,
            ),
        ),
        (
            "tree",
            DecisionTreeClassifier(
                random_state=42,
                max_depth=5,
            ),
        ),
    ])


def main():
    texts, labels = load_labeled_emails()

    print(f"Loaded {len(texts)} labeled emails")
    print(f"Number of categories: {len(set(labels))}")

    class_counts = {}
    for label in labels:
        class_counts[label] = class_counts.get(label, 0) + 1

    print("\nClass distribution:")
    for label, count in sorted(class_counts.items()):
        print(f"{label}: {count}")

    cv = StratifiedKFold(
        n_splits=2,
        shuffle=True,
        random_state=42,
    )

    models = {
        "Dummy baseline": DummyClassifier(
            strategy="most_frequent"
        ),

        "Decision Tree": DecisionTreeClassifier(
            random_state=42,
            max_depth=5,
        ),

        "Logistic Regression": LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
        ),

        "Linear SVM": LinearSVC(
            class_weight="balanced",
        ),
    }

    results = {}

    for name, classifier in models.items():
        model = Pipeline([
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    min_df=1,
                ),
            ),
            ("classifier", classifier),
        ])

        predictions = cross_val_predict(
            model,
            texts,
            labels,
            cv=cv,
        )

        accuracy = accuracy_score(labels, predictions)

        macro_f1 = f1_score(
            labels,
            predictions,
            average="macro",
            zero_division=0,
        )

        weighted_f1 = f1_score(
            labels,
            predictions,
            average="weighted",
            zero_division=0,
        )

        results[name] = predictions

        print(f"\n=== {name} ===")
        print(f"Accuracy:    {accuracy:.3f}")
        print(f"Macro F1:    {macro_f1:.3f}")
        print(f"Weighted F1: {weighted_f1:.3f}")
if __name__ == "__main__":
    main()