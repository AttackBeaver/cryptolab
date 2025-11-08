from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import string

class FrequencyAnalysisModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Частотный анализ шифра Цезаря"
        self.description = "Взлом шифра Цезаря методом частотного анализа"
        self.complexity = "intermediate"
        self.category = "cryptanalysis"
        self.icon = ""
        self.order = 1
        
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
        st.title("🔍 Частотный анализ")
        st.subheader("Взлом шифра Цезаря методом анализа частот букв")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка"):
            st.markdown("""
            **Частотный анализ** - один из старейших методов криптоанализа, основанный на том, 
            что в каждом языке буквы встречаются с определенной частотой.
            
            **Принцип работы:**
            1. Собираем статистику частот букв в зашифрованном тексте
            2. Сравниваем с эталонным распределением частот языка
            3. Находим сдвиг, при котором распределение наиболее близко к эталонному
            4. Этот сдвиг и есть ключ шифра!
            
            **Историческое значение:**
            - Использовался для взлома моноалфавитных шифров
            - Эффективен против шифра Цезаря, простой замены и т.д.
            - Бесполезен против полиалфавитных шифров (Виженер)
            
            **Эффективность:** Работает лучше всего на текстах длиной более 100 символов
            """)
        
        # Выбор языка
        language = st.radio(
            "Выберите язык текста:",
            ["Английский", "Русский"],
            index=0,
            horizontal=True
        )
        
        # col1, col2 = st.columns([2, 1])
        
        # with col1:
        st.subheader("🔐 Ввод зашифрованного текста")
        
        # Примеры текстов для тестирования
        examples = {
            "Английский": "YMNX NX F QJYYJW FSI FQUMJWFQ BNYM YT TZW FSI TZW DTZ F KJB",
            "Русский": "ПТЛЗ Б ЛЗЁ ЫЛДФЁТВ ТФКЕ ФЬФКЗУФЬ ЫПТЗ РИ ИБК ТФКЕ ИБК ЛИБ ЫПЗ"
        }
        
        cipher_text = st.text_area(
            "Зашифрованный текст:",
            examples[language],
            height=150,
            help="Введите текст, зашифрованный шифром Цезаря"
        )
        
        # Предупреждение о длине текста
        text_length = len([c for c in cipher_text.upper() if c in self.get_alphabet(language)])
        if text_length < 50:
            st.warning(f"⚠️ Текст короткий ({text_length} букв). Для надежного анализа нужно >50 букв.")
        else:
            st.success(f"✅ Текст достаточной длины ({text_length} букв)")
        
        # with col2:
        st.subheader("🎯 Управление анализом")
        if st.button("🔍 Начать анализ", type="primary", use_container_width=True):
            if not cipher_text.strip():
                st.error("Введите зашифрованный текст!")
            else:
                with st.spinner("Анализирую частоты..."):
                    self.analyze_text(cipher_text, language)
        
        st.markdown("---")
        st.markdown("""
        **Советы:**
        - Используйте длинные тексты
        - Убедитесь, что язык выбран правильно
        - Проверьте результат ручным подбором
        """)
        
        # Ручной подбор сдвига
        st.markdown("---")
        st.subheader("🎮 Интерактивный подбор сдвига")
        
        if cipher_text.strip():
            alphabet_size = 26 if language == "Английский" else 33
            shift = st.slider("Сдвиг для дешифровки:", 0, alphabet_size-1, 0, 
                            help="Покрутите ползунок чтобы найти правильный сдвиг")
            
            decrypted = self.caesar_decrypt(cipher_text, shift, language)
            st.text_area("Результат дешифровки:", decrypted, height=100)
            
            # Подсветка когда найден правильный сдвиг
            if self.is_likely_text(decrypted, language):
                st.success("🎉 Вероятно, это правильный текст!")
    
    def analyze_text(self, cipher_text, language):
        """Основной метод анализа текста"""
        
        # Отладочная информация
        st.write("🔍 **Отладочная информация:**")
        
        # Шаг 1: Анализ частот в зашифрованном тексте
        cipher_freq = self.calculate_frequencies(cipher_text, language)
        
        # Покажем топ-5 самых частых букв в шифртексте
        top_letters = sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        st.write(f"Топ-5 букв в шифртексте: {[f'{ltr}({freq:.1f}%)' for ltr, freq in top_letters]}")
        
        # Покажем топ-5 самых частых букв в языке
        ref_top = sorted(self.reference_frequencies[language].items(), key=lambda x: x[1], reverse=True)[:5]
        st.write(f"Топ-5 букв в языке: {[f'{ltr}({freq:.1f}%)' for ltr, freq in ref_top]}")
        
        # Шаг 2: Поиск наилучшего сдвига
        best_shift, best_score, all_scores = self.find_best_shift(cipher_freq, language)
        
        st.write(f"Найденный сдвиг: **{best_shift}** (оценка качества: {best_score:.3f})")
        
        # Покажем топ-3 кандидата
        top_candidates = sorted(all_scores.items(), key=lambda x: x[1])[:3]
        st.write(f"Лучшие кандидаты: {[f'сдвиг {shift}({score:.3f})' for shift, score in top_candidates]}")
        
        # Шаг 3: Визуализация
        self.visualize_analysis(cipher_freq, language, best_shift, best_score, all_scores)
        
        # Шаг 4: Показ результатов
        self.show_results(cipher_text, best_shift, language)
    
    def get_alphabet(self, language):
        """Возвращает алфавит для выбранного языка"""
        if language == "Английский":
            return [chr(i) for i in range(65, 91)]  # A-Z (26 букв)
        else:  # Русский
            # А-Я (32 буквы) + Ё
            alphabet = [chr(i) for i in range(1040, 1072)]  # А-Я
            # Добавляем Ё в правильную позицию (после Е)
            alphabet.insert(6, 'Ё')  # А, Б, В, Г, Д, Е, Ё, Ж, ...
            return alphabet
    
    def calculate_frequencies(self, text, language):
        """Вычисляет частоты букв в тексте"""
        # Получаем алфавит для языка
        alphabet = self.get_alphabet(language)
        
        # Считаем буквы
        text_upper = text.upper()
        letter_count = Counter([char for char in text_upper if char in alphabet])
        total_letters = sum(letter_count.values())
        
        # Вычисляем частоты в процентах
        frequencies = {}
        for letter in alphabet:
            count = letter_count.get(letter, 0)
            frequencies[letter] = (count / total_letters * 100) if total_letters > 0 else 0
        
        return frequencies
    
    def find_best_shift(self, cipher_freq, language):
        """Находит наилучший сдвиг путем сравнения с эталонными частотами"""
        alphabet = self.get_alphabet(language)
        alphabet_size = len(alphabet)
        ref_freq = self.reference_frequencies[language]
        
        best_shift = 0
        best_score = float('inf')
        all_scores = {}
        
        # Перебираем все возможные сдвиги
        for shift in range(alphabet_size):
            total_diff = 0
            compared_pairs = 0
            
            # Для каждой буквы в эталонном распределении
            for original_letter, expected_freq in ref_freq.items():
                if original_letter not in alphabet:
                    continue
                    
                # Вычисляем, какой будет зашифрованная буква при данном сдвиге
                original_index = alphabet.index(original_letter)
                cipher_index = (original_index + shift) % alphabet_size
                cipher_letter = alphabet[cipher_index]
                
                # Получаем наблюдаемую частоту для этой зашифрованной буквы
                observed_freq = cipher_freq.get(cipher_letter, 0)
                
                # Учитываем разницу
                if expected_freq > 0:
                    diff = (observed_freq - expected_freq) ** 2
                    total_diff += diff
                    compared_pairs += 1
            
            # Вычисляем среднюю квадратичную ошибку
            if compared_pairs > 0:
                score = total_diff / compared_pairs
            else:
                score = float('inf')
            
            all_scores[shift] = score
            
            if score < best_score:
                best_score = score
                best_shift = shift
        
        return best_shift, best_score, all_scores
    
    def visualize_analysis(self, cipher_freq, language, best_shift, best_score, all_scores):
        """Визуализирует сравнение частот"""
        alphabet = self.get_alphabet(language)
        ref_freq = self.reference_frequencies[language]
        
        # Создаем DataFrame для отображения
        freq_data = []
        for letter in alphabet:
            if letter in ref_freq:
                freq_data.append({
                    'Буква': letter,
                    'Эталонная частота (%)': ref_freq[letter],
                    'Частота в тексте (%)': round(cipher_freq.get(letter, 0), 2),
                    'Разница': round(abs(ref_freq[letter] - cipher_freq.get(letter, 0)), 2)
                })
        
        df = pd.DataFrame(freq_data)
        
        # Показываем таблицу
        st.subheader("📊 Таблица частот")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Строим графики
        st.subheader("📈 Визуализация анализа")
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12))
        
        # График 1: Столбчатая диаграмма сравнения частот
        x = np.arange(len(alphabet))
        width = 0.35
        
        ref_values = [ref_freq.get(letter, 0) for letter in alphabet]
        cipher_values = [cipher_freq.get(letter, 0) for letter in alphabet]
        
        bars1 = ax1.bar(x - width/2, ref_values, width, label='Эталонные частоты', alpha=0.7, color='blue')
        bars2 = ax1.bar(x + width/2, cipher_values, width, label='Частоты в тексте', alpha=0.7, color='red')
        ax1.set_xlabel('Буквы')
        ax1.set_ylabel('Частота (%)')
        ax1.set_title('Сравнение частот букв')
        ax1.set_xticks(x)
        ax1.set_xticklabels(alphabet)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # График 2: Оценки качества для всех сдвигов
        shifts = list(all_scores.keys())
        scores = list(all_scores.values())
        ax2.plot(shifts, scores, 'go-', linewidth=2, markersize=4, label='Оценка качества')
        ax2.axvline(x=best_shift, color='red', linestyle='--', label=f'Лучший сдвиг: {best_shift}')
        ax2.set_xlabel('Сдвиг')
        ax2.set_ylabel('Оценка качества (меньше = лучше)')
        ax2.set_title('Качество дешифровки для разных сдвигов')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # График 3: Лучшее сопоставление частот
        best_ref_values = []
        best_cipher_values = []
        best_letters = []
        
        for letter in alphabet:
            if letter in ref_freq:
                # Для лучшего сдвига: какая буква соответствует исходной
                original_index = (alphabet.index(letter) - best_shift) % len(alphabet)
                original_letter = alphabet[original_index]
                expected_freq = ref_freq.get(original_letter, 0)
                
                best_ref_values.append(expected_freq)
                best_cipher_values.append(cipher_freq.get(letter, 0))
                best_letters.append(letter)
        
        x_best = np.arange(len(best_letters))
        ax3.bar(x_best - width/2, best_ref_values, width, label='Ожидаемые частоты', alpha=0.7, color='green')
        ax3.bar(x_best + width/2, best_cipher_values, width, label='Фактические частоты', alpha=0.7, color='orange')
        ax3.set_xlabel('Буквы (после применения лучшего сдвига)')
        ax3.set_ylabel('Частота (%)')
        ax3.set_title('Сопоставление частот при лучшем сдвиге')
        ax3.set_xticks(x_best)
        ax3.set_xticklabels(best_letters)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def show_results(self, cipher_text, best_shift, language):
        """Показывает результаты дешифровки"""
        st.subheader("🎉 Результат взлома")
        
        decrypted = self.caesar_decrypt(cipher_text, best_shift, language)
        st.success(f"**Расшифрованный текст:**")
        st.info(decrypted)
        
        st.markdown(f"""
        **Детали взлома:**
        - Найденный сдвиг: **{best_shift}**
        - Метод: частотный анализ
        - Сравнение с эталонным распределением языка
        
        **Проверка:** Используйте ползунок выше чтобы проверить соседние сдвиги
        """)
    
    def caesar_decrypt(self, text, shift, language):
        """Дешифрует текст методом Цезаря"""
        alphabet = self.get_alphabet(language)
        alphabet_size = len(alphabet)
        result = ""
        
        for char in text:
            upper_char = char.upper()
            if upper_char in alphabet:
                pos = alphabet.index(upper_char)
                new_pos = (pos - shift) % alphabet_size
                if char.isupper():
                    result += alphabet[new_pos]
                else:
                    result += alphabet[new_pos].lower()
            else:
                result += char
        
        return result
    
    def is_likely_text(self, text, language):
        """Проверяет, похож ли текст на осмысленный текст на указанном языке"""
        # Простая эвристика: проверяем наличие часто встречающихся слов
        common_words = {
            'Английский': ['THE', 'AND', 'YOU', 'THAT', 'WAS', 'FOR', 'ARE', 'WITH', 'THIS', 'HAVE'],
            'Русский': ['И', 'В', 'НЕ', 'НА', 'Я', 'БЫТЬ', 'С', 'ЧТО', 'Он', 'ОНА', 'ЭТО', 'ТО']
        }
        
        text_upper = text.upper()
        words = text_upper.split()
        
        # Если есть несколько общих слов, считаем текст осмысленным
        common_count = sum(1 for word in words if word in common_words[language])
        return common_count >= 2