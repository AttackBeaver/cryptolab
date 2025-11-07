import streamlit as st
from modules.demo.welcome import WelcomeModule
from modules.classical_ciphers.caesar import CaesarCipherModule

# Настройка страницы
st.set_page_config(
    page_title="CryptoLab - Siberian Professional College",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

class CryptoLabApp:
    def __init__(self):
        self.modules = self.load_modules()
    
    def load_modules(self):
        """Загружаем модули вручную (потом автоматизируем)"""
        return {
            "welcome": WelcomeModule(),
            "caesar": CaesarCipherModule()
        }
    
    def render_sidebar(self):
        """Отрисовка навигации в сайдбаре"""
        st.sidebar.title("🔐 CryptoLab")
        st.sidebar.markdown("---")
        
        # Выбор модуля
        module_names = {name: module.name for name, module in self.modules.items()}
        selected_module = st.sidebar.selectbox(
            "Выберите модуль:",
            options=list(module_names.keys()),
            format_func=lambda x: module_names[x]
        )
        
        # Информация о выбранном модуле
        current_module = self.modules[selected_module]
        st.sidebar.markdown("---")
        st.sidebar.info(f"""
        **{current_module.name}**
        
        {current_module.description}
        
        """)
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
            <div style='text-align: center; color: var(--text-color);'>
                <small>© 2025 БПОУ ОО «Сибирский профессиональный колледж»</small><br>
                <small>Преподаватель/Разработчик: <strong>Стариков А.В.</strong></small>
            </div>
            """, unsafe_allow_html=True)
        
        return selected_module
    
    def run(self):
        """Запуск приложения"""
        selected_module = self.render_sidebar()
        
        # Отрисовка выбранного модуля
        module = self.modules[selected_module]
        module.render()

# Запуск приложения
if __name__ == "__main__":
    app = CryptoLabApp()
    app.run()