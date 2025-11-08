from modules.base_module import CryptoModule
import streamlit as st

class CaesarCipherModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Шифр Цезаря"
        self.description = "Классический шифр замены с сдвигом"
        self.complexity = "beginner"
        self.category = "classical"
        self.icon = ""
        self.order = 1
    
    def render(self):
        st.title("🔐 Шифр Цезаря")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка"):
            st.markdown("""
            **Шифр Цезаря** - один из древнейших шифров, названный в честь Юлия Цезаря.
            
            **Принцип работы:**
            - Каждая буква в тексте заменяется на букву, находящуюся на фиксированное число позиций (сдвиг) дальше в алфавите
            - Алфавит зацикливается: после Z идет A, после Я идет А
            
            **Математическая формула:**
            - Шифрование: `E(x) = (x + k) mod N`
            - Дешифрование: `D(x) = (x - k) mod N`
            
            Где:
            - `x` - позиция буквы в алфавите (A=0, B=1, ..., Z=25 или А=0, Б=1, ..., Я=32)
            - `k` - ключ (сдвиг)
            - `N` - размер алфавита (26 для английского, 33 для русского)
            """)
        
        # Выбор языка
        col_lang, col_shift = st.columns(2)
        
        with col_lang:
            language = st.radio(
                "Выберите язык алфавита:",
                ["Английский", "Русский"],
                index=0,
                horizontal=True
            )
        
        with col_shift:
            max_shift = 25 if language == "Английский" else 32
            shift = st.slider("Сдвиг:", 1, max_shift, 3)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔒 Шифрование")
            text = st.text_input("Текст для шифрования:", "HELLO" if language == "Английский" else "ПРИВЕТ", key="encrypt_text")
            
            if st.button("Зашифровать", key="encrypt_btn"):
                encrypted = self.caesar_encrypt(text, shift, language)
                st.success(f"Результат: **{encrypted}**")
                
                # Показываем пример преобразования первой буквы
                if text:
                    first_letter = text[0].upper()
                    if first_letter.isalpha():
                        encrypted_letter = self.caesar_encrypt(first_letter, shift, language)
                        st.info(f"Пример: {first_letter} → {encrypted_letter}")
        
        with col2:
            st.subheader("🔓 Расшифровка")
            default_cipher = "KHOOR" if language == "Английский" else "ТУЛЕУ"
            cipher_text = st.text_input("Текст для расшифровки:", default_cipher, key="decrypt_text")
            shift_decrypt = st.slider("Сдвиг для расшифровки:", 1, max_shift, 3, key="decrypt_shift")
            
            if st.button("Расшифровать", key="decrypt_btn"):
                decrypted = self.caesar_decrypt(cipher_text, shift_decrypt, language)
                st.success(f"Результат: **{decrypted}**")
        
        # Визуализация алфавита
        st.markdown("---")
        st.subheader("🎯 Визуализация преобразования")
        
        if st.checkbox("Показать таблицу преобразования алфавита"):
            self.show_alphabet_table(shift, language)
    
    def get_alphabet(self, language):
        """Возвращает алфавит для выбранного языка"""
        if language == "Английский":
            return [chr(i) for i in range(65, 91)]  # A-Z
        else:  # Русский
            # Кириллические буквы от А до Я (без Ё)
            return [chr(i) for i in range(1040, 1072)]  # А-Я
    
    def caesar_encrypt(self, text, shift, language):
        """Шифрует текст методом Цезаря для выбранного языка"""
        result = ""
        alphabet = self.get_alphabet(language)
        alphabet_size = len(alphabet)
        
        for char in text:
            upper_char = char.upper()
            if upper_char in alphabet:
                # Находим позицию буквы в алфавите
                pos = alphabet.index(upper_char)
                # Применяем сдвиг по модулю
                new_pos = (pos + shift) % alphabet_size
                # Сохраняем регистр исходной буквы
                if char.isupper():
                    result += alphabet[new_pos]
                else:
                    result += alphabet[new_pos].lower()
            else:
                result += char
        return result
    
    def caesar_decrypt(self, text, shift, language):
        """Дешифрует текст методом Цезаря для выбранного языка"""
        return self.caesar_encrypt(text, -shift, language)
    
    def show_alphabet_table(self, shift, language):
        """Показывает таблицу преобразования алфавита"""
        import pandas as pd
        
        alphabet = self.get_alphabet(language)
        encrypted = [self.caesar_encrypt(ch, shift, language) for ch in alphabet]
        
        # Создаем DataFrame для красивого отображения
        df = pd.DataFrame({
            'Исходная': alphabet,
            '→': ['→'] * len(alphabet),
            'Зашифрованная': encrypted
        })
        
        # Отображаем таблицу
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Дополнительная информация
        st.markdown(f"""
        **Информация:**
        - Размер алфавита: **{len(alphabet)}** символов
        - Максимальный сдвиг: **{len(alphabet) - 1}**
        - Текущий сдвиг: **{shift}**
        """)