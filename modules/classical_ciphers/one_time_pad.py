from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import numpy as np
import random
import secrets
from typing import List, Tuple

class OneTimePadModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Одноразовый блокнот"
        self.description = "Шифр Вернама - теоретически невзламываемая криптосистема"
        self.complexity = "advanced"
        self.category = "classical"
        self.icon = ""
        self.order = 9
    
    def render(self):
        st.title("📓 Одноразовый блокнот (Шифр Вернама)")
        
        # Инициализация состояний
        if 'otp_encrypt_key' not in st.session_state:
            st.session_state.otp_encrypt_key = ""
        if 'otp_encrypt_key_generated' not in st.session_state:
            st.session_state.otp_encrypt_key_generated = ""
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **Одноразовый блокнот (Шифр Вернама)** - единственная известная криптосистема, обладающая **идеальной криптографической стойкостью**.
            
            **Математические основы:**
            - **Операция XOR**: `A ⊕ B = C`, где `C ⊕ B = A`
            - **Свойства XOR**: 
              - Коммутативность: `A ⊕ B = B ⊕ A`
              - Ассоциативность: `(A ⊕ B) ⊕ C = A ⊕ (B ⊕ C)`
              - Обратимость: `A ⊕ A = 0`, `A ⊕ 0 = A`
            
            **Принцип работы:**
            1. Генерируется случайный ключ той же длины, что и сообщение
            2. Каждый бит сообщения объединяется с соответствующим битом ключа через XOR
            3. Для дешифрования применяется та же операция с тем же ключом
            
            **Условия идеальной стойкости:**
            - ✅ Ключ **истинно случайный**
            - ✅ Ключ **той же длины**, что и сообщение
            - ✅ Ключ **никогда не используется повторно**
            - ✅ Ключ **хранится в секрете**
            
            **Теорема Шеннона:** Если выполнены все условия, то взлом невозможен даже при бесконечных вычислительных ресурсах.
            """)
        
        st.markdown("---")
        
        # Выбор режима работы
        mode = st.radio(
            "Режим работы:",
            ["🔐 Шифрование/Дешифрование", "🎯 Визуализация процесса", "🔬 Криптоанализ"],
            horizontal=True
        )
        
        if mode == "🔐 Шифрование/Дешифрование":
            self.render_encryption_section()
        elif mode == "🎯 Визуализация процесса":
            self.render_visualization_section()
        else:
            self.render_cryptanalysis_section()
    
    def text_to_binary(self, text: str) -> str:
        """Преобразует текст в бинарную строку"""
        binary = ''
        for char in text:
            # Преобразуем символ в 8-битный код
            binary += format(ord(char), '08b')
        return binary
    
    def binary_to_text(self, binary: str) -> str:
        """Преобразует бинарную строку в текст"""
        text = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text
    
    def generate_random_key(self, length: int) -> str:
        """Генерирует криптографически безопасный случайный ключ"""
        # Используем secrets для криптографически безопасной генерации
        key_bits = ''
        for _ in range(length):
            key_bits += str(secrets.randbelow(2))
        return key_bits
    
    def xor_operation(self, text_bits: str, key_bits: str) -> str:
        """Выполняет операцию XOR между двумя битовыми строками"""
        if len(text_bits) != len(key_bits):
            raise ValueError("Длины текста и ключа должны совпадать")
        
        result = ''
        for t_bit, k_bit in zip(text_bits, key_bits):
            result += str(int(t_bit) ^ int(k_bit))
        return result
    
    def render_encryption_section(self):
        """Отрисовывает секцию шифрования/дешифрования"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔒 Шифрование")
            self.render_encryption()
        
        with col2:
            st.subheader("🔓 Расшифровка")
            self.render_decryption()
    
    def render_encryption(self):
        """Отрисовывает интерфейс шифрования"""
        plaintext = st.text_area(
            "Исходный текст:",
            "SECRET",
            height=100,
            key="otp_encrypt_input"
        )
        
        # Генерация ключа
        col_key, col_gen = st.columns([3, 1])
        
        with col_key:
            # Используем сгенерированный ключ или ручной ввод
            current_key = st.session_state.otp_encrypt_key_generated if st.session_state.otp_encrypt_key_generated else st.session_state.otp_encrypt_key
            
            key_input = st.text_area(
                "Ключ (бинарный):",
                value=current_key,
                height=100,
                key="otp_encrypt_key_input",
                placeholder="Введите бинарный ключ или сгенерируйте автоматически"
            )
            
            # Сохраняем ручной ввод
            if key_input != current_key:
                st.session_state.otp_encrypt_key = key_input
                st.session_state.otp_encrypt_key_generated = ""  # Сбрасываем сгенерированный ключ
        
        with col_gen:
            st.write("")  # Отступ
            st.write("")  # Отступ
            if st.button("🎲 Сгенерировать ключ", key="gen_encrypt_key", use_container_width=True):
                if plaintext:
                    text_binary = self.text_to_binary(plaintext)
                    random_key = self.generate_random_key(len(text_binary))
                    st.session_state.otp_encrypt_key_generated = random_key
                    st.session_state.otp_encrypt_key = random_key
                    st.rerun()
                else:
                    st.error("Введите текст для генерации ключа")
        
        # Используем сгенерированный ключ или ручной ввод
        current_key = st.session_state.otp_encrypt_key_generated if st.session_state.otp_encrypt_key_generated else st.session_state.otp_encrypt_key
        
        if st.button("Зашифровать", key="encrypt_otp_btn", use_container_width=True):
            if plaintext and current_key:
                try:
                    # Преобразуем текст в бинарный формат
                    text_binary = self.text_to_binary(plaintext)
                    
                    # Проверяем длину ключа
                    if len(current_key) != len(text_binary):
                        st.error(f"Длина ключа ({len(current_key)} бит) должна совпадать с длиной текста ({len(text_binary)} бит)")
                        return
                    
                    # Выполняем шифрование
                    encrypted_binary = self.xor_operation(text_binary, current_key)
                    encrypted_text = self.binary_to_text(encrypted_binary)
                    
                    st.success("Зашифрованный текст:")
                    st.code(encrypted_text, language="text")
                    
                    # Показываем детали
                    self.show_encryption_details(plaintext, text_binary, current_key, encrypted_binary, encrypted_text)
                    
                except Exception as e:
                    st.error(f"Ошибка шифрования: {e}")
            else:
                st.error("Введите текст и ключ")
    
    def render_decryption(self):
        """Отрисовывает интерфейс дешифрования"""
        ciphertext = st.text_area(
            "Зашифрованный текст:",
            "",
            height=100,
            key="otp_decrypt_input"
        )
        
        # Инициализация состояния для дешифрования
        if 'otp_decrypt_key' not in st.session_state:
            st.session_state.otp_decrypt_key = ""
        
        key_input = st.text_area(
            "Ключ (бинарный):",
            value=st.session_state.otp_decrypt_key,
            height=100,
            key="otp_decrypt_key_input",
            placeholder="Введите тот же ключ, что использовался для шифрования"
        )
        
        # Сохраняем ввод ключа
        if key_input != st.session_state.otp_decrypt_key:
            st.session_state.otp_decrypt_key = key_input
        
        if st.button("Расшифровать", key="decrypt_otp_btn", use_container_width=True):
            if ciphertext and key_input:
                try:
                    # Преобразуем текст в бинарный формат
                    cipher_binary = self.text_to_binary(ciphertext)
                    
                    # Проверяем длину ключа
                    if len(key_input) != len(cipher_binary):
                        st.error(f"Длина ключа ({len(key_input)} бит) должна совпадать с длиной текста ({len(cipher_binary)} бит)")
                        return
                    
                    # Выполняем дешифрование
                    decrypted_binary = self.xor_operation(cipher_binary, key_input)
                    decrypted_text = self.binary_to_text(decrypted_binary)
                    
                    st.success("Расшифрованный текст:")
                    st.code(decrypted_text, language="text")
                    
                    # Показываем детали
                    self.show_decryption_details(ciphertext, cipher_binary, key_input, decrypted_binary, decrypted_text)
                    
                except Exception as e:
                    st.error(f"Ошибка дешифрования: {e}")
            else:
                st.error("Введите текст и ключ")
    
    def render_visualization_section(self):
        """Отрисовывает секцию визуализации"""
        st.subheader("🎯 Визуализация работы одноразового блокнота")
        
        # Инициализация состояния для визуализации
        if 'viz_otp_text' not in st.session_state:
            st.session_state.viz_otp_text = "A"
        
        demo_text = st.text_input(
            "Текст для демонстрации:", 
            st.session_state.viz_otp_text, 
            key="viz_otp_text_input"
        )
        
        if demo_text != st.session_state.viz_otp_text:
            st.session_state.viz_otp_text = demo_text
        
        if st.button("Показать процесс", key="viz_otp_btn"):
            if st.session_state.viz_otp_text:
                self.show_visualization_process(st.session_state.viz_otp_text)
            else:
                st.error("Введите текст для демонстрации")
        
        # Демонстрация свойств XOR
        st.markdown("---")
        st.subheader("🧮 Свойства операции XOR")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            a = st.selectbox("Бит A:", [0, 1], key="xor_a")
        with col2:
            b = st.selectbox("Бит B:", [0, 1], key="xor_b")
        with col3:
            result = a ^ b
            st.metric("A ⊕ B", result)
        
        # Таблица истинности XOR
        st.markdown("**Таблица истинности XOR:**")
        xor_truth_table = pd.DataFrame({
            'A': [0, 0, 1, 1],
            'B': [0, 1, 0, 1],
            'A ⊕ B': [0, 1, 1, 0]
        })
        st.dataframe(xor_truth_table, use_container_width=True, hide_index=True)
        
        # Демонстрация обратимости
        st.markdown("---")
        st.subheader("🔄 Свойство обратимости")
        
        # Инициализация состояния для обратимости
        if 'reversible_demo' not in st.session_state:
            st.session_state.reversible_demo = "HELLO"
        
        demo_reversible = st.text_input(
            "Текст для демонстрации обратимости:", 
            st.session_state.reversible_demo, 
            key="reversible_demo_input"
        )
        
        if demo_reversible != st.session_state.reversible_demo:
            st.session_state.reversible_demo = demo_reversible
        
        if st.button("Показать обратимость", key="reversible_btn"):
            self.show_reversibility(st.session_state.reversible_demo)
    
    def render_cryptanalysis_section(self):
        """Отрисовывает секцию криптоанализа"""
        st.subheader("🔬 Криптоанализ одноразового блокнота")
        
        st.markdown("""
        ### Почему одноразовый блокнот невозможно взломать?
        
        **Математическое доказательство:**
        - Для любого шифротекста C и любого открытого текста P существует ключ K такой, что C = P ⊕ K
        - Все ключи равновероятны
        - Невозможно определить, какой из возможных ключей является правильным
        """)
        
        # Демонстрация множества возможных расшифровок
        st.markdown("### 🎲 Демонстрация множества возможных расшифровок")
        
        # Инициализация состояния для криптоанализа
        if 'crypto_demo' not in st.session_state:
            st.session_state.crypto_demo = "0100100001000101010011000100110001001111"
        
        cipher_demo = st.text_input(
            "Шифротекст (бинарный):", 
            st.session_state.crypto_demo, 
            key="crypto_demo_input"
        )
        
        if cipher_demo != st.session_state.crypto_demo:
            st.session_state.crypto_demo = cipher_demo
        
        if st.button("Показать возможные расшифровки", key="crypto_btn"):
            self.show_possible_decryptions(st.session_state.crypto_demo)
        
        # Демонстрация проблемы повторного использования ключа
        st.markdown("---")
        st.subheader("⚠️ Опасность повторного использования ключа")
        
        # Инициализация состояний для повторного использования
        if 'reuse_text1' not in st.session_state:
            st.session_state.reuse_text1 = "ATTACK"
        if 'reuse_text2' not in st.session_state:
            st.session_state.reuse_text2 = "RETREAT"
        if 'reuse_enc1' not in st.session_state:
            st.session_state.reuse_enc1 = ""
        if 'reuse_enc2' not in st.session_state:
            st.session_state.reuse_enc2 = ""
        
        col1, col2 = st.columns(2)
        
        with col1:
            text1 = st.text_input("Сообщение 1:", st.session_state.reuse_text1, key="reuse_text1_input")
            if text1 != st.session_state.reuse_text1:
                st.session_state.reuse_text1 = text1
            
            encrypted1 = st.text_input("Шифротекст 1 (бинарный):", st.session_state.reuse_enc1, key="reuse_enc1_input")
            if encrypted1 != st.session_state.reuse_enc1:
                st.session_state.reuse_enc1 = encrypted1
        
        with col2:
            text2 = st.text_input("Сообщение 2:", st.session_state.reuse_text2, key="reuse_text2_input")
            if text2 != st.session_state.reuse_text2:
                st.session_state.reuse_text2 = text2
            
            encrypted2 = st.text_input("Шифротекст 2 (бинарный):", st.session_state.reuse_enc2, key="reuse_enc2_input")
            if encrypted2 != st.session_state.reuse_enc2:
                st.session_state.reuse_enc2 = encrypted2
        
        if st.button("Показать уязвимость", key="reuse_btn"):
            self.show_reuse_vulnerability(
                st.session_state.reuse_text1, 
                st.session_state.reuse_text2, 
                st.session_state.reuse_enc1, 
                st.session_state.reuse_enc2
            )
    
    def show_encryption_details(self, plaintext: str, text_binary: str, key_binary: str, encrypted_binary: str, encrypted_text: str):
        """Показывает детали процесса шифрования"""
        st.markdown("**Детали шифрования:**")
        
        # Создаем таблицу для отображения процесса
        process_data = []
        
        # Показываем первые несколько символов для наглядности
        max_chars = min(5, len(plaintext))
        
        for i in range(max_chars):
            char = plaintext[i]
            char_binary = text_binary[i*8:(i+1)*8]
            key_segment = key_binary[i*8:(i+1)*8]
            encrypted_segment = encrypted_binary[i*8:(i+1)*8]
            
            process_data.append({
                'Символ': char,
                'Бинарный код': char_binary,
                'Ключ': key_segment,
                'XOR результат': encrypted_segment,
                'Шифросимвол': self.binary_to_text(encrypted_segment)
            })
        
        df = pd.DataFrame(process_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Статистика
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Длина текста", f"{len(plaintext)} символов")
        with col2:
            st.metric("Бит текста", f"{len(text_binary)} бит")
        with col3:
            st.metric("Бит ключа", f"{len(key_binary)} бит")
    
    def show_decryption_details(self, ciphertext: str, cipher_binary: str, key_binary: str, decrypted_binary: str, decrypted_text: str):
        """Показывает детали процесса дешифрования"""
        st.markdown("**Детали дешифрования:**")
        
        # Создаем таблицу для отображения процесса
        process_data = []
        
        # Показываем первые несколько символов для наглядности
        max_chars = min(5, len(ciphertext))
        
        for i in range(max_chars):
            char = ciphertext[i]
            char_binary = cipher_binary[i*8:(i+1)*8]
            key_segment = key_binary[i*8:(i+1)*8]
            decrypted_segment = decrypted_binary[i*8:(i+1)*8]
            
            process_data.append({
                'Шифросимвол': char,
                'Бинарный код': char_binary,
                'Ключ': key_segment,
                'XOR результат': decrypted_segment,
                'Расшифрованный': self.binary_to_text(decrypted_segment)
            })
        
        df = pd.DataFrame(process_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    def show_visualization_process(self, text: str):
        """Показывает визуализацию процесса шифрования"""
        # Генерируем ключ
        text_binary = self.text_to_binary(text)
        key_binary = self.generate_random_key(len(text_binary))
        encrypted_binary = self.xor_operation(text_binary, key_binary)
        
        st.markdown("### 🔍 Пошаговая визуализация:")
        
        for i, char in enumerate(text):
            st.markdown(f"**Символ {i+1}: '{char}'**")
            
            # Получаем бинарные представления для текущего символа
            char_binary = text_binary[i*8:(i+1)*8]
            key_segment = key_binary[i*8:(i+1)*8]
            encrypted_segment = encrypted_binary[i*8:(i+1)*8]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("**Текст:**")
                st.code(f"{char}\n{char_binary}")
            
            with col2:
                st.markdown("**⊕**")
                st.markdown("<div style='text-align: center; font-size: 24px; margin-top: 20px;'>⊕</div>", unsafe_allow_html=True)
            
            with col3:
                st.markdown("**Ключ:**")
                st.code(f"{key_segment}")
            
            with col4:
                st.markdown("**Результат:**")
                st.code(f"{encrypted_segment}")
            
            # Показываем побитовую операцию
            st.markdown("**Побитовая операция XOR:**")
            
            bit_operation = ""
            for j, (t_bit, k_bit) in enumerate(zip(char_binary, key_segment)):
                result_bit = str(int(t_bit) ^ int(k_bit))
                bit_operation += f"{t_bit} ⊕ {k_bit} = {result_bit}\n"
            
            st.text_area("", bit_operation, height=150, key=f"bit_op_{i}")
            
            st.markdown("---")
    
    def show_reversibility(self, text: str):
        """Демонстрирует свойство обратимости XOR"""
        text_binary = self.text_to_binary(text)
        key_binary = self.generate_random_key(len(text_binary))
        
        # Шифрование
        encrypted_binary = self.xor_operation(text_binary, key_binary)
        
        # Дешифрование
        decrypted_binary = self.xor_operation(encrypted_binary, key_binary)
        decrypted_text = self.binary_to_text(decrypted_binary)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Исходный текст:**")
            st.info(f"```\n{text}\n```")
            st.text(f"Бинарно: {text_binary}")
        
        with col2:
            st.markdown("**После шифрования:**")
            st.warning(f"```\n{self.binary_to_text(encrypted_binary)}\n```")
            st.text(f"Бинарно: {encrypted_binary}")
        
        with col3:
            st.markdown("**После дешифрования:**")
            if text == decrypted_text:
                st.success(f"```\n{decrypted_text}\n✅\n```")
            else:
                st.error(f"```\n{decrypted_text}\n❌\n```")
            st.text(f"Бинарно: {decrypted_binary}")
        
        st.success("✅ Свойство обратимости подтверждено: P ⊕ K ⊕ K = P")
    
    def show_possible_decryptions(self, cipher_binary: str):
        """Показывает множество возможных расшифровок"""
        if len(cipher_binary) % 8 != 0:
            st.error("Длина шифротекста должна быть кратна 8 битам")
            return
        
        st.markdown("**Возможные расшифровки (случайные ключи):**")
        
        # Генерируем несколько случайных ключей и показываем результаты
        possible_decryptions = []
        
        for i in range(5):  # Показываем 5 случайных расшифровок
            random_key = self.generate_random_key(len(cipher_binary))
            decrypted_binary = self.xor_operation(cipher_binary, random_key)
            decrypted_text = self.binary_to_text(decrypted_binary)
            
            # Проверяем, содержит ли результат только печатные символы
            if all(32 <= ord(c) <= 126 for c in decrypted_text):
                possible_decryptions.append({
                    'Ключ': random_key[:32] + "..." if len(random_key) > 32 else random_key,
                    'Расшифровка': decrypted_text,
                    'Правдоподобность': '✅' if decrypted_text.isprintable() else '❌'
                })
        
        if possible_decryptions:
            df = pd.DataFrame(possible_decryptions)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.info("Все расшифровки одинаково правдоподобны - невозможно определить правильную!")
        else:
            st.warning("Не удалось сгенерировать правдоподобные расшифровки")
    
    def show_reuse_vulnerability(self, text1: str, text2: str, enc1: str, enc2: str):
        """Демонстрирует уязвимость при повторном использовании ключа"""
        if not text1 or not text2:
            st.error("Введите оба сообщения")
            return
        
        # Если шифротексты не предоставлены, генерируем их с одним ключом
        if not enc1 or not enc2:
            # Используем один ключ для обоих сообщений (НЕПРАВИЛЬНО!)
            key = self.generate_random_key(max(len(self.text_to_binary(text1)), len(self.text_to_binary(text2))))
            
            enc1 = self.xor_operation(self.text_to_binary(text1), key[:len(self.text_to_binary(text1))])
            enc2 = self.xor_operation(self.text_to_binary(text2), key[:len(self.text_to_binary(text2))])
        
        st.error("⚠️ Обнаружено повторное использование ключа!")
        
        # Показываем, как можно извлечь информацию
        st.markdown("**Извлечение информации через XOR шифротекстов:**")
        
        # C1 ⊕ C2 = (P1 ⊕ K) ⊕ (P2 ⊕ K) = P1 ⊕ P2
        if len(enc1) == len(enc2):
            p1_xor_p2 = self.xor_operation(enc1, enc2)
            
            # Пытаемся найти общие паттерны
            st.markdown(f"**P1 ⊕ P2 =** `{p1_xor_p2}`")
            
            # Показываем, как это может помочь криптоаналитику
            st.warning("""
            **Криптоаналитик теперь знает:**
            - P1 ⊕ P2 (разность двух открытых текстов)
            - Может использовать частотный анализ
            - Может искать известные слова и паттерны
            - Может применить лингвистический анализ
            """)

# Для обратной совместимости
class OneTimePadCipher(OneTimePadModule):
    pass
