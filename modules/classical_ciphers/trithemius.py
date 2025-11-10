from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import numpy as np

class TrithemiusCipherModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Шифр Трисимуса"
        self.description = "Полиалфавитный шифр на основе таблицы и прогрессивного сдвига"
        self.complexity = "intermediate"
        self.category = "classical"
        self.icon = ""
        self.order = 7
    
    def render(self):
        st.title("🔠 Шифр Трисимуса")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **Шифр Трисимуса** (или квадрат Трисимуса) - полиалфавитный шифр, разработанный немецким монахом Иоганном Тритемием в XV веке.
            
            **Принцип работы:**
            1. Создается таблица (обычно 6×6 или 5×6) с буквами алфавита
            2. Каждая буква имеет координаты (строка, столбец)
            3. Для шифрования используется прогрессивный сдвиг:
               - Первая буква: сдвиг 0
               - Вторая буква: сдвиг 1
               - Третья буква: сдвиг 2
               - и т.д.
            
            **Математическая модель:**
            - Для буквы на позиции i: `E(x_i) = (x_i + i) mod N`
            - Где `x_i` - позиция буквы в алфавите, `i` - номер буквы в тексте
            
            **Историческое значение:**
            - Один из первых полиалфавитных шифров
            - Предшественник шифра Виженера
            - Использовался в дипломатической переписке
            """)
        
        # Выбор языка и параметров
        col_lang, col_method = st.columns(2)
        
        with col_lang:
            language = st.radio(
                "Выберите язык алфавита:",
                ["Английский", "Русский"],
                index=0,
                horizontal=True
            )
        
        with col_method:
            method = st.radio(
                "Метод шифрования:",
                ["Прогрессивный сдвиг", "Табличный метод"],
                index=0,
                horizontal=True
            )
        
        st.markdown("---")
        
        if method == "Табличный метод":
            self.render_table_method(language)
        else:
            self.render_progressive_method(language)
    
    def get_alphabet(self, language):
        """Возвращает алфавит для выбранного языка"""
        if language == "Английский":
            return [chr(i) for i in range(65, 91)]  # A-Z
        else:  # Русский
            return [chr(i) for i in range(1040, 1072)]  # А-Я
    
    def create_trithemius_table(self, language):
        """Создает таблицу Трисимуса"""
        alphabet = self.get_alphabet(language)
        alphabet_size = len(alphabet)
        
        # Определяем размеры таблицы
        if language == "Английский":
            rows, cols = 6, 6  # 6×6 для английского (36 символов)
        else:
            rows, cols = 6, 6  # 6×6 для русского (33 символа + 3 пустых)
        
        table = []
        index = 0
        
        for i in range(rows):
            row = []
            for j in range(cols):
                if index < alphabet_size:
                    row.append(alphabet[index])
                    index += 1
                else:
                    row.append("")  # Пустые ячейки для неполных таблиц
            table.append(row)
        
        return table
    
    def render_table_method(self, language):
        """Отрисовывает табличный метод шифрования"""
        st.subheader("📊 Табличный метод")
        
        # Создаем и показываем таблицу
        table = self.create_trithemius_table(language)
        st.markdown("**Таблица Трисимуса:**")
        
        # Отображаем таблицу
        self.display_table(table, language)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔒 Шифрование")
            plaintext = st.text_area(
                "Исходный текст:",
                "HELLO" if language == "Английский" else "ПРИВЕТ",
                height=100,
                key="table_encrypt"
            ).upper()
            
            if st.button("Зашифровать табличным методом", key="table_encrypt_btn"):
                encrypted = self.table_encrypt(plaintext, table, language)
                st.success("Зашифрованный текст:")
                st.code(encrypted, language="text")
                
                # Показываем процесс шифрования
                if plaintext:
                    self.show_encryption_process(plaintext, encrypted, "табличного")
        
        with col2:
            st.subheader("🔓 Расшифровка")
            ciphertext = st.text_area(
                "Текст для расшифровки:",
                "",
                height=100,
                key="table_decrypt"
            ).upper()
            
            if st.button("Расшифровать табличным методом", key="table_decrypt_btn"):
                decrypted = self.table_decrypt(ciphertext, table, language)
                st.success("Расшифрованный текст:")
                st.code(decrypted, language="text")
    
    def render_progressive_method(self, language):
        """Отрисовывает метод прогрессивного сдвига"""
        st.subheader("📈 Метод прогрессивного сдвига")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔒 Шифрование")
            plaintext = st.text_area(
                "Исходный текст:",
                "CRYPTO" if language == "Английский" else "ТЕКСТ",
                height=100,
                key="prog_encrypt"
            )
            
            start_shift = st.number_input("Начальный сдвиг:", min_value=0, max_value=25, value=0, key="start_shift")
            
            if st.button("Зашифровать прогрессивным методом", key="prog_encrypt_btn"):
                encrypted = self.progressive_encrypt(plaintext, start_shift, language)
                st.success("Зашифрованный текст:")
                st.code(encrypted, language="text")
                
                # Показываем процесс шифрования
                if plaintext:
                    self.show_progressive_process(plaintext, encrypted, start_shift, language, "шифрования")
        
        with col2:
            st.subheader("🔓 Расшифровка")
            ciphertext = st.text_area(
                "Текст для расшифровки:",
                "",
                height=100,
                key="prog_decrypt"
            )
            
            start_shift_decrypt = st.number_input("Начальный сдвиг:", min_value=0, max_value=25, value=0, key="start_shift_decrypt")
            
            if st.button("Расшифровать прогрессивным методом", key="prog_decrypt_btn"):
                decrypted = self.progressive_decrypt(ciphertext, start_shift_decrypt, language)
                st.success("Расшифрованный текст:")
                st.code(decrypted, language="text")
        
        # Визуализация прогрессивного сдвига
        st.markdown("---")
        st.subheader("🎯 Визуализация прогрессивного сдвига")
        
        demo_text = st.text_input("Текст для демонстрации:", "ABC", key="demo_progressive")
        if st.button("Показать преобразование", key="demo_btn"):
            self.demo_progressive_shift(demo_text, language)
    
    def table_encrypt(self, text, table, language):
        """Шифрует текст табличным методом"""
        result = ""
        alphabet = self.get_alphabet(language)
        
        for i, char in enumerate(text):
            if char.upper() in alphabet:
                # Находим координаты буквы в таблице
                coords = self.find_character_coords(char.upper(), table)
                if coords:
                    row, col = coords
                    # Прогрессивный сдвиг: увеличиваем строку на номер позиции
                    new_row = (row + i) % len(table)
                    result += table[new_row][col]
                else:
                    result += char
            else:
                result += char
        return result
    
    def table_decrypt(self, text, table, language):
        """Дешифрует текст табличным методом"""
        result = ""
        alphabet = self.get_alphabet(language)
        
        for i, char in enumerate(text):
            if char.upper() in alphabet:
                # Находим координаты зашифрованной буквы
                coords = self.find_character_coords(char.upper(), table)
                if coords:
                    row, col = coords
                    # Обратный прогрессивный сдвиг
                    new_row = (row - i) % len(table)
                    result += table[new_row][col]
                else:
                    result += char
            else:
                result += char
        return result
    
    def progressive_encrypt(self, text, start_shift, language):
        """Шифрует текст методом прогрессивного сдвига"""
        result = ""
        alphabet = self.get_alphabet(language)
        alphabet_size = len(alphabet)
        
        for i, char in enumerate(text):
            upper_char = char.upper()
            if upper_char in alphabet:
                pos = alphabet.index(upper_char)
                # Прогрессивный сдвиг: start_shift + позиция в тексте
                shift = (start_shift + i) % alphabet_size
                new_pos = (pos + shift) % alphabet_size
                
                if char.isupper():
                    result += alphabet[new_pos]
                else:
                    result += alphabet[new_pos].lower()
            else:
                result += char
        return result
    
    def progressive_decrypt(self, text, start_shift, language):
        """Дешифрует текст методом прогрессивного сдвига"""
        result = ""
        alphabet = self.get_alphabet(language)
        alphabet_size = len(alphabet)
        
        for i, char in enumerate(text):
            upper_char = char.upper()
            if upper_char in alphabet:
                pos = alphabet.index(upper_char)
                # Обратный прогрессивный сдвиг
                shift = (start_shift + i) % alphabet_size
                new_pos = (pos - shift) % alphabet_size
                
                if char.isupper():
                    result += alphabet[new_pos]
                else:
                    result += alphabet[new_pos].lower()
            else:
                result += char
        return result
    
    def find_character_coords(self, char, table):
        """Находит координаты символа в таблице"""
        for i, row in enumerate(table):
            for j, cell in enumerate(row):
                if cell == char:
                    return (i, j)
        return None
    
    def display_table(self, table, language):
        """Отображает таблицу Трисимуса"""
        df = pd.DataFrame(table)
        
        # Стилизуем таблицу
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Показываем координаты
        st.markdown("**Координаты букв:**")
        coords_text = ""
        for i, row in enumerate(table):
            for j, cell in enumerate(row):
                if cell:  # Только для непустых ячеек
                    coords_text += f"{cell}:({i},{j}) "
            coords_text += "\n"
        
        st.text_area("Координаты:", coords_text, height=150, key="coords_display")
    
    def show_encryption_process(self, plaintext, encrypted, method_name):
        """Показывает процесс шифрования"""
        st.markdown("**Процесс шифрования:**")
        
        process_data = []
        for i, (p_char, e_char) in enumerate(zip(plaintext, encrypted)):
            if p_char.isalpha():
                process_data.append({
                    'Позиция': i,
                    'Исходная': p_char,
                    '→': '→',
                    'Зашифрованная': e_char,
                    'Сдвиг': i
                })
        
        if process_data:
            df_process = pd.DataFrame(process_data)
            st.dataframe(df_process, use_container_width=True, hide_index=True)
    
    def show_progressive_process(self, plaintext, encrypted, start_shift, language, operation):
        """Показывает процесс прогрессивного шифрования/дешифрования"""
        st.markdown(f"**Процесс {operation}:**")
        
        alphabet = self.get_alphabet(language)
        process_data = []
        
        for i, (p_char, e_char) in enumerate(zip(plaintext, encrypted)):
            if p_char.upper() in alphabet:
                p_pos = alphabet.index(p_char.upper())
                e_pos = alphabet.index(e_char.upper())
                shift = (start_shift + i) % len(alphabet)
                
                process_data.append({
                    'Поз.': i,
                    'Буква': p_char,
                    'Поз. в алф.': p_pos,
                    'Сдвиг': shift,
                    'Новая поз.': (p_pos + shift) % len(alphabet) if operation == "шифрования" else (e_pos - shift) % len(alphabet),
                    'Результат': e_char
                })
        
        if process_data:
            df_process = pd.DataFrame(process_data)
            st.dataframe(df_process, use_container_width=True, hide_index=True)
    
    def demo_progressive_shift(self, text, language):
        """Демонстрирует прогрессивный сдвиг"""
        st.markdown("**Демонстрация прогрессивного сдвига:**")
        
        alphabet = self.get_alphabet(language)
        
        for i, char in enumerate(text):
            if char.upper() in alphabet:
                pos = alphabet.index(char.upper())
                shift = i
                new_pos = (pos + shift) % len(alphabet)
                
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Буква", char)
                with col2:
                    st.metric("Позиция", pos)
                with col3:
                    st.metric("Сдвиг", shift)
                with col4:
                    st.metric("Новая позиция", new_pos)
                with col5:
                    st.metric("Результат", alphabet[new_pos])
                
                st.progress((i + 1) / len(text))

# Для обратной совместимости
class TrithemiusCipher(TrithemiusCipherModule):
    pass
