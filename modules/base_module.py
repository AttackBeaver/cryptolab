from abc import ABC, abstractmethod

class CryptoModule(ABC):
    def __init__(self):
        self.name = "Unnamed Module"
        self.description = "No description"
        self.category = "uncategorized"
        self.icon = ""  # Иконка для отображения в интерфейсе
        self.order = 0  # Порядок отображения в категории
    
    @abstractmethod
    def render(self):
        """Основной метод, который вызывает Streamlit"""
        pass
    
    def get_info(self):
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "icon": self.icon,
            "order": self.order
        }