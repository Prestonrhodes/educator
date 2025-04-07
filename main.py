import os
from prompt_toolkit import prompt
from educator.core import LLM
from educator.profile import UserProfile
from educator.teacher import Teacher
from educator.game import Game
from rich import print as rprint
import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

def main():
    rprint("[bold white on cyan] Welcome to Educator v1.0 - Learn Anything, Fast! [/bold white on cyan]")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        rprint("[bold red]Yo, set your OPENAI_API_KEY first![/bold red]")
        return
    llm = LLM(api_key=api_key)
    profile = UserProfile()
    game = Game()
    engage_mode = prompt("Enable Engage Mode for a more conversational experience? (yes/no): ").lower() == 'yes'
    topic = prompt("What do you wanna master? ").replace("i want to learn ", "").replace("i want to maste ", "").strip()
    teacher = Teacher(llm, topic, profile, game, engage_mode)

    teacher.start_lesson()
    rprint("[bright_blue]Type 'next' (lesson), 'quiz' (test), 'ask' (question), 'status' (progress), 'export' (save), 'restart' (new topic), 'quit' (exit)[/bright_blue]")

    while True:
        user_input = prompt("> ").lower()
        if "quit" in user_input:
            rprint(f"[bold magenta]Peace out! Points: {game.points} | Level: {game.level} | Mastery: {game.mastery}[/bold magenta]")
            break
        elif "next" in user_input:
            teacher.next_lesson()
        elif "quiz" in user_input:
            teacher.take_quiz()
        elif "ask" in user_input:
            question = prompt("What’s your question? ")
            teacher.handle_question(question)
        elif "status" in user_input:
            rprint(f"[bold magenta]Points: {game.points} | Level: {game.level} | Mastery: {game.mastery}[/bold magenta]")
        elif "restart" in user_input:
            topic = prompt("New topic—what do you wanna master now? ").replace("i want to learn ", "").replace("i want to maste ", "").strip()
            teacher = Teacher(llm, topic, profile, game, engage_mode)
            teacher.start_lesson()
        elif "export" in user_input:
            format_choice = prompt("Save as 'pdf' or 'csv'? ").lower()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            if format_choice == "pdf":
                naming_prompt = f"Generate a concise, professional filename for a PDF export of lessons on {teacher.topic}, including the topic and timestamp {timestamp}. Format as 'Topic_Timestamp.pdf'."
                pdf_filename = llm.generate(naming_prompt, stream=False)
                if not pdf_filename.endswith(".pdf"):
                    pdf_filename += ".pdf"
                doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
                styles = getSampleStyleSheet()
                custom_style = ParagraphStyle(
                    name='Custom',
                    fontSize=12,
                    leading=14,
                    spaceAfter=12,
                )
                story = []
                story.append(Paragraph(f"Educator Lessons on {teacher.topic}", styles['Title']))
                story.append(Spacer(1, 12))
                for lesson in teacher.lesson_history:
                    story.append(Paragraph(lesson, custom_style))
                    story.append(Spacer(1, 12))
                doc.build(story)
                rprint(f"[bold green]Saved lessons to {pdf_filename}[/bold green]")
            elif format_choice == "csv":
                csv_filename = f"{teacher.topic}_educator_lessons_{timestamp}.csv"
                with open(csv_filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Lesson"])
                    for lesson in teacher.lesson_history:
                        writer.writerow([lesson])
                rprint(f"[bold green]Saved lessons to {csv_filename}[/bold green]")
            else:
                rprint("[yellow]Pick 'pdf' or 'csv' next time![/yellow]")
        elif "help" in user_input:
            rprint("[bright_blue]Commands: 'next' (lesson), 'quiz' (test), 'ask' (question), 'status' (progress), 'export' (save), 'restart' (new topic), 'quit' (exit)[/bright_blue]")
        else:
            rprint("[yellow]Huh? Try 'next', 'quiz', 'ask', 'status', 'export', 'restart', 'help', or 'quit'.[/yellow]")

if __name__ == "__main__":
    main()
