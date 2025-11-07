from modules.base_module import CryptoModule
import streamlit as st

class WelcomeModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Добро пожаловать"
        self.description = "Введение в платформу"
        self.complexity = "beginner"
        self.category = "demo"
    
    def render(self):
        st.title("🔐 CryptoLab - Siberian Professional College")
        st.subheader("Исследуй, взламывай, понимай")
        
        st.markdown("""
        ### Добро пожаловать в интерактивную лабораторию криптографии!
        
        Разработано в рамках дисциплины: "Криптографические средства защиты информации".
        """)
        
        st.success("🚀 Выберите модуль из бокового меню чтобы начать!")