from rich import print as rprint

class Game:
    def __init__(self):
        self.points = 0

    def award_points(self, amount):
        self.points += amount
        rprint(f"[bold green]+{amount} points! Total: {self.points}[/bold green]")
        if self.points >= 100 and self.level == 1:
            rprint("[bold yellow]Level Up! You’re now Intermediate![/bold yellow]")
        elif self.points >= 200 and self.level == 2:
            rprint("[bold yellow]Level Up! You’re now Advanced![/bold yellow]")

    @property
    def level(self):
        return self.points // 100  # Level up every 100 points

    @property
    def mastery(self):
        if self.points < 100:
            return "Beginner"
        elif self.points < 200:
            return "Intermediate"
        else:
            return "Advanced"
