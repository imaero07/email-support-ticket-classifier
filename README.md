# Email Support Ticket Classifier

A team Python project for automated classification and routing of incoming IT support requests.

## Overview

The system processes incoming emails, identifies the type of IT support request, assigns one of 13 categories, and routes the message for further processing.

The project explores two approaches:
- rule-based classification
- decision-tree-based classification

## My Contribution

This was a team project.

My individual contribution:
- proposed the original project idea and use case
- led functional testing and validation
- designed and tested scenarios across different request categories
- identified ambiguous and incorrectly processed cases
- contributed to evaluating the system's classification behavior

## Features

- Email parsing
- Classification into 13 support-request categories
- Rule-based classification
- Decision-tree classification
- Confidence-based fallback for ambiguous requests
- Automatic file routing
- Logging
- Classification metrics
- Automated tests

## Project Structure

- `src/` — application source code
- `tests/` — automated tests
- `inbox/` — synthetic sample emails used for testing
- `labels.csv` — email labels
- `requirements.txt` — Python dependencies

## Dataset

The repository contains 100+ synthetic email samples created for development and testing.

No real customer or personal data is included.

## Technologies

- Python
- scikit-learn
- pytest
- joblib

## Current Limitations

The original model evaluation was performed primarily on training data.  
A proper held-out evaluation is being added to measure performance on unseen emails.

## Future Improvements

- train/test evaluation
- per-class precision, recall, and F1-score
- error analysis
- improved handling of ambiguous requests
- comparison of multiple classification algorithms

## Context

Developed as a team academic project in 2026.

## Model Evaluation

The original project reported performance on training data, which does not reliably measure generalization.

I later revisited the evaluation methodology and introduced 2-fold stratified cross-validation on 75 labeled emails across 10 semantic categories.

| Model | Accuracy | Macro F1 | Weighted F1 |
|---|---:|---:|---:|
| Dummy baseline | 26.7% | 0.042 | 0.112 |
| Decision Tree | 26.7% | 0.244 | 0.238 |
| Logistic Regression | **62.7%** | **0.644** | **0.636** |
| Linear SVM | 60.0% | 0.627 | 0.608 |

Logistic Regression achieved the strongest overall performance in this experiment.

The dataset is small and imbalanced, particularly for categories such as Client, Spam, and HR, so these results should be interpreted as preliminary rather than production-level performance.