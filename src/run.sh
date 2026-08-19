#!/bin/bash
echo "Запуск сортировщика писем"
if ! command -v python3 &> /dev/null; then
    echo "Ошибка: python3 не установлен"
    exit 1
fi
echo "Обработка писем"
python3 main.py --input ../inbox --output ../ --ml
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "Обработка завершена успешно"
else
    echo "Произошла ошибка при обработке (код $EXIT_CODE)"
    exit 1
fi