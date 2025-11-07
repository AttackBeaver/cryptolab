from abc import ABC, abstractmethod

class CryptoModule(ABC):
    def __init__(self):
        self.name = "Unnamed Module"
        self.description = "No description"
        self.complexity = "beginner"
        self.category = "uncategorized"

    @abstractmethod
    def render(self):
        """Основной метод, который вызывает Streamlit"""
        pass

    def get_info(self):
        return {
            "name": self.name,
            "description": self.description,
            "complexity": self.complexity,
            "category": self.category
        }
