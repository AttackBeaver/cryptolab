from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd

class VigenereCipherModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Шифр Виженера"
        self.description = "Полиалфавитный шифр с использованием ключевого слова"
        self.complexity = "beginner"
        self.category = "classical"
        self.icon = ""
        self.order = 2
    
    def render(self):
        st.title("Шифр Виженера")
        
        # Теоретическая справка
        with st.expander("Теоретическая справка"):
            st.markdown("""
            **Шифр Виженера** - полиалфавитный шифр, усовершенствование шифра Цезаря.
            
            **Принцип работы:**
            - Используется ключевое слово, которое повторяется до длины текста
            - Каждая буква ключа определяет свой сдвиг для соответствующей буквы текста
            - Таким образом, одна и та же буква текста шифруется по-разному в разных позициях
            
            **Историческое значение:**
            - Считался невзламываемым в течение 300 лет
            - Был назван "невозможным шифром"
            - Прорыв в криптоанализе произошел только в 19 веке
            
            **Формула шифрования:**
            - `E_i = (T_i + K_i) mod N`
            - `D_i = (C_i - K_i) mod N`
            
            Где:
            - `T_i` - буква открытого текста
            - `K_i` - буква ключа
            - `N` - размер алфавита
            """)
        
        # Выбор языка
        language = st.radio(
            "Выберите язык алфавита:",
            ["Английский", "Русский"],
            index=0,
            horizontal=True
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Шифрование")
            plaintext = st.text_area(
                "Текст для шифрования:",
                "ATTACKATDAWN" if language == "Английский" else "ПРИСТУПИТЕУТРОМ",
                height=100
            )
            encrypt_key = st.text_input("Ключевое слово:", "KEY" if language == "Английский" else "КЛЮЧ")
            
            if st.button("Зашифровать", key="encrypt_btn"):
                if not encrypt_key.isalpha():
                    st.error("Ключ должен содержать только буквы!")
                else:
                    encrypted = self.vigenere_encrypt(plaintext, encrypt_key, language)
                    st.success(f"**Результат:** {encrypted}")
                    
                    # Показываем процесс
                    st.info("**Процесс шифрования:**")
                    self.show_encryption_process(plaintext, encrypt_key, language)
        
        with col2:
            st.subheader("Расшифровка")
            ciphertext = st.text_area(
                "Текст для расшифровки:",
                "KXRKGIKXBKAL" if language == "Английский" else "ФЩРЮБЦЫЧСБФЩЛЭЪ",
                height=100
            )
            decrypt_key = st.text_input("Ключевое слово для расшифровки:", "KEY" if language == "Английский" else "КЛЮЧ", key="decrypt_key")
            
            if st.button("Расшифровать", key="decrypt_btn"):
                if not decrypt_key.isalpha():
                    st.error("Ключ должен содержать только буквы!")
                else:
                    decrypted = self.vigenere_decrypt(ciphertext, decrypt_key, language)
                    st.success(f"**Результат:** {decrypted}")
        
        # Визуализация таблицы Виженера
        st.markdown("---")
        st.subheader("Таблица Виженера")
        
        if st.checkbox("Показать таблицу Виженера"):
            self.show_vigenere_table(language)
        
        # Демонстрация уязвимости
        st.markdown("---")
        st.subheader("Демонстрация уязвимости")
        
        if st.checkbox("Показать повторение ключа"):
            sample_text = "ДЛИННЫЙТЕКСТДЛЯДЕМОНСТРАЦИИ" if language == "Русский" else "LONGTEXTFORDEMONSTRATION"
            sample_key = "KEY" if language == "Английский" else "КЛЮЧ"
            
            st.write("**Повторение ключа:**")
            expanded_key = self.expand_key(sample_text, sample_key)
            
            df = pd.DataFrame({
                'Текст': list(sample_text),
                'Ключ': list(expanded_key),
                'Позиция': range(len(sample_text))
            })
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.warning("Повторение ключа - основная уязвимость шифра Виженера!")

    def get_alphabet(self, language):
        """Возвращает алфавит для выбранного языка"""
        if language == "Английский":
            return [chr(i) for i in range(65, 91)]  # A-Z
        else:  # Русский
            return [chr(i) for i in range(1040, 1072)]  # А-Я

    def expand_key(self, text, key):
        """Расширяет ключ до длины текста"""
        key = key.upper()
        expanded = []
        key_index = 0
        
        for char in text.upper():
            if char.isalpha():
                expanded.append(key[key_index % len(key)])
                key_index += 1
            else:
                expanded.append(' ')
        
        return ''.join(expanded)

    def vigenere_encrypt(self, text, key, language):
        """Шифрует текст методом Виженера"""
        alphabet = self.get_alphabet(language)
        alphabet_size = len(alphabet)
        result = []
        
        expanded_key = self.expand_key(text, key)
        text_upper = text.upper()
        
        for i, char in enumerate(text_upper):
            if char in alphabet:
                text_pos = alphabet.index(char)
                key_char = expanded_key[i]
                key_pos = alphabet.index(key_char)
                
                new_pos = (text_pos + key_pos) % alphabet_size
                result.append(alphabet[new_pos])
            else:
                result.append(char)
        
        return ''.join(result)

    def vigenere_decrypt(self, text, key, language):
        """Дешифрует текст методом Виженера"""
        alphabet = self.get_alphabet(language)
        alphabet_size = len(alphabet)
        result = []
        
        expanded_key = self.expand_key(text, key)
        text_upper = text.upper()
        
        for i, char in enumerate(text_upper):
            if char in alphabet:
                text_pos = alphabet.index(char)
                key_char = expanded_key[i]
                key_pos = alphabet.index(key_char)
                
                new_pos = (text_pos - key_pos) % alphabet_size
                result.append(alphabet[new_pos])
            else:
                result.append(char)
        
        return ''.join(result)

    def show_vigenere_table(self, language):
        """Показывает таблицу Виженера"""
        alphabet = self.get_alphabet(language)
        alphabet_size = len(alphabet)
        
        # Создаем таблицу Виженера
        table_data = []
        for i in range(alphabet_size):
            row = []
            for j in range(alphabet_size):
                row.append(alphabet[(i + j) % alphabet_size])
            table_data.append(row)
        
        df = pd.DataFrame(table_data, columns=alphabet, index=alphabet)
        
        st.write("**Таблица Виженера (строка - текст, столбец - ключ):**")
        st.dataframe(df, use_container_width=True)
        
        st.markdown("""
        **Как пользоваться таблицей:**
        1. Найдите букву открытого текста в левом столбце
        2. Найдите букву ключа в верхней строке  
        3. На пересечении - зашифрованная буква
        """)

    def show_encryption_process(self, text, key, language):
        """Показывает подробный процесс шифрования"""
        alphabet = self.get_alphabet(language)
        expanded_key = self.expand_key(text, key)
        
        process_data = []
        for i, char in enumerate(text.upper()):
            if char in alphabet:
                text_pos = alphabet.index(char)
                key_char = expanded_key[i]
                key_pos = alphabet.index(key_char)
                encrypted_pos = (text_pos + key_pos) % len(alphabet)
                encrypted_char = alphabet[encrypted_pos]
                
                process_data.append({
                    'Позиция': i + 1,
                    'Буква текста': char,
                    'Позиция текста': text_pos,
                    'Буква ключа': key_char,
                    'Позиция ключа': key_pos,
                    'Результат': f"({text_pos} + {key_pos}) mod {len(alphabet)} = {encrypted_pos}",
                    'Зашифрованная': encrypted_char
                })
        
        if process_data:
            st.dataframe(pd.DataFrame(process_data), use_container_width=True)