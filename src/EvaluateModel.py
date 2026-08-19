from pathlib import Path
import csv

import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    ConfusionMatrixDisplay,
)
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
    filenames = []

    with open(LABELS_FILE, newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file)

        for row in rows:
            if row["true_label"] in EXCLUDED_LABELS:
                continue

            path = INBOX_DIR / row["filename"]

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
            filenames.append(row["filename"])

    return texts, labels, filenames


def main():
    texts, labels, filenames = load_labeled_emails()

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

        accuracy = accuracy_score(
            labels,
            predictions,
        )

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

    best_predictions = results["Logistic Regression"]

    output_dir = Path("../evaluation")
    output_dir.mkdir(exist_ok=True)

    ConfusionMatrixDisplay.from_predictions(
        labels,
        best_predictions,
        labels=sorted(set(labels)),
        xticks_rotation=45,
        cmap="Blues",
        colorbar=False,
    )

    plt.title(
        "Logistic Regression - Cross-Validated Predictions"
    )
    plt.tight_layout()

    output_path = (
        output_dir
        / "confusion_matrix_logistic_regression.png"
    )

    plt.savefig(
        output_path,
        dpi=200,
    )
    plt.close()

    print(
        f"\nConfusion matrix saved to: {output_path}"
    )

    print("\n=== MISCLASSIFIED EMAILS ===")

    error_rows = []
    confusion_pairs = {}

    for row in error_rows:
        pair = (
            row["true_label"],
            row["predicted_label"],
        )

        confusion_pairs[pair] = (
            confusion_pairs.get(pair, 0) + 1
        )

    print("\n=== MOST COMMON CONFUSIONS ===")

    for (true_label, predicted_label), count in sorted(
        confusion_pairs.items(),
        key=lambda item: item[1],
        reverse=True,
    ):
        print(
            f"{true_label} -> {predicted_label}: {count}"
        )


    for filename, text, true_label, predicted_label in zip(
        filenames,
        texts,
        labels,
        best_predictions,
    ):
        if true_label != predicted_label:
            preview = text.replace("\n", " ")[:160]

            print(
                f"{filename}: "
                f"{true_label} -> {predicted_label} | "
                f"{preview}"
            )

            error_rows.append({
                "filename": filename,
                "true_label": true_label,
                "predicted_label": predicted_label,
                "text_preview": preview,
            })

    errors_path = output_dir / "misclassified_emails.csv"

    with open(
        errors_path,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "filename",
                "true_label",
                "predicted_label",
                "text_preview",
            ],
        )

        writer.writeheader()
        writer.writerows(error_rows)

    print(
        f"\nTotal misclassified emails: {len(error_rows)}"
    )
    print(
        f"Misclassified emails saved to: {errors_path}"
    )


if __name__ == "__main__":
    main()