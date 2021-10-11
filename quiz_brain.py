"""
quiz_brain.py
    Control the behaviors of a quiz game
"""

from quiz_database import QuizDatabase


class QuizBrain:
    """
    Class for the quiz game controller
    """
    def __init__(self, amount=10, difficulty="any"):
        self.suite = QuizDatabase(amount=amount, difficulty=difficulty)
        self.score = 0

    def get_question_and_correct_answer(self) -> tuple[str, bool]:
        return self.suite.database.popitem()

    def increase_score(self):
        self.score += 1

    def get_score(self) -> int:
        return self.score

    def get_quiz_amount(self) -> int:
        return len(self.suite.database)
