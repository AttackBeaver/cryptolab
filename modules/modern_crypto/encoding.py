from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import numpy as np
import base64
import binascii
import zlib
import secrets
from typing import Dict, List, Tuple

class EncodingModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Кодирование/Декодирование"
        self.description = "Base64, ASCII, CRC32 - методы преобразования и контроля данных"
        self.complexity = "intermediate"
        self.category = "modern"
        self.icon = ""
        self.order = 1
    
    def render(self):
        st.title("🔤 Кодирование и Декодирование")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            ### Base64
            **Назначение:** Кодирование бинарных данных в текстовый формат для безопасной передачи.
            
            **Принцип работы:**
            - Использует 64 символа: A-Z, a-z, 0-9, +, /
            - Каждые 3 байта (24 бита) кодируются в 4 символа Base64
            - Дополнение '=' используется для выравнивания
            
            **Применение:**
            - Передача бинарных данных через текстовые протоколы (email, HTTP)
            - Хранение бинарных данных в JSON/XML
            - Data URL в веб-разработке
            
            ### ASCII
            **Назначение:** Стандарт кодирования символов для представления текста в компьютерах.
            
            **Особенности:**
            - 7-битная кодировка (128 символов)
            - Включает управляющие символы и печатные символы
            - Основы для многих современных кодировок
            
            ### CRC32 (Cyclic Redundancy Check)
            **Назначение:** Обнаружение ошибок в передаваемых данных.
            
            **Принцип работы:**
            - Вычисляет контрольную сумму на основе полиномиального деления
            - 32-битная хеш-функция
            - Обнаруживает одиночные и множественные ошибки
            
            **Применение:**
            - Проверка целостности файлов
            - Сетевые протоколы
            - Системы хранения данных
            """)
        
        st.markdown("---")
        
        # Выбор метода кодирования
        encoding_method = st.radio(
            "Метод кодирования:",
            ["Base64", "ASCII", "CRC32"],
            horizontal=True
        )
        
        if encoding_method == "Base64":
            self.render_base64_section()
        elif encoding_method == "ASCII":
            self.render_ascii_section()
        else:
            self.render_crc32_section()
    
    def render_base64_section(self):
        """Отрисовывает секцию Base64"""
        st.subheader("🔤 Base64 Кодирование/Декодирование")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📤 Кодирование в Base64")
            self.render_base64_encoding()
        
        with col2:
            st.markdown("### 📥 Декодирование из Base64")
            self.render_base64_decoding()
        
        # Дополнительная информация о Base64
        st.markdown("---")
        self.render_base64_info()
    
    def render_base64_encoding(self):
        """Отрисовывает интерфейс кодирования Base64"""
        input_type = st.radio(
            "Тип входных данных:",
            ["Текст", "Файл"],
            key="base64_enc_type",
            horizontal=True
        )
        
        if input_type == "Текст":
            plaintext = st.text_area(
                "Текст для кодирования:",
                "Hello, World!",
                height=100,
                key="base64_enc_text"
            )
            
            if st.button("Закодировать в Base64", key="base64_enc_btn", use_container_width=True):
                if plaintext:
                    try:
                        # Кодируем в Base64
                        encoded_bytes = base64.b64encode(plaintext.encode('utf-8'))
                        encoded_text = encoded_bytes.decode('utf-8')
                        
                        st.success("Закодированный текст (Base64):")
                        st.code(encoded_text, language="text")
                        
                        # Показываем детали кодирования
                        self.show_base64_encoding_details(plaintext, encoded_text)
                        
                    except Exception as e:
                        st.error(f"Ошибка кодирования: {e}")
                else:
                    st.error("Введите текст для кодирования")
        
        else:  # Файл
            uploaded_file = st.file_uploader(
                "Выберите файл для кодирования:",
                type=None,
                key="base64_file_upload"
            )
            
            if uploaded_file is not None:
                file_contents = uploaded_file.getvalue()
                
                if st.button("Закодировать файл в Base64", key="base64_file_enc_btn", use_container_width=True):
                    try:
                        encoded_bytes = base64.b64encode(file_contents)
                        encoded_text = encoded_bytes.decode('utf-8')
                        
                        st.success("Файл закодирован в Base64:")
                        
                        # Показываем первые 500 символов для предпросмотра
                        if len(encoded_text) > 500:
                            st.text_area("Base64 (первые 500 символов):", encoded_text[:500], height=150)
                            st.info(f"Полная длина: {len(encoded_text)} символов")
                        else:
                            st.text_area("Base64:", encoded_text, height=150)
                        
                        # Предлагаем скачать результат
                        self.download_base64_file(encoded_text, uploaded_file.name)
                        
                    except Exception as e:
                        st.error(f"Ошибка кодирования файла: {e}")
    
    def render_base64_decoding(self):
        """Отрисовывает интерфейс декодирования Base64"""
        base64_input = st.text_area(
            "Base64 текст для декодирования:",
            "SGVsbG8sIFdvcmxkIQ==",
            height=100,
            key="base64_dec_text"
        )
        
        output_type = st.radio(
            "Тип вывода:",
            ["Текст", "Бинарные данные"],
            key="base64_output_type",
            horizontal=True
        )
        
        if st.button("Декодировать из Base64", key="base64_dec_btn", use_container_width=True):
            if base64_input:
                try:
                    # Декодируем из Base64
                    decoded_bytes = base64.b64decode(base64_input)
                    
                    if output_type == "Текст":
                        decoded_text = decoded_bytes.decode('utf-8', errors='replace')
                        st.success("Декодированный текст:")
                        st.code(decoded_text, language="text")
                    else:
                        st.success("Бинарные данные:")
                        hex_representation = binascii.hexlify(decoded_bytes).decode('utf-8')
                        st.code(hex_representation, language="text")
                    
                    # Показываем детали декодирования
                    self.show_base64_decoding_details(base64_input, decoded_bytes)
                    
                except Exception as e:
                    st.error(f"Ошибка декодирования: {e}")
            else:
                st.error("Введите Base64 текст для декодирования")
    
    def render_base64_info(self):
        """Показывает дополнительную информацию о Base64"""
        st.subheader("📊 Информация о Base64")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Таблица символов Base64:**")
            base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
            
            # Создаем таблицу символов
            chars_data = []
            for i, char in enumerate(base64_chars):
                chars_data.append({
                    'Индекс': i,
                    'Символ': char,
                    'Бинарно': format(i, '06b')
                })
            
            df_chars = pd.DataFrame(chars_data)
            st.dataframe(df_chars, use_container_width=True, height=300)
        
        with col2:
            st.markdown("**Пример кодирования:**")
            
            example_text = "Man"
            example_binary = ''.join(format(ord(c), '08b') for c in example_text)
            example_encoded = base64.b64encode(example_text.encode()).decode()
            
            st.markdown(f"""
            **Текст:** "{example_text}"
            
            **Бинарно (24 бита):** {example_binary}
            
            **Разбивка на 6-битные группы:**
            - {example_binary[:6]} → {base64_chars[int(example_binary[:6], 2)]} (индекс {int(example_binary[:6], 2)})
            - {example_binary[6:12]} → {base64_chars[int(example_binary[6:12], 2)]} (индекс {int(example_binary[6:12], 2)})
            - {example_binary[12:18]} → {base64_chars[int(example_binary[12:18], 2)]} (индекс {int(example_binary[12:18], 2)})
            - {example_binary[18:24]} → {base64_chars[int(example_binary[18:24], 2)]} (индекс {int(example_binary[18:24], 2)})
            
            **Результат:** {example_encoded}
            """)
    
    def render_ascii_section(self):
        """Отрисовывает секцию ASCII"""
        st.subheader("🔡 ASCII Кодирование/Декодирование")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📤 Текст → ASCII коды")
            self.render_ascii_encoding()
        
        with col2:
            st.markdown("### 📥 ASCII коды → Текст")
            self.render_ascii_decoding()
        
        # Таблица ASCII
        st.markdown("---")
        self.render_ascii_table()
    
    def render_ascii_encoding(self):
        """Отрисовывает интерфейс кодирования ASCII"""
        text_to_encode = st.text_area(
            "Текст для преобразования в ASCII:",
            "Hello",
            height=100,
            key="ascii_enc_text"
        )
        
        output_format = st.radio(
            "Формат вывода:",
            ["Десятичный", "Шестнадцатеричный", "Бинарный", "Восьмеричный"],
            key="ascii_output_format",
            horizontal=True
        )
        
        if st.button("Преобразовать в ASCII", key="ascii_enc_btn", use_container_width=True):
            if text_to_encode:
                try:
                    ascii_codes = []
                    
                    for char in text_to_encode:
                        code = ord(char)
                        
                        if output_format == "Десятичный":
                            representation = str(code)
                        elif output_format == "Шестнадцатеричный":
                            representation = format(code, '02X')
                        elif output_format == "Бинарный":
                            representation = format(code, '08b')
                        else:  # Восьмеричный
                            representation = format(code, '03o')
                        
                        ascii_codes.append({
                            'Символ': char,
                            'Код': representation
                        })
                    
                    st.success("ASCII коды:")
                    df = pd.DataFrame(ascii_codes)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Показываем объединенную строку
                    codes_string = ' '.join([item['Код'] for item in ascii_codes])
                    st.text_area("Объединенные коды:", codes_string, height=50)
                    
                except Exception as e:
                    st.error(f"Ошибка преобразования: {e}")
            else:
                st.error("Введите текст для преобразования")
    
    def render_ascii_decoding(self):
        """Отрисовывает интерфейс декодирования ASCII"""
        ascii_input = st.text_area(
            "ASCII коды для декодирования:",
            "72 101 108 108 111",
            height=100,
            key="ascii_dec_text"
        )
        
        input_format = st.radio(
            "Формат ввода:",
            ["Десятичный", "Шестнадцатеричный", "Бинарный", "Восьмеричный"],
            key="ascii_input_format",
            horizontal=True
        )
        
        if st.button("Преобразовать в текст", key="ascii_dec_btn", use_container_width=True):
            if ascii_input:
                try:
                    # Разделяем коды
                    codes = ascii_input.split()
                    decoded_text = ""
                    decoding_details = []
                    
                    for code in codes:
                        try:
                            if input_format == "Десятичный":
                                char_code = int(code)
                            elif input_format == "Шестнадцатеричный":
                                char_code = int(code, 16)
                            elif input_format == "Бинарный":
                                char_code = int(code, 2)
                            else:  # Восьмеричный
                                char_code = int(code, 8)
                            
                            character = chr(char_code)
                            decoded_text += character
                            
                            decoding_details.append({
                                'Код': code,
                                'Десятичный': char_code,
                                'Символ': character,
                                'Валидность': '✅' if 0 <= char_code <= 127 else '❌'
                            })
                            
                        except ValueError:
                            decoding_details.append({
                                'Код': code,
                                'Десятичный': 'Ошибка',
                                'Символ': '❌',
                                'Валидность': '❌'
                            })
                    
                    st.success("Декодированный текст:")
                    st.code(decoded_text, language="text")
                    
                    # Показываем детали декодирования
                    st.markdown("**Детали декодирования:**")
                    df = pd.DataFrame(decoding_details)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                except Exception as e:
                    st.error(f"Ошибка декодирования: {e}")
            else:
                st.error("Введите ASCII коды для декодирования")
    
    def render_ascii_table(self):
        """Показывает таблицу ASCII символов"""
        st.subheader("📋 Таблица ASCII символов")
        
        # Создаем таблицу ASCII (только печатные символы)
        ascii_data = []
        for code in range(32, 127):  # Печатные символы
            character = chr(code)
            ascii_data.append({
                'Десятичный': code,
                'Шестнадцатеричный': format(code, '02X'),
                'Восьмеричный': format(code, '03o'),
                'Бинарный': format(code, '08b'),
                'Символ': character,
                'Описание': self.get_ascii_description(code)
            })
        
        # Разбиваем на страницы для лучшей производительности
        page_size = 50
        total_pages = (len(ascii_data) + page_size - 1) // page_size
        
        page = st.number_input("Страница:", min_value=1, max_value=total_pages, value=1)
        
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, len(ascii_data))
        
        df_ascii = pd.DataFrame(ascii_data[start_idx:end_idx])
        st.dataframe(df_ascii, use_container_width=True, height=400)
    
    def render_crc32_section(self):
        """Отрисовывает секцию CRC32"""
        st.subheader("🔍 CRC32 - Контрольная сумма")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Вычисление CRC32")
            self.render_crc32_calculation()
        
        with col2:
            st.markdown("### ✅ Проверка CRC32")
            self.render_crc32_verification()
        
        # Информация о CRC32
        st.markdown("---")
        self.render_crc32_info()
    
    def render_crc32_calculation(self):
        """Отрисовывает интерфейс вычисления CRC32"""
        input_type = st.radio(
            "Тип входных данных:",
            ["Текст", "Файл"],
            key="crc32_input_type",
            horizontal=True
        )
        
        if input_type == "Текст":
            text_for_crc = st.text_area(
                "Текст для вычисления CRC32:",
                "Hello, World!",
                height=100,
                key="crc32_text"
            )
            
            if st.button("Вычислить CRC32", key="crc32_calc_btn", use_container_width=True):
                if text_for_crc:
                    try:
                        crc32_value = zlib.crc32(text_for_crc.encode('utf-8')) & 0xffffffff
                        
                        st.success("CRC32 контрольная сумма:")
                        
                        col_hex, col_dec = st.columns(2)
                        with col_hex:
                            st.metric("Шестнадцатеричный", format(crc32_value, '08X'))
                        with col_dec:
                            st.metric("Десятичный", crc32_value)
                        
                        # Показываем дополнительную информацию
                        st.info(f"**Размер данных:** {len(text_for_crc)} байт")
                        
                    except Exception as e:
                        st.error(f"Ошибка вычисления: {e}")
                else:
                    st.error("Введите текст для вычисления CRC32")
        
        else:  # Файл
            uploaded_file = st.file_uploader(
                "Выберите файл для вычисления CRC32:",
                type=None,
                key="crc32_file_upload"
            )
            
            if uploaded_file is not None:
                if st.button("Вычислить CRC32 файла", key="crc32_file_btn", use_container_width=True):
                    try:
                        file_contents = uploaded_file.getvalue()
                        crc32_value = zlib.crc32(file_contents) & 0xffffffff
                        
                        st.success(f"CRC32 для файла '{uploaded_file.name}':")
                        
                        col_hex, col_dec, col_size = st.columns(3)
                        with col_hex:
                            st.metric("Шестнадцатеричный", format(crc32_value, '08X'))
                        with col_dec:
                            st.metric("Десятичный", crc32_value)
                        with col_size:
                            st.metric("Размер файла", f"{len(file_contents)} байт")
                        
                    except Exception as e:
                        st.error(f"Ошибка вычисления: {e}")
    
    def render_crc32_verification(self):
        """Отрисовывает интерфейс проверки CRC32"""
        text_to_verify = st.text_area(
            "Текст для проверки:",
            "Hello, World!",
            height=80,
            key="crc32_verify_text"
        )
        
        expected_crc32 = st.text_input(
            "Ожидаемый CRC32 (шестнадцатеричный):",
            "EBE6C6E6",
            key="crc32_expected"
        )
        
        if st.button("Проверить CRC32", key="crc32_verify_btn", use_container_width=True):
            if text_to_verify and expected_crc32:
                try:
                    # Вычисляем текущий CRC32
                    current_crc32 = zlib.crc32(text_to_verify.encode('utf-8')) & 0xffffffff
                    expected_value = int(expected_crc32, 16)
                    
                    col_curr, col_exp, col_result = st.columns(3)
                    
                    with col_curr:
                        st.metric("Вычисленный CRC32", format(current_crc32, '08X'))
                    
                    with col_exp:
                        st.metric("Ожидаемый CRC32", expected_crc32.upper())
                    
                    with col_result:
                        if current_crc32 == expected_value:
                            st.success("✅ Совпадает")
                        else:
                            st.error("❌ Не совпадает")
                    
                except ValueError:
                    st.error("Неверный формат ожидаемого CRC32. Используйте шестнадцатеричный формат.")
                except Exception as e:
                    st.error(f"Ошибка проверки: {e}")
            else:
                st.error("Введите текст и ожидаемый CRC32")
    
    def render_crc32_info(self):
        """Показывает информацию о CRC32"""
        st.subheader("📈 Информация о CRC32")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Полином CRC32:**
            ```
            x³² + x²⁶ + x²³ + x²² + x¹⁶ + x¹² + x¹¹ + x¹⁰ + x⁸ + x⁷ + x⁵ + x⁴ + x² + x + 1
            ```
            
            **Шестнадцатеричное представление:**
            - Нормальный: 0x04C11DB7
            - Реверсивный: 0xEDB88320
            
            **Свойства:**
            - Обнаруживает все одиночные ошибки
            - Обнаруживает все двойные ошибки
            - Обнаруживает все ошибки нечетной кратности
            - Обнаруживает пакеты ошибок до 32 бит
            """)
        
        with col2:
            st.markdown("""
            **Применение:**
            - ZIP, GZIP архивы
            - Файловые системы (NTFS, ext4)
            - Сетевые протоколы (Ethernet)
            - Базы данных
            
            **Ограничения:**
            - Не криптографическая хеш-функция
            - Уязвима к коллизиям
            - Не защищает от злонамеренных изменений
            """)
    
    def show_base64_encoding_details(self, plaintext: str, encoded_text: str):
        """Показывает детали кодирования Base64"""
        st.markdown("**Детали кодирования:**")
        
        # Преобразуем текст в байты
        text_bytes = plaintext.encode('utf-8')
        
        col_len, col_ratio = st.columns(2)
        with col_len:
            st.metric("Длина исходного текста", f"{len(plaintext)} символов")
        with col_ratio:
            original_size = len(text_bytes)
            encoded_size = len(encoded_text)
            overhead = ((encoded_size - original_size) / original_size) * 100
            st.metric("Избыточность", f"{overhead:.1f}%")
        
        # Показываем побайтовое преобразование для первых нескольких символов
        st.markdown("**Побайтовое преобразование (первые 3 символа):**")
        
        demo_data = []
        for i, char in enumerate(plaintext[:3]):
            byte_val = ord(char)
            binary_val = format(byte_val, '08b')
            
            demo_data.append({
                'Символ': char,
                'Десятичный': byte_val,
                'Бинарный': binary_val
            })
        
        df_demo = pd.DataFrame(demo_data)
        st.dataframe(df_demo, use_container_width=True, hide_index=True)
    
    def show_base64_decoding_details(self, encoded_text: str, decoded_bytes: bytes):
        """Показывает детали декодирования Base64"""
        st.markdown("**Детали декодирования:**")
        
        col_len, col_size = st.columns(2)
        with col_len:
            st.metric("Длина Base64", f"{len(encoded_text)} символов")
        with col_size:
            st.metric("Размер данных", f"{len(decoded_bytes)} байт")
        
        # Проверяем padding
        padding_count = encoded_text.count('=')
        if padding_count > 0:
            st.info(f"Использовано дополнение: {padding_count} символа '='")
    
    def get_ascii_description(self, code: int) -> str:
        """Возвращает описание ASCII символа"""
        descriptions = {
            32: "Пробел", 33: "Восклицательный знак", 34: "Двойная кавычка",
            35: "Решетка", 36: "Знак доллара", 37: "Процент", 38: "Амперсанд",
            39: "Одинарная кавычка", 40: "Левая круглая скобка", 41: "Правая круглая скобка",
            42: "Звездочка", 43: "Плюс", 44: "Запятая", 45: "Дефис", 46: "Точка",
            47: "Слеш", 48: "Цифра 0", 49: "Цифра 1", 50: "Цифра 2", 51: "Цифра 3",
            52: "Цифра 4", 53: "Цифра 5", 54: "Цифра 6", 55: "Цифра 7", 56: "Цифра 8",
            57: "Цифра 9", 58: "Двоеточие", 59: "Точка с запятой", 60: "Знак меньше",
            61: "Равно", 62: "Знак больше", 63: "Вопросительный знак", 64: "Собака",
            65: "Латинская A", 90: "Латинская Z", 97: "Латинская a", 122: "Латинская z"
        }
        
        return descriptions.get(code, "Печатный символ")
    
    def download_base64_file(self, base64_content: str, original_filename: str):
        """Создает кнопку для скачивания Base64 контента"""
        import io
        
        # Создаем временный файл для скачивания
        b64 = base64.b64encode(base64_content.encode()).decode()
        
        download_filename = f"encoded_{original_filename}.b64"
        
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{download_filename}">📥 Скачать Base64 файл</a>'
        st.markdown(href, unsafe_allow_html=True)

# Для обратной совместимости
class EncodingCipher(EncodingModule):
    pass
