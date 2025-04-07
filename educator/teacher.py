from rich.panel import Panel
from rich import print as rprint
from prompt_toolkit import prompt
import time
try:
    import speech_recognition as sr
    import pyttsx3
except ImportError:
    sr = None
    pyttsx3 = None

class Teacher:
    def __init__(self, llm, topic, profile, game, engage_mode=False, voice_mode=False):
        self.llm = llm
        self.topic = topic
        self.profile = profile
        self.game = game
        self.lesson_history = []
        self.engage_mode = engage_mode
        self.voice_mode = voice_mode and sr is not None and pyttsx3 is not None  # Disable voice if imports fail
        self.lesson_system_prompt = f"Teach {self.topic} interactively. Provide clear, concise lessons with no quizzes or future lesson content—focus only on the current lesson’s teaching material. Build on previous lessons: {', '.join(self.lesson_history)}, adapt to user input, and keep it engaging."
        self.quiz_system_prompt = f"Generate challenging quiz questions for {self.topic} based on all prior lessons: {', '.join(self.lesson_history)}. Make them tough but educational, with multiple-choice options (a, b, c, d), and do NOT include the correct answer in the question."
        self.lesson_num = 1
        self.last_response = ""
        self.performance_score = 0  # Track overall performance (0-100)
        self.performance_history = []  # Track scores for adaptive adjustments
        if self.voice_mode:
            try:
                self.engine = pyttsx3.init()
                self.recognizer = sr.Recognizer()
            except Exception as e:
                rprint(f"[bold red]Voice Mode failed to initialize: {e}. Switching to text mode.[/bold red]")
                self.voice_mode = False
        else:
            self.engine = None
            self.recognizer = None

    def start_lesson(self):
        lesson_text = self.next_lesson()
        if self.engage_mode:
            self._ask_follow_up_question(lesson_text)
        return lesson_text

    def next_lesson(self):
        # Adjust lesson difficulty based on performance
        difficulty = self._get_difficulty()
        lesson_header = f"Lesson {self.lesson_num}: {self.topic} - Part {self.lesson_num}"
        rprint(Panel(lesson_header, title="Lesson", style="bold bright_cyan"))
        if self.voice_mode:
            self.engine.say(lesson_header)
            self.engine.runAndWait()
        rprint("[cyan]Generating lesson...[/cyan]")
        lesson_prompt = f"Give Lesson {self.lesson_num} on {self.topic} at a {difficulty} level (beginner, intermediate, advanced). Focus only on this lesson’s content, building on previous lessons: {', '.join(self.lesson_history)} if any exist. Do not include content for future lessons, quizzes, or unrelated material."
        lesson_text = ""
        for chunk in self.llm.generate(lesson_prompt, self.lesson_system_prompt, stream=True):
            lesson_text += chunk
            print(chunk, end="", flush=True)
            time.sleep(0.05)  # Typing effect
        print()  # Newline after streaming
        rprint(Panel(lesson_text, title="Lesson Recap", style="bright_blue"))
        if self.voice_mode:
            self.engine.say(lesson_text)
            self.engine.runAndWait()
        self.lesson_history.append(f"Lesson {self.lesson_num}: {lesson_text[:50]}...")
        self.game.award_points(5)
        rprint(f"[bold magenta]Progress: [{'#' * (self.lesson_num - 1)}{' ' * (10 - self.lesson_num)}] {self.lesson_num}/10[/bold magenta]")
        rprint("[bold bright_cyan]What’s next? 'next' (lesson), 'quiz' (test), 'ask' (question), 'status' (progress), 'export' (save), 'restart' (new topic), 'quit' (exit)[/bold bright_cyan]")
        self.lesson_num += 1
        if self.engage_mode and self.lesson_num % 3 == 0:
            self._reflection_space(lesson_text)
        return lesson_header + "\n" + lesson_text

    def _get_difficulty(self):
        if not self.performance_history:
            return "beginner"
        avg_score = sum(self.performance_history) / len(self.performance_history)
        self.performance_score = avg_score
        if avg_score < 40:
            return "beginner"
        elif avg_score < 70:
            return "intermediate"
        else:
            return "advanced"

    def _ask_follow_up_question(self, context):
        follow_up_prompt = f"Generate a thoughtful, open-ended follow-up question based on the content: '{context}' on {self.topic}. Make it specific to the content and encourage deeper thinking."
        follow_up = self.llm.generate(follow_up_prompt, stream=False)
        rprint(f"[bold yellow]Let’s dig deeper:[/bold yellow] {follow_up}")
        if self.voice_mode:
            self.engine.say(f"Let’s dig deeper: {follow_up}")
            self.engine.runAndWait()
            user_response = self._voice_input("Your thoughts, or say 'skip' to pass: ")
        else:
            user_response = prompt("Your thoughts (or 'skip'): ")
        if user_response.lower() != 'skip':
            self.last_response = user_response
            rprint("[bright_green]Got it! Let’s keep exploring.[/bright_green]")
            if self.voice_mode:
                self.engine.say("Got it! Let’s keep exploring.")
                self.engine.runAndWait()
            self._adapt_flow(user_response)
            # Score the response for performance
            score_prompt = f"Evaluate the user’s response: '{user_response}' to the question: '{follow_up}' on {self.topic}. Score it 0-100 based on depth and relevance."
            score_text = self.llm.generate(score_prompt, stream=False)
            score_str = ''.join(filter(str.isdigit, score_text.split("score")[-1].split()[0])) if "score" in score_text.lower() else "50"
            try:
                score = int(score_str)
            except ValueError:
                score = 50
            self.performance_history.append(score)
            rprint(f"[bold green]Engagement Score: {score}%[/bold green]")

    def _reflection_space(self, lesson_text):
        reflection_prompt = f"Generate a reflection prompt tied to this lesson content: '{lesson_text}' on {self.topic}. Encourage the user to share insights or feelings about the material."
        reflection = self.llm.generate(reflection_prompt, stream=False)
        rprint(f"[bold yellow]{reflection}[/bold yellow]")
        if self.voice_mode:
            self.engine.say(reflection)
            self.engine.runAndWait()
            user_input = self._voice_input("Your reflection, or say 'skip': ")
        else:
            user_input = prompt("Your reflection (or 'skip'): ")
        if user_input.lower() != 'skip':
            rprint("[bright_green]Thanks for sharing! That adds a lot to our journey.[/bright_green]")
            if self.voice_mode:
                self.engine.say("Thanks for sharing! That adds a lot to our journey.")
                self.engine.runAndWait()
            # Score the reflection for performance
            score_prompt = f"Evaluate the user’s reflection: '{user_input}' on {self.topic}. Score it 0-100 based on depth and insight."
            score_text = self.llm.generate(score_prompt, stream=False)
            score_str = ''.join(filter(str.isdigit, score_text.split("score")[-1].split()[0])) if "score" in score_text.lower() else "50"
            try:
                score = int(score_str)
            except ValueError:
                score = 50
            self.performance_history.append(score)
            rprint(f"[bold green]Reflection Score: {score}%[/bold green]")

    def _adapt_flow(self, user_response):
        adapt_prompt = f"Based on the user’s response: '{user_response}' to a question about {self.topic}, suggest a brief follow-up topic or mini-lesson (1-2 sentences) to deepen their understanding."
        mini_lesson = self.llm.generate(adapt_prompt, stream=False)
        rprint(f"[bold cyan]Mini-Lesson:[/bold cyan] {mini_lesson}")
        if self.voice_mode:
            self.engine.say(mini_lesson)
            self.engine.runAndWait()
        self.lesson_history.append(f"Mini-Lesson: {mini_lesson[:50]}...")

    def _voice_input(self, prompt_text):
        rprint(prompt_text)
        if self.voice_mode:
            self.engine.say(prompt_text)
            self.engine.runAndWait()
            with sr.Microphone() as source:
                try:
                    audio = self.recognizer.listen(source, timeout=5)
                    return self.recognizer.recognize_google(audio)
                except sr.UnknownValueError:
                    rprint("[yellow]Sorry, I didn’t catch that. Please type your response instead.[/yellow]")
                    return prompt("Type your response: ")
                except sr.RequestError:
                    rprint("[yellow]Voice recognition failed. Please type your response instead.[/yellow]")
                    return prompt("Type your response: ")
        else:
            return prompt("Type your response: ")

    def take_quiz(self):
        quiz_prompt = f"Generate a challenging quiz question about {self.topic} based on all lessons so far: {', '.join(self.lesson_history)}. Provide four multiple-choice options (a, b, c, d), but do NOT include the correct answer."
        quiz = self.llm.generate(quiz_prompt, self.quiz_system_prompt, stream=False)
        rprint(Panel(quiz, title="Quiz", style="bold yellow"))
        if self.voice_mode:
            self.engine.say(quiz)
            self.engine.runAndWait()
            user_input = self._voice_input("Your answer (a, b, c, or d): ")
        else:
            user_input = prompt("Your answer (a, b, c, or d): ")
        check_prompt = f"User answered '{user_input}' to this quiz: '{quiz}'. Evaluate it, score 0-100, and provide detailed feedback with the correct answer to help the user learn."
        check = self.llm.generate(check_prompt, self.lesson_system_prompt, stream=False)
        rprint(Panel(check, title="Answer Check", style="bright_green"))
        score_str = ''.join(filter(str.isdigit, check.split("score")[-1].split()[0])) if "score" in check.lower() else "50"
        try:
            score = int(score_str)
        except ValueError:
            score = 50  # Fallback if score parsing fails
        points = max(5, score // 10)  # 5-10 points based on score
        self.game.award_points(points)
        self.performance_history.append(score)  # Track quiz score for performance
        rprint(f"[bold green]Score: {score}% | +{points} points![/bold green]")
        rprint("[bold bright_cyan]What’s next? 'next' (lesson), 'quiz' (test), 'ask' (question), 'status' (progress), 'export' (save), 'restart' (new topic), 'quit' (exit)[/bold bright_cyan]")
        if self.engage_mode:
            self._ask_follow_up_question(check)
        return f"Quiz: {quiz}\nAnswer: {user_input}\nFeedback: {check}\nScore: {score}% | Points: +{points}"

    def handle_question(self, question):
        response = self.llm.generate(f"User asked: '{question}'. Answer it and tie it to {self.topic}, considering {', '.join(self.lesson_history)}.", self.lesson_system_prompt, stream=False)
        rprint(Panel(response, title="AI Response", style="bright_green"))
        if self.engage_mode:
            self._ask_follow_up_question(response)
        rprint("[bold bright_cyan]What’s next? 'next' (lesson), 'quiz' (test), 'ask' (question), 'status' (progress), 'export' (save), 'restart' (new topic), 'quit' (exit)[/bold bright_cyan]")
        return f"Question: {question}\nAnswer: {response}"
