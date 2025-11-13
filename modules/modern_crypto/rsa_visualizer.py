from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import math
from sympy import isprime, mod_inverse

class RSAVisualizerModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "RSA"
        self.description = "Визуализация алгоритма RSA и генерации ключей"
        self.category = "modern"
        self.icon = ""
        self.order = 3
        
        # Простые числа для демонстрации (небольшие для наглядности)
        self.demo_primes = {
            "Маленькие (для демонстрации)": [3, 5, 7, 11, 13, 17, 19, 23, 29, 31],
            "Средние (учебные)": [101, 103, 107, 109, 113, 127, 131, 137, 139, 149],
            "Большие (реальные)": [1009, 1013, 1019, 1021, 1031, 1033, 1039, 1049, 1051, 1061]
        }
        
        # Инициализация состояния
        if 'rsa_generated' not in st.session_state:
            st.session_state.rsa_generated = False
        if 'rsa_params' not in st.session_state:
            st.session_state.rsa_params = {}
    
    def render(self):
        st.title("🔑 RSA - Алгоритм шифрования")
        st.subheader("Генерация ключей и шифрование с открытым ключом")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            ### Алгоритм RSA (Rivest–Shamir–Adleman)
            
            **Основные этапы:**
            1. **Генерация ключей:**
               - Выбираем два простых числа `p` и `q`
               - Вычисляем `n = p * q`
               - Вычисляем функцию Эйлера `φ(n) = (p-1)*(q-1)`
               - Выбираем открытую экспоненту `e` (1 < e < φ(n), взаимно простое с φ(n))
               - Вычисляем секретную экспоненту `d = e⁻¹ mod φ(n)`
            
            2. **Шифрование:**
               - Открытый ключ: `(e, n)`
               - Шифрование: `C = Mᵉ mod n`
            
            3. **Дешифрование:**
               - Закрытый ключ: `(d, n)`
               - Дешифрование: `M = Cᵈ mod n`
            
            **Математическая основа:**
            - Теорема Эйлера: `Mᵠ⁽ⁿ⁾ ≡ 1 mod n`
            - Следствие: `Mᵉᵈ ≡ M mod n`
            
            **Безопасность:** Основана на сложности факторизации больших чисел `n = p * q`
            """)
        
        # Если ключи уже сгенерированы, показываем демонстрацию
        if st.session_state.rsa_generated:
            self.show_demo_section()
        else:
            # Выбор режима работы
            mode = st.radio(
                "Режим работы:",
                ["🎯 Автоматическая генерация", "🔧 Ручной ввод параметров"],
                horizontal=True
            )
            
            if mode == "🎯 Автоматическая генерация":
                self.render_auto_mode()
            else:
                self.render_manual_mode()
    
    def render_auto_mode(self):
        """Режим автоматической генерации ключей"""
        st.markdown("### 🎯 Автоматическая генерация ключей RSA")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Выбор размера простых чисел
            prime_size = st.selectbox(
                "Размер простых чисел:",
                list(self.demo_primes.keys()),
                index=0
            )
            
            # Выбор простых чисел
            available_primes = self.demo_primes[prime_size]
            p = st.selectbox("Выберите простое число p:", available_primes, index=0)
            q = st.selectbox("Выберите простое число q:", available_primes, index=1)
            
            # Проверка что p и q разные
            if p == q:
                st.error("p и q должны быть разными простыми числами!")
                return
        
        with col2:
            # Выбор открытой экспоненты
            st.markdown("**Открытая экспонента e:**")
            e_options = {
                "3": 3,
                "17": 17, 
                "65537": 65537,
                "Другая": "custom"
            }
            
            e_choice = st.radio("Стандартные значения:", list(e_options.keys()), horizontal=True)
            
            if e_options[e_choice] == "custom":
                e_custom = st.number_input("Введите e:", min_value=3, max_value=100000, value=17)
                e = e_custom
            else:
                e = e_options[e_choice]
        
        # Генерация ключей
        if st.button("🔑 Сгенерировать ключи", type="primary"):
            with st.spinner("Генерирую ключи..."):
                self.generate_and_show_keys(p, q, e)
    
    def render_manual_mode(self):
        """Режим ручного ввода параметров"""
        st.markdown("### 🔧 Ручной ввод параметров RSA")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Параметры ключей:**")
            p = st.number_input("Простое число p:", min_value=2, max_value=10000, value=61)
            q = st.number_input("Простое число q:", min_value=2, max_value=10000, value=53)
            e = st.number_input("Открытая экспонента e:", min_value=3, max_value=100000, value=17)
            
            # Проверки
            if not isprime(p):
                st.error("p должно быть простым числом!")
                return
            if not isprime(q):
                st.error("q должно быть простым числом!")
                return
            if p == q:
                st.error("p и q должны быть разными!")
                return
        
        with col2:
            st.markdown("**Шифрование/дешифрование:**")
            message = st.number_input(
                "Число для шифрования M:",
                min_value=0,
                max_value=1000,
                value=65,
                help="Должно быть меньше n = p * q"
            )
        
        if st.button("🔐 Выполнить шифрование", type="primary"):
            with st.spinner("Выполняю вычисления..."):
                self.perform_rsa_operations(p, q, e, message)
    
    def generate_and_show_keys(self, p, q, e):
        """Генерирует и показывает ключи RSA"""
        st.markdown("---")
        st.markdown("## 🔑 Генерация ключей RSA")
        
        # Шаг 1: Вычисление n
        st.markdown("### 1. Вычисление модуля n")
        n = p * q
        st.latex(f"n = p \\times q = {p} \\times {q} = {n}")
        
        # Шаг 2: Вычисление φ(n)
        st.markdown("### 2. Вычисление функции Эйлера φ(n)")
        phi_n = (p - 1) * (q - 1)
        st.latex(f"\\phi(n) = (p-1) \\times (q-1) = ({p}-1) \\times ({q}-1) = {phi_n}")
        
        # Шаг 3: Проверка открытой экспоненты e
        st.markdown("### 3. Проверка открытой экспоненты e")
        st.latex(f"e = {e}")
        
        # Проверяем что e и φ(n) взаимно просты
        gcd_e_phi = math.gcd(e, phi_n)
        if gcd_e_phi != 1:
            st.error(f"e и φ(n) не взаимно просты! НОД({e}, {phi_n}) = {gcd_e_phi}")
            st.info("Выберите другое значение e")
            return
        else:
            st.success(f"✓ e и φ(n) взаимно просты (НОД = 1)")
        
        # Шаг 4: Вычисление секретной экспоненты d
        st.markdown("### 4. Вычисление секретной экспоненты d")
        try:
            d = mod_inverse(e, phi_n)
            st.latex(f"d = e^{{-1}} \\mod \\phi(n) = {e}^{{-1}} \\mod {phi_n} = {d}")
            
            # Проверка: e*d ≡ 1 mod φ(n)
            check = (e * d) % phi_n
            if check == 1:
                st.success(f"✓ Проверка: {e} × {d} ≡ 1 mod {phi_n}")
            else:
                st.error(f"Ошибка: {e} × {d} ≡ {check} mod {phi_n}")
                
        except Exception as ex:
            st.error(f"Ошибка вычисления d: {ex}")
            return
        
        # Шаг 5: Итоговые ключи
        st.markdown("### 5. Итоговые ключи")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("**Открытый ключ (public):**")
            st.latex(f"({e}, {n})")
            st.info("Используется для шифрования")
        
        with col2:
            st.success("**Закрытый ключ (private):**")
            st.latex(f"({d}, {n})")
            st.warning("Секретный! Используется для дешифрования")
        
        # Сохраняем параметры в session_state
        st.session_state.rsa_params = {
            'p': p, 'q': q, 'e': e, 'd': d, 'n': n, 'phi_n': phi_n
        }
        st.session_state.rsa_generated = True
        
        # Кнопка для перехода к демонстрации
        st.markdown("---")
        if st.button("🎯 Перейти к демонстрации шифрования", type="primary"):
            st.rerun()
    
    def show_demo_section(self):
        """Показывает раздел демонстрации шифрования"""
        params = st.session_state.rsa_params
        p, q, e, d, n = params['p'], params['q'], params['e'], params['d'], params['n']
        
        # Показываем текущие ключи
        st.markdown("## 🔑 Текущие ключи RSA")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Открытый ключ:** ({e}, {n})")
        with col2:
            st.info(f"**Закрытый ключ:** ({d}, {n})")
        
        # Кнопка для сброса и генерации новых ключей
        if st.button("🔄 Сгенерировать новые ключи"):
            st.session_state.rsa_generated = False
            st.session_state.rsa_params = {}
            st.rerun()
        
        st.markdown("---")
        st.markdown("## 🎯 Демонстрация шифрования")
        
        # Выбор сообщения для демонстрации
        st.markdown("### Выберите сообщение для шифрования:")
        
        # Динамически вычисляем безопасные значения для демонстрации
        safe_values = self.get_safe_demo_values(n)
        
        demo_messages = {
            f"Число {safe_values[0]}": safe_values[0],
            f"Число {safe_values[1]}": safe_values[1],
            f"Число {safe_values[2]}": safe_values[2],
            "Свое число": "custom"
        }
        
        message_choice = st.radio("Примеры:", list(demo_messages.keys()), horizontal=True, key="demo_choice")
        
        if demo_messages[message_choice] == "custom":
            # Безопасное значение по умолчанию - первое из безопасных значений
            default_value = min(42, n-1)  # Не больше n-1
            message = st.number_input(
                "Введите число M:", 
                min_value=0, 
                max_value=n-1, 
                value=default_value, 
                key="custom_message"
            )
        else:
            message = demo_messages[message_choice]
        
        if st.button("🔐 Выполнить шифрование", key="demo_encrypt"):
            # Проверяем что сообщение меньше n
            if message >= n:
                st.error(f"Сообщение M={message} должно быть меньше n={n}")
                return
            
            # Шифрование
            st.markdown("### Процесс шифрования")
            st.latex(f"C = M^e \\mod n = {message}^{{{e}}} \\mod {n}")
            
            cipher = pow(message, e, n)
            st.latex(f"C = {cipher}")
            
            # Дешифрование
            st.markdown("### Процесс дешифрования")
            st.latex(f"M = C^d \\mod n = {cipher}^{{{d}}} \\mod {n}")
            
            decrypted = pow(cipher, d, n)
            st.latex(f"M = {decrypted}")
            
            # Визуализация
            self.plot_rsa_process(message, cipher, decrypted, e, d, n)
            
            # Проверка
            if decrypted == message:
                st.balloons()
                st.success("🎉 Шифрование и дешифрование прошли успешно!")
            else:
                st.error("❌ Ошибка в процессе шифрования/дешифрования")

    def get_safe_demo_values(self, n):
        """Возвращает безопасные значения для демонстрации в зависимости от n"""
        if n <= 10:
            # Очень маленькие n
            return [2, 3, 4]
        elif n <= 50:
            # Маленькие n
            return [5, 10, 15]
        elif n <= 100:
            # Средние n
            return [10, 25, 42]
        elif n <= 1000:
            # Большие n
            return [42, 65, 100]
        else:
            # Очень большие n
            return [65, 100, 255]
    
    def perform_rsa_operations(self, p, q, e, message):
        """Выполняет операции RSA с заданными параметрами"""
        st.markdown("---")
        st.markdown("## 🔐 Операции RSA")
        
        # Вычисляем параметры
        n = p * q
        phi_n = (p - 1) * (q - 1)
        
        # Проверяем сообщение
        if message >= n:
            st.error(f"Сообщение M={message} должно быть меньше n={n}")
            return
        
        # Вычисляем d
        try:
            d = mod_inverse(e, phi_n)
        except:
            st.error("Не удалось вычислить d. Убедитесь что e и φ(n) взаимно просты.")
            return
        
        # Шифрование
        st.markdown("### Шифрование")
        st.latex(f"C = M^e \\mod n = {message}^{{{e}}} \\mod {n}")
        
        cipher = pow(message, e, n)
        st.latex(f"C = {cipher}")
        
        # Дешифрование
        st.markdown("### Дешифрование")
        st.latex(f"M = C^d \\mod n = {cipher}^{{{d}}} \\mod {n}")
        
        decrypted = pow(cipher, d, n)
        st.latex(f"M = {decrypted}")
        
        # Проверка
        if decrypted == message:
            st.success("✓ Шифрование и дешифрование прошли успешно!")
        else:
            st.error("✗ Ошибка: исходное и дешифрованное сообщения не совпадают")
        
        # Показываем ключи
        st.markdown("### Использованные ключи")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Открытый ключ:** ({e}, {n})")
        
        with col2:
            st.info(f"**Закрытый ключ:** ({d}, {n})")
    
    def plot_rsa_process(self, M, C, M_decrypted, e, d, n):
        """Визуализирует процесс RSA"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        
        # График 1: Исходное сообщение
        ax1.bar(['Исходное M'], [M], color='green', alpha=0.7)
        ax1.set_ylabel('Значение')
        ax1.set_title('Исходное сообщение')
        ax1.text(0, M, str(M), ha='center', va='bottom')
        
        # График 2: Зашифрованное сообщение
        ax2.bar(['Зашифрованное C'], [C], color='red', alpha=0.7)
        ax2.set_ylabel('Значение')
        ax2.set_title('Зашифрованное сообщение')
        ax2.text(0, C, str(C), ha='center', va='bottom')
        
        # График 3: Расшифрованное сообщение
        ax3.bar(['Расшифрованное M'], [M_decrypted], color='blue', alpha=0.7)
        ax3.set_ylabel('Значение')
        ax3.set_title('Расшифрованное сообщение')
        ax3.text(0, M_decrypted, str(M_decrypted), ha='center', va='bottom')
        
        # График 4: Сравнение
        values = [M, C, M_decrypted]
        labels = ['Исходное M', 'Зашифрованное C', 'Расшифрованное M']
        colors = ['green', 'red', 'blue']
        
        ax4.bar(labels, values, color=colors, alpha=0.7)
        ax4.set_ylabel('Значение')
        ax4.set_title('Сравнение значений')
        ax4.tick_params(axis='x', rotation=45)
        
        for i, v in enumerate(values):
            ax4.text(i, v, str(v), ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Детальная информация
        st.markdown("#### 📊 Детали процесса:")
        process_data = {
            'Операция': ['Исходное сообщение', 'Шифрование', 'Дешифрование'],
            'Формула': [
                f'M = {M}',
                f'C = {M}**{e} mod {n}',
                f'M = {C}**{d} mod {n}'
            ],
            'Результат': [str(M), str(C), str(M_decrypted)]
        }
        
        st.table(pd.DataFrame(process_data))