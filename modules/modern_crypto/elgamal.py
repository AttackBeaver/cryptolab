from modules.base_module import CryptoModule
import streamlit as st
import secrets
import random
from typing import List, Tuple, Dict
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass
import hashlib

@dataclass
class ElGamalKeyPair:
    private: int
    public: int
    p: int
    g: int

@dataclass
class ElGamalCiphertext:
    c1: int
    c2: int

class ElGamalModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Шифрование Эль-Гамаля"
        self.description = "Асимметричное шифрование на основе дискретного логарифмирования"
        self.category = "modern"
        self.icon = ""
        self.order = 10
        
        # Предварительно вычисленные безопасные простые числа для демонстрации
        self.demo_primes = {
            256: {
                "p": 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
                "g": 2
            },
            512: {
                "p": 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD97,
                "g": 2
            },
            1024: {
                "p": 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF4F,
                "g": 2
            }
        }

    def render(self):
        st.title("🎯 Шифрование Эль-Гамаля")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **Шифрование Эль-Гамаля** - алгоритм с открытым ключом, основанный на проблеме дискретного логарифмирования.
            
            ### 🎯 Историческая справка:
            - **Разработан**: 1985 год, Тахер Эль-Гамаль
            - **Основа**: Проблема дискретного логарифмирования
            - **Применение**: SSL/TLS, PGP, цифровые подписи
            
            ### 🔐 Математические основы:
            
            **Генерация ключей:**
            ```
            1. Выбирается большое простое число p
            2. Выбирается генератор g мультипликативной группы Zp*
            3. Выбирается закрытый ключ: x ∈ [1, p-2]  
            4. Вычисляется открытый ключ: y = g^x mod p
            ```
            
            **Шифрование сообщения M:**
            ```
            1. Выбирается случайное k ∈ [1, p-2]
            2. Вычисляется c1 = g^k mod p
            3. Вычисляется c2 = M * y^k mod p
            4. Шифротекст: (c1, c2)
            ```
            
            **Дешифрование:**
            ```
            1. Вычисляется s = c1^x mod p
            2. Вычисляется s^(-1) mod p  
            3. M = c2 * s^(-1) mod p
            ```
            
            ### 🛡️ Свойства безопасности:
            - **Стойкость**: Основана на сложности дискретного логарифмирования
            - **Probabilistic**: Одно сообщение дает разные шифротексты
            - **Гомоморфность**: Поддерживает мультипликативную гомоморфность
            - **Размер**: Шифротекст в 2 раза больше открытого текста
            
            ### ⚠️ Особенности:
            - Требует случайного k для каждого сообщения
            - Уязвим к атакам при повторном использовании k
            - Медленнее симметричных алгоритмов
            """)

        st.markdown("---")
        
        # Основной интерфейс с вкладками
        tab1, tab2, tab3, tab4 = st.tabs(["🔑 Генерация ключей", "🔐 Шифрование", "🔓 Дешифрование", "🎯 Визуализация"])

        with tab1:
            self.render_key_generation()
        
        with tab2:
            self.render_encryption_section()
            
        with tab3:
            self.render_decryption_section()
            
        with tab4:
            self.render_visualization_section()

    def render_key_generation(self):
        """Генерация ключевой пары Эль-Гамаля"""
        st.header("🔑 Генерация ключевой пары Эль-Гамаля")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⚙️ Параметры системы")
            
            # Выбор размера ключа
            key_size = st.selectbox(
                "Размер модуля p:",
                [256, 512, 1024],
                index=1,
                key="key_size_select",
                format_func=lambda x: f"{x} бит"
            )
            
            # Параметры
            params = self.demo_primes[key_size]
            
            st.text_input(
                "Простое число p:",
                hex(params["p"]),
                disabled=True,
                key="p_display"
            )
            
            st.text_input(
                "Генератор g:",
                str(params["g"]),
                disabled=True,
                key="g_display"
            )
            
            # Генерация ключей
            if st.button("🎲 Сгенерировать ключевую пару", key="gen_keys_btn", use_container_width=True):
                private_key = secrets.randbelow(params["p"] - 2) + 1
                public_key = pow(params["g"], private_key, params["p"])
                
                key_pair = ElGamalKeyPair(
                    private=private_key,
                    public=public_key,
                    p=params["p"],
                    g=params["g"]
                )
                
                st.session_state.elgamal_key_pair = key_pair
                st.rerun()
        
        with col2:
            st.subheader("🔑 Результаты")
            
            if 'elgamal_key_pair' in st.session_state:
                key_pair = st.session_state.elgamal_key_pair
                
                st.success("✅ Ключевая пара сгенерирована!")
                
                st.text_area(
                    "Закрытый ключ (x):",
                    hex(key_pair.private),
                    height=80,
                    key="private_key_display"
                )
                
                st.text_area(
                    "Открытый ключ (y = g^x mod p):",
                    hex(key_pair.public),
                    height=80,
                    key="public_key_display"
                )
                
                # Детали ключей
                with st.expander("🔍 Детали ключей"):
                    self.display_key_details(key_pair)
            else:
                st.info("👆 Сгенерируйте ключевую пару для отображения")

    def render_encryption_section(self):
        """Шифрование сообщения"""
        st.header("🔐 Шифрование сообщения")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📨 Входные данные")
            
            message = st.text_area(
                "Сообщение для шифрования:",
                "Hello ElGamal!",
                height=100,
                key="enc_message"
            )
            
            public_key = st.text_input(
                "Открытый ключ получателя (hex):",
                st.session_state.get('elgamal_key_pair', '').public if 'elgamal_key_pair' in st.session_state else '',
                key="enc_public_key"
            )
            
            p_hex = st.text_input(
                "Модуль p (hex):",
                hex(st.session_state.elgamal_key_pair.p) if 'elgamal_key_pair' in st.session_state else hex(self.demo_primes[512]["p"]),
                key="enc_p"
            )
            
            g = st.number_input(
                "Генератор g:",
                value=2,
                key="enc_g"
            )
            
            if st.button("🔒 Зашифровать", key="encrypt_btn", use_container_width=True):
                if message and public_key and p_hex:
                    try:
                        p = int(p_hex, 16)
                        public_key_int = int(public_key, 16)
                        
                        ciphertext = self.elgamal_encrypt(message, public_key_int, p, g)
                        
                        st.session_state.ciphertext = ciphertext
                        st.session_state.encrypted_message = message
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Ошибка шифрования: {e}")
                else:
                    st.error("⚠️ Заполните все поля")
        
        with col2:
            st.subheader("📄 Результат шифрования")
            
            if 'ciphertext' in st.session_state:
                ciphertext = st.session_state.ciphertext
                
                st.success("✅ Сообщение зашифровано!")
                
                st.text_input(
                    "Компонент c1 (g^k mod p):",
                    hex(ciphertext.c1),
                    key="c1_display"
                )
                
                st.text_input(
                    "Компонент c2 (M * y^k mod p):", 
                    hex(ciphertext.c2),
                    key="c2_display"
                )
                
                st.text_area(
                    "Полный шифротекст (hex):",
                    f"{ciphertext.c1:0{len(hex(ciphertext.c1))-2}X}{ciphertext.c2:0{len(hex(ciphertext.c2))-2}X}",
                    height=100,
                    key="full_ciphertext_display"
                )
                
                # Детали шифрования
                with st.expander("🔍 Детали процесса шифрования"):
                    self.display_encryption_details(st.session_state.encrypted_message, ciphertext)
            else:
                st.info("👆 Зашифруйте сообщение для отображения")

    def render_decryption_section(self):
        """Дешифрование сообщения"""
        st.header("🔓 Дешифрование сообщения")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📨 Зашифрованное сообщение")
            
            c1_hex = st.text_input(
                "Компонент c1 (hex):",
                st.session_state.get('ciphertext', '').c1 if 'ciphertext' in st.session_state else '',
                key="dec_c1"
            )
            
            c2_hex = st.text_input(
                "Компонент c2 (hex):",
                st.session_state.get('ciphertext', '').c2 if 'ciphertext' in st.session_state else '',
                key="dec_c2"
            )
            
            private_key = st.text_input(
                "Закрытый ключ (hex):",
                hex(st.session_state.elgamal_key_pair.private) if 'elgamal_key_pair' in st.session_state else '',
                key="dec_private_key"
            )
            
            p_hex = st.text_input(
                "Модуль p (hex):",
                hex(st.session_state.elgamal_key_pair.p) if 'elgamal_key_pair' in st.session_state else hex(self.demo_primes[512]["p"]),
                key="dec_p"
            )
            
            if st.button("🔓 Дешифровать", key="decrypt_btn", use_container_width=True):
                if c1_hex and c2_hex and private_key and p_hex:
                    try:
                        c1 = int(c1_hex, 16)
                        c2 = int(c2_hex, 16)
                        private_key_int = int(private_key, 16)
                        p = int(p_hex, 16)
                        
                        ciphertext = ElGamalCiphertext(c1, c2)
                        plaintext = self.elgamal_decrypt(ciphertext, private_key_int, p)
                        
                        st.session_state.decrypted_message = plaintext
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Ошибка дешифрования: {e}")
                else:
                    st.error("⚠️ Заполните все поля")
        
        with col2:
            st.subheader("📄 Результат дешифрования")
            
            if 'decrypted_message' in st.session_state:
                st.success("✅ Сообщение дешифровано!")
                
                st.text_area(
                    "Дешифрованное сообщение:",
                    st.session_state.decrypted_message,
                    height=150,
                    key="decrypted_message_display"
                )
                
                # Проверка совпадения с исходным сообщением
                if 'encrypted_message' in st.session_state:
                    if st.session_state.decrypted_message == st.session_state.encrypted_message:
                        st.success("🎉 Сообщение корректно дешифровано!")
                    else:
                        st.error("❌ Дешифрованное сообщение не совпадает с исходным!")
                
                # Детали дешифрования
                with st.expander("🔍 Детали процесса дешифрования"):
                    self.display_decryption_details(st.session_state.decrypted_message)
            else:
                st.info("👆 Дешифруйте сообщение для отображения")

    def render_visualization_section(self):
        """Визуализация работы алгоритма"""
        st.header("🎯 Визуализация алгоритма Эль-Гамаля")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Параметры демонстрации")
            
            demo_message = st.text_input(
                "Сообщение для демонстрации:",
                "TEST",
                key="demo_message"
            )
            
            demo_p = st.number_input(
                "Модуль p (для демонстрации):",
                min_value=100,
                max_value=100000,
                value=10007,
                key="demo_p"
            )
            
            demo_g = st.number_input(
                "Генератор g:",
                min_value=2,
                max_value=100,
                value=5,
                key="demo_g"
            )
            
            if st.button("▶️ Запустить демонстрацию", key="demo_btn"):
                if demo_message:
                    self.visualize_elgamal_process(demo_message, demo_p, demo_g)
        
        with col2:
            st.subheader("🏗️ Структура алгоритма")
            
            # Схема алгоритма
            st.markdown("""
            **Схема шифрования Эль-Гамаля:**
            
            ```
            Генерация ключей:
            ----------------
            x = случайное число ∈ [1, p-2]
            y = g^x mod p
            
            Шифрование:
            -----------
            k = случайное число ∈ [1, p-2]  
            c1 = g^k mod p
            c2 = M * y^k mod p
            
            Дешифрование:
            -------------
            s = c1^x mod p
            s_inv = s^(-1) mod p
            M = c2 * s_inv mod p
            ```
            """)
            
            # Свойства
            st.markdown("""
            **Ключевые свойства:**
            - ✅ Probabilistic шифрование
            - ✅ Стойкость к IND-CPA
            - ✅ Гомоморфное умножение
            - ❌ Детерминированное шифрование
            - ❌ Стойкость к IND-CCA2
            """)

    def display_key_details(self, key_pair: ElGamalKeyPair):
        """Отображает детали ключевой пары"""
        st.markdown("**Математические вычисления:**")
        
        st.text(f"Закрытый ключ (x): {key_pair.private}")
        st.text(f"Открытый ключ (y = g^x mod p):")
        st.text(f"  y = {key_pair.g}^{key_pair.private} mod {key_pair.p}")
        st.text(f"  y = {key_pair.public}")
        
        st.markdown("**Проверка:**")
        # Проверяем вычисление открытого ключа
        computed_public = pow(key_pair.g, key_pair.private, key_pair.p)
        if computed_public == key_pair.public:
            st.success("✓ Открытый ключ вычислен корректно")
        else:
            st.error("✗ Ошибка в вычислении открытого ключа")

    def display_encryption_details(self, message: str, ciphertext: ElGamalCiphertext):
        """Отображает детали процесса шифрования"""
        if 'elgamal_key_pair' in st.session_state:
            key_pair = st.session_state.elgamal_key_pair
            
            st.markdown("**Процесс шифрования:**")
            
            # Преобразуем сообщение в число
            message_num = self.message_to_number(message, key_pair.p)
            st.text(f"Сообщение как число: {message_num}")
            
            # Вычисляем y^k mod p (для демонстрации)
            # В реальном алгоритме k неизвестно, но для демонстрации можем вычислить
            # Находим k из c1 = g^k mod p (это задача дискретного логарифма)
            st.text(f"c1 = g^k mod p = {ciphertext.c1}")
            st.text(f"c2 = M * y^k mod p = {ciphertext.c2}")
            
            st.markdown("""
            **Формулы:**
            - c1 = g^k mod p
            - c2 = M * (g^x)^k mod p = M * g^(xk) mod p
            """)

    def display_decryption_details(self, message: str):
        """Отображает детали процесса дешифрования"""
        if 'elgamal_key_pair' in st.session_state and 'ciphertext' in st.session_state:
            key_pair = st.session_state.elgamal_key_pair
            ciphertext = st.session_state.ciphertext
            
            st.markdown("**Процесс дешифрования:**")
            
            # Вычисляем s = c1^x mod p
            s = pow(ciphertext.c1, key_pair.private, key_pair.p)
            st.text(f"s = c1^x mod p = {ciphertext.c1}^{key_pair.private} mod {key_pair.p} = {s}")
            
            # Вычисляем s^(-1) mod p
            s_inv = pow(s, -1, key_pair.p)
            st.text(f"s^(-1) mod p = {s_inv}")
            
            # Вычисляем M = c2 * s^(-1) mod p
            M = (ciphertext.c2 * s_inv) % key_pair.p
            st.text(f"M = c2 * s^(-1) mod p = {ciphertext.c2} * {s_inv} mod {key_pair.p} = {M}")
            
            # Преобразуем число обратно в сообщение
            recovered_message = self.number_to_message(M, key_pair.p)
            st.text(f"Восстановленное сообщение: '{recovered_message}'")

    def visualize_elgamal_process(self, message: str, p: int, g: int):
        """Визуализирует процесс работы алгоритма Эль-Гамаля"""
        st.markdown("### 🔄 Визуализация процесса Эль-Гамаля")
        
        # Генерация ключей
        st.markdown("#### 🔑 Генерация ключей")
        
        private_key = random.randint(1, p-2)
        public_key = pow(g, private_key, p)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Закрытый ключ (x)", private_key)
        with col2:
            st.metric("Открытый ключ (y)", public_key)
        with col3:
            st.metric("Вычисление", f"{g}^{private_key} mod {p}")
        
        # Шифрование
        st.markdown("#### 🔐 Шифрование")
        
        message_num = self.message_to_number(message, p)
        k = random.randint(1, p-2)
        c1 = pow(g, k, p)
        c2 = (message_num * pow(public_key, k, p)) % p
        
        encryption_steps = [
            ("Сообщение как число", message_num),
            ("Случайное k", k),
            ("c1 = g^k mod p", c1),
            ("y^k mod p", pow(public_key, k, p)),
            ("c2 = M * y^k mod p", c2)
        ]
        
        for step, value in encryption_steps:
            st.text(f"{step}: {value}")
        
        # Дешифрование
        st.markdown("#### 🔓 Дешифрование")
        
        s = pow(c1, private_key, p)
        s_inv = pow(s, -1, p)
        decrypted_num = (c2 * s_inv) % p
        decrypted_message = self.number_to_message(decrypted_num, p)
        
        decryption_steps = [
            ("s = c1^x mod p", s),
            ("s^(-1) mod p", s_inv),
            ("M = c2 * s^(-1) mod p", decrypted_num),
            ("Восстановленное сообщение", decrypted_message)
        ]
        
        for step, value in decryption_steps:
            st.text(f"{step}: {value}")
        
        # Проверка
        if message == decrypted_message:
            st.success("🎉 Алгоритм работает корректно!")
        else:
            st.error("❌ Ошибка в работе алгоритма!")
        
        # Графическая визуализация
        st.markdown("#### 📊 Графическое представление")
        
        steps = ["Исходное\nсообщение", "Шифрование", "Дешифрование", "Результат"]
        values = [message_num, c2, decrypted_num, message_num]
        
        fig = go.Figure(data=[go.Bar(x=steps, y=values)])
        fig.update_layout(
            title="Преобразование сообщения в процессе шифрования/дешифрования",
            yaxis_title="Числовое значение"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Основные алгоритмы Эль-Гамаля

    def elgamal_encrypt(self, message: str, public_key: int, p: int, g: int) -> ElGamalCiphertext:
        """Шифрует сообщение алгоритмом Эль-Гамаля"""
        # Преобразуем сообщение в число
        message_num = self.message_to_number(message, p)
        
        # Выбираем случайное k
        k = secrets.randbelow(p - 2) + 1
        
        # Вычисляем компоненты шифротекста
        c1 = pow(g, k, p)
        c2 = (message_num * pow(public_key, k, p)) % p
        
        return ElGamalCiphertext(c1, c2)

    def elgamal_decrypt(self, ciphertext: ElGamalCiphertext, private_key: int, p: int) -> str:
        """Дешифрует сообщение алгоритмом Эль-Гамаля"""
        # Вычисляем s = c1^x mod p
        s = pow(ciphertext.c1, private_key, p)
        
        # Вычисляем обратный элемент s^(-1) mod p
        s_inv = pow(s, -1, p)
        
        # Вычисляем исходное число M = c2 * s^(-1) mod p
        message_num = (ciphertext.c2 * s_inv) % p
        
        # Преобразуем число обратно в сообщение
        return self.number_to_message(message_num, p)

    def message_to_number(self, message: str, p: int) -> int:
        """Преобразует строку в число для шифрования"""
        # Простое преобразование: каждый символ в его ASCII код
        number = 0
        for char in message:
            number = (number * 256 + ord(char)) % p
        return number

    def number_to_message(self, number: int, p: int) -> str:
        """Преобразует число обратно в строку"""
        # Обратное преобразование из числа в строку
        message = ""
        temp = number
        while temp > 0:
            message = chr(temp % 256) + message
            temp //= 256
        return message

    # Дополнительные функции

    def generate_safe_prime(self, bits: int) -> int:
        """Генерирует безопасное простое число (p = 2q + 1)"""
        # Для демонстрации используем предварительно вычисленные простые числа
        return self.demo_primes[bits]["p"]

    def is_generator(self, g: int, p: int) -> bool:
        """Проверяет, является ли g генератором группы Zp*"""
        # Простая проверка для демонстрации
        return pow(g, (p-1)//2, p) != 1

# Для обратной совместимости
class ElGamalCipher(ElGamalModule):
    pass