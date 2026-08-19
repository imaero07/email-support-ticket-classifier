import argparse
import csv
from pathlib import Path
from collections import defaultdict
import logging
log = logging.getLogger(__name__)

def load_true_labels(csv_path):
    if not Path(csv_path).exists():
        log.error(f"Ошибка: файл {csv_path} не найден")
        return None
    true_labels = {}
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            filename = row["filename"].strip()
            label = row["true_label"].strip()
            true_labels[filename] = label
    return true_labels


def load_predicted_labels(output_folder):
    if not Path(output_folder).exists():
        log.error(f"Ошибка: папка {output_folder} не существует")
        return None
    predicted_labels = {}
    output_path = Path(output_folder)

    for category_folder in output_path.iterdir():
        if category_folder.is_dir():
            category_name = category_folder.name
            for file in  category_folder.iterdir():
                if file.is_file():
                    predicted_labels[file.name] = category_name

    return predicted_labels


def compute_metrics(true_labels, predicted_labels):
    all_categories = set(true_labels.values()) | set(predicted_labels.values())
    tp = defaultdict(int)
    fp = defaultdict(int)
    fn = defaultdict(int)

    correct = 0
    total = 0

    common_files = set(true_labels.keys()) & set(predicted_labels.keys())

    if not common_files:
        log.warning("Нет совпадающих файлов между labels.csv и папкой output")
        log.warning("Проверь что имена файлов в CSV совпадают с именами файлов в подпапках.")
        return None, None

    for filename in common_files:
        true = true_labels[filename]
        pred = predicted_labels[filename]
        total += 1

        if true == pred:
            correct += 1
            tp[true] += 1
        else:
            fp[pred] += 1
            fn[true] += 1  

    if total > 0:
        accuracy = correct / total
    else:
        accuracy = 0

    error_rate = 1 -accuracy

    overall = {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "error_rate": error_rate,
    }

    per_class = {}
    for cat in sorted(all_categories):
        t = tp[cat]
        f_pos = fp[cat]
        f_neg = fn[cat]

        if (t + f_pos) > 0:
            precision = t / (t + f_pos)
        else:
            precision = 0.0

        if (t + f_neg) > 0:
            recall = t / (t + f_neg)
        else:
            recall = 0.0

        if (precision + recall) > 0:
            f1 = (2 * precision * recall) / (precision + recall)
        else:
            f1 = 0.0

        per_class[cat] = {
            "tp": t,
            "fp": f_pos,
            "fn": f_neg,
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

    return overall, per_class


def print_report(overall, per_class):
    res = "\n"
    res += "Отчет по метрикам\n\n"
    res += f"Оценено  f{overall['total']} писем\n"
    res += f"Правильно: {overall['correct']}\n"
    res += "Accuracy:"
    res += format(overall['accuracy'], '.2%')
    res += "\n"
    res += "Error Rate:"
    res += format(overall['error_rate'], '.2%')
    res += "\n"
    res += f"{'Категория':<12} {'Precision':>10} {'Recall':>8} {'F1':>8} {'TP':>5} {'FP':>5} {'FN':>5}\n"
    for cat, m in per_class.items():
        res += f"{cat:<12} {m['precision']:>9.2%} {m['recall']:>7.2%} {m['f1']:>7.2%} {m['tp']:>5} {m['fp']:>5} {m['fn']:>5}\n"
    return res
