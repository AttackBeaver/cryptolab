from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import numpy as np
import secrets
from typing import List, Tuple
import matplotlib.pyplot as plt
from PIL import Image
import io

class ECBModeModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Режим ECB"
        self.description = "Electronic Codebook - базовый режим работы блочных шифров"
        self.complexity = "intermediate"
        self.category = "modern"
        self.icon = ""
        self.order = 6
    
    def render(self):
        st.title("📝 Режим ECB (Electronic Codebook)")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **ECB (Electronic Codebook)** - простейший режим работы блочных шифров, где каждый блок открытого текста 
            шифруется независимо с использованием одного и того же ключа.
            
            **Принцип работы:**
            - Исходные данные разбиваются на блоки фиксированного размера
            - Каждый блок шифруется независимо одинаковым ключом
            - Блоки объединяются в шифротекст
            
            **Математическая запись:**
            ```
            Cᵢ = E(K, Pᵢ) для i = 1, 2, ..., n
            Pᵢ = D(K, Cᵢ) для i = 1, 2, ..., n
            ```
            Где:
            - Pᵢ - i-й блок открытого текста
            - Cᵢ - i-й блок шифротекста  
            - E - функция шифрования
            - D - функция дешифрования
            - K - ключ
            
            **Преимущества:**
            - Простота реализации
            - Параллелизация шифрования/дешифрования
            - Независимость блоков (можно дешифровать любой блок отдельно)
            
            **Недостатки:**
            - ❗ Уязвимость к анализу шаблонов
            - ❗ Отсутствие диффузии (одинаковые блоки дают одинаковые шифротексты)
            - ❗ Уязвимость к атакам подстановки
            - ❗ Не скрывает структуру данных
            
            **Применение:**
            - Простые протоколы передачи данных
            - Шифрование случайных данных
            - Образовательные цели
            - ❌ Не рекомендуется для конфиденциальных данных!
            """)
        
        st.markdown("---")
        
        # Выбор типа данных
        data_type = st.radio(
            "Тип данных для шифрования:",
            ["📝 Текст", "🖼️ Изображение", "🔢 Числовые данные"],
            horizontal=True
        )
        
        if data_type == "📝 Текст":
            self.render_text_ecb()
        elif data_type == "🖼️ Изображение":
            self.render_image_ecb()
        else:
            self.render_numeric_ecb()
    
    def render_text_ecb(self):
        """Режим ECB для текстовых данных"""
        st.subheader("📝 Шифрование текста в режиме ECB")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔒 Шифрование")
            self.render_text_encryption()
        
        with col2:
            st.markdown("### 🔓 Дешифрование")
            self.render_text_decryption()
        
        # Визуализация шаблонов
        st.markdown("---")
        self.render_pattern_analysis()
    
    def render_text_encryption(self):
        """Шифрование текста в режиме ECB"""
        plaintext = st.text_area(
            "Открытый текст:",
            "HELLOHELLOHELLOHELLOHELLOHELLOHELLO",
            height=100,
            key="ecb_enc_text",
            help="Попробуйте текст с повторяющимися блоками для демонстрации уязвимостей ECB"
        )
        
        # Выбор алгоритма
        cipher_type = st.selectbox(
            "Алгоритм шифрования:",
            ["XOR (демонстрационный)", "Простая замена", "AES-128"],
            key="ecb_cipher_type"
        )
        
        # Генерация ключа
        col_key, col_gen = st.columns([3, 1])
        
        with col_key:
            if 'ecb_enc_key' not in st.session_state:
                st.session_state.ecb_enc_key = "SECRETKEY"
            
            key = st.text_input(
                "Ключ:",
                st.session_state.ecb_enc_key,
                key="ecb_enc_key_input"
            )
        
        with col_gen:
            st.write("")  # Отступ
            st.write("")  # Отступ
            if st.button("🎲 Ключ", key="gen_ecb_key", use_container_width=True):
                random_key = ''.join(chr(secrets.randbelow(26) + 65) for _ in range(8))
                st.session_state.ecb_enc_key = random_key
                st.rerun()
        
        block_size = st.slider(
            "Размер блока (символов):",
            min_value=2,
            max_value=16,
            value=8,
            key="ecb_block_size"
        )
        
        if st.button("Зашифровать ECB", key="ecb_enc_btn", use_container_width=True):
            if plaintext and key:
                try:
                    encrypted_blocks, ciphertext = self.ecb_encrypt_text(plaintext, key, block_size, cipher_type)
                    
                    st.success("Зашифрованный текст:")
                    st.code(ciphertext, language="text")
                    
                    # Показываем процесс по блокам
                    self.show_encryption_process(plaintext, encrypted_blocks, block_size, cipher_type)
                    
                except Exception as e:
                    st.error(f"Ошибка шифрования: {e}")
            else:
                st.error("Введите текст и ключ")
    
    def render_text_decryption(self):
        """Дешифрование текста в режиме ECB"""
        ciphertext = st.text_area(
            "Шифротекст:",
            "",
            height=100,
            key="ecb_dec_text"
        )
        
        key = st.text_input(
            "Ключ:",
            "SECRETKEY",
            key="ecb_dec_key"
        )
        
        block_size = st.slider(
            "Размер блока (символов):",
            min_value=2,
            max_value=16,
            value=8,
            key="ecb_dec_block_size"
        )
        
        cipher_type = st.selectbox(
            "Алгоритм шифрования:",
            ["XOR (демонстрационный)", "Простая замена", "AES-128"],
            key="ecb_dec_cipher_type"
        )
        
        if st.button("Дешифровать ECB", key="ecb_dec_btn", use_container_width=True):
            if ciphertext and key:
                try:
                    decrypted_text = self.ecb_decrypt_text(ciphertext, key, block_size, cipher_type)
                    
                    st.success("Дешифрованный текст:")
                    st.code(decrypted_text, language="text")
                    
                except Exception as e:
                    st.error(f"Ошибка дешифрования: {e}")
            else:
                st.error("Введите шифротекст и ключ")
    
    def render_image_ecb(self):
        """Режим ECB для изображений"""
        st.subheader("🖼️ Шифрование изображений в режиме ECB")
        
        st.markdown("""
        **ECB для изображений ярко демонстрирует уязвимость режима:**
        - Структура изображения сохраняется в шифротексте
        - Одинаковые области дают одинаковые зашифрованные блоки
        - Возможно визуальное распознавание контуров
        """)
        
        # Загрузка изображения
        uploaded_file = st.file_uploader(
            "Выберите изображение для шифрования:",
            type=['png', 'jpg', 'jpeg'],
            key="ecb_image_upload"
        )
        
        if uploaded_file is not None:
            # Показываем оригинальное изображение
            image = Image.open(uploaded_file)
            st.image(image, caption="Оригинальное изображение", use_column_width=True)
            
            # Параметры шифрования
            col1, col2 = st.columns(2)
            
            with col1:
                block_size = st.slider(
                    "Размер блока (пиксели):",
                    min_value=4,
                    max_value=32,
                    value=8,
                    key="ecb_image_block_size"
                )
                
                encryption_strength = st.slider(
                    "Интенсивность шифрования:",
                    min_value=1,
                    max_value=10,
                    value=5,
                    key="ecb_encryption_strength"
                )
            
            with col2:
                if st.button("Зашифровать изображение ECB", key="ecb_image_enc_btn"):
                    self.encrypt_image_ecb(image, block_size, encryption_strength)
                
                if st.button("Показать уязвимости ECB", key="ecb_vulnerability_btn"):
                    self.demo_ecb_vulnerabilities(image)
    
    def render_numeric_ecb(self):
        """Режим ECB для числовых данных"""
        st.subheader("🔢 Шифрование числовых данных в режиме ECB")
        
        st.markdown("""
        **Демонстрация уязвимостей ECB на числовых данных:**
        - Одинаковые числа дают одинаковые шифротексты
        - Возможен частотный анализ
        - Отсутствие диффузии между блоками
        """)
        
        # Генерация числовых данных
        data_type = st.radio(
            "Тип числовых данных:",
            ["Повторяющаяся последовательность", "Случайные числа", "Арифметическая прогрессия"],
            key="numeric_data_type"
        )
        
        if st.button("Сгенерировать и зашифровать данные", key="numeric_ecb_btn"):
            self.demo_numeric_ecb(data_type)
    
    def render_pattern_analysis(self):
        """Анализ шаблонов в ECB"""
        st.subheader("🔍 Анализ шаблонов в режиме ECB")
        
        st.markdown("""
        **Проблема шаблонов в ECB:**
        Одинаковые блоки открытого текста всегда дают одинаковые блоки шифротекста, 
        что позволяет анализировать структуру данных даже без знания ключа.
        """)
        
        # Демонстрация с простым текстом
        demo_text = st.text_input(
            "Текст для анализа шаблонов:",
            "AAAAAAAABBBBBBBBAAAAAAAABBBBBBBB",
            key="pattern_text"
        )
        
        if st.button("Проанализировать шаблоны", key="pattern_btn"):
            self.analyze_ecb_patterns(demo_text)
    
    def ecb_encrypt_text(self, plaintext: str, key: str, block_size: int, cipher_type: str) -> Tuple[List[str], str]:
        """Шифрует текст в режиме ECB"""
        # Дополняем текст до кратного block_size
        padded_text = self.pad_text(plaintext, block_size)
        
        # Разбиваем на блоки
        blocks = [padded_text[i:i+block_size] for i in range(0, len(padded_text), block_size)]
        
        encrypted_blocks = []
        
        for block in blocks:
            if cipher_type == "XOR (демонстрационный)":
                encrypted_block = self.xor_encrypt(block, key)
            elif cipher_type == "Простая замена":
                encrypted_block = self.substitution_encrypt(block, key)
            else:  # AES-128
                encrypted_block = self.demo_aes_encrypt(block, key)
            
            encrypted_blocks.append(encrypted_block)
        
        # Объединяем блоки
        ciphertext = ''.join(encrypted_blocks)
        
        return encrypted_blocks, ciphertext
    
    def ecb_decrypt_text(self, ciphertext: str, key: str, block_size: int, cipher_type: str) -> str:
        """Дешифрует текст в режиме ECB"""
        # Разбиваем на блоки
        blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
        
        decrypted_blocks = []
        
        for block in blocks:
            if cipher_type == "XOR (демонстрационный)":
                decrypted_block = self.xor_decrypt(block, key)
            elif cipher_type == "Простая замена":
                decrypted_block = self.substitution_decrypt(block, key)
            else:  # AES-128
                decrypted_block = self.demo_aes_decrypt(block, key)
            
            decrypted_blocks.append(decrypted_block)
        
        # Объединяем и убираем дополнение
        decrypted_text = ''.join(decrypted_blocks)
        return self.unpad_text(decrypted_text)
    
    def pad_text(self, text: str, block_size: int) -> str:
        """Дополняет текст до кратного block_size"""
        padding_length = block_size - (len(text) % block_size)
        if padding_length == block_size:
            padding_length = 0
        
        padding_char = chr(padding_length) if padding_length > 0 else ''
        return text + padding_char * padding_length
    
    def unpad_text(self, text: str) -> str:
        """Убирает дополнение из текста"""
        if not text:
            return text
        
        padding_length = ord(text[-1])
        if padding_length < len(text) and all(c == text[-1] for c in text[-padding_length:]):
            return text[:-padding_length]
        
        return text
    
    def xor_encrypt(self, block: str, key: str) -> str:
        """Простое XOR шифрование для демонстрации"""
        result = []
        key_len = len(key)
        
        for i, char in enumerate(block):
            key_char = key[i % key_len]
            encrypted_char = chr(ord(char) ^ ord(key_char))
            result.append(encrypted_char)
        
        return ''.join(result)
    
    def xor_decrypt(self, block: str, key: str) -> str:
        """XOR дешифрование (симметрично шифрованию)"""
        return self.xor_encrypt(block, key)
    
    def substitution_encrypt(self, block: str, key: str) -> str:
        """Простая подстановка"""
        result = []
        key_sum = sum(ord(c) for c in key) % 26
        
        for char in block:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - base + key_sum) % 26
                result.append(chr(base + shifted))
            else:
                result.append(char)
        
        return ''.join(result)
    
    def substitution_decrypt(self, block: str, key: str) -> str:
        """Обратная подстановка"""
        result = []
        key_sum = sum(ord(c) for c in key) % 26
        
        for char in block:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shifted = (ord(char) - base - key_sum) % 26
                result.append(chr(base + shifted))
            else:
                result.append(char)
        
        return ''.join(result)
    
    def demo_aes_encrypt(self, block: str, key: str) -> str:
        """Демонстрационное AES-подобное шифрование"""
        # Упрощенная версия для демонстрации
        import hashlib
        
        # Используем хеш для имитации AES
        combined = block + key
        hash_obj = hashlib.md5(combined.encode())
        return hash_obj.hexdigest()[:len(block)*2].upper()
    
    def demo_aes_decrypt(self, block: str, key: str) -> str:
        """Демонстрационное AES-подобное дешифрование"""
        # В реальном AES здесь было бы настоящее дешифрование
        # Для демонстрации возвращаем фиктивный результат
        return "A" * len(block)
    
    def show_encryption_process(self, plaintext: str, encrypted_blocks: List[str], block_size: int, cipher_type: str):
        """Показывает процесс шифрования по блокам"""
        st.markdown("### 🔄 Процесс шифрования по блокам")
        
        # Разбиваем оригинальный текст на блоки
        padded_text = self.pad_text(plaintext, block_size)
        original_blocks = [padded_text[i:i+block_size] for i in range(0, len(padded_text), block_size)]
        
        # Создаем таблицу для отображения
        process_data = []
        
        for i, (orig_block, enc_block) in enumerate(zip(original_blocks, encrypted_blocks)):
            # Проверяем наличие шаблонов
            pattern_detected = "✅ Нет" if i == 0 or orig_block != original_blocks[i-1] else "❌ Есть"
            
            process_data.append({
                'Блок': i + 1,
                'Открытый текст': orig_block,
                '→': '→',
                'Шифротекст': enc_block,
                'Шаблон': pattern_detected
            })
        
        df = pd.DataFrame(process_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Анализ безопасности
        self.analyze_ecb_security(original_blocks, encrypted_blocks)
    
    def analyze_ecb_security(self, original_blocks: List[str], encrypted_blocks: List[str]):
        """Анализирует безопасность ECB шифрования"""
        st.markdown("### 🛡️ Анализ безопасности")
        
        # Проверяем повторяющиеся блоки
        original_patterns = {}
        encrypted_patterns = {}
        
        for i, block in enumerate(original_blocks):
            if block in original_patterns:
                original_patterns[block].append(i)
            else:
                original_patterns[block] = [i]
        
        for i, block in enumerate(encrypted_blocks):
            if block in encrypted_patterns:
                encrypted_patterns[block].append(i)
            else:
                encrypted_patterns[block] = [i]
        
        # Находим уязвимости
        vulnerabilities = []
        
        # Проверка 1: Одинаковые открытые блоки -> одинаковые шифрованные блоки
        for orig_block, orig_positions in original_patterns.items():
            if len(orig_positions) > 1:
                # Проверяем, что соответствующие шифрованные блоки тоже одинаковы
                enc_blocks = [encrypted_blocks[pos] for pos in orig_positions]
                if len(set(enc_blocks)) == 1:
                    vulnerabilities.append(f"❌ Блок '{orig_block}' (позиции {orig_positions}) всегда шифруется одинаково")
        
        # Проверка 2: Разные открытые блоки -> разные шифрованные блоки (желательно)
        if not vulnerabilities:
            st.success("✅ Не обнаружено явных уязвимостей шаблонов")
        else:
            st.error("🚨 Обнаружены уязвимости ECB:")
            for vuln in vulnerabilities:
                st.write(vuln)
            
            st.warning("""
            **Рекомендации:**
            - Используйте режимы с диффузией (CBC, CFB, OFB)
            - Добавьте случайный вектор инициализации (IV)
            - Используйте режим аутентифицированного шифрования (GCM)
            """)
    
    def encrypt_image_ecb(self, image: Image.Image, block_size: int, strength: int):
        """Шифрует изображение в режиме ECB"""
        st.markdown("### 🖼️ Результат ECB шифрования изображения")
        
        # Конвертируем в RGB если нужно
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Создаем копию для шифрования
        encrypted_image = image.copy()
        pixels = encrypted_image.load()
        
        width, height = image.size
        
        # Шифруем по блокам
        blocks_processed = 0
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                # Обрабатываем блок
                for i in range(min(block_size, height - y)):
                    for j in range(min(block_size, width - x)):
                        # Простое "шифрование" - инвертируем цвета
                        r, g, b = pixels[x + j, y + i]
                        pixels[x + j, y + i] = (
                            (r + strength * 25) % 256,
                            (g + strength * 17) % 256, 
                            (b + strength * 31) % 256
                        )
                
                blocks_processed += 1
                progress = blocks_processed / ((width // block_size + 1) * (height // block_size + 1))
                progress_bar.progress(progress)
        
        status_text.text("✅ Шифрование завершено")
        
        # Показываем результаты
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Оригинальное изображение", use_column_width=True)
        
        with col2:
            st.image(encrypted_image, caption="Зашифрованное в ECB", use_column_width=True)
        
        st.warning("""
        **Наблюдение:** Несмотря на шифрование, структура изображения остается видимой!
        Это демонстрирует главную уязвимость режима ECB - отсутствие диффузии.
        """)
    
    def demo_ecb_vulnerabilities(self, image: Image.Image):
        """Демонстрирует уязвимости ECB на изображениях"""
        st.markdown("### 🎯 Демонстрация уязвимостей ECB")
        
        # Создаем простое изображение с повторяющимися паттернами
        pattern_size = 50
        demo_image = Image.new('RGB', (200, 200), color='white')
        pixels = demo_image.load()
        
        # Создаем шахматный паттерн
        for y in range(200):
            for x in range(200):
                if (x // pattern_size + y // pattern_size) % 2 == 0:
                    pixels[x, y] = (0, 0, 0)  # Черный
                else:
                    pixels[x, y] = (255, 255, 255)  # Белый
        
        # "Шифруем" в ECB
        encrypted_demo = demo_image.copy()
        enc_pixels = encrypted_demo.load()
        block_size = 10
        
        for y in range(0, 200, block_size):
            for x in range(0, 200, block_size):
                # Применяем простое преобразование к каждому блоку
                for i in range(min(block_size, 200 - y)):
                    for j in range(min(block_size, 200 - x)):
                        r, g, b = enc_pixels[x + j, y + i]
                        enc_pixels[x + j, y + i] = (
                            (r + 128) % 256,
                            (g + 64) % 256,
                            (b + 192) % 256
                        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(demo_image, caption="Оригинал с паттернами", use_column_width=True)
        
        with col2:
            st.image(encrypted_demo, caption="'Зашифрованный' ECB", use_column_width=True)
        
        st.error("""
        **Критическая уязвимость:** Паттерны оригинала полностью сохраняются в зашифрованном изображении!
        Атакующий может легко определить структуру данных без знания ключа.
        """)
    
    def demo_numeric_ecb(self, data_type: str):
        """Демонстрирует ECB на числовых данных"""
        st.markdown("### 🔢 Шифрование числовых данных в ECB")
        
        # Генерируем данные
        if data_type == "Повторяющаяся последовательность":
            data = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
        elif data_type == "Случайные числа":
            data = [secrets.randbelow(10) for _ in range(12)]
        else:  # Арифметическая прогрессия
            data = list(range(1, 13))
        
        # "Шифруем" данные (простая демонстрация)
        key = 7
        encrypted_data = [(x + key) % 10 for x in data]
        
        # Создаем визуализацию
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Оригинальные данные
        ax1.bar(range(len(data)), data, color='blue', alpha=0.7)
        ax1.set_title('Оригинальные данные')
        ax1.set_xlabel('Позиция')
        ax1.set_ylabel('Значение')
        ax1.grid(True, alpha=0.3)
        
        # Зашифрованные данные
        ax2.bar(range(len(encrypted_data)), encrypted_data, color='red', alpha=0.7)
        ax2.set_title('Зашифрованные данные (ECB)')
        ax2.set_xlabel('Позиция')
        ax2.set_ylabel('Значение')
        ax2.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        # Анализ
        st.markdown("### 📊 Анализ результатов")
        
        analysis_data = []
        for i, (orig, enc) in enumerate(zip(data, encrypted_data)):
            pattern_info = "Повтор" if i > 0 and orig == data[i-1] and enc == encrypted_data[i-1] else "Уникальный"
            analysis_data.append({
                'Позиция': i + 1,
                'Оригинал': orig,
                'Шифротекст': enc,
                'Шаблон': pattern_info
            })
        
        df = pd.DataFrame(analysis_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Проверяем уязвимости
        unique_original = len(set(data))
        unique_encrypted = len(set(encrypted_data))
        
        if unique_encrypted < unique_original:
            st.error(f"❌ Потеря информации: {unique_original} уникальных значений → {unique_encrypted} уникальных шифротекстов")
        elif unique_encrypted == unique_original:
            st.warning("⚠️ Сохранена структура данных: количество уникальных значений не изменилось")
        else:
            st.success("✅ Хорошая диффузия: увеличение количества уникальных значений")
    
    def analyze_ecb_patterns(self, text: str):
        """Анализирует шаблоны в ECB шифровании"""
        st.markdown("### 🔍 Детальный анализ шаблонов")
        
        block_size = 8
        key = "SECRETKEY"
        
        # Шифруем текст
        encrypted_blocks, ciphertext = self.ecb_encrypt_text(text, key, block_size, "XOR (демонстрационный)")
        
        # Анализируем частоты
        original_blocks = [text[i:i+block_size] for i in range(0, len(self.pad_text(text, block_size)), block_size)]
        
        # Создаем тепловую карту схожести
        similarity_matrix = np.zeros((len(original_blocks), len(original_blocks)))
        
        for i in range(len(original_blocks)):
            for j in range(len(original_blocks)):
                if original_blocks[i] == original_blocks[j]:
                    similarity_matrix[i][j] = 1
                elif encrypted_blocks[i] == encrypted_blocks[j]:
                    similarity_matrix[i][j] = 0.5
                else:
                    similarity_matrix[i][j] = 0
        
        # Визуализация
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Тепловая карта оригинальных блоков
        im1 = ax1.imshow(similarity_matrix, cmap='RdYlBu_r', interpolation='nearest')
        ax1.set_title('Схожесть оригинальных блоков')
        ax1.set_xlabel('Номер блока')
        ax1.set_ylabel('Номер блока')
        plt.colorbar(im1, ax=ax1)
        
        # График уникальности блоков
        unique_blocks_orig = len(set(original_blocks))
        unique_blocks_enc = len(set(encrypted_blocks))
        
        categories = ['Оригинальные блоки', 'Шифрованные блоки']
        values = [unique_blocks_orig, unique_blocks_enc]
        colors = ['blue', 'red']
        
        bars = ax2.bar(categories, values, color=colors, alpha=0.7)
        ax2.set_title('Уникальность блоков')
        ax2.set_ylabel('Количество уникальных блоков')
        
        # Добавляем значения на столбцы
        for bar, value in zip(bars, values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                    f'{value}', ha='center', va='bottom')
        
        st.pyplot(fig)
        
        # Выводы
        if unique_blocks_orig == unique_blocks_enc:
            st.error("""
            🚨 **Критическая уязвимость:** Количество уникальных блоков не изменилось!
            Это означает, что структура данных полностью сохранилась в шифротексте.
            """)
        elif unique_blocks_enc < unique_blocks_orig:
            st.warning("""
            ⚠️ **Уязвимость:** Потеря уникальности блоков при шифровании.
            Несколько разных блоков открытого текста дали одинаковые блоки шифротекста.
            """)
        else:
            st.success("""
            ✅ **Хороший признак:** Увеличение уникальности блоков.
            Однако в ECB это не защищает от анализа шаблонов одинаковых блоков.
            """)

# Для обратной совместимости
class ECBMode(ECBModeModule):
    pass
