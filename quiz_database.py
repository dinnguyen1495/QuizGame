"""
quiz_database.py
    Questions and answers for a quiz game
"""

import requests
import html


class QuizDatabase:
    """
    Class for Quiz
    """
    def __init__(self, amount: int, qtype="boolean", difficulty="any", category=0):
        self.params = {
            'amount': amount,
            'type': qtype
        }
        if difficulty != "any":
            self.params.update({'difficulty': difficulty})
        if 9 <= category <= 32:
            self.params.update({'category': category})
        self.amount = amount
        self.database = self.create_quiz_database()

    def create_quiz_database(self) -> dict[str, bool]:
        """
        Get the questions and answers using Open Trivia Database's API
        Link: https://opentdb.com/api_config.php
        :return: dictionary of questions and their answers in True or False
        """
        database = dict()
        response = requests.get('https://opentdb.com/api.php', params=self.params)
        response.raise_for_status()
        data = response.json() if response and response.status_code == 200 else None
        for question_dict in data["results"]:
            question = html.unescape(question_dict["question"])
            answer = True if question_dict["correct_answer"] == 'True' else False
            database.update({question: answer})
        return database
