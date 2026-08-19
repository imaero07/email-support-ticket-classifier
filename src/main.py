import argparse
from pathlib import Path
from EmailReader import EmailReader
from Classifier import Classifier
from FileMover import FileMover
from Logger import Logger
from Metrics import load_true_labels, compute_metrics, print_report
import logging
from MLClassifier import MLClassifier
import ModelTrain

log = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Сортировщик писем")
    parser.add_argument("--input", default="../inbox", help="папка с письмами")
    parser.add_argument("--output", default="../", help="путь для папки")
    parser.add_argument("--debug", action="store_true", help="режим debug")
    parser.add_argument("--ml", action="store_true", help="использовать ML-классификатор вместо правил")
    args = parser.parse_args()
    logger = Logger(args.debug)

    if not Path(args.input).exists():
        log.error(f"Директория {args.input} не найдена")
        return

    log.info(f"Директория input: {args.input}, директория output: {args.output}output")

    reader = EmailReader()
    if args.ml:
        model_path = "../ml_model.joblib"
        if not Path(model_path).exists():
            log.info("Модель не найдена, запускается обучение")
            ModelTrain.train(args.input, model_path)
        classifier = MLClassifier(model_path)
    else:
        classifier = Classifier()

    mover = FileMover(args.output)
    predicted_labels = {}

    for path in Path(args.input).iterdir():
        if path.is_file():
            email = reader.read(path)
            category = classifier.classify(email)
            predicted_labels[path.name] = category
            logger.email_log(email, category)
            mover.move_files(email, category)

    log.info(logger.result_report())

    if Path("../labels.csv").exists():
        true_labels = load_true_labels("../labels.csv")
        if true_labels:
            overall, per_class = compute_metrics(true_labels, predicted_labels)
            if overall:
                log.info(print_report(overall, per_class))

if __name__ == "__main__":
    main()
