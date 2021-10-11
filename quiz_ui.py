"""
quiz_ui.py
    GUI for the quiz game and visualized behaviors
"""

from quiz_brain import QuizBrain
from tkinter import Tk, Frame, Canvas, Button, Label, Radiobutton, StringVar, IntVar, PhotoImage


class QuizUI:
    """
    Class for quiz game's GUI
    """
    def __init__(self):
        """
        Initialize the quiz game and wait for user input for number of questions
        """
        self.score_label = None
        self.notify_label = None
        self.question_counter_label = None
        self.canvas = None
        self.question_text = None
        self.true_button = None
        self.true_label = None
        self.false_button = None
        self.false_label = None
        self.quiz_brain = None
        self.question_counter = None
        self.question = None
        self.answer = None

        self.window = Tk()
        self.window.focus_force()
        self.window.geometry("+400+200")
        self.window.minsize(width=300, height=200)
        self.window.title('Quiz Game')
        self.window.resizable(width=False, height=False)
        self.window.config(padx=20, pady=20)

        self.frame = Frame(self.window)
        self.frame.pack()

        nq_label = Label(self.frame, text='Number of questions')
        nq_label.grid(row=0, column=0, padx=5, pady=5)

        self.number_of_question = IntVar()
        r1 = Radiobutton(self.frame, text='5', variable=self.number_of_question, value=5, command=None)
        r1.grid(row=1, column=0, padx=5, pady=5)
        r2 = Radiobutton(self.frame, text='10', variable=self.number_of_question, value=10, command=None)
        r2.grid(row=2, column=0, padx=5, pady=5)
        r3 = Radiobutton(self.frame, text='20', variable=self.number_of_question, value=20, command=None)
        r3.grid(row=3, column=0, padx=5, pady=5)
        r4 = Radiobutton(self.frame, text='50', variable=self.number_of_question, value=50, command=None)
        r4.grid(row=4, column=0, padx=5, pady=5)
        r5 = Radiobutton(self.frame, text='100', variable=self.number_of_question, value=100, command=None)
        r5.grid(row=5, column=0, padx=5, pady=5)
        r1.select()

        diff_label = Label(self.frame, text='Difficulty')
        diff_label.grid(row=0, column=1, padx=5, pady=5)

        self.difficulty = StringVar()
        d1 = Radiobutton(self.frame, text='Any', variable=self.difficulty, value="any", command=None)
        d1.grid(row=1, column=1, padx=5, pady=5)
        d2 = Radiobutton(self.frame, text='Easy', variable=self.difficulty, value="easy", command=None)
        d2.grid(row=2, column=1, padx=5, pady=5)
        d3 = Radiobutton(self.frame, text='Medium', variable=self.difficulty, value="medium", command=None)
        d3.grid(row=3, column=1, padx=5, pady=5)
        d4 = Radiobutton(self.frame, text='Hard', variable=self.difficulty, value="hard", command=None)
        d4.grid(row=4, column=1, padx=5, pady=5)
        d1.select()

        button = Button(self.frame, text='Start the game', command=self.start_quiz_game)
        button.grid(row=6, column=0, padx=5, pady=5, columnspan=2)

        self.window.mainloop()

    def start_quiz_game(self) -> None:
        """
        Start the quiz game
        """
        self.frame.destroy()
        self.frame = Frame(self.window)
        self.frame.pack()

        self.quiz_brain = QuizBrain(amount=self.number_of_question.get(), difficulty=self.difficulty.get())
        self.question, self.answer = self.quiz_brain.get_question_and_correct_answer()

        self.question_counter = 1
        self.question_counter_label = Label(self.frame,
                                            text=f'Question {self.question_counter}/{self.number_of_question.get()}',
                                            font=('Arial', 15))
        self.question_counter_label.grid(row=0, column=1, padx=5, sticky='e')

        self.notify_label = Label(self.frame, text='', font=('Arial', 15, 'italic'), fg='red')
        self.notify_label.grid(row=0, column=0, padx=5, sticky='w')

        self.canvas = Canvas(self.frame, width=300, height=414)
        bg_img = PhotoImage(file='.//images//background.png')
        self.canvas.create_image(150, 207, image=bg_img)
        self.question_text = self.canvas.create_text(150, 207, text=self.question, font=('Arial', 20, 'bold'),
                                                     fill='black', width=260)
        self.canvas.grid(row=2, column=0, pady=30, columnspan=2)

        self.score_label = Label(self.frame, text='Score: 0', font=('Arial', 15, 'bold'))
        self.score_label.grid(row=3, column=0, pady=10, columnspan=2)

        true_button_img = PhotoImage(file='.//images//true.png')
        self.true_button = Button(self.frame, image=true_button_img, highlightthickness=0, command=self.check_if_true)
        self.true_button.grid(row=4, column=0)

        self.true_label = Label(self.frame, text='True', font=('Arial', 12, 'italic'))
        self.true_label.grid(row=5, column=0)

        false_button_img = PhotoImage(file='.//images//false.png')
        self.false_button = Button(self.frame, image=false_button_img, highlightthickness=0, command=self.check_if_false)
        self.false_button.grid(row=4, column=1)

        self.false_label = Label(self.frame, text='False', font=('Arial', 12, 'italic'))
        self.false_label.grid(row=5, column=1)

        self.window.mainloop()

    def switch_question(self) -> None:
        """
        Change the question and show it. Also increases the question counter
        """
        if self.quiz_brain.get_quiz_amount() == 0:
            self.canvas.itemconfig(self.question_text,
                                   justify='center',
                                   text=f'Your final score: {self.quiz_brain.get_score()}\n\n\n'
                                                            f'✔ to Restart\nX to Exit')
            self.quiz_brain, self.question, self.answer = None, None, None
            return
        self.question, self.answer = self.quiz_brain.get_question_and_correct_answer()
        self.question_counter += 1
        self.canvas.itemconfig(self.question_text, text=self.question)
        self.question_counter_label.config(text=f'Question {self.question_counter}/{self.number_of_question.get()}')

    def check_if_true(self) -> None:
        """
        Behaviors when the player picks a right answer
        """
        if self.quiz_brain is None:
            self.window.destroy()
            self.__init__()
            return
        if self.answer:
            self.quiz_brain.increase_score()
            self.score_label.config(text=f'Score: {self.quiz_brain.get_score()}')
            self.notify_label.config(text='Correct!')
        else:
            self.notify_label.config(text='Wrong!')
        self.switch_question()

    def check_if_false(self) -> None:
        """
        Behaviors when the player picks a wrong answer
        """
        if self.quiz_brain is None:
            self.window.destroy()
            return
        if not self.answer:
            self.quiz_brain.increase_score()
            self.score_label.config(text=f'Score: {self.quiz_brain.get_score()}')
            self.notify_label.config(text='Correct!')
        else:
            self.notify_label.config(text='Wrong!')
        self.switch_question()
