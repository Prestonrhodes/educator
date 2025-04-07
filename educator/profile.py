class UserProfile:
    def __init__(self):
        self.style = "default"

    def adjust_style(self, feedback):
        if "simple" in feedback.lower():
            self.style = "simple"
        elif "examples" in feedback.lower():
            self.style = "example-heavy"
        elif "technical" in feedback.lower():
            self.style = "technical"
        print(f"Teaching style adjusted to: {self.style}")
