from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd

class AtbashCipherModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Шифр Атбаш"
        self.description = "Классический шифр подстановки с обратным алфавитом"
        self.complexity = "beginner"
        self.category = "classical"
        self.icon = ""
        self.order = 6
    
    def render(self):
        st.title("🔄 Шифр Атбаш")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **Шифр Атбаш** - один из древнейших моноалфавитных шифров подстановки, использовавшийся еще в древнееврейском языке.
            
            **Принцип работы:**
            - Алфавит записывается в прямом порядке, а под ним - в обратном
            - Каждая буква заменяется на букву, стоящую напротив в обратном алфавите
            - Для английского алфавита: A→Z, B→Y, C→X, ..., Z→A
            - Для русского алфавита: А→Я, Б→Ю, В→Э, ..., Я→А
            
            **Математическая формула:**
            - Для алфавита размером N: `E(x) = (N - 1 - x)`
            
            Где:
            - `x` - позиция буквы в алфавите (A=0, B=1, ..., Z=25)
            - `N` - размер алфавита
            
            **Особенности:**
            - Шифр является **инволюцией** - шифрование и дешифрование выполняются одинаково
            - Прост в использовании, но уязвим для частотного анализа
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
            st.subheader("🔒 Шифрование")
            plaintext = st.text_area(
                "Исходный текст:",
                "HELLO WORLD" if language == "Английский" else "ПРИВЕТ МИР",
                height=100,
                key="encrypt_input"
            )
            
            if st.button("Зашифровать", key="encrypt_btn", use_container_width=True):
                encrypted = self.atbash_encrypt(plaintext, language)
                st.success("Зашифрованный текст:")
                st.code(encrypted, language="text")
                
                # Показываем статистику
                self.show_text_stats(plaintext, encrypted, "шифрования")
        
        with col2:
            st.subheader("🔓 Расшифровка")
            default_cipher = "SVOOL DLIOW" if language == "Английский" else "ПРИВЕТ МИР"
            ciphertext = st.text_area(
                "Текст для расшифровки:",
                self.atbash_encrypt(default_cipher, language) if language == "Английский" else "Похищщт Фчо",
                height=100,
                key="decrypt_input"
            )
            
            if st.button("Расшифровать", key="decrypt_btn", use_container_width=True):
                decrypted = self.atbash_decrypt(ciphertext, language)
                st.success("Расшифрованный текст:")
                st.code(decrypted, language="text")
                
                # Показываем статистику
                self.show_text_stats(ciphertext, decrypted, "расшифровки")
        
        # Визуализация алфавита
        st.markdown("---")
        st.subheader("🎯 Визуализация преобразования алфавита")
        
        if st.checkbox("Показать таблицу преобразования алфавита"):
            self.show_alphabet_table(language)
            
        # Демонстрация инволюции
        st.markdown("---")
        st.subheader("🔁 Демонстрация свойства инволюции")
        
        demo_text = st.text_input(
            "Текст для демонстрации:",
            "CRYPTO" if language == "Английский" else "КРИПТО",
            key="demo_input"
        )
        
        if st.button("Показать двойное преобразование", use_container_width=True):
            self.demo_involution(demo_text, language)
    
    def get_alphabet(self, language):
        """Возвращает алфавит для выбранного языка"""
        if language == "Английский":
            return [chr(i) for i in range(65, 91)]  # A-Z
        else:  # Русский
            return [chr(i) for i in range(1040, 1072)]  # А-Я
    
    def atbash_encrypt(self, text, language):
        """Шифрует текст методом Атбаш"""
        result = ""
        alphabet = self.get_alphabet(language)
        alphabet_size = len(alphabet)
        
        for char in text:
            upper_char = char.upper()
            if upper_char in alphabet:
                # Находим позицию буквы в алфавите
                pos = alphabet.index(upper_char)
                # Применяем преобразование Атбаш
                new_pos = alphabet_size - 1 - pos
                # Сохраняем регистр исходной буквы
                if char.isupper():
                    result += alphabet[new_pos]
                else:
                    result += alphabet[new_pos].lower()
            else:
                result += char
        return result
    
    def atbash_decrypt(self, text, language):
        """Дешифрует текст методом Атбаш"""
        # Атбаш является инволюцией, поэтому шифрование = дешифрование
        return self.atbash_encrypt(text, language)
    
    def show_alphabet_table(self, language):
        """Показывает таблицу преобразования алфавита"""
        alphabet = self.get_alphabet(language)
        transformed = [self.atbash_encrypt(ch, language) for ch in alphabet]
        
        # Создаем DataFrame для красивого отображения
        df = pd.DataFrame({
            'Исходная буква': alphabet,
            '→': ['→'] * len(alphabet),
            'Преобразованная': transformed
        })
        
        # Отображаем таблицу
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Дополнительная информация
        st.markdown(f"""
        **Информация об алфавите:**
        - Размер алфавита: **{len(alphabet)}** символов
        - Первая буква: **{alphabet[0]}** → **{transformed[0]}**
        - Последняя буква: **{alphabet[-1]}** → **{transformed[-1]}**
        - Середина алфавита: **{alphabet[len(alphabet)//2]}** → **{transformed[len(alphabet)//2]}**
        """)
    
    def show_text_stats(self, original, transformed, operation):
        """Показывает статистику преобразования"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Исходная длина", len(original))
        with col2:
            st.metric("Результирующая длина", len(transformed))
        with col3:
            changed_chars = sum(1 for o, t in zip(original, transformed) if o != t and o.isalpha())
            st.metric("Изменено букв", changed_chars)
    
    def demo_involution(self, text, language):
        """Демонстрирует свойство инволюции (двойное применение = исходный текст)"""
        st.markdown("**Свойство инволюции:** двойное применение шифра возвращает исходный текст")
        
        step1 = self.atbash_encrypt(text, language)
        step2 = self.atbash_encrypt(step1, language)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"**Исходный текст:**\n{text}")
        with col2:
            st.warning(f"**После первого применения:**\n{step1}")
        with col3:
            if text == step2:
                st.success(f"**После второго применения:**\n{step2} ✅")
            else:
                st.error(f"**После второго применения:**\n{step2} ❌")
        
        # Визуализация преобразований
        if len(text) <= 10:  # Показываем только для коротких текстов
            st.markdown("**Пошаговая визуализация:**")
            for i, char in enumerate(text):
                if char.isalpha():
                    step1_char = self.atbash_encrypt(char, language)
                    step2_char = self.atbash_encrypt(step1_char, language)
                    
                    col_a, col_b, col_c, col_d = st.columns([1, 1, 1, 2])
                    with col_a:
                        st.write(f"`{char}`")
                    with col_b:
                        st.write("→")
                    with col_c:
                        st.write(f"`{step1_char}`")
                    with col_d:
                        if char == step2_char:
                            st.success("✅ Инволюция")
                        else:
                            st.error("❌ Ошибка")

# Для обратной совместимости (если нужно)
class AtbashCipher(AtbashCipherModule):
    pass