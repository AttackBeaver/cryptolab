from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import numpy as np
import random

class GronsfeldCipherModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Шифр Гронсфельда"
        self.description = "Усовершенствованный шифр Виженера с числовым ключом"
        self.complexity = "intermediate"
        self.category = "classical"
        self.icon = ""
        self.order = 8
    
    def render(self):
        st.title("Шифр Гронсфельда")
        
        # Теоретическая справка
        with st.expander("Теоретическая справка", expanded=False):
            st.markdown("""
            **Шифр Гронсфельда** - полиалфавитный шифр, разработанный графом Гронсфельдом в XVII веке как усовершенствование шифра Виженера.
            
            **Основные особенности:**
            - Использует **числовой ключ** вместо буквенного
            - Каждая цифра ключа определяет сдвиг для соответствующей буквы
            - Более простая реализация по сравнению с Виженером
            - Сохраняет криптостойкость полиалфавитных шифров
            
            **Принцип работы:**
            1. Ключ - последовательность цифр (например: 1234)
            2. Ключ повторяется до длины текста
            3. Каждая цифра ключа определяет величину сдвига для соответствующей буквы
            
            **Математическая модель:**
            - Шифрование: `E(x_i) = (x_i + k_i) mod N`
            - Дешифрование: `D(x_i) = (x_i - k_i) mod N`
            
            Где:
            - `x_i` - позиция i-й буквы в алфавите
            - `k_i` - цифра ключа для i-й позиции
            - `N` - размер алфавита
            
            **Преимущества перед Виженером:**
            - Более простой ключ (только цифры)
            - Легче запомнить числовую последовательность
            - Сохранение криптостойкости
            """)
        
        # Выбор языка
        language = st.radio(
            "Выберите язык алфавита:",
            ["Английский", "Русский"],
            index=0,
            horizontal=True
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_encryption_section(language)
        
        with col2:
            self.render_decryption_section(language)
        
        # Дополнительные инструменты
        st.markdown("---")
        self.render_tools_section(language)
    
    def get_alphabet(self, language):
        """Возвращает алфавит для выбранного языка"""
        if language == "Английский":
            return [chr(i) for i in range(65, 91)]  # A-Z
        else:  # Русский
            return [chr(i) for i in range(1040, 1072)]  # А-Я
    
    def validate_key(self, key):
        """Проверяет корректность ключа"""
        if not key:
            return False, "Ключ не может быть пустым"
        
        if not all(char.isdigit() for char in key):
            return False, "Ключ должен содержать только цифры"
        
        return True, "Ключ корректен"
    
    def extend_key(self, key, length):
        """Расширяет ключ до нужной длины"""
        extended_key = ""
        key_length = len(key)
        
        for i in range(length):
            extended_key += key[i % key_length]
        
        return extended_key
    
    def gronsfeld_encrypt(self, text, key, language):
        """Шифрует текст методом Гронсфельда"""
        result = ""
        alphabet = self.get_alphabet(language)
        alphabet_size = len(alphabet)
        
        # Оставляем только буквы для шифрования
        text_letters = [char for char in text if char.upper() in alphabet]
        
        if not text_letters:
            return text
        
        # Расширяем ключ
        extended_key = self.extend_key(key, len(text_letters))
        
        letter_index = 0
        for char in text:
            upper_char = char.upper()
            if upper_char in alphabet:
                # Получаем цифру ключа для текущей позиции
                key_digit = int(extended_key[letter_index])
                
                # Находим позицию буквы в алфавите
                pos = alphabet.index(upper_char)
                
                # Применяем сдвиг
                new_pos = (pos + key_digit) % alphabet_size
                
                # Сохраняем регистр
                if char.isupper():
                    result += alphabet[new_pos]
                else:
                    result += alphabet[new_pos].lower()
                
                letter_index += 1
            else:
                result += char
        
        return result
    
    def gronsfeld_decrypt(self, text, key, language):
        """Дешифрует текст методом Гронсфельда"""
        result = ""
        alphabet = self.get_alphabet(language)
        alphabet_size = len(alphabet)
        
        # Оставляем только буквы для дешифрования
        text_letters = [char for char in text if char.upper() in alphabet]
        
        if not text_letters:
            return text
        
        # Расширяем ключ
        extended_key = self.extend_key(key, len(text_letters))
        
        letter_index = 0
        for char in text:
            upper_char = char.upper()
            if upper_char in alphabet:
                # Получаем цифру ключа для текущей позиции
                key_digit = int(extended_key[letter_index])
                
                # Находим позицию буквы в алфавите
                pos = alphabet.index(upper_char)
                
                # Применяем обратный сдвиг
                new_pos = (pos - key_digit) % alphabet_size
                
                # Сохраняем регистр
                if char.isupper():
                    result += alphabet[new_pos]
                else:
                    result += alphabet[new_pos].lower()
                
                letter_index += 1
            else:
                result += char
        
        return result
    
    def render_encryption_section(self, language):
        """Отрисовывает секцию шифрования"""
        st.subheader("Шифрование")
        
        # Инициализация состояния для генерации ключа
        if 'gronsfeld_encrypt_key' not in st.session_state:
            st.session_state.gronsfeld_encrypt_key = "1234"
        
        plaintext = st.text_area(
            "Исходный текст:",
            "ATTACK AT DAWN" if language == "Английский" else "АТАКА НА РАССВЕТЕ",
            height=100,
            key="encrypt_input"
        )
        
        # Контейнер для ключа с возможностью обновления
        key_container = st.container()
        
        with key_container:
            col_key, col_gen = st.columns([3, 1])
            
            with col_key:
                key = st.text_input(
                    "Числовой ключ:",
                    value=st.session_state.gronsfeld_encrypt_key,
                    max_chars=20,
                    key="encrypt_key_input",
                    help="Ключ должен содержать только цифры (0-9)"
                )
            
            with col_gen:
                st.write("")  # Отступ
                st.write("")  # Отступ
                if st.button("Сгенерировать", key="gen_encrypt_key", use_container_width=True):
                    random_key = ''.join(str(random.randint(0, 9)) for _ in range(6))
                    st.session_state.gronsfeld_encrypt_key = random_key
                    st.rerun()
        
        # Проверка ключа
        is_valid, message = self.validate_key(key)
        if key:
            if is_valid:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
        
        if st.button("Зашифровать", key="encrypt_btn", use_container_width=True):
            if is_valid:
                encrypted = self.gronsfeld_encrypt(plaintext, key, language)
                st.success("Зашифрованный текст:")
                st.code(encrypted, language="text")
                
                # Показываем процесс шифрования
                self.show_encryption_process(plaintext, encrypted, key, language)
            else:
                st.error("Исправьте ключ перед шифрованием")
    
    def render_decryption_section(self, language):
        """Отрисовывает секцию дешифрования"""
        st.subheader("Расшифровка")
        
        # Инициализация состояния для генерации ключа
        if 'gronsfeld_decrypt_key' not in st.session_state:
            st.session_state.gronsfeld_decrypt_key = "1234"
        
        ciphertext = st.text_area(
            "Текст для расшифровки:",
            "",
            height=100,
            key="decrypt_input"
        )
        
        # Контейнер для ключа с возможностью обновления
        key_container = st.container()
        
        with key_container:
            col_key, col_gen = st.columns([3, 1])
            
            with col_key:
                key = st.text_input(
                    "Числовой ключ:",
                    value=st.session_state.gronsfeld_decrypt_key,
                    max_chars=20,
                    key="decrypt_key_input",
                    help="Введите ключ, использованный для шифрования"
                )
            
            with col_gen:
                st.write("")  # Отступ
                st.write("")  # Отступ
                if st.button("Сгенерировать", key="gen_decrypt_key", use_container_width=True):
                    random_key = ''.join(str(random.randint(0, 9)) for _ in range(6))
                    st.session_state.gronsfeld_decrypt_key = random_key
                    st.rerun()
        
        # Проверка ключа
        is_valid, message = self.validate_key(key)
        if key:
            if is_valid:
                st.success(f"✅ {message}")
            else:
                st.error(f"❌ {message}")
        
        if st.button("Расшифровать", key="decrypt_btn", use_container_width=True):
            if is_valid and ciphertext:
                decrypted = self.gronsfeld_decrypt(ciphertext, key, language)
                st.success("Расшифрованный текст:")
                st.code(decrypted, language="text")
                
                # Показываем процесс дешифрования
                self.show_decryption_process(ciphertext, decrypted, key, language)
            else:
                st.error("Введите текст для расшифровки и корректный ключ")
    
    def render_tools_section(self, language):
        """Отрисовывает дополнительные инструменты"""
        st.subheader("Инструменты анализа")
        
        tab1, tab2, tab3 = st.tabs(["Визуализация", "Сравнение с Виженером", "Демонстрация"])
        
        with tab1:
            self.render_visualization_tab(language)
        
        with tab2:
            self.render_comparison_tab(language)
        
        with tab3:
            self.render_demo_tab(language)
    
    def render_visualization_tab(self, language):
        """Вкладка визуализации процесса"""
        st.markdown("**Визуализация процесса шифрования:**")
        
        # Используем уникальные ключи для вкладки
        demo_text = st.text_input("Текст для визуализации:", "CRYPTO", key="viz_text_gronsfeld")
        demo_key = st.text_input("Ключ для визуализации:", "123", key="viz_key_gronsfeld")
        
        if st.button("Показать процесс", key="viz_btn_gronsfeld") and demo_text and demo_key:
            self.show_detailed_process(demo_text, demo_key, language)
    
    def render_comparison_tab(self, language):
        """Вкладка сравнения с Виженером"""
        st.markdown("**Сравнение шифров Гронсфельда и Виженера:**")
        
        # Используем уникальные ключи для вкладки
        comparison_text = st.text_input("Текст для сравнения:", "HELLO", key="comp_text_gronsfeld")
        gronsfeld_key = st.text_input("Ключ Гронсфельда:", "1234", key="comp_gronsfeld_key")
        vigenere_key = st.text_input("Ключ Виженера:", "BCDE", key="comp_vigenere_key")
        
        if st.button("Сравнить", key="comp_btn_gronsfeld"):
            self.compare_with_vigenere(comparison_text, gronsfeld_key, vigenere_key, language)
    
    def render_demo_tab(self, language):
        """Вкладка демонстрации"""
        st.markdown("**Демонстрация работы шифра:**")
        
        if st.button("Показать пример работы", key="demo_btn_gronsfeld"):
            self.show_work_example(language)
    
    def show_encryption_process(self, plaintext, encrypted, key, language):
        """Показывает процесс шифрования"""
        alphabet = self.get_alphabet(language)
        
        # Фильтруем только буквы
        plain_letters = [char for char in plaintext if char.upper() in alphabet]
        encrypted_letters = [char for char in encrypted if char.upper() in alphabet]
        
        if not plain_letters:
            return
        
        extended_key = self.extend_key(key, len(plain_letters))
        
        st.markdown("**Процесс шифрования:**")
        process_data = []
        
        for i, (p_char, e_char) in enumerate(zip(plain_letters, encrypted_letters)):
            key_digit = int(extended_key[i])
            p_pos = alphabet.index(p_char.upper())
            e_pos = alphabet.index(e_char.upper())
            
            process_data.append({
                'Поз.': i,
                'Буква': p_char,
                'Поз. в алф.': p_pos,
                'Ключ': key_digit,
                'Новая поз.': (p_pos + key_digit) % len(alphabet),
                'Результат': e_char
            })
        
        df = pd.DataFrame(process_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    def show_decryption_process(self, ciphertext, decrypted, key, language):
        """Показывает процесс дешифрования"""
        alphabet = self.get_alphabet(language)
        
        # Фильтруем только буквы
        cipher_letters = [char for char in ciphertext if char.upper() in alphabet]
        decrypted_letters = [char for char in decrypted if char.upper() in alphabet]
        
        if not cipher_letters:
            return
        
        extended_key = self.extend_key(key, len(cipher_letters))
        
        st.markdown("**Процесс дешифрования:**")
        process_data = []
        
        for i, (c_char, d_char) in enumerate(zip(cipher_letters, decrypted_letters)):
            key_digit = int(extended_key[i])
            c_pos = alphabet.index(c_char.upper())
            d_pos = alphabet.index(d_char.upper())
            
            process_data.append({
                'Поз.': i,
                'Буква': c_char,
                'Поз. в алф.': c_pos,
                'Ключ': key_digit,
                'Новая поз.': (c_pos - key_digit) % len(alphabet),
                'Результат': d_char
            })
        
        df = pd.DataFrame(process_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    def show_detailed_process(self, text, key, language):
        """Показывает детальный процесс преобразования"""
        alphabet = self.get_alphabet(language)
        text_letters = [char for char in text if char.upper() in alphabet]
        extended_key = self.extend_key(key, len(text_letters))
        
        st.markdown("**Детальный процесс:**")
        
        for i, char in enumerate(text_letters):
            key_digit = int(extended_key[i])
            pos = alphabet.index(char.upper())
            new_pos = (pos + key_digit) % len(alphabet)
            
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                st.write(f"**{char}**")
            with col2:
                st.write(f"Поз.: {pos}")
            with col3:
                st.write("+")
            with col4:
                st.write(f"Ключ: {key_digit}")
            with col5:
                st.write(f"= {new_pos}")
            with col6:
                st.write(f"→ **{alphabet[new_pos]}**")
            
            st.progress((i + 1) / len(text_letters))
    
    def compare_with_vigenere(self, text, gronsfeld_key, vigenere_key, language):
        """Сравнивает шифры Гронсфельда и Виженера"""
        try:
            # Импортируем модуль Виженера
            from modules.classical_ciphers.vigenere import VigenereCipherModule
            vigenere_module = VigenereCipherModule()
            
            # Шифруем обоими методами
            gronsfeld_encrypted = self.gronsfeld_encrypt(text, gronsfeld_key, language)
            vigenere_encrypted = vigenere_module.vigenere_encrypt(text, vigenere_key, language)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Шифр Гронсфельда**")
                st.metric("Исходный текст", text)
                st.metric("Ключ", gronsfeld_key)
                st.metric("Результат", gronsfeld_encrypted)
            
            with col2:
                st.markdown("**Шифр Виженера**")
                st.metric("Исходный текст", text)
                st.metric("Ключ", vigenere_key)
                st.metric("Результат", vigenere_encrypted)
            
            # Сравниваем характеристики
            st.markdown("**Сравнительная таблица:**")
            comparison_data = {
                'Параметр': ['Тип ключа', 'Длина ключа', 'Сложность ключа', 'Результат'],
                'Гронсфельд': ['Числовой', str(len(gronsfeld_key)), 'Проще', gronsfeld_encrypted],
                'Виженер': ['Буквенный', str(len(vigenere_key)), 'Сложнее', vigenere_encrypted]
            }
            
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
        except ImportError:
            st.warning("Модуль Виженера не найден для сравнения")
    
    def show_work_example(self, language):
        """Показывает пример работы шифра"""
        example_text = "SECRET" if language == "Английский" else "СЕКРЕТ"
        example_key = "314159"
        
        st.markdown("**Пример работы шифра Гронсфельда:**")
        
        encrypted = self.gronsfeld_encrypt(example_text, example_key, language)
        
        st.info(f"""
        **Исходный текст:** {example_text}
        **Ключ:** {example_key}
        **Зашифрованный текст:** {encrypted}
        """)
        
        # Показываем математические выкладки
        alphabet = self.get_alphabet(language)
        extended_key = self.extend_key(example_key, len(example_text))
        
        st.markdown("**Математические преобразования:**")
        for i, char in enumerate(example_text):
            key_digit = int(extended_key[i])
            pos = alphabet.index(char.upper())
            new_pos = (pos + key_digit) % len(alphabet)
            
            st.write(f"{char} ({pos}) + {key_digit} = {new_pos} → {alphabet[new_pos]}")

# Для обратной совместимости
class GronsfeldCipher(GronsfeldCipherModule):
    pass
