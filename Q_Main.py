import json
import random
from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, END, N, S, E, W
from datetime import datetime

class japaneseQuiz:
    def __init__(self, master):
        self.master = master
        master.title("japanese Quiz")
        master.geometry("800x800")
        master.resizable(False, False)

        # Load the data from the JSON file (wip)
        with open('term_meta_bank_1.json', 'r', encoding='utf-8') as file:
            self.data = json.load(file)

        # Set your desired frequency range
        self.min_frequency = 200
        self.max_frequency = 1000

        # Filter the data based on frequency range
        self.filtered_data = self.filter_by_frequency(self.data, self.min_frequency, self.max_frequency)

        # Set the number of questions for the quiz
        self.num_questions = 3

        # Initialise variables
        self.current_question = 0
        self.quiz_results = []

        # Font size adjustment
        self.font_size = 12

        # Create GUI elements
        self.label_question = Label(master, text="What is the reading for the japanese word:", font=("Calibri", self.font_size))
        self.entry_answer = Entry(master, font=("Calibri", self.font_size))
        self.button_submit = Button(master, text="Submit", command=self.check_answer, font=("Calibri", self.font_size))

        # Bind Enter key to submit button
        master.bind('<Return>', lambda event=None: self.button_submit.invoke())

        # Place GUI elements on the window
        self.label_question.grid(row=0, column=0, columnspan=2, sticky=W, padx=25, pady=15)
        self.entry_answer.grid(row=1, column=0, columnspan=2, sticky=W+E, padx=25, pady=15)
        self.button_submit.grid(row=2, column=0, columnspan=2, sticky=W+E, padx=25, pady=15)

        # Create a Text widget for displaying questions and answers
        self.text_results = Text(master, wrap="word", font=("Calibri", self.font_size))
        self.text_results.config(state="disabled")  # Make the Text widget read-only
        self.scrollbar_results = Scrollbar(master, command=self.text_results.yview)
        self.text_results['yscrollcommand'] = self.scrollbar_results.set

        # Place the Text widget and Scrollbar on the window
        self.text_results.grid(row=3, column=0, columnspan=2, sticky=W+E, padx=25, pady=15)
        self.scrollbar_results.grid(row=3, column=2, sticky=N+S)

        # Initialise
        self.load_question()

    def filter_by_frequency(self, data, min_frequency, max_frequency):
        return [item for item in data if 'frequency' in item[2] 
                and 'value' in item[2]['frequency'] 
                and min_frequency <= item[2]['frequency']['value'] <= max_frequency]

    def load_question(self):
        if self.current_question < self.num_questions:
            random_item = random.choice(self.filtered_data)
            self.correct_reading = random_item[2]['reading']
            self.japanese_word = random_item[0]

            self.label_question.config(text=f"What is the reading for the japanese word: {self.japanese_word}")
            self.entry_answer.delete(0, 'end')  # Clears
        else:
            self.show_results()

    def check_answer(self):
        user_input = self.entry_answer.get()
        is_correct = user_input == self.correct_reading
        result = {
            'japanese_word': self.japanese_word,
            'correct_reading': self.correct_reading,
            'user_input': user_input,
            'is_correct': is_correct
        }
        self.quiz_results.append(result)

        feedback = f"{len(self.quiz_results)}. {result['japanese_word']} - Your answer: {result['user_input']} - Correct reading: {result['correct_reading']} - {'Correct' if result['is_correct'] else 'Incorrect'}\n"

        # Display feedback in the Text widget
        self.text_results.config(state="normal")  # Allow modifications
        self.text_results.insert(END, feedback)  # Insert new feedback
        self.text_results.config(state="disabled")  # Make the Text widget read-only again

        self.current_question += 1
        self.load_question()

    def show_results(self):
        results_text = self.text_results.get(1.0, END)  # Get existing content
        results_text += "\nQuiz completed. Showing results:\n"
        for idx, result in enumerate(self.quiz_results, start=1):
            css_class = 'correct' if result['is_correct'] else 'incorrect'
            results_text += f"{idx}. {result['japanese_word']} - Your answer: {result['user_input']} - Correct reading: {result['correct_reading']} - {'Correct' if result['is_correct'] else 'Incorrect'}\n"

        # Display results in the Text widget
        self.text_results.config(state="normal")  # Allow modifications
        self.text_results.delete(1.0, END)  # Clear previous content
        self.text_results.insert(END, results_text)  # Insert new content
        self.text_results.config(state="disabled")  # Make the Text widget read-only again

        # Generate HTML page with quiz results
        self.generate_html()

        # Close the GUI window after the quiz is completed
        self.master.destroy()

    def generate_html(self):
        try:
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            html_filename = f"C:/Projects/Project-JPQ2023/quiz_results_{current_datetime}.html"

            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Quiz Results - {current_datetime}</title>
                <style>
                    body {{
                        font-family: 'Calibri', sans-serif;
                        background-color: #f4f4f4;
                        color: #333;
                        margin: 20px;
                    }}
                    h1 {{
                        color: #007BFF;
                    }}
                    p {{
                        margin-bottom: 8px;
                    }}
                    .correct {{
                        color: #28a745;
                    }}
                    .incorrect {{
                        color: #dc3545;
                    }}
                }}
                </style>
            </head>
            <body>
                <h1>Quiz Results - {current_datetime}</h1>
            """

            for result in self.quiz_results:
                css_class = 'correct' if result['is_correct'] else 'incorrect'
                html_content += f"<p class='{css_class}'>{result['japanese_word']} - Your answer: {result['user_input']} - Correct reading: {result['correct_reading']} - {'Correct' if result['is_correct'] else 'Incorrect'}</p>"

            html_content += """
                <script>
                    // Potential JS for later
                </script>
            </body>
            </html>
            """

            with open(html_filename, 'w', encoding='utf-8') as html_file:
                html_file.write(html_content)

            print(f"HTML file created successfully: {html_filename}")

        except Exception as e:
            print(f"An error occurred while creating the HTML file: {e}")

if __name__ == "__main__":
    root = Tk()
    app = japaneseQuiz(root)
    root.mainloop()
