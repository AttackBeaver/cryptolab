from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import random
import string

class PolybiusBreakModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Взлом Полибианского квадрата"
        self.description = "Методы криптоанализа и взлома квадрата Полибия"
        self.category = "cryptanalysis"
        self.icon = ""
        self.order = 3
    
    def render(self):
        st.title("🔓 Взлом Полибианского квадрата")
        st.subheader("Методы криптоанализа и восстановления ключа")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            ### Методы криптоанализа Полибианского квадрата
            
            **Уязвимости шифра:**
            1. **Статистический анализ** - частоты букв сохраняются в координатах
            2. **Паттерны в координатах** - повторяющиеся последовательности
            3. **Известный открытый текст** - восстановление отображения
            4. **Анализ структуры квадрата** - поиск закономерностей
            
            **Основные подходы:**
            - **Частотный анализ координат** - самые частые координаты → самые частые буквы
            - **Анализ биграмм** - частые сочетания букв
            - **Метод проб и ошибок** - перебор возможных квадратов
            - **Использование известных слов** - криптоанализ по контексту
            """)
        
        # Выбор метода атаки
        attack_method = st.radio(
            "Выберите метод атаки:",
            ["📊 Частотный анализ", "🔍 Анализ паттернов", "🎯 Атака по известному тексту", "🔄 Автоматический взлом"],
            horizontal=True
        )
        
        if attack_method == "📊 Частотный анализ":
            self.render_frequency_analysis()
        elif attack_method == "🔍 Анализ паттернов":
            self.render_pattern_analysis()
        elif attack_method == "🎯 Атака по известному тексту":
            self.render_known_plaintext_attack()
        else:
            self.render_auto_break()
    
    def render_frequency_analysis(self):
        """Частотный анализ зашифрованного текста"""
        st.markdown("### 📊 Частотный анализ координат")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Ввод зашифрованного текста")
            ciphertext = st.text_area(
                "Зашифрованный текст:",
                "23 15 31 31 34 23 15 31 31 34 44 11 42 44 32 15 43",
                height=150,
                help="Введите текст, зашифрованный квадратом Полибия (координаты через пробел)"
            )
            
            language = st.radio(
                "Предполагаемый язык:",
                ["Английский", "Русский"],
                index=0,
                horizontal=True
            )
            
            square_size = st.radio(
                "Предполагаемый размер квадрата:",
                ["5×5", "6×5", "6×6"],
                index=0,
                horizontal=True
            )
        
        with col2:
            st.markdown("#### Анализ частот")
            
            if st.button("📈 Выполнить частотный анализ", type="primary"):
                if not ciphertext.strip():
                    st.error("Введите зашифрованный текст!")
                    return
                
                with st.spinner("Анализирую частоты координат..."):
                    self.perform_frequency_analysis(ciphertext, language, square_size)
        
        # Теория частотного анализа
        st.markdown("---")
        st.markdown("#### 📚 Теория частотного анализа")
        
        if language == "Английский":
            freq_data = [
                {'Буква': 'E', 'Частота%': 12.7, 'Пример': 'THE, BEEN, SEE'},
                {'Буква': 'T', 'Частота%': 9.1, 'Пример': 'THE, IT, THAT'},
                {'Буква': 'A', 'Частота%': 8.2, 'Пример': 'AND, HAVE, ARE'},
                {'Буква': 'O', 'Частота%': 7.5, 'Пример': 'OF, TO, FOR'},
                {'Буква': 'I', 'Частота%': 7.0, 'Пример': 'IN, IS, IT'},
            ]
        else:
            freq_data = [
                {'Буква': 'О', 'Частота%': 10.97, 'Пример': 'ОН, ОНА, ЭТО'},
                {'Буква': 'Е', 'Частота%': 8.45, 'Пример': 'НЕТ, ДА, ЕСТЬ'},
                {'Буква': 'А', 'Частота%': 7.75, 'Пример': 'И, А, ДА'},
                {'Буква': 'И', 'Частота%': 7.32, 'Пример': 'ИЛИ, ИМ, ИХ'},
                {'Буква': 'Н', 'Частота%': 6.70, 'Пример': 'ОН, НА, НО'},
            ]
        
        st.dataframe(pd.DataFrame(freq_data), use_container_width=True, hide_index=True)
        
        st.info("""
        **Принцип:** Самые частые координаты в шифротексте соответствуют самым частым буквам языка.
        Сравнивая распределение частот координат с эталонным распределением букв, 
        можно восстановить отображение координат на буквы.
        """)
    
    def perform_frequency_analysis(self, ciphertext, language, square_size):
        """Выполняет частотный анализ зашифрованного текста"""
        # Парсим координаты
        coordinates = self.parse_coordinates(ciphertext)
        
        if not coordinates:
            st.error("Не удалось распознать координаты в тексте!")
            return
        
        # Анализируем частоты координат
        coord_freq = Counter(coordinates)
        total_coords = len(coordinates)
        
        # Сортируем по частоте
        sorted_coords = coord_freq.most_common()
        
        # Эталонные частоты букв
        if language == "Английский":
            letter_freq = {
                'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
                'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8,
                'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
                'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15,
                'Q': 0.10, 'Z': 0.07
            }
            # Для квадрата 5×5 объединяем I и J
            if square_size == "5×5":
                letter_freq['I'] = letter_freq.get('I', 0) + letter_freq.get('J', 0)
                if 'J' in letter_freq:
                    del letter_freq['J']
        else:  # Русский
            letter_freq = {
                'О': 10.97, 'Е': 8.45, 'А': 7.75, 'И': 7.32, 'Н': 6.70, 'Т': 6.26,
                'С': 5.47, 'Р': 5.21, 'В': 4.97, 'Л': 4.96, 'К': 3.47, 'М': 3.20,
                'Д': 3.18, 'П': 2.81, 'У': 2.62, 'Я': 2.01, 'Ы': 1.90, 'Ь': 1.74,
                'Г': 1.70, 'З': 1.65, 'Б': 1.59, 'Ч': 1.45, 'Й': 1.21, 'Х': 0.97,
                'Ж': 0.94, 'Ю': 0.64, 'Ш': 0.61, 'Ц': 0.48, 'Щ': 0.36, 'Э': 0.32,
                'Ф': 0.26, 'Ъ': 0.04, 'Ё': 0.04
            }
        
        # Ограничиваем по размеру квадрата
        max_letters = 25 if square_size == "5×5" else 30 if square_size == "6×5" else 36
        letter_freq = dict(list(letter_freq.items())[:max_letters])
        
        # Создаем предполагаемое отображение
        mapping = {}
        for i, (coord, _) in enumerate(sorted_coords[:len(letter_freq)]):
            if i < len(letter_freq):
                letter = list(letter_freq.keys())[i]
                mapping[coord] = letter
        
        # Показываем результаты
        st.success("### 🎯 Результаты частотного анализа")
        
        # Таблица соответствий
        st.markdown("#### 📋 Предполагаемое отображение координат на буквы")
        mapping_data = []
        for coord, letter in mapping.items():
            mapping_data.append({
                'Координаты': coord,
                'Предполагаемая буква': letter,
                'Частота в тексте': f"{(coord_freq[coord]/total_coords)*100:.1f}%",
                'Ожидаемая частота': f"{letter_freq[letter]:.1f}%"
            })
        
        st.dataframe(pd.DataFrame(mapping_data), use_container_width=True, hide_index=True)
        
        # Пробуем дешифровать
        st.markdown("#### 🔤 Попытка дешифровки")
        decrypted = self.decrypt_with_mapping(ciphertext, mapping)
        st.text_area("Дешифрованный текст (предварительно):", decrypted, height=100)
        
        # Визуализация частот
        self.visualize_frequency_comparison(coord_freq, letter_freq, total_coords, mapping)
        
        # Рекомендации по ручной корректировке
        st.markdown("---")
        st.markdown("#### 🛠️ Рекомендации по улучшению")
        st.write("""
        1. **Ищите осмысленные слова** в дешифрованном тексте
        2. **Корректируйте отображение** для частых биграмм (TH, HE, IN, ER и т.д.)
        3. **Используйте контекст** - предполагаемые темы сообщения
        4. **Проверяйте короткие слова** (I, A, THE, AND, TO)
        """)
    
    def render_pattern_analysis(self):
        """Анализ паттернов и биграмм"""
        st.markdown("### 🔍 Анализ паттернов и биграмм")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ciphertext = st.text_area(
                "Зашифрованный текст:",
                "23 15 31 31 34 44 11 42 44 32 15 43 23 15 31 31 34",
                height=150,
                key="pattern_text"
            )
            
            analysis_type = st.radio(
                "Тип анализа:",
                ["Анализ биграмм", "Поиск повторений", "Анализ расстояний"],
                horizontal=True
            )
        
        with col2:
            st.markdown("#### Статистический анализ")
            
            if st.button("🔍 Анализировать паттерны", type="primary"):
                if not ciphertext.strip():
                    st.error("Введите зашифрованный текст!")
                    return
                
                with st.spinner("Анализирую паттерны..."):
                    coordinates = self.parse_coordinates(ciphertext)
                    
                    if not coordinates:
                        st.error("Не удалось распознать координаты!")
                        return
                    
                    if analysis_type == "Анализ биграмм":
                        self.analyze_bigrams(coordinates)
                    elif analysis_type == "Поиск повторений":
                        self.find_repetitions(coordinates, ciphertext)
                    else:
                        self.analyze_distances(coordinates)
        
        # Теория анализа паттернов
        st.markdown("---")
        st.markdown("#### 📚 Теория анализа паттернов")
        
        st.write("""
        **Биграммы (сочетания двух букв):**
        - **Английский**: TH, HE, IN, ER, AN, RE, ED, ON, ES, ST, EN, AT, TO, NT, HA
        - **Русский**: СТ, ЕН, ОВ, НО, НА, РА, ВО, КО, ТО, РЕ, ЛИ, ПО, ПР, ЕС, ВЕ
        
        **Повторяющиеся последовательности:**
        - Могут указывать на часто встречающиеся слова (THE, AND, THAT)
        - Помогают определить размер квадрата
        - Позволяют найти границы слов
        """)
    
    def analyze_bigrams(self, coordinates):
        """Анализирует биграммы в зашифрованном тексте"""
        st.success("### 📊 Анализ биграмм")
        
        # Считаем биграммы
        bigrams = []
        for i in range(len(coordinates) - 1):
            bigram = f"{coordinates[i]}-{coordinates[i+1]}"
            bigrams.append(bigram)
        
        bigram_freq = Counter(bigrams)
        
        # Показываем топ-10 биграмм
        st.markdown("#### 🎯 Самые частые биграммы координат")
        bigram_data = []
        for bigram, count in bigram_freq.most_common(15):
            bigram_data.append({
                'Биграмма': bigram,
                'Частота': count,
                'Процент': f"{(count/len(bigrams))*100:.1f}%"
            })
        
        st.dataframe(pd.DataFrame(bigram_data), use_container_width=True, hide_index=True)
        
        # Сравнение с эталонными биграммами
        st.markdown("#### 📈 Сравнение с эталонными биграммами")
        
        # Эталонные биграммы для английского
        english_bigrams = [
            'TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ED', 'ON', 'ES', 'ST',
            'EN', 'AT', 'TO', 'NT', 'HA', 'ND', 'OU', 'EA', 'NG', 'AS'
        ]
        
        # Предполагаем отображение для топ биграмм
        st.info("**Предполагаемое отображение для топ-5 биграмм:**")
        mapping_suggestions = []
        for i, (bigram, _) in enumerate(bigram_freq.most_common(5)):
            if i < len(english_bigrams):
                mapping_suggestions.append(f"**{bigram}** → **{english_bigrams[i]}**")
        
        st.write(" | ".join(mapping_suggestions))
        
        # Визуализация распределения биграмм
        self.visualize_bigram_analysis(bigram_freq)
        
        # Рекомендации
        st.markdown("---")
        st.markdown("#### 💡 Рекомендации по использованию биграмм")
        st.write("""
        1. **Проверьте предполагаемые биграммы** в контексте
        2. **Ищите осмысленные сочетания** (THE, AND, ING)
        3. **Учитывайте позицию в слове** - начальные/конечные биграммы
        4. **Используйте для проверки** частотного анализа
        """)
    
    def find_repetitions(self, coordinates, ciphertext):
        """Находит повторяющиеся последовательности"""
        st.success("### 🔁 Поиск повторяющихся последовательностей")
        
        # Ищем повторяющиеся паттерны длиной 2-4 координаты
        patterns = {}
        
        for pattern_length in range(2, 5):
            for i in range(len(coordinates) - pattern_length + 1):
                pattern = tuple(coordinates[i:i + pattern_length])
                if pattern in patterns:
                    patterns[pattern].append(i)
                else:
                    patterns[pattern] = [i]
        
        # Фильтруем только повторяющиеся паттерны
        repeating_patterns = {pattern: positions for pattern, positions in patterns.items() if len(positions) > 1}
        
        if not repeating_patterns:
            st.info("⚠️ Повторяющиеся последовательности не найдены")
            return
        
        # Показываем найденные паттерны
        st.markdown("#### 📋 Найденные повторяющиеся последовательности")
        
        pattern_data = []
        for pattern, positions in sorted(repeating_patterns.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            pattern_str = ' '.join(pattern)
            distances = []
            for i in range(1, len(positions)):
                distances.append(positions[i] - positions[i-1])
            
            pattern_data.append({
                'Паттерн': pattern_str,
                'Повторения': len(positions),
                'Позиции': ', '.join(map(str, positions)),
                'Расстояния': ', '.join(map(str, distances))
            })
        
        st.dataframe(pd.DataFrame(pattern_data), use_container_width=True, hide_index=True)
        
        # Анализ возможных слов
        st.markdown("#### 🎯 Возможные соответствия")
        st.write("""
        **Частые английские слова:**
        - 2 буквы: OF, TO, IN, IT, IS, BE, AS, AT, SO, WE, HE, BY, OR, DO, IF
        - 3 буквы: THE, AND, FOR, ARE, BUT, NOT, YOU, ALL, ANY, CAN, HAD, HER
        - 4 буквы: THAT, WITH, HAVE, THIS, WILL, YOUR, FROM, THEY, KNOW, WANT
        
        **Сравните длину паттернов с типичными словами!**
        """)
        
        # Визуализация повторений
        self.visualize_repetitions(coordinates, repeating_patterns)
    
    def render_known_plaintext_attack(self):
        """Атака по известному открытому тексту"""
        st.markdown("### 🎯 Атака по известному открытому тексту")
        
        st.info("""
        **Принцип атаки:** Если известен фрагмент открытого текста и соответствующий ему шифротекст,
        можно восстановить часть квадрата Полибия и использовать эту информацию для взлома остального текста.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Известная пара текст-шифр")
            known_plaintext = st.text_input(
                "Известный открытый текст:",
                "HELLO",
                help="Фрагмент текста, который точно есть в сообщении"
            )
            
            known_ciphertext = st.text_input(
                "Соответствующий шифротекст:",
                "23 15 31 31 34",
                help="Координаты, соответствующие известному тексту"
            )
        
        with col2:
            st.markdown("#### Полный шифротекст для взлома")
            full_ciphertext = st.text_area(
                "Полный зашифрованный текст:",
                "23 15 31 31 34 44 11 42 44 32 15 43 23 15 31 31 34 11 33 44",
                height=100
            )
            
            if st.button("🔓 Выполнить атаку", type="primary"):
                if not all([known_plaintext, known_ciphertext, full_ciphertext]):
                    st.error("Заполните все поля!")
                    return
                
                with st.spinner("Выполняю атаку по известному тексту..."):
                    self.perform_known_plaintext_attack(known_plaintext, known_ciphertext, full_ciphertext)
        
        # Примеры использования
        st.markdown("---")
        st.markdown("#### 📝 Примеры известных текстов")
        
        examples = {
            "Английский": [
                "THE", "AND", "THAT", "WITH", "HAVE",
                "THIS", "WILL", "YOUR", "FROM", "THEY"
            ],
            "Русский": [
                "ПРИВЕТ", "МИР", "ЭТО", "ТАК", "ЧТО",
                "КАК", "ГДЕ", "КОГДА", "ПОЧЕМУ", "КТО"
            ]
        }
        
        for lang, words in examples.items():
            with st.expander(f"Частые слова ({lang})"):
                st.write(", ".join(words))
    
    def perform_known_plaintext_attack(self, known_plaintext, known_ciphertext, full_ciphertext):
        """Выполняет атаку по известному открытому тексту"""
        # Парсим координаты
        known_coords = self.parse_coordinates(known_ciphertext)
        full_coords = self.parse_coordinates(full_ciphertext)
        
        if len(known_plaintext) != len(known_coords):
            st.error(f"Длина известного текста ({len(known_plaintext)}) не совпадает с количеством координат ({len(known_coords)})!")
            return
        
        # Создаем отображение из известной пары
        mapping = {}
        for i, (plain_char, coord) in enumerate(zip(known_plaintext.upper(), known_coords)):
            mapping[coord] = plain_char
        
        st.success("### 🎯 Восстановленное отображение")
        
        # Показываем известные соответствия
        mapping_data = []
        for coord, char in mapping.items():
            mapping_data.append({
                'Координаты': coord,
                'Буква': char,
                'Статус': '✅ Известно'
            })
        
        st.dataframe(pd.DataFrame(mapping_data), use_container_width=True, hide_index=True)
        
        # Дешифруем полный текст с известными соответствиями
        st.markdown("#### 🔤 Дешифрованный текст (частично)")
        
        decrypted = []
        unknown_count = 0
        
        for coord in full_coords:
            if coord in mapping:
                decrypted.append(mapping[coord])
            else:
                decrypted.append('?')
                unknown_count += 1
        
        decrypted_text = ''.join(decrypted)
        
        st.text_area("Результат:", decrypted_text, height=100)
        st.info(f"**Неизвестных символов:** {unknown_count} из {len(full_coords)}")
        
        # Анализ для восстановления остального отображения
        if unknown_count > 0:
            st.markdown("#### 🔍 Рекомендации по восстановлению полного отображения")
            
            # Частотный анализ неизвестных координат
            unknown_coords = [coord for coord in full_coords if coord not in mapping]
            unknown_freq = Counter(unknown_coords)
            
            st.write("**Самые частые неизвестные координаты:**")
            unknown_data = []
            for coord, count in unknown_freq.most_common(10):
                unknown_data.append({
                    'Координаты': coord,
                    'Частота': count,
                    'Процент': f"{(count/len(unknown_coords))*100:.1f}%"
                })
            
            st.dataframe(pd.DataFrame(unknown_data), use_container_width=True, hide_index=True)
            
            st.write("""
            **Следующие шаги:**
            1. **Используйте контекст** - предположите слова вокруг известных фрагментов
            2. **Примените частотный анализ** к неизвестным координатам
            3. **Ищите осмысленные слова** в частично дешифрованном тексте
            4. **Проверяйте грамматику** и типичные окончания слов
            """)
    
    def render_auto_break(self):
        """Автоматический взлом с эвристиками"""
        st.markdown("### 🔄 Автоматический взлом")
        
        st.warning("""
        ⚠️ **Автоматический взлом** использует эвристики и может потребовать ручной проверки результатов.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            ciphertext = st.text_area(
                "Зашифрованный текст:",
                "23 15 31 31 34 44 11 42 44 32 15 43 23 15 31 31 34 11 33 44 15 43 11 42 31",
                height=150,
                key="auto_text"
            )
            
            language = st.radio(
                "Язык текста:",
                ["Английский", "Русский"],
                index=0,
                key="auto_lang"
            )
            
            max_attempts = st.slider("Максимум попыток:", 100, 5000, 1000)
        
        with col2:
            st.markdown("#### Эвристики для взлома")
            
            use_heuristics = st.multiselect(
                "Использовать эвристики:",
                [
                    "Частотный анализ букв",
                    "Анализ биграмм", 
                    "Словарная проверка",
                    "Грамматические правила",
                    "Контекстный анализ"
                ],
                default=["Частотный анализ букв", "Анализ биграмм"]
            )
            
            if st.button("🤖 Начать автоматический взлом", type="primary"):
                if not ciphertext.strip():
                    st.error("Введите зашифрованный текст!")
                    return
                
                with st.spinner("Выполняю автоматический взлом..."):
                    self.perform_auto_break(ciphertext, language, use_heuristics, max_attempts)
    
    def perform_auto_break(self, ciphertext, language, heuristics, max_attempts):
        """Выполняет автоматический взлом с использованием эвристик"""
        coordinates = self.parse_coordinates(ciphertext)
        
        if not coordinates:
            st.error("Не удалось распознать координаты!")
            return
        
        # Простой алгоритм автоматического взлома
        st.success("### 🔄 Процесс автоматического взлома")
        
        # Создаем прогресс-бар
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        best_score = -1
        best_mapping = {}
        best_decryption = ""
        
        # Эталонные частоты
        if language == "Английский":
            letter_freq = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3, 'H': 6.1}
            common_words = ['THE', 'AND', 'THAT', 'WITH', 'HAVE', 'THIS', 'WILL', 'YOUR', 'FROM']
        else:
            letter_freq = {'О': 10.97, 'Е': 8.45, 'А': 7.75, 'И': 7.32, 'Н': 6.70, 'Т': 6.26, 'С': 5.47}
            common_words = ['ПРИВЕТ', 'МИР', 'ЭТО', 'ТАК', 'ЧТО', 'КАК', 'ГДЕ', 'КОГДА']
        
        # Упрощенный перебор
        for attempt in range(min(max_attempts, 1000)):
            progress = (attempt + 1) / min(max_attempts, 1000)
            progress_bar.progress(progress)
            status_text.text(f"Попытка {attempt + 1}/{min(max_attempts, 1000)}")
            
            # Создаем случайное отображение
            coords_list = list(set(coordinates))
            letters = list(letter_freq.keys())[:len(coords_list)]
            random.shuffle(letters)
            
            mapping = {coord: letter for coord, letter in zip(coords_list, letters)}
            
            # Дешифруем
            decrypted = ''.join([mapping.get(coord, '?') for coord in coordinates])
            
            # Оцениваем качество
            score = self.score_decryption(decrypted, letter_freq, common_words, heuristics)
            
            if score > best_score:
                best_score = score
                best_mapping = mapping.copy()
                best_decryption = decrypted
        
        progress_bar.empty()
        status_text.empty()
        
        # Показываем результаты
        st.success(f"🎉 Найден лучший вариант (оценка: {best_score:.2f})")
        
        st.markdown("#### 🔤 Дешифрованный текст")
        st.text_area("Результат:", best_decryption, height=100)
        
        st.markdown("#### 📋 Использованное отображение")
        mapping_data = []
        for coord, letter in best_mapping.items():
            mapping_data.append({
                'Координаты': coord,
                'Буква': letter
            })
        
        st.dataframe(pd.DataFrame(mapping_data), use_container_width=True, hide_index=True)
        
        # Анализ качества
        st.markdown("#### 📊 Анализ качества дешифровки")
        
        # Подсчет осмысленных слов
        meaningful_words = 0
        for word in common_words:
            if word in best_decryption:
                meaningful_words += 1
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Оценка качества", f"{best_score:.2f}")
        with col2:
            st.metric("Осмысленные слова", meaningful_words)
        with col3:
            word_ratio = (meaningful_words / len(common_words)) * 100
            st.metric("Качество словаря", f"{word_ratio:.1f}%")
        
        st.info("""
        **Рекомендации:**
        - Если текст выглядит осмысленным - взлом успешен!
        - Если нет - попробуйте увеличить количество попыток
        - Используйте ручную корректировку на основе частичных результатов
        """)
    
    # Вспомогательные методы
    
    def parse_coordinates(self, text):
        """Парсит координаты из текста"""
        # Убираем лишние пробелы и разбиваем
        text = text.strip()
        coordinates = []
        
        # Пробуем разные разделители
        if ' ' in text:
            parts = text.split()
        else:
            # Если нет пробелов, разбиваем по парам символов
            parts = [text[i:i+2] for i in range(0, len(text), 2)]
        
        for part in parts:
            if len(part) == 2 and part[0].isdigit() and part[1].isdigit():
                coordinates.append(part)
            elif len(part) == 2 and part[0].isalpha() and part[1].isalpha():
                coordinates.append(part.upper())
        
        return coordinates
    
    def decrypt_with_mapping(self, ciphertext, mapping):
        """Дешифрует текст с использованием отображения"""
        coordinates = self.parse_coordinates(ciphertext)
        decrypted = []
        
        for coord in coordinates:
            if coord in mapping:
                decrypted.append(mapping[coord])
            else:
                decrypted.append('?')
        
        return ''.join(decrypted)
    
    def score_decryption(self, text, letter_freq, common_words, heuristics):
        """Оценивает качество дешифрованного текста"""
        score = 0
        
        if "Частотный анализ букв" in heuristics:
            # Проверяем соответствие частот
            text_letters = [char for char in text if char.isalpha()]
            if text_letters:
                text_freq = Counter(text_letters)
                for letter, expected_freq in letter_freq.items():
                    if letter in text_freq:
                        actual_freq = (text_freq[letter] / len(text_letters)) * 100
                        score += 10 - abs(actual_freq - expected_freq)
        
        if "Анализ биграмм" in heuristics:
            # Проверяем наличие частых биграмм
            bigrams = [text[i:i+2] for i in range(len(text)-1)]
            common_bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE'] if len(common_words[0]) == 3 else ['СТ', 'ЕН', 'ОВ', 'НО']
            for bigram in common_bigrams:
                if bigram in text:
                    score += 5
        
        if "Словарная проверка" in heuristics:
            # Проверяем наличие общих слов
            for word in common_words:
                if word in text:
                    score += 20
        
        return score
    
    def analyze_distances(self, coordinates):
        """Анализирует расстояния между координатами"""
        st.success("### 📏 Анализ расстояний между координатами")
        
        # Анализ уникальных координат
        unique_coords = list(set(coordinates))
        st.info(f"**Уникальных координат:** {len(unique_coords)}")
        
        # Анализ распределения первых и вторых цифр
        first_digits = [int(coord[0]) for coord in coordinates if coord[0].isdigit()]
        second_digits = [int(coord[1]) for coord in coordinates if coord[1].isdigit()]
        
        if first_digits and second_digits:
            st.markdown("#### 🔢 Распределение цифр в координатах")
            
            col1, col2 = st.columns(2)
            
            with col1:
                first_freq = Counter(first_digits)
                st.write("**Первые цифры:**")
                for digit in sorted(first_freq.keys()):
                    st.write(f"{digit}: {first_freq[digit]} раз")
            
            with col2:
                second_freq = Counter(second_digits)
                st.write("**Вторые цифры:**")
                for digit in sorted(second_freq.keys()):
                    st.write(f"{digit}: {second_freq[digit]} раз")
            
            # Определяем возможный размер квадрата
            max_first = max(first_digits) if first_digits else 0
            max_second = max(second_digits) if second_digits else 0
            
            st.success(f"**Предполагаемый размер квадрата:** {max_first}×{max_second}")
    
    # Методы визуализации
    
    def visualize_frequency_comparison(self, coord_freq, letter_freq, total_coords, mapping):
        """Визуализирует сравнение частот"""
        st.markdown("#### 📈 Визуализация сравнения частот")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # График 1: Фактические частоты координат
        top_coords = [coord for coord, _ in coord_freq.most_common(10)]
        top_freqs = [coord_freq[coord] for coord in top_coords]
        top_percent = [(freq/total_coords)*100 for freq in top_freqs]
        
        bars1 = ax1.bar(range(len(top_coords)), top_percent, color='skyblue', alpha=0.7)
        ax1.set_title('Самые частые координаты в шифротексте')
        ax1.set_xlabel('Координаты')
        ax1.set_ylabel('Частота (%)')
        ax1.set_xticks(range(len(top_coords)))
        ax1.set_xticklabels(top_coords, rotation=45)
        
        for i, (bar, percent) in enumerate(zip(bars1, top_percent)):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                    f'{percent:.1f}%', ha='center', va='bottom')
        
        # График 2: Ожидаемые частоты букв
        top_letters = list(letter_freq.keys())[:10]
        top_letter_freqs = [letter_freq[letter] for letter in top_letters]
        
        bars2 = ax2.bar(range(len(top_letters)), top_letter_freqs, color='lightgreen', alpha=0.7)
        ax2.set_title('Ожидаемые частоты букв в языке')
        ax2.set_xlabel('Буквы')
        ax2.set_ylabel('Частота (%)')
        ax2.set_xticks(range(len(top_letters)))
        ax2.set_xticklabels(top_letters, rotation=45)
        
        for i, (bar, freq) in enumerate(zip(bars2, top_letter_freqs)):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                    f'{freq:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def visualize_bigram_analysis(self, bigram_freq):
        """Визуализирует анализ биграмм"""
        st.markdown("#### 📊 Распределение биграмм")
        
        # Берем топ-15 биграмм
        top_bigrams = [bigram for bigram, _ in bigram_freq.most_common(15)]
        top_freqs = [bigram_freq[bigram] for bigram in top_bigrams]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        bars = ax.bar(range(len(top_bigrams)), top_freqs, color='orange', alpha=0.7)
        ax.set_title('Самые частые биграммы координат')
        ax.set_xlabel('Биграммы')
        ax.set_ylabel('Частота')
        ax.set_xticks(range(len(top_bigrams)))
        ax.set_xticklabels(top_bigrams, rotation=45)
        
        for bar, freq in zip(bars, top_freqs):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), 
                   str(freq), ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    def visualize_repetitions(self, coordinates, repeating_patterns):
        """Визуализирует повторяющиеся паттерны"""
        if not repeating_patterns:
            return
        
        st.markdown("#### 📍 Визуализация повторений в тексте")
        
        # Берем топ-3 самых частых паттерна
        top_patterns = sorted(repeating_patterns.items(), key=lambda x: len(x[1]), reverse=True)[:3]
        
        fig, axes = plt.subplots(len(top_patterns), 1, figsize=(12, 3*len(top_patterns)))
        if len(top_patterns) == 1:
            axes = [axes]
        
        for idx, (pattern, positions) in enumerate(top_patterns):
            ax = axes[idx]
            pattern_length = len(pattern)
            
            # Создаем визуализацию позиций
            for pos in positions:
                ax.axvspan(pos, pos + pattern_length, alpha=0.3, color=f'C{idx}')
            
            ax.set_xlim(0, len(coordinates))
            ax.set_ylim(0, 1)
            ax.set_yticks([])
            ax.set_xlabel('Позиция в тексте')
            ax.set_title(f'Паттерн: {" ".join(pattern)} (повторяется {len(positions)} раз)')
        
        plt.tight_layout()
        st.pyplot(fig)

# Необходимый импорт
import matplotlib.pyplot as plt