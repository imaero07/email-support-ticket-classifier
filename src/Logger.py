import logging

class Logger:
    def __init__(self, debug):
        self.categories = dict()
        self.total_emails = 0
        self.errors = 0
        level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler("../Emails.log", encoding="utf-8"),
                logging.StreamHandler()
            ]
        )

    def email_log(self, email, category):
        self.categories[category] = self.categories.get(category, 0) + 1
        self.total_emails += 1
        if not email.correct:
            self.errors += 1

    def result_report(self):
        res = ""
        res += f"Всего писем: {self.total_emails}\n"
        res += f"Из них некорректных писем: {self.errors}\n"
        for category, count in self.categories.items():
            res += f"В категории {category} писем: {count}\n"
        return res
