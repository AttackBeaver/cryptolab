import streamlit as st
from datetime import datetime
from utils.module_loader import ModuleLoader

# Настройка страницы
st.set_page_config(
    page_title="CryptoLab - Siberian Professional College",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

class CryptoLabApp:
    def __init__(self):
        self.module_loader = ModuleLoader()
        self.modules = {}
        self.categories = {}
        self.load_all_modules()
    
    def load_all_modules(self):
        """Загружает все модули автоматически"""
        self.modules = self.module_loader.discover_modules()
        self.categories = self.module_loader.get_modules_by_category()
    
    def render_sidebar(self):
        """Отрисовка чистого и минималистичного сайдбара"""       
        # Заголовок
        st.sidebar.title("CryptoLab")
        st.sidebar.caption("Лаборатория криптографии")
        
        # Кнопка "На главную"
        if st.session_state.get('selected_module_id'):
            if st.sidebar.button(
                "🏠",
                key="home_button",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state.selected_module_id = None
                st.rerun()
                
        # Навигация по модулям
        self.render_module_navigation()
                
        return st.session_state.get('selected_module_id')
    
    def render_module_navigation(self):
        """Отрисовывает чистую навигацию по модулям"""
        
        # Конфигурация категорий
        category_config = {
            "math": {"icon": "", "name": "Математические основы криптографии"},
            "classical": {"icon": "", "name": "Классические шифры"},
            "cryptanalysis": {"icon": "", "name": "Криптоанализ"},
            "modern": {"icon": "", "name": "Современная криптография"},
            "protocols": {"icon": "", "name": "Протоколы"},
            "hash": {"icon": "", "name": "Хеш-функции"},
            "stream": {"icon": "", "name": "Поточное шифрование"}
        }
        
        # Порядок категорий
        category_order = ["math","classical", "cryptanalysis", "modern", "protocols", "hash", "stream"]
        
        # Отрисовываем категории и модули
        for category in category_order:
            if category in self.categories and self.categories[category]:
                config = category_config.get(category, {"icon": "", "name": category.title()})
                
                # Expander для категории
                with st.sidebar.expander(f"{config['icon']} {config['name']}", expanded=False):
                    # Сортируем модули по порядку
                    modules = sorted(self.categories[category], key=lambda x: x.order)
                    
                    for module in modules:
                        module_id = next((mid for mid, m in self.modules.items() if m == module), None)
                        if module_id:
                            # Простая кнопка без лишней информации
                            is_selected = st.session_state.get('selected_module_id') == module_id
                            
                            if st.button(
                                f"{module.icon} {module.name}",
                                key=f"nav_{module_id}",
                                use_container_width=True,
                                type="primary" if is_selected else "secondary"
                            ):
                                st.session_state.selected_module_id = module_id
                                st.rerun()
        
    def render_main_content(self, selected_module_id):
        """Отрисовка основного контента"""
        if selected_module_id and selected_module_id in self.modules:
            # Показываем выбранный модуль
            module = self.modules[selected_module_id]
            module.render()
        else:
            # Показываем стартовую страницу
            self.render_welcome()
    
    def render_welcome(self):
        """Главная стартовая страница"""                
        st.title("🔐 CryptoLab - Siberian Professional College")
        st.markdown("Лаборатория криптографии и защиты информации")
        
        st.markdown("---")
        
        # Основное описание
        st.markdown("""
        ### Образовательная платформа
        
        **CryptoLab** - это интерактивная среда для изучения криптографических алгоритмов и методов защиты информации, 
        разработанная для студентов направлений **ИТ и Информационная безопасность**.
        """)
        
        st.markdown("---")
        col6, col7 = st.columns(2)
        
        with col6:
            st.markdown("""
            ### Что вы найдете здесь:
            
            - **Классические шифры** - исторические алгоритмы от Цезаря до Виженера
            - **Криптоанализ** - методы взлома и анализа шифров
            - **Современные алгоритмы** - актуальные криптографические методы
            - **Интерактивные демонстрации** - визуализация работы алгоритмов
            """)
        with col7:
            st.markdown("""
            ### Как начать:
            
            Выберите интересующий модуль в **левом меню** → изучите теорию → экспериментируйте с параметрами → анализируйте результаты.
            
            **Рекомендуем начать с Математических основ** - это БАЗА.
            """)
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            # Информация о дисциплинах
            st.markdown("### Дисциплины")
            st.markdown("""
            - **Криптографические средства защиты информации**
            - **Криптографические методы защиты информации**
            - **Основы криптографии**
            """)
        with col2:
            # Минималистичная статистика
            st.markdown("### О платформе")
            st.markdown(f"""
            - **Модулей:** {len(self.modules)}
            - **Обновлено:** {datetime.now().strftime('%d.%m.%Y')}
            """)
        
        # Дополнительная информация в отдельной секции
        st.markdown("---")
        
        col3, col4, col5 = st.columns(3)
        
        with col3:
            st.markdown("### Образовательные цели")
            st.markdown("""
            - Понимание принципов работы алгоритмов
            - Развитие аналитического мышления
            - Визуализация криптографических процессов
            """)
        with col4:
            st.markdown("### Методики")
            st.markdown("""
            - Интерактивные эксперименты
            - Пошаговая визуализация
            - Анализ результатов
            """)
        with col5:
            st.markdown("### Технологии")
            st.markdown("""
            - Streamlit
            - Cryptography
            - Matplotlib
            - NumPy
            """)
    
    def render_footer(self):
        """Футер"""
        st.markdown("---")
        current_year = datetime.now().year
        st.markdown(
            f"""
            <div style='text-align: center; padding: 2rem 0; color: #666; font-size: 0.9rem;'>
                <div>БПОУ ОО «Сибирский профессиональный колледж»</div>
                <div>© {current_year} Преподаватель: <strong>Стариков А.В.</strong></div>
                <div style='margin-top: 0.5rem; font-size: 0.8rem;'>Направления: Информационные технологии • Информационная безопасность</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def run(self):
        """Запуск приложения"""
        selected_module_id = self.render_sidebar()
        self.render_main_content(selected_module_id)
        self.render_footer()

# Запуск приложения
if __name__ == "__main__":
    app = CryptoLabApp()
    app.run()