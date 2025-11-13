from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import numpy as np
import zlib
import gzip
import bz2
import lzma
import binascii
import base64
from io import BytesIO
from typing import Dict, List, Tuple
import heapq
from collections import Counter, defaultdict

class CompressionModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Методы сжатия"
        self.description = "Алгоритмы сжатия данных: RLE, Хаффман, LZ77, DEFLATE"
        self.complexity = "advanced"
        self.category = "protocols"
        self.icon = ""
        self.order = 1
    
    def render(self):
        st.title("🗜️ Методы сжатия данных")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            ### Основные понятия сжатия данных
            
            **Сжатие без потерь:** Исходные данные могут быть полностью восстановлены.
            
            **Сжатие с потерями:** Часть информации теряется (используется для изображений, аудио, видео).
            
            **Коэффициент сжатия:** Отношение размера исходных данных к размеру сжатых данных.
            
            ### Алгоритмы сжатия:
            
            **1. RLE (Run-Length Encoding)**
            - Простейший алгоритм сжатия
            - Заменяет последовательности одинаковых символов на пары (символ, количество)
            - Эффективен для данных с длинными повторяющимися последовательностями
            
            **2. Кодирование Хаффмана**
            - Статистический алгоритм сжатия
            - Часто встречающиеся символы кодируются короткими кодами
            - Редкие символы - длинными кодами
            - Оптимальный префиксный код
            
            **3. LZ77 (Lempel-Ziv 1977)**
            - Словарный метод сжатия
            - Заменяет повторяющиеся фразы ссылками на предыдущие вхождения
            - Основа для DEFLATE (ZIP, GZIP)
            
            **4. DEFLATE**
            - Комбинация LZ77 и кодирования Хаффмана
            - Используется в ZIP, GZIP, PNG
            - Высокая степень сжатия
            """)
        
        st.markdown("---")
        
        # Выбор метода сжатия
        compression_method = st.radio(
            "Метод сжатия:",
            ["RLE", "Хаффман", "LZ77", "DEFLATE", "Сравнение алгоритмов"],
            horizontal=True
        )
        
        if compression_method == "RLE":
            self.render_rle_section()
        elif compression_method == "Хаффман":
            self.render_huffman_section()
        elif compression_method == "LZ77":
            self.render_lz77_section()
        elif compression_method == "DEFLATE":
            self.render_deflate_section()
        else:
            self.render_comparison_section()
    
    def render_rle_section(self):
        """Отрисовывает секцию RLE сжатия"""
        st.subheader("🔢 RLE (Run-Length Encoding)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📤 Сжатие RLE")
            self.render_rle_encoding()
        
        with col2:
            st.markdown("### 📥 Распаковка RLE")
            self.render_rle_decoding()
        
        # Дополнительная информация о RLE
        st.markdown("---")
        self.render_rle_info()
    
    def render_rle_encoding(self):
        """Отрисовывает интерфейс сжатия RLE"""
        input_type = st.radio(
            "Тип входных данных:",
            ["Текст", "Числовая последовательность"],
            key="rle_enc_type",
            horizontal=True
        )
        
        if input_type == "Текст":
            text = st.text_area(
                "Текст для сжатия:",
                "AAAABBBCCDAA",
                height=100,
                key="rle_enc_text"
            )
        else:
            numbers = st.text_area(
                "Числовая последовательность (через пробел):",
                "1 1 1 2 2 3 4 4 4 4",
                height=100,
                key="rle_enc_numbers"
            )
        
        encoding_format = st.radio(
            "Формат кодирования:",
            ["Символ-Количество", "Байтовый"],
            key="rle_format",
            horizontal=True
        )
        
        if st.button("Сжать RLE", key="rle_enc_btn", use_container_width=True):
            if input_type == "Текст" and text:
                try:
                    compressed = self.rle_encode(text, encoding_format)
                    original_size = len(text.encode('utf-8'))
                    compressed_size = len(compressed.encode('utf-8'))
                    
                    st.success("Сжатые данные:")
                    st.code(compressed, language="text")
                    
                    self.show_compression_stats(original_size, compressed_size, "RLE")
                    self.show_rle_encoding_details(text, compressed)
                    
                except Exception as e:
                    st.error(f"Ошибка сжатия: {e}")
            
            elif input_type == "Числовая последовательность" and numbers:
                try:
                    # Преобразуем строку чисел в список
                    number_list = list(map(int, numbers.split()))
                    compressed = self.rle_encode_numbers(number_list, encoding_format)
                    
                    original_size = len(numbers)
                    compressed_size = len(compressed)
                    
                    st.success("Сжатые данные:")
                    st.code(compressed, language="text")
                    
                    self.show_compression_stats(original_size, compressed_size, "RLE")
                    
                except Exception as e:
                    st.error(f"Ошибка сжатия: {e}")
            else:
                st.error("Введите данные для сжатия")
    
    def render_rle_decoding(self):
        """Отрисовывает интерфейс распаковки RLE"""
        rle_input = st.text_area(
            "RLE данные для распаковки:",
            "4A3B2C1D2A",
            height=100,
            key="rle_dec_text"
        )
        
        input_type = st.radio(
            "Тип данных:",
            ["Текст", "Числа"],
            key="rle_dec_type",
            horizontal=True
        )
        
        if st.button("Распаковать RLE", key="rle_dec_btn", use_container_width=True):
            if rle_input:
                try:
                    if input_type == "Текст":
                        decompressed = self.rle_decode(rle_input)
                    else:
                        decompressed = self.rle_decode_numbers(rle_input)
                    
                    st.success("Распакованные данные:")
                    st.code(decompressed, language="text")
                    
                    # Показываем детали распаковки
                    self.show_rle_decoding_details(rle_input, decompressed)
                    
                except Exception as e:
                    st.error(f"Ошибка распаковки: {e}")
            else:
                st.error("Введите RLE данные для распаковки")
    
    def render_rle_info(self):
        """Показывает информацию о RLE"""
        st.subheader("📊 Информация о RLE")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Преимущества RLE:**
            - Простота реализации
            - Быстрое сжатие и распаковка
            - Эффективен для данных с повторениями
            
            **Недостатки RLE:**
            - Может увеличивать размер данных без повторений
            - Неэффективен для текста на естественных языках
            
            **Применение:**
            - Форматы изображений (BMP, PCX)
            - Простые архиваторы
            - Системы передачи данных
            """)
        
        with col2:
            st.markdown("""
            **Пример работы RLE:**
            
            Исходные данные: `AAAABBBCCDAA`
            
            Процесс сжатия:
            - AAAA → 4A
            - BBB → 3B  
            - CC → 2C
            - D → 1D
            - AA → 2A
            
            Результат: `4A3B2C1D2A`
            
            **Эффективность:**
            - Исходный размер: 12 байт
            - Сжатый размер: 10 байт
            - Коэффициент сжатия: 1.2
            """)
    
    def render_huffman_section(self):
        """Отрисовывает секцию кодирования Хаффмана"""
        st.subheader("🌳 Кодирование Хаффмана")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📤 Сжатие Хаффмана")
            self.render_huffman_encoding()
        
        with col2:
            st.markdown("### 📥 Распаковка Хаффмана")
            self.render_huffman_decoding()
        
        # Дерево Хаффмана
        st.markdown("---")
        self.render_huffman_tree_section()
    
    def render_huffman_encoding(self):
        """Отрисовывает интерфейс сжатия Хаффмана"""
        text = st.text_area(
            "Текст для сжатия Хаффмана:",
            "this is an example for huffman encoding",
            height=100,
            key="huffman_enc_text"
        )
        
        if st.button("Сжать Хаффманом", key="huffman_enc_btn", use_container_width=True):
            if text:
                try:
                    # Строим дерево Хаффмана и кодируем
                    root = self.build_huffman_tree(text)
                    codes = self.generate_huffman_codes(root)
                    encoded_text, encoded_binary = self.huffman_encode(text, codes)
                    
                    st.success("Коды Хаффмана:")
                    
                    # Показываем таблицу кодов
                    codes_data = []
                    for char, code in codes.items():
                        if char == ' ':
                            display_char = '[пробел]'
                        elif char == '\n':
                            display_char = '[новая строка]'
                        else:
                            display_char = char
                        codes_data.append({'Символ': display_char, 'Код': code, 'Частота': text.count(char)})
                    
                    df_codes = pd.DataFrame(codes_data)
                    st.dataframe(df_codes, use_container_width=True, height=300)
                    
                    st.success("Закодированный текст:")
                    st.code(encoded_text, language="text")
                    
                    # Статистика
                    original_size = len(text.encode('utf-8')) * 8  # в битах
                    compressed_size = len(encoded_binary)
                    compression_ratio = original_size / compressed_size if compressed_size > 0 else 0
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Исходный размер", f"{original_size} бит")
                    with col2:
                        st.metric("Сжатый размер", f"{compressed_size} бит")
                    with col3:
                        st.metric("Коэффициент", f"{compression_ratio:.2f}")
                    
                except Exception as e:
                    st.error(f"Ошибка сжатия: {e}")
            else:
                st.error("Введите текст для сжатия")
    
    def render_huffman_decoding(self):
        """Отрисовывает интерфейс распаковки Хаффмана"""
        encoded_text = st.text_area(
            "Закодированный текст Хаффмана:",
            "1000111001111011111100001111111010010010011100101101101001010101001011110011011110111110001110100001011010001110001011100100001111101100011110101001001000101111001101000100101",
            height=100,
            key="huffman_dec_text"
        )
        
        codes_input = st.text_area(
            "Коды Хаффмана (в формате 'символ:код', каждый с новой строки):",
            " :110\nt:1111\nh:1000\ni:1010\ns:1011\na:1001\n :110\ne:1110\nx:01000\nm:01001\np:01010\nl:01011\nf:01100\no:01101\nr:01110\nu:01111\nn:000\nc:0010\nd:0011\ng:0000",
            height=150,
            key="huffman_codes_input"
        )
        
        if st.button("Распаковать Хаффмана", key="huffman_dec_btn", use_container_width=True):
            if encoded_text and codes_input:
                try:
                    # Парсим коды
                    codes = {}
                    for line in codes_input.split('\n'):
                        if ':' in line:
                            char, code = line.split(':', 1)
                            if char == '[пробел]':
                                char = ' '
                            elif char == '[новая строка]':
                                char = '\n'
                            codes[char.strip()] = code.strip()
                    
                    decoded_text = self.huffman_decode(encoded_text, codes)
                    
                    st.success("Распакованный текст:")
                    st.code(decoded_text, language="text")
                    
                except Exception as e:
                    st.error(f"Ошибка распаковки: {e}")
            else:
                st.error("Введите закодированный текст и коды")
    
    def render_huffman_tree_section(self):
        """Показывает визуализацию дерева Хаффмана"""
        st.subheader("🌳 Визуализация дерева Хаффмана")
        
        demo_text = st.text_input(
            "Текст для построения дерева:",
            "huffman",
            key="huffman_tree_text"
        )
        
        if st.button("Построить дерево", key="huffman_tree_btn"):
            if demo_text:
                try:
                    root = self.build_huffman_tree(demo_text)
                    tree_visualization = self.visualize_huffman_tree(root)
                    
                    st.success("Дерево Хаффмана:")
                    st.text(tree_visualization)
                    
                    # Показываем частоты символов
                    freq = Counter(demo_text)
                    freq_data = [{'Символ': k, 'Частота': v} for k, v in freq.items()]
                    df_freq = pd.DataFrame(freq_data)
                    st.dataframe(df_freq, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Ошибка построения дерева: {e}")
    
    def render_lz77_section(self):
        """Отрисовывает секцию LZ77 сжатия"""
        st.subheader("🔍 LZ77 Сжатие")
        
        text = st.text_area(
            "Текст для сжатия LZ77:",
            "ABRACADABRABRABRA",
            height=100,
            key="lz77_text"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            window_size = st.slider("Размер окна:", 5, 50, 10, key="lz77_window")
        with col2:
            lookahead_size = st.slider("Размер буфера:", 3, 20, 5, key="lz77_lookahead")
        
        if st.button("Сжать LZ77", key="lz77_enc_btn", use_container_width=True):
            if text:
                try:
                    compressed = self.lz77_encode(text, window_size, lookahead_size)
                    
                    st.success("Сжатые данные LZ77:")
                    
                    # Показываем токены
                    tokens_data = []
                    for token in compressed:
                        tokens_data.append({
                            'Смещение': token[0],
                            'Длина': token[1],
                            'Следующий символ': token[2] if token[2] else 'EOF'
                        })
                    
                    df_tokens = pd.DataFrame(tokens_data)
                    st.dataframe(df_tokens, use_container_width=True)
                    
                    # Статистика
                    original_size = len(text)
                    compressed_size = len(compressed) * 3  # примерная оценка
                    
                    self.show_compression_stats(original_size, compressed_size, "LZ77")
                    
                    # Декодируем для проверки
                    decoded = self.lz77_decode(compressed)
                    st.info(f"Проверка распаковки: {decoded}")
                    
                except Exception as e:
                    st.error(f"Ошибка сжатия: {e}")
            else:
                st.error("Введите текст для сжатия")
        
        # Информация о LZ77
        st.markdown("---")
        self.render_lz77_info()
    
    def render_lz77_info(self):
        """Показывает информацию о LZ77"""
        st.subheader("📖 Принцип работы LZ77")
        
        st.markdown("""
        **Скользящее окно LZ77:**
        
        ```
        [Уже обработанные данные] | [Текущая позиция] | [Буфер предпросмотра]
        ←--- Окно поиска ---→        ←- Буфер -→
        ```
        
        **Токен LZ77:** (смещение, длина, следующий символ)
        
        **Пример:**
        - Текст: `ABRACADABRABRABRA`
        - Токены: `(0,0,'A'), (0,0,'B'), (0,0,'R'), (0,0,'A'), (0,0,'C'), ...`
        
        **При совпадении:**
        - Находим самую длинную совпадающую строку в окне поиска
        - Создаем токен (смещение, длина, следующий символ)
        - Смещаем окно на длину + 1
        """)
    
    def render_deflate_section(self):
        """Отрисовывает секцию DEFLATE сжатия"""
        st.subheader("🎯 DEFLATE Сжатие")
        
        input_type = st.radio(
            "Тип данных:",
            ["Текст", "Файл"],
            key="deflate_type",
            horizontal=True
        )
        
        if input_type == "Текст":
            text = st.text_area(
                "Текст для DEFLATE сжатия:",
                "Hello, World! This is a test text for DEFLATE compression algorithm.",
                height=100,
                key="deflate_text"
            )
            
            if st.button("Сжать DEFLATE", key="deflate_enc_btn", use_container_width=True):
                if text:
                    try:
                        # Сжимаем с помощью zlib (DEFLATE)
                        compressed_data = zlib.compress(text.encode('utf-8'))
                        compressed_hex = binascii.hexlify(compressed_data).decode('utf-8')
                        compressed_b64 = base64.b64encode(compressed_data).decode('utf-8')
                        
                        original_size = len(text.encode('utf-8'))
                        compressed_size = len(compressed_data)
                        
                        st.success("Сжатые данные DEFLATE:")
                        
                        tab1, tab2 = st.tabs(["Шестнадцатеричный", "Base64"])
                        
                        with tab1:
                            st.code(compressed_hex, language="text")
                        with tab2:
                            st.code(compressed_b64, language="text")
                        
                        self.show_compression_stats(original_size, compressed_size, "DEFLATE")
                        
                        # Распаковываем для проверки
                        decompressed_data = zlib.decompress(compressed_data)
                        decompressed_text = decompressed_data.decode('utf-8')
                        
                        st.info(f"Проверка распаковки: {decompressed_text}")
                        
                    except Exception as e:
                        st.error(f"Ошибка сжатия: {e}")
                else:
                    st.error("Введите текст для сжатия")
        
        else:  # Файл
            uploaded_file = st.file_uploader(
                "Выберите файл для DEFLATE сжатия:",
                type=['txt', 'csv', 'json', 'xml'],
                key="deflate_file_upload"
            )
            
            if uploaded_file is not None:
                if st.button("Сжать файл DEFLATE", key="deflate_file_btn", use_container_width=True):
                    try:
                        file_contents = uploaded_file.getvalue()
                        
                        # Сжимаем файл
                        compressed_data = zlib.compress(file_contents)
                        
                        original_size = len(file_contents)
                        compressed_size = len(compressed_data)
                        
                        st.success(f"Результат сжатия файла '{uploaded_file.name}':")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Исходный размер", f"{original_size} байт")
                        with col2:
                            st.metric("Сжатый размер", f"{compressed_size} байт")
                        with col3:
                            ratio = (1 - compressed_size / original_size) * 100
                            st.metric("Экономия", f"{ratio:.1f}%")
                        
                        # Предлагаем скачать сжатый файл
                        self.download_compressed_file(compressed_data, uploaded_file.name + '.deflate')
                        
                    except Exception as e:
                        st.error(f"Ошибка сжатия файла: {e}")
    
    def render_comparison_section(self):
        """Отрисовывает секцию сравнения алгоритмов"""
        st.subheader("📊 Сравнение алгоритмов сжатия")
        
        text = st.text_area(
            "Текст для сравнения алгоритмов:",
            "This is a test text to compare different compression algorithms. " * 3,
            height=100,
            key="compare_text"
        )
        
        if st.button("Сравнить алгоритмы", key="compare_btn", use_container_width=True):
            if text:
                try:
                    results = []
                    
                    # RLE
                    rle_compressed = self.rle_encode(text, "Символ-Количество")
                    rle_size = len(rle_compressed.encode('utf-8'))
                    results.append({'Алгоритм': 'RLE', 'Размер': rle_size})
                    
                    # Хаффман
                    root = self.build_huffman_tree(text)
                    codes = self.generate_huffman_codes(root)
                    _, huffman_binary = self.huffman_encode(text, codes)
                    huffman_size = (len(huffman_binary) + 7) // 8  # биты в байты
                    results.append({'Алгоритм': 'Хаффман', 'Размер': huffman_size})
                    
                    # DEFLATE
                    deflate_compressed = zlib.compress(text.encode('utf-8'))
                    deflate_size = len(deflate_compressed)
                    results.append({'Алгоритм': 'DEFLATE', 'Размер': deflate_size})
                    
                    # Исходный размер
                    original_size = len(text.encode('utf-8'))
                    
                    # Создаем таблицу результатов
                    df_results = pd.DataFrame(results)
                    df_results['Коэффициент'] = original_size / df_results['Размер']
                    df_results['Экономия %'] = (1 - df_results['Размер'] / original_size) * 100
                    
                    st.success("Результаты сравнения:")
                    st.dataframe(df_results, use_container_width=True)
                    
                    # Визуализация
                    st.markdown("### 📈 Визуализация эффективности")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # График размеров
                        chart_data = pd.DataFrame({
                            'Алгоритм': ['Исходный'] + list(df_results['Алгоритм']),
                            'Размер': [original_size] + list(df_results['Размер'])
                        })
                        st.bar_chart(chart_data.set_index('Алгоритм'))
                    
                    with col2:
                        # График экономии
                        economy_data = pd.DataFrame({
                            'Алгоритм': df_results['Алгоритм'],
                            'Экономия': df_results['Экономия %']
                        })
                        st.bar_chart(economy_data.set_index('Алгоритм'))
                    
                except Exception as e:
                    st.error(f"Ошибка сравнения: {e}")
            else:
                st.error("Введите текст для сравнения")
    
    # Реализация алгоритмов сжатия
    
    def rle_encode(self, text: str, format_type: str) -> str:
        """Кодирование RLE"""
        if not text:
            return ""
        
        result = []
        i = 0
        
        while i < len(text):
            count = 1
            while i + count < len(text) and text[i + count] == text[i]:
                count += 1
            
            if format_type == "Символ-Количество":
                result.append(f"{count}{text[i]}")
            else:  # Байтовый
                result.append(f"{count:02X}{ord(text[i]):02X}")
            
            i += count
        
        return ''.join(result)
    
    def rle_decode(self, encoded: str) -> str:
        """Декодирование RLE"""
        result = []
        i = 0
        
        while i < len(encoded):
            # Ищем начало числа
            j = i
            while j < len(encoded) and encoded[j].isdigit():
                j += 1
            
            if j > i:
                count = int(encoded[i:j])
                char = encoded[j]
                result.append(char * count)
                i = j + 1
            else:
                i += 1
        
        return ''.join(result)
    
    def rle_encode_numbers(self, numbers: List[int], format_type: str) -> str:
        """Кодирование RLE для числовой последовательности"""
        if not numbers:
            return ""
        
        result = []
        i = 0
        
        while i < len(numbers):
            count = 1
            while i + count < len(numbers) and numbers[i + count] == numbers[i]:
                count += 1
            
            if format_type == "Символ-Количество":
                result.append(f"{count}:{numbers[i]}")
            else:
                result.append(f"{count:02X}:{numbers[i]:02X}")
            
            i += count
        
        return ' '.join(result)
    
    def rle_decode_numbers(self, encoded: str) -> str:
        """Декодирование RLE для числовой последовательности"""
        result = []
        tokens = encoded.split()
        
        for token in tokens:
            if ':' in token:
                count_str, num_str = token.split(':', 1)
                try:
                    count = int(count_str)
                    num = int(num_str)
                    result.extend([str(num)] * count)
                except ValueError:
                    continue
        
        return ' '.join(result)
    
    class HuffmanNode:
        """Узел дерева Хаффмана"""
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None
        
        def __lt__(self, other):
            return self.freq < other.freq
    
    def build_huffman_tree(self, text: str):
        """Построение дерева Хаффмана"""
        if not text:
            return None
        
        # Подсчет частот
        frequency = Counter(text)
        
        # Создаем узлы
        heap = []
        for char, freq in frequency.items():
            heapq.heappush(heap, (freq, self.HuffmanNode(char, freq)))
        
        # Строим дерево
        while len(heap) > 1:
            freq1, node1 = heapq.heappop(heap)
            freq2, node2 = heapq.heappop(heap)
            
            merged = self.HuffmanNode(None, freq1 + freq2)
            merged.left = node1
            merged.right = node2
            
            heapq.heappush(heap, (merged.freq, merged))
        
        return heap[0][1] if heap else None
    
    def generate_huffman_codes(self, node, code="", codes=None):
        """Генерация кодов Хаффмана"""
        if codes is None:
            codes = {}
        
        if node is None:
            return codes
        
        if node.char is not None:
            codes[node.char] = code
        
        self.generate_huffman_codes(node.left, code + "0", codes)
        self.generate_huffman_codes(node.right, code + "1", codes)
        
        return codes
    
    def huffman_encode(self, text: str, codes: Dict[str, str]):
        """Кодирование текста Хаффманом"""
        encoded_text = ''.join(codes[char] for char in text)
        return encoded_text, encoded_text
    
    def huffman_decode(self, encoded_text: str, codes: Dict[str, str]):
        """Декодирование текста Хаффмана"""
        # Создаем обратный словарь
        reverse_codes = {v: k for k, v in codes.items()}
        
        result = []
        current_code = ""
        
        for bit in encoded_text:
            current_code += bit
            if current_code in reverse_codes:
                result.append(reverse_codes[current_code])
                current_code = ""
        
        return ''.join(result)
    
    def visualize_huffman_tree(self, node, prefix="", is_left=True):
        """Визуализация дерева Хаффмана"""
        if node is None:
            return ""
        
        result = ""
        if node.char is not None:
            char_display = node.char if node.char != ' ' else '[пробел]'
            result += f"{prefix}{'└── ' if is_left else '┌── '}{char_display} ({node.freq})\n"
        else:
            result += f"{prefix}{'└── ' if is_left else '┌── '}* ({node.freq})\n"
        
        if node.left or node.right:
            if node.left:
                result += self.visualize_huffman_tree(node.left, prefix + ("    " if is_left else "│   "), True)
            if node.right:
                result += self.visualize_huffman_tree(node.right, prefix + ("    " if is_left else "│   "), False)
        
        return result
    
    def lz77_encode(self, text: str, window_size: int, lookahead_size: int):
        """Кодирование LZ77"""
        i = 0
        compressed = []
        
        while i < len(text):
            match = (0, 0, text[i])  # (offset, length, next_char)
            
            # Ищем совпадение в окне
            window_start = max(0, i - window_size)
            search_buffer = text[window_start:i]
            
            # Ищем самую длинную совпадающую подстроку
            for length in range(1, min(lookahead_size, len(text) - i) + 1):
                substring = text[i:i+length]
                pos = search_buffer.rfind(substring)
                
                if pos != -1:
                    offset = len(search_buffer) - pos
                    if length == lookahead_size and i + length < len(text):
                        match = (offset, length, text[i+length])
                    elif i + length == len(text):
                        match = (offset, length, '')
                    else:
                        match = (offset, length, text[i+length])
            
            compressed.append(match)
            i += match[1] + 1 if match[1] > 0 else 1
        
        return compressed
    
    def lz77_decode(self, compressed):
        """Декодирование LZ77"""
        result = []
        
        for offset, length, char in compressed:
            if length > 0:
                start = len(result) - offset
                for i in range(length):
                    result.append(result[start + i])
            if char and char != 'EOF':
                result.append(char)
        
        return ''.join(result)
    
    def show_compression_stats(self, original_size: int, compressed_size: int, algorithm: str):
        """Показывает статистику сжатия"""
        st.markdown("**📈 Статистика сжатия:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Исходный размер", f"{original_size} байт")
        with col2:
            st.metric("Сжатый размер", f"{compressed_size} байт")
        with col3:
            if compressed_size > 0:
                ratio = original_size / compressed_size
                economy = (1 - compressed_size / original_size) * 100
                st.metric("Коэффициент", f"{ratio:.2f}")
                st.metric("Экономия", f"{economy:.1f}%")
    
    def show_rle_encoding_details(self, original: str, compressed: str):
        """Показывает детали кодирования RLE"""
        st.markdown("**🔍 Детали кодирования RLE:**")
        
        # Анализ эффективности
        original_chars = len(original)
        compressed_chars = len(compressed)
        
        analysis_data = []
        i = 0
        while i < len(compressed):
            if compressed[i].isdigit():
                j = i
                while j < len(compressed) and compressed[j].isdigit():
                    j += 1
                if j < len(compressed):
                    count = int(compressed[i:j])
                    char = compressed[j]
                    analysis_data.append({
                        'Последовательность': char * count,
                        'Кодирование': compressed[i:j+1],
                        'Эффективность': '✅' if count > 2 else '➖'
                    })
                    i = j + 1
                else:
                    i += 1
            else:
                i += 1
        
        if analysis_data:
            df_analysis = pd.DataFrame(analysis_data)
            st.dataframe(df_analysis, use_container_width=True)
    
    def show_rle_decoding_details(self, encoded: str, decoded: str):
        """Показывает детали декодирования RLE"""
        st.markdown("**🔍 Детали декодирования RLE:**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Закодированная длина", f"{len(encoded)} символов")
        with col2:
            st.metric("Распакованная длина", f"{len(decoded)} символов")
    
    def download_compressed_file(self, compressed_data: bytes, filename: str):
        """Создает кнопку для скачивания сжатого файла"""
        b64 = base64.b64encode(compressed_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">📥 Скачать сжатый файл</a>'
        st.markdown(href, unsafe_allow_html=True)

# Для обратной совместимости
class CompressionCipher(CompressionModule):
    pass
