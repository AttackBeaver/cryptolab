from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import string

class VigenereBreakModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Взлом шифра Виженера"
        self.description = "Криптоанализ через индекс совпадений и частотный анализ"
        self.category = "cryptanalysis"
        self.icon = ""
        self.order = 2
        
        # Эталонные частоты для английского и русского языков
        self.reference_frequencies = {
            'Английский': {
                'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 
                'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8, 
                'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0, 
                'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15,
                'Q': 0.10, 'Z': 0.07
            },
            'Русский': {
                'О': 10.97, 'Е': 8.45, 'А': 7.75, 'И': 7.32, 'Н': 6.70, 'Т': 6.26,
                'С': 5.47, 'Р': 5.21, 'В': 4.97, 'Л': 4.96, 'К': 3.47, 'М': 3.20,
                'Д': 3.18, 'П': 2.81, 'У': 2.62, 'Я': 2.01, 'Ы': 1.90, 'Ь': 1.74,
                'Г': 1.70, 'З': 1.65, 'Б': 1.59, 'Ч': 1.45, 'Й': 1.21, 'Х': 0.97,
                'Ж': 0.94, 'Ю': 0.64, 'Ш': 0.61, 'Ц': 0.48, 'Щ': 0.36, 'Э': 0.32,
                'Ф': 0.26, 'Ъ': 0.04, 'Ё': 0.04
            }
        }
    
    def render(self):
        st.title("🔓 Взлом шифра Виженера")
        st.subheader("Криптоанализ через индекс совпадений и частотный анализ")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            ### Метод криптоанализа шифра Виженера
            
            **Исторический контекст:** Шифр Виженера считался невзламываемым в течение 300 лет, 
            пока Чарльз Бэббидж не разработал метод взлома в 19 веке.
            
            **Принцип взлома:**
            1. **Определение длины ключа** через индекс совпадений (Index of Coincidence)
            2. **Разделение текста** на группы по позициям ключа
            3. **Частотный анализ** для каждой группы (как для шифра Цезаря)
            4. **Восстановление ключа** по найденным сдвигам
            
            **Индекс совпадений (IOC):**
            - Мера вероятности того, что два случайно выбранных символа одинаковы
            - Для естественного языка: ~0.065 (английский), ~0.055 (русский)
            - Для случайного текста: ~0.038 (26 букв)
            - Пики IOC указывают на возможную длину ключа
            """)
        
        # Выбор языка
        language = st.radio(
            "Выберите язык текста:",
            ["Английский", "Русский"],
            index=0,
            horizontal=True
        )
        
        # Ввод зашифрованного текста
        st.markdown("### 🔐 Ввод зашифрованного текста")
        
        # Примеры для тестирования
        examples = {
            "Английский": "KXWXCYQKZVVN XH WPQ IZIXMZOM, EOPQ QV WXZ LQCM EOPQ KXWXCYQKZVVN XH WPQ IZIXMZOM",
            "Русский": "ФЩРЮБЦЫЧСБФЩЛЭЪ ФЮ ЛЗЁ ЫЛДФЁТВ, ТФКЕ ФЬФКЗУФЬ ЫПТЗ РИ ИБК ТФКЕ ФЩРЮБЦЫЧСБФЩЛЭЪ ФЮ ЛЗЁ ЫЛДФЁТВ"
        }
        
        cipher_text = st.text_area(
            "Зашифрованный текст Виженером:",
            examples[language],
            height=150,
            help="Введите текст, зашифрованный шифром Виженера"
        )
        
        # Отладочная информация
        with st.expander("🔧 Отладочная информация", expanded=False):
            if cipher_text.strip():
                alphabet = self.get_alphabet(language)
                clean_text = ''.join([c for c in cipher_text.upper() if c in alphabet])
                st.write(f"Букв в тексте: {len(clean_text)}")
                st.write(f"Топ-5 букв: {self.get_top_letters_debug(clean_text, language)}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🔍 Автоматический анализ")
            
            if st.button("🚀 Начать автоматический взлом", type="primary", use_container_width=True):
                if not cipher_text.strip():
                    st.error("Введите зашифрованный текст!")
                else:
                    with st.spinner("Анализирую текст..."):
                        self.break_vigenere(cipher_text, language)
        
        with col2:
            st.markdown("### ⚙️ Ручные режимы")
            
            # Режим 1: Ручной ввод длины ключа
            st.markdown("**Режим 1: Указание длины ключа**")
            manual_key_length = st.number_input(
                "Длина ключа:",
                min_value=2,
                max_value=20,
                value=3,
                help="Если автоматика не справляется, укажите длину ключа вручную"
            )
            
            if st.button("🔧 Взлом с указанной длиной", use_container_width=True):
                if not cipher_text.strip():
                    st.error("Введите зашифрованный текст!")
                else:
                    with st.spinner("Анализирую с указанной длиной ключа..."):
                        self.break_vigenere_manual_length(cipher_text, language, manual_key_length)
            
            st.markdown("---")
            
            # Режим 2: Ручной ввод ключа
            st.markdown("**Режим 2: Прямой ввод ключа**")
            manual_key = st.text_input(
                "Ключ для расшифровки:",
                value="KEY" if language == "Английский" else "КЛЮЧ",
                help="Введите предполагаемый ключ (например: КРИПТОГРАФИЯ вместо КРИПТТГРАФМГ)"
            )
            
            if st.button("🔑 Расшифровать с указанным ключом", use_container_width=True):
                if not cipher_text.strip():
                    st.error("Введите зашифрованный текст!")
                elif not manual_key.strip():
                    st.error("Введите ключ!")
                else:
                    with st.spinner("Расшифровываю..."):
                        self.decrypt_with_key(cipher_text, language, manual_key)
    
    def get_alphabet(self, language):
        """Возвращает алфавит для выбранного языка"""
        if language == "Английский":
            return [chr(i) for i in range(65, 91)]  # A-Z
        else:  # Русский
            alphabet = [chr(i) for i in range(1040, 1072)]  # А-Я
            alphabet.insert(6, 'Ё')  # Добавляем Ё
            return alphabet
    
    def calculate_ioc(self, text):
        """Вычисляет индекс совпадений для текста"""
        if len(text) < 2:
            return 0
        
        total_chars = len(text)
        frequencies = Counter(text)
        
        ioc = 0
        for count in frequencies.values():
            ioc += count * (count - 1)
        
        ioc /= total_chars * (total_chars - 1)
        return ioc
    
    def find_key_length(self, cipher_text, language, max_key_length=20):
        """Определяет длину ключа через индекс совпадений"""
        alphabet = self.get_alphabet(language)
        cipher_clean = ''.join([c for c in cipher_text.upper() if c in alphabet])
        
        if len(cipher_clean) < 50:
            st.warning("⚠️ Текст слишком короткий для надежного определения длины ключа")
        
        ioc_results = []
        
        for key_len in range(1, max_key_length + 1):
            # Разделяем текст на группы
            groups = [''] * key_len
            for i, char in enumerate(cipher_clean):
                groups[i % key_len] += char
            
            # Вычисляем средний IOC для групп
            group_iocs = []
            for group in groups:
                if len(group) > 1:
                    group_ioc = self.calculate_ioc(group)
                    group_iocs.append(group_ioc)
            
            if group_iocs:
                avg_ioc = sum(group_iocs) / len(group_iocs)
                ioc_results.append((key_len, avg_ioc))
            else:
                ioc_results.append((key_len, 0))
        
        return ioc_results
    
    def break_vigenere(self, cipher_text, language):
        """Основной метод взлома шифра Виженера"""
        
        st.markdown("---")
        st.markdown("## 🎯 Процесс автоматического взлома")
        
        # Шаг 1: Определение длины ключа
        st.markdown("### 1. Определение длины ключа")
        
        ioc_results = self.find_key_length(cipher_text, language)
        
        if not ioc_results:
            st.error("Не удалось проанализировать текст")
            return
        
        # Визуализация IOC
        self.plot_ioc_results(ioc_results, language)
        
        # Выбираем наиболее вероятную длину ключа (игнорируем длину 1)
        filtered_results = [r for r in ioc_results if r[0] > 1]
        if not filtered_results:
            filtered_results = ioc_results
        
        best_key_length = max(filtered_results, key=lambda x: x[1])[0]
        st.success(f"**Наиболее вероятная длина ключа:** {best_key_length}")
        
        # Шаг 2: Взлом для найденной длины ключа
        self.break_with_key_length(cipher_text, language, best_key_length, "автоматического")
    
    def break_vigenere_manual_length(self, cipher_text, language, key_length):
        """Взлом с указанной длиной ключа"""
        st.markdown("---")
        st.markdown("## 🎯 Процесс взлома (ручной режим - длина ключа)")
        st.info(f"Используется указанная длина ключа: {key_length}")
        self.break_with_key_length(cipher_text, language, key_length, "ручного")
    
    def break_with_key_length(self, cipher_text, language, key_length, mode="автоматического"):
        """Взлом шифра для заданной длины ключа"""
        
        # Шаг 2: Разделение текста на группы
        st.markdown("### 2. Разделение текста на группы")
        
        alphabet = self.get_alphabet(language)
        cipher_clean = ''.join([c for c in cipher_text.upper() if c in alphabet])
        
        groups = [''] * key_length
        for i, char in enumerate(cipher_clean):
            groups[i % key_length] += char
        
        # Показываем группы
        group_df = pd.DataFrame({
            'Позиция ключа': range(1, key_length + 1),
            'Длина группы': [len(group) for group in groups],
            'Текст группы': [group[:30] + '...' if len(group) > 30 else group for group in groups]
        })
        st.dataframe(group_df, use_container_width=True, hide_index=True)
        
        # Шаг 3: Частотный анализ для каждой группы
        st.markdown("### 3. Частотный анализ по группам")
        
        key_letters = []
        full_analysis = []
        
        for pos, group in enumerate(groups):
            if len(group) < 10:  # Минимальная длина для анализа
                st.warning(f"Группа {pos+1} слишком короткая для надежного анализа")
                key_letters.append('?')
                continue
                
            # Находим лучший сдвиг для этой группы
            best_shift, best_score = self.find_best_shift_for_group(group, language)
            key_letter = alphabet[best_shift]
            key_letters.append(key_letter)
            
            # Собираем информацию для отчета
            group_freq = self.calculate_frequencies(group, language)
            full_analysis.append({
                'Позиция': pos + 1,
                'Длина группы': len(group),
                'Лучший сдвиг': best_shift,
                'Буква ключа': key_letter,
                'Оценка качества': f"{best_score:.3f}",
                'Топ-3 буквы в группе': self.get_top_letters(group_freq, 3)
            })
        
        # Показываем анализ по группам
        if full_analysis:
            analysis_df = pd.DataFrame(full_analysis)
            st.dataframe(analysis_df, use_container_width=True, hide_index=True)
        else:
            st.error("Не удалось проанализировать группы")
            return
        
        # Шаг 4: Восстановление ключа и расшифровка
        st.markdown("### 4. Результат взлома")
        
        found_key = ''.join(key_letters)
        st.success(f"**Найденный ключ:** `{found_key}`")
        
        # Показываем подсказку для ручного исправления
        if mode == "автоматического":
            st.info("💡 **Совет:** Если ключ выглядит неправильно (например: КРИПТТГРАФМГ), "
                   "попробуйте исправить его в ручном режиме ввода ключа!")
        
        # Расшифровываем текст
        decrypted_text = self.vigenere_decrypt(cipher_text, found_key, language)
        st.success("**Расшифрованный текст:**")
        st.info(decrypted_text)
        
        # Проверяем, похож ли текст на осмысленный
        if self.is_likely_text(decrypted_text, language):
            st.success("✅ Текст выглядит осмысленным!")
        else:
            st.warning("⚠️ Текст может быть некорректно расшифрован")
            
            if mode == "автоматического":
                st.info("🔧 Попробуйте использовать ручной режим с указанием длины ключа или прямого ввода ключа")
        
        # Показываем сравнение
        st.markdown("#### 📊 Сравнение")
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_area("Зашифрованный текст:", cipher_text, height=150, key=f"cipher_{mode}")
        
        with col2:
            st.text_area("Расшифрованный текст:", decrypted_text, height=150, key=f"decrypted_{mode}")
    
    def decrypt_with_key(self, cipher_text, language, key):
        """Расшифровка с указанным ключом"""
        st.markdown("---")
        st.markdown("## 🎯 Расшифровка с указанным ключом")
        
        # Проверяем ключ
        alphabet = self.get_alphabet(language)
        key_clean = ''.join([c for c in key.upper() if c in alphabet])
        
        if not key_clean:
            st.error("Ключ должен содержать только буквы выбранного языка!")
            return
        
        st.success(f"**Используемый ключ:** `{key_clean}`")
        
        # Расшифровываем текст
        decrypted_text = self.vigenere_decrypt(cipher_text, key_clean, language)
        st.success("**Расшифрованный текст:**")
        st.info(decrypted_text)
        
        # Проверяем, похож ли текст на осмысленный
        if self.is_likely_text(decrypted_text, language):
            st.success("✅ Текст выглядит осмысленным!")
        else:
            st.warning("⚠️ Текст может быть некорректно расшифрован. Попробуйте другой ключ.")
        
        # Показываем сравнение
        st.markdown("#### 📊 Сравнение")
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_area("Зашифрованный текст:", cipher_text, height=150, key="cipher_manual")
        
        with col2:
            st.text_area("Расшифрованный текст:", decrypted_text, height=150, key="decrypted_manual")
    
    def find_best_shift_for_group(self, group_text, language):
        """Находит лучший сдвиг для группы текста через частотный анализ"""
        alphabet = self.get_alphabet(language)
        ref_freq = self.reference_frequencies[language]
        
        group_freq = self.calculate_frequencies(group_text, language)
        
        best_shift = 0
        best_score = float('inf')
        
        for shift in range(len(alphabet)):
            score = 0
            matched = 0
            
            for letter, expected_freq in ref_freq.items():
                if letter in alphabet:
                    # Вычисляем, какая буква должна быть в зашифрованном тексте
                    original_index = alphabet.index(letter)
                    cipher_index = (original_index + shift) % len(alphabet)
                    cipher_letter = alphabet[cipher_index]
                    
                    observed_freq = group_freq.get(cipher_letter, 0)
                    
                    # Используем квадратичную ошибку
                    error = (observed_freq - expected_freq) ** 2
                    score += error
                    matched += 1
            
            if matched > 0:
                score = score / matched  # Нормализуем
                
            if score < best_score:
                best_score = score
                best_shift = shift
        
        return best_shift, best_score
    
    def calculate_frequencies(self, text, language):
        """Вычисляет частоты букв в тексте"""
        alphabet = self.get_alphabet(language)
        text_upper = text.upper()
        
        letter_count = Counter([char for char in text_upper if char in alphabet])
        total_letters = sum(letter_count.values())
        
        frequencies = {}
        for letter in alphabet:
            count = letter_count.get(letter, 0)
            frequencies[letter] = (count / total_letters * 100) if total_letters > 0 else 0
        
        return frequencies
    
    def get_top_letters(self, frequencies, n=3):
        """Возвращает топ-N самых частых букв"""
        sorted_letters = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        return ', '.join([f"{letter}({freq:.1f}%)" for letter, freq in sorted_letters[:n]])
    
    def get_top_letters_debug(self, text, language):
        """Отладочная функция для получения топ букв"""
        alphabet = self.get_alphabet(language)
        text_upper = ''.join([c for c in text.upper() if c in alphabet])
        
        if not text_upper:
            return "Нет букв"
            
        counter = Counter(text_upper)
        total = sum(counter.values())
        
        top_letters = counter.most_common(5)
        return ', '.join([f"{letter}({count/total*100:.1f}%)" for letter, count in top_letters])
    
    def vigenere_decrypt(self, text, key, language):
        """Дешифрует текст методом Виженера"""
        alphabet = self.get_alphabet(language)
        result = []
        
        key = key.upper()
        key_index = 0
        
        for char in text:
            upper_char = char.upper()
            if upper_char in alphabet:
                # Дешифруем букву
                text_pos = alphabet.index(upper_char)
                key_char = key[key_index % len(key)]
                key_pos = alphabet.index(key_char)
                
                new_pos = (text_pos - key_pos) % len(alphabet)
                
                if char.isupper():
                    result.append(alphabet[new_pos])
                else:
                    result.append(alphabet[new_pos].lower())
                
                key_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def is_likely_text(self, text, language):
        """Проверяет, похож ли текст на осмысленный"""
        common_words = {
            'Английский': ['THE', 'AND', 'YOU', 'THAT', 'WAS', 'FOR', 'ARE', 'WITH', 'THIS', 'HAVE'],
            'Русский': ['И', 'В', 'НЕ', 'НА', 'Я', 'БЫТЬ', 'С', 'ЧТО', 'ОН', 'ОНА', 'ЭТО', 'ТО', 'ВОТ']
        }
        
        text_upper = text.upper()
        words = text_upper.split()
        
        # Если есть несколько общих слов, считаем текст осмысленным
        common_count = sum(1 for word in words if word in common_words[language])
        return common_count >= 2
    
    def plot_ioc_results(self, ioc_results, language):
        """Визуализирует результаты расчета IOC"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        key_lengths = [result[0] for result in ioc_results]
        ioc_values = [result[1] for result in ioc_results]
        
        # Референсные значения IOC
        lang_ioc_ref = 0.065 if language == "Английский" else 0.055
        random_ioc_ref = 1 / len(self.get_alphabet(language))
        
        bars = ax.bar(key_lengths, ioc_values, alpha=0.7, color='lightblue')
        ax.axhline(y=lang_ioc_ref, color='green', linestyle='--', label=f'IOC естественного языка (~{lang_ioc_ref:.3f})')
        ax.axhline(y=random_ioc_ref, color='red', linestyle='--', label=f'IOC случайного текста (~{random_ioc_ref:.3f})')
        
        # Подсвечиваем лучший результат (игнорируем длину 1)
        filtered_results = [r for r in ioc_results if r[0] > 1]
        if filtered_results:
            best_key_length = max(filtered_results, key=lambda x: x[1])[0]
            best_idx = key_lengths.index(best_key_length)
            bars[best_idx].set_color('orange')
            bars[best_idx].set_alpha(0.9)
        
        ax.set_xlabel('Длина ключа')
        ax.set_ylabel('Индекс совпадений (IOC)')
        ax.set_title('Определение длины ключа через индекс совпадений')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        # Таблица результатов
        ioc_df = pd.DataFrame({
            'Длина ключа': key_lengths,
            'Индекс совпадений': [f'{ioc:.4f}' for ioc in ioc_values]
        })
        st.dataframe(ioc_df, use_container_width=True, hide_index=True)