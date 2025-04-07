# Educator: The AI-Powered Learning Framework 🌟📚

Welcome to **Educator**—a groundbreaking, AI-driven learning platform that makes education accessible, engaging, and personalized for *everyone*! Whether you’re mastering baking cookies 🍪, understanding cat behavior 🐾, or diving into coding 💻, Educator adapts to your learning style with structured courses, adaptive paths, conversational engagement, and voice interaction. It’s not just a tool—it’s your personal AI tutor! 🤖

## Why Educator Is a Game-Changer 🚀
Educator isn’t your average learning app—it’s a revolution in ed-tech! Here’s why it’s important:
- **Personalized Learning** 🎯: Adaptive learning paths adjust lesson difficulty based on your performance—no more one-size-fits-all!
- **Conversational Engagement** 💬: Engage Mode asks you thoughtful follow-up questions and reflections tied to the content, making learning feel like a real conversation.
- **Voice Interaction** 🎙️: Speak your questions and hear lessons narrated—perfect for hands-free learning or accessibility.
- **Flexible Deployment** 🌐: Run it locally with your own LLM (like Ollama) or use the OpenAI API (e.g., ChatGPT) for cloud power.
- **Export & Share** 📄: Save your lessons as beautifully formatted PDFs or CSVs with AI-named files—share your learning journey with ease!
- **API Access** 🔌: Integrate Educator into your apps or scripts with a built-in Flask API.

Educator is built for learners, educators, and developers who want to make education fun, interactive, and tailored to individual needs. It’s the future of learning—right now! 🌍

## How It Works: Process Map 🗺️
Here’s how Educator takes you from curious learner to topic master:

Start Learning Journey 🚀
├── Choose Topic 📝 (e.g., "cats")
├── Enable Engage Mode? 💬 (yes/no)
├── Enable Voice Mode? 🎙️ (yes/no)
├── Lesson 1 📚 (AI-generated, adaptive difficulty)
│   ├── Learn Content (streamed in real-time)
│   ├── Engage Mode (if enabled):
│   │   ├── Follow-Up Question (e.g., "How often does your cat purr?")
│   │   ├── Mini-Lesson (based on your response)
│   │   └── Reflection (every 3 lessons, e.g., "How do you feel about your cat’s habits?")
│   └── Voice Mode (if enabled): Hear lesson, speak responses
├── Next Lesson? 🔄 (type "next")
├── Ask a Question? ❓ (type "ask", e.g., "Why does my cat have an infection?")
├── Take a Quiz? 📊 (type "quiz", challenging questions)
├── Switch Topics? 🔄 (type "restart", e.g., switch to "gaming")
├── Export Progress? 📄 (type "export", save as PDF/CSV)
└── Quit When Done 🏁 (type "quit")


### Adaptive Learning in Action 🧠
- **Performance Tracking**: Educator tracks your quiz scores, question responses, and engagement (0-100).
- **Dynamic Adjustment**:
  - Score < 40%: Beginner lessons (simpler content).
  - Score 40-70%: Intermediate lessons (standard content).
  - Score > 70%: Advanced lessons (challenging content).
- **Example**: If you score 30% on a quiz about cat behavior, the next lesson stays beginner-level with more foundational content. Ace it with 80%, and it jumps to advanced topics like feline psychology!

## Getting Started: Setup Guide 🛠️
Let’s get you up and running with Educator in just a few steps! Whether you’re using a local LLM or the OpenAI API, we’ve got you covered.

### Prerequisites
- **Python 3.9+** 🐍: Make sure Python is installed on your system.
- **Git** 📦: To clone the repo.
- **OpenAI API Key** 🔑 (optional): If using OpenAI (e.g., ChatGPT) instead of a local LLM.
- **Local LLM** (optional): If running locally (e.g., Ollama, AnythingLLM).

### Step 1: Clone the Repo 📥
```bash
git clone https://github.com/prestonrhodes/educator.git
cd educator

### Step 2: Set Up a Virtual Environment 🌍
python3 -m venv educator_env
source educator_env/bin/activate

### Step 3: Install Dependencies 📦
pip install prompt_toolkit rich reportlab openai speechrecognition pyttsx3 flask

### Step 4: Configure Your API or Local LLM 🔧
Using OpenAI API (e.g., ChatGPT):
Set your OpenAI API key:y
export OPENAI_API_KEY="your-api-key-here"
The default setup in educator/core.py uses the OpenAI API (gpt-3.5-turbo).
Using a Local LLM (e.g., Ollama):
Install Ollama or your preferred local LLM (e.g., DeepSeek-R1-Distill-Qwen-32B-4bit as you’ve used before).
Update educator/core.py to use your local LLM. Replace the OpenAI client with your local LLM client:

# In educator/core.py
# Comment out OpenAI client
# self.client = OpenAI(api_key=api_key)
# Add your local LLM client (example for Ollama)
from ollama import Client
self.client = Client(host='http://localhost:11434')  # Adjust host/port as needed
self.model = "your-llm-model-name"  # e.g., "deepseek-r1-distill-qwen-32b-4bit"
Modify the generate method in core.py to use your local LLM’s API (example for Ollama):

def generate(self, prompt, system_prompt="", stream=False):
    messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
    messages.append({"role": "user", "content": prompt})
    if stream:
        response = self.client.chat(model=self.model, messages=messages, stream=True)
        for chunk in response:
            yield chunk['message']['content']
    else:
        response = self.client.chat(model=self.model, messages=messages)
        return response['message']['content']

### Step 5: Run Educator 🎉
python main.py

### Process Map: How Educator Works 🗺️
Start Learning Journey 🚀
├── Choose Topic 📝 (e.g., "cats")
├── Enable Engage Mode? 💬 (yes/no)
├── Enable Voice Mode? 🎙️ (yes/no)
├── Lesson 1 📚 (AI-generated, adaptive difficulty)
│   ├── Learn Content (streamed in real-time)
│   ├── Engage Mode (if enabled):
│   │   ├── Follow-Up Question (e.g., "How often does your cat purr?")
│   │   ├── Mini-Lesson (based on your response)
│   │   └── Reflection (every 3 lessons, e.g., "How do you feel about your cat’s habits?")
│   └── Voice Mode (if enabled): Hear lesson, speak responses
├── Next Lesson? 🔄 (type "next")
├── Ask a Question? ❓ (type "ask", e.g., "Why does my cat have an infection?")
├── Take a Quiz? 📊 (type "quiz", challenging questions)
├── Switch Topics? 🔄 (type "restart", e.g., switch to "gaming")
├── Export Progress? 📄 (type "export", save as PDF/CSV)
└── Quit When Done 🏁 (type "quit")

### Adaptive Learning in Action 🧠
Performance Tracking: Educator tracks your quiz scores, question responses, and engagement (0-100).
Dynamic Adjustment:
Score < 40%: Beginner lessons (simpler content).
Score 40-70%: Intermediate lessons (standard content).
Score > 70%: Advanced lessons (challenging content).
Example: If you score 30% on a quiz about cat behavior, the next lesson stays beginner-level with more foundational content. Ace it with 80%, and it jumps to advanced topics like feline psychology!

### Why This Framework Matters 🌟
Educator is a game-changer in ed-tech because it:

Democratizes Learning 🌍: Anyone can learn any topic, at their own pace, with personalized content.
Engages Like a Tutor 💬: Engage Mode makes learning feel like a conversation, not a lecture.
Adapts to You 🧠: Adaptive paths ensure you’re always challenged just the right amount.
Accessible for All 🎙️: Voice Mode makes it hands-free and inclusive for visually impaired users.
Developer-Friendly 🔌: The API lets devs integrate Educator into their own apps or workflows.
Whether you’re a student, educator, or developer, Educator empowers you to learn, teach, and build in ways that were never possible before. It’s the future of education—right now! 🚀

### Contributing 🤝
Want to make Educator even better? Here’s how to contribute:

Fork the repo 🍴
Make your changes (e.g., add new course modules, improve the UI, or enhance the API) ✍️
Submit a pull request 📬
Join our Discord (link coming soon) to share ideas and compete on the leaderboard! 🎮

### License 📜
MIT License—feel free to use, modify, and share! See the  file for details.

### Get in Touch 📩
Got questions or ideas? Reach out on GitHub or join our community on Discord (link coming soon)! Let’s make learning awesome together! 🌟

