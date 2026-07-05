from dataclasses import dataclass

@dataclass
class Task:
    title: str
    content: str
    due_date: str

    def __eq__(self, other):
        return self.title == other.title and self.content == other.content