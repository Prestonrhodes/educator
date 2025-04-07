# Educator: AI-Powered Learning Framework

Educator is a state-of-the-art, AI-driven learning platform that makes education accessible and engaging. With structured courses, adaptive learning paths, conversational engagement, and voice interaction, it’s perfect for learning anything—from baking cookies to understanding cat behavior.

## Features
- **Structured Courses**: Learn any topic with clear, concise lessons.
- **Adaptive Learning**: Lessons adjust difficulty based on your performance.
- **Engage Mode**: Conversational follow-ups and reflections tied to the content.
- **Voice Mode**: Speak questions and hear lessons narrated.
- **Quizzes**: Challenging questions to test your knowledge.
- **Export**: Save lessons as PDF or CSV with AI-named files.
- **API**: Programmatic access for integration into apps or scripts.

## Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/prestonrhodes/educator.git
   cd educator

python3 -m venv educator_env
source educator_env/bin/activate

pip install prompt_toolkit rich reportlab openai speechrecognition pyttsx3 flask

export OPENAI_API_KEY="your-api-key-here"

python main.py

EXAMPLE: Welcome to Educator v1.0 - Learn Anything, Fast!
Enable Engage Mode? (yes/no): yes
Enable Voice Mode? (yes/no): yes
What do you wanna master? cats
Lesson 1: cats - Part 1
Cats are fascinating pets...
Let’s dig deeper: How often do you notice your cat purring?
Your thoughts (or 'skip'): It purrs a lot when I pet it.
Got it! Let’s keep exploring.
Mini-Lesson: Purring often signals contentment, but can also indicate stress...

Contributing
Fork the repo, make your changes, and submit a pull request. Join our Discord (link coming soon) to share ideas and compete on the leaderboard!

License
MIT License—feel free to use, modify, and share!
