class Email:
    def __init__(self, recipient, sender, subject, body, source_path, correct=True):
        self.recipient = recipient.lower()
        self.sender = sender.lower()
        self.subject = subject.lower()
        self.body = body.lower()
        self.source_path = source_path
        self.correct = correct