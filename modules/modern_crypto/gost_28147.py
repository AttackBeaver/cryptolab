from modules.base_module import CryptoModule
import streamlit as st
import secrets
import struct
from typing import List, Tuple, Dict
import pandas as pd
import numpy as np
import binascii
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend

class GOST28147Module(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "ГОСТ 28147-89"
        self.description = "Советский и российский стандарт симметричного шифрования"
        self.category = "modern"
        self.icon = ""
        self.order = 9
        
        # Стандартная таблица замен (S-блоки)
        self.s_boxes = [
            # S1
            [
                4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3,
                14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9
            ],
            # S2
            [
                5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11,
                7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3
            ],
            # S3
            [
                8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7,
                1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2
            ],
            # S4
            [
                7, 14, 12, 2, 1, 13, 10, 0, 6, 9, 8, 4, 5, 15, 3, 11,
                13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9
            ],
            # S5
            [
                2, 11, 15, 5, 13, 4, 6, 9, 8, 10, 3, 12, 7, 0, 1, 14,
                8, 13, 11, 0, 4, 10, 7, 1, 15, 12, 6, 5, 9, 3, 2, 14
            ],
            # S6
            [
                1, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 15,
                10, 6, 3, 15, 13, 8, 4, 14, 7, 11, 12, 0, 5, 2, 9, 1
            ],
            # S7
            [
                15, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 14, 13, 11,
                3, 0, 6, 13, 9, 14, 15, 8, 5, 12, 11, 7, 10, 1, 4, 2
            ],
            # S8
            [
                11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 15, 14, 13, 12,
                12, 9, 6, 3, 0, 13, 10, 7, 4, 1, 14, 11, 8, 5, 2, 15
            ]
        ]
        
        # Режимы работы ГОСТ
        self.modes = {
            "ECB": "Простая замена",
            "CFB": "Обратная связь по шифротексту", 
            "CBC": "Сцепление блоков шифротекста",
            "OFB": "Обратная связь по выходу"
        }

    def render(self):
        st.title("🛡️ ГОСТ 28147-89")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **ГОСТ 28147-89** - советский и российский стандарт симметричного шифрования, также известный как «Магма».
            
            **Основные характеристики:**
            - **Тип алгоритма**: Симметричный блочный шифр
            - **Размер блока**: 64 бита
            - **Размер ключа**: 256 бит (32 байта)
            - **Количество раундов**: 32
            - **Структура**: Сеть Фейстеля
            
            **Историческое значение:**
            - Разработан в СССР в 1989 году
            - Используется в российских государственных органах
            - Стандарт для защиты информации в РФ
            - Известен высокой стойкостью к криптоанализу
            
            **Особенности алгоритма:**
            - 8 различных S-блоков (таблиц замен)
            - Сложная схема выработки ключей
            - 32 раунда преобразований
            - Режимы работы: ECB, CFB, CBC, OFB
            
            **Стойкость:**
            - Устойчив к дифференциальному и линейному криптоанализу
            - Нет известных практических атак
            - Рекомендован для защиты государственной тайны
            """)

        st.markdown("---")
        
        # Выбор режима работы
        mode = st.radio(
            "Режим работы:",
            ["🔐 Шифрование/Дешифрование", "🎯 Визуализация раундов", "🔧 Генерация ключей", "📊 Сравнение с AES"],
            horizontal=True
        )

        if mode == "🔐 Шифрование/Дешифрование":
            self.render_encryption_section()
        elif mode == "🎯 Визуализация раундов":
            self.render_round_visualization()
        elif mode == "🔧 Генерация ключей":
            self.render_key_generation()
        else:
            self.render_comparison_section()

    def render_encryption_section(self):
        """Секция шифрования/дешифрования"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔒 Шифрование ГОСТ")
            self.render_gost_encryption()
        
        with col2:
            st.subheader("🔓 Дешифрование ГОСТ")
            self.render_gost_decryption()

    def render_gost_encryption(self):
        """Интерфейс шифрования ГОСТ"""
        plaintext = st.text_area(
            "Открытый текст:",
            "Hello GOST!",
            height=100,
            key="gost_enc_text"
        )
        
        # Выбор режима
        mode = st.selectbox(
            "Режим работы:",
            list(self.modes.keys()),
            key="gost_enc_mode",
            format_func=lambda x: f"{x} - {self.modes[x]}"
        )
        
        # Генерация ключа
        col_key, col_gen = st.columns([3, 1])
        
        with col_key:
            if 'gost_enc_key' not in st.session_state:
                st.session_state.gost_enc_key = secrets.token_hex(32)
            
            key = st.text_input(
                "Ключ (64 hex символа):",
                st.session_state.gost_enc_key,
                key="gost_enc_key_input"
            )
        
        with col_gen:
            st.write("")  # Отступ
            st.write("")  # Отступ
            if st.button("🎲 Ключ", key="gen_gost_key", use_container_width=True):
                st.session_state.gost_enc_key = secrets.token_hex(32)
                st.rerun()
        
        # Вектор инициализации для некоторых режимов
        if mode in ["CFB", "CBC", "OFB"]:
            col_iv, col_iv_gen = st.columns([3, 1])
            with col_iv:
                if 'gost_enc_iv' not in st.session_state:
                    st.session_state.gost_enc_iv = secrets.token_hex(16)
                
                iv = st.text_input(
                    "IV (32 hex символа):",
                    st.session_state.gost_enc_iv,
                    key="gost_enc_iv_input"
                )
            
            with col_iv_gen:
                st.write("")
                st.write("")
                if st.button("🎲 IV", key="gen_gost_iv", use_container_width=True):
                    st.session_state.gost_enc_iv = secrets.token_hex(16)
                    st.rerun()
        else:
            iv = "0" * 32  # Для ECB не используется

        if st.button("Зашифровать ГОСТ", key="gost_enc_btn", use_container_width=True):
            if plaintext and key:
                try:
                    # Проверяем ключ
                    if len(key) != 64:
                        st.error("Ключ должен содержать ровно 64 шестнадцатеричных символа")
                        return
                    
                    # Шифруем
                    ciphertext = self.gost_encrypt(plaintext, key, mode, iv if 'iv' in locals() else None)
                    
                    st.success("✅ Зашифрованный текст (hex):")
                    st.code(ciphertext, language="text")
                    
                    # Показываем детали
                    self.show_encryption_details(plaintext, key, ciphertext, mode)
                    
                except Exception as e:
                    st.error(f"❌ Ошибка шифрования: {e}")
            else:
                st.error("⚠️ Введите текст и ключ")

    def render_gost_decryption(self):
        """Интерфейс дешифрования ГОСТ"""
        ciphertext = st.text_input(
            "Шифротекст (hex):",
            "",
            key="gost_dec_text",
            placeholder="Введите hex-строку шифротекста"
        )
        
        mode = st.selectbox(
            "Режим работы:",
            list(self.modes.keys()),
            key="gost_dec_mode",
            format_func=lambda x: f"{x} - {self.modes[x]}"
        )
        
        key = st.text_input(
            "Ключ (64 hex символа):",
            key="gost_dec_key"
        )
        
        if mode in ["CFB", "CBC", "OFB"]:
            iv = st.text_input(
                "IV (32 hex символа):",
                key="gost_dec_iv"
            )
        else:
            iv = None

        if st.button("Дешифровать ГОСТ", key="gost_dec_btn", use_container_width=True):
            if ciphertext and key:
                try:
                    # Проверяем ключ
                    if len(key) != 64:
                        st.error("Ключ должен содержать 64 шестнадцатеричных символа")
                        return
                    
                    # Дешифруем
                    plaintext = self.gost_decrypt(ciphertext, key, mode, iv)
                    
                    st.success("✅ Дешифрованный текст:")
                    st.code(plaintext, language="text")
                    
                except Exception as e:
                    st.error(f"❌ Ошибка дешифрования: {e}")
            else:
                st.error("⚠️ Введите шифротекст и ключ")

    def render_round_visualization(self):
        """Визуализация раундов ГОСТ"""
        st.subheader("🎯 Визуализация раундов ГОСТ 28147-89")
        
        demo_text = st.text_input(
            "Текст для демонстрации (8 символов):",
            "GOSTDEMO",
            key="demo_gost_text"
        )
        
        demo_key = st.text_input(
            "Ключ для демонстрации (64 hex):",
            "0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF",
            key="demo_gost_key"
        )
        
        if st.button("Показать раунды", key="demo_rounds_btn"):
            if demo_text and demo_key:
                try:
                    if len(demo_text) != 8:
                        demo_text = demo_text[:8].ljust(8, ' ')
                    
                    self.visualize_gost_rounds(demo_text, demo_key)
                    
                except Exception as e:
                    st.error(f"Ошибка визуализации: {e}")
            else:
                st.error("Заполните все поля")

    def render_key_generation(self):
        """Генерация ключей"""
        st.subheader("🔧 Генерация ключей ГОСТ")
        
        # Показываем S-блоки
        st.markdown("### 🎲 Таблицы замен (S-блоки)")
        self.display_s_boxes()
        
        # Генерация раундовых ключей
        st.markdown("### 🔑 Генерация раундовых ключей")
        
        master_key = st.text_input(
            "Мастер-ключ (64 hex):",
            "0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF",
            key="key_gen_input"
        )
        
        if st.button("Сгенерировать раундовые ключи", key="key_gen_btn"):
            if master_key:
                try:
                    if len(master_key) != 64:
                        st.error("Ключ должен содержать 64 шестнадцатеричных символа")
                        return
                    
                    round_keys = self.key_expansion(master_key)
                    
                    st.success("✅ Сгенерированные раундовые ключи:")
                    
                    # Показываем таблицу ключей
                    keys_data = []
                    for i, key in enumerate(round_keys):
                        keys_data.append({
                            'Раунд': i + 1,
                            'Ключ (hex)': key,
                            'Длина': f"{len(key)//2} байт"
                        })
                    
                    df_keys = pd.DataFrame(keys_data)
                    st.dataframe(df_keys, use_container_width=True, height=400)
                    
                except Exception as e:
                    st.error(f"Ошибка генерации ключей: {e}")
            else:
                st.error("Введите мастер-ключ")

    def render_comparison_section(self):
        """Сравнение с AES"""
        st.subheader("📊 Сравнение ГОСТ 28147-89 с AES")
        
        # Сравнительная таблица
        comparison_data = {
            'Параметр': [
                'Страна происхождения',
                'Год стандартизации',
                'Размер блока',
                'Размер ключа',
                'Количество раундов',
                'Структура',
                'S-блоки',
                'Стойкость',
                'Применение'
            ],
            'ГОСТ 28147-89': [
                'СССР/Россия',
                '1989',
                '64 бита',
                '256 бит',
                '32',
                'Сеть Фейстеля',
                '8 различных',
                'Очень высокая',
                'Гос. органы РФ'
            ],
            'AES-256': [
                'США/Бельгия',
                '2001',
                '128 бит',
                '256 бит',
                '14',
                'SP-сеть',
                '1 (фиксированный)',
                'Очень высокая',
                'Международный'
            ]
        }

        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Дополнительная информация
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Преимущества ГОСТ:**
            - Большее количество раундов (32 vs 14)
            - 8 различных S-блоков
            - Простая аппаратная реализация
            - Проверенная стойкость
            - Отечественная разработка
            
            **Особенности:**
            - Использует сеть Фейстеля
            - Меньший размер блока (64 бита)
            - Сложная схема ключей
            - Разные режимы работы
            """)
        
        with col2:
            st.markdown("""
            **Преимущества AES:**
            - Больший размер блока (128 бит)
            - Международный стандарт
            - Аппаратное ускорение (AES-NI)
            - Широкая поддержка
            - Высокая производительность
            
            **Применение ГОСТ:**
            - Банковская сфера России
            - Государственные органы
            - Защита гостайны
            - Криптографические устройства
            """)

    def display_s_boxes(self):
        """Отображает таблицы замен (S-блоки)"""
        for s_box_num, s_box in enumerate(self.s_boxes, 1):
            with st.expander(f"S-блок {s_box_num}"):
                # Создаем таблицу 16x2
                data = []
                for i in range(16):
                    data.append({
                        'Вход': f"{i:01X}",
                        'Выход 1': f"{s_box[i]:01X}",
                        'Вход': f"{(i+16):01X}",
                        'Выход 2': f"{s_box[i+16]:01X}"
                    })
                
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True, hide_index=True)

    def gost_encrypt(self, plaintext: str, key_hex: str, mode: str, iv: str = None) -> str:
        """Шифрует текст с помощью ГОСТ 28147-89"""
        try:
            # Преобразуем в байты
            plaintext_bytes = plaintext.encode('utf-8')
            key_bytes = bytes.fromhex(key_hex)
            
            if iv:
                iv_bytes = bytes.fromhex(iv)
            else:
                iv_bytes = b'\x00' * 8  # По умолчанию нулевой IV
            
            # Дополняем данные до размера блока (8 байт)
            block_size = 8
            padded_data = self.pad_data(plaintext_bytes, block_size)
            
            # Шифруем в зависимости от режима
            if mode == "ECB":
                ciphertext = self.ecb_encrypt(padded_data, key_bytes)
            elif mode == "CBC":
                ciphertext = self.cbc_encrypt(padded_data, key_bytes, iv_bytes)
            elif mode == "CFB":
                ciphertext = self.cfb_encrypt(padded_data, key_bytes, iv_bytes)
            elif mode == "OFB":
                ciphertext = self.ofb_encrypt(padded_data, key_bytes, iv_bytes)
            else:
                raise ValueError(f"Неизвестный режим: {mode}")
            
            return ciphertext.hex()
            
        except Exception as e:
            raise Exception(f"Ошибка шифрования ГОСТ: {e}")

    def gost_decrypt(self, ciphertext_hex: str, key_hex: str, mode: str, iv: str = None) -> str:
        """Дешифрует текст с помощью ГОСТ 28147-89"""
        try:
            # Преобразуем в байты
            ciphertext_bytes = bytes.fromhex(ciphertext_hex)
            key_bytes = bytes.fromhex(key_hex)
            
            if iv:
                iv_bytes = bytes.fromhex(iv)
            else:
                iv_bytes = b'\x00' * 8
            
            # Дешифруем в зависимости от режима
            if mode == "ECB":
                decrypted = self.ecb_decrypt(ciphertext_bytes, key_bytes)
            elif mode == "CBC":
                decrypted = self.cbc_decrypt(ciphertext_bytes, key_bytes, iv_bytes)
            elif mode == "CFB":
                decrypted = self.cfb_decrypt(ciphertext_bytes, key_bytes, iv_bytes)
            elif mode == "OFB":
                decrypted = self.ofb_decrypt(ciphertext_bytes, key_bytes, iv_bytes)
            else:
                raise ValueError(f"Неизвестный режим: {mode}")
            
            # Убираем дополнение
            plaintext_bytes = self.unpad_data(decrypted)
            
            return plaintext_bytes.decode('utf-8')
            
        except Exception as e:
            raise Exception(f"Ошибка дешифрования ГОСТ: {e}")

    def pad_data(self, data: bytes, block_size: int) -> bytes:
        """Дополнение данных до размера блока"""
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def unpad_data(self, data: bytes) -> bytes:
        """Удаление дополнения"""
        padding_length = data[-1]
        return data[:-padding_length]

    # Основные функции ГОСТ

    def key_expansion(self, key_hex: str) -> List[str]:
        """Генерация раундовых ключей"""
        key_bytes = bytes.fromhex(key_hex)
        round_keys = []
        
        # Делим 256-битный ключ на 8 32-битных подключей
        subkeys = [key_bytes[i:i+4] for i in range(0, 32, 4)]
        
        # Генерируем ключи для 32 раундов
        for round_num in range(32):
            if round_num < 24:
                key_index = round_num % 8
            else:
                key_index = 7 - (round_num % 8)
            
            round_keys.append(subkeys[key_index].hex())
        
        return round_keys

    def feistel_function(self, data: int, key: int) -> int:
        """Функция Фейстеля для одного раунда"""
        # Сложение с ключом по модулю 2^32
        temp = (data + key) & 0xFFFFFFFF
        
        # Применение S-блоков
        result = 0
        for i in range(8):
            # Берем 4 бита
            s_box_input = (temp >> (4 * i)) & 0xF
            # Применяем S-блок
            s_box_output = self.s_boxes[i][s_box_input]
            # Добавляем к результату
            result |= (s_box_output << (4 * i))
        
        # Циклический сдвиг на 11 бит влево
        result = ((result << 11) | (result >> 21)) & 0xFFFFFFFF
        
        return result

    def gost_round(self, left: int, right: int, round_key: int) -> Tuple[int, int]:
        """Один раунд ГОСТ"""
        new_right = left ^ self.feistel_function(right, round_key)
        return right, new_right

    def encrypt_block(self, block: bytes, key_hex: str) -> bytes:
        """Шифрует один блок ГОСТ"""
        # Преобразуем блок в два 32-битных числа
        left, right = struct.unpack('<II', block)
        
        # Генерируем раундовые ключи
        round_keys_hex = self.key_expansion(key_hex)
        round_keys = [int(key, 16) for key in round_keys_hex]
        
        # 32 раунда преобразований
        for i in range(32):
            left, right = self.gost_round(left, right, round_keys[i])
        
        # Финальная перестановка
        return struct.pack('<II', right, left)

    def decrypt_block(self, block: bytes, key_hex: str) -> bytes:
        """Дешифрует один блок ГОСТ"""
        # Преобразуем блок в два 32-битных числа
        left, right = struct.unpack('<II', block)
        
        # Генерируем раундовые ключи (в обратном порядке для дешифрования)
        round_keys_hex = self.key_expansion(key_hex)
        round_keys = [int(key, 16) for key in round_keys_hex[::-1]]
        
        # 32 раунда преобразований
        for i in range(32):
            left, right = self.gost_round(left, right, round_keys[i])
        
        # Финальная перестановка
        return struct.pack('<II', right, left)

    # Режимы работы

    def ecb_encrypt(self, data: bytes, key: bytes) -> bytes:
        """Режим ECB"""
        result = b''
        key_hex = key.hex()
        
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            encrypted_block = self.encrypt_block(block, key_hex)
            result += encrypted_block
        
        return result

    def ecb_decrypt(self, data: bytes, key: bytes) -> bytes:
        """Режим ECB (дешифрование)"""
        result = b''
        key_hex = key.hex()
        
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            decrypted_block = self.decrypt_block(block, key_hex)
            result += decrypted_block
        
        return result

    def cbc_encrypt(self, data: bytes, key: bytes, iv: bytes) -> bytes:
        """Режим CBC"""
        result = b''
        key_hex = key.hex()
        prev_block = iv
        
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            # XOR с предыдущим блоком
            block = bytes(a ^ b for a, b in zip(block, prev_block))
            encrypted_block = self.encrypt_block(block, key_hex)
            result += encrypted_block
            prev_block = encrypted_block
        
        return result

    def cbc_decrypt(self, data: bytes, key: bytes, iv: bytes) -> bytes:
        """Режим CBC (дешифрование)"""
        result = b''
        key_hex = key.hex()
        prev_block = iv
        
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            decrypted_block = self.decrypt_block(block, key_hex)
            # XOR с предыдущим блоком
            decrypted_block = bytes(a ^ b for a, b in zip(decrypted_block, prev_block))
            result += decrypted_block
            prev_block = block
        
        return result

    def cfb_encrypt(self, data: bytes, key: bytes, iv: bytes) -> bytes:
        """Режим CFB"""
        result = b''
        key_hex = key.hex()
        shift_register = iv
        
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            # Шифруем регистр сдвига
            encrypted_register = self.encrypt_block(shift_register, key_hex)
            # XOR с открытым текстом
            cipher_block = bytes(a ^ b for a, b in zip(block, encrypted_register))
            result += cipher_block
            # Обновляем регистр сдвига
            shift_register = cipher_block
        
        return result

    def cfb_decrypt(self, data: bytes, key: bytes, iv: bytes) -> bytes:
        """Режим CFB (дешифрование)"""
        result = b''
        key_hex = key.hex()
        shift_register = iv
        
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            # Шифруем регистр сдвига
            encrypted_register = self.encrypt_block(shift_register, key_hex)
            # XOR с шифротекстом
            plain_block = bytes(a ^ b for a, b in zip(block, encrypted_register))
            result += plain_block
            # Обновляем регистр сдвига
            shift_register = block
        
        return result

    def ofb_encrypt(self, data: bytes, key: bytes, iv: bytes) -> bytes:
        """Режим OFB"""
        result = b''
        key_hex = key.hex()
        shift_register = iv
        
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            # Шифруем регистр сдвига
            encrypted_register = self.encrypt_block(shift_register, key_hex)
            # XOR с открытым текстом
            cipher_block = bytes(a ^ b for a, b in zip(block, encrypted_register))
            result += cipher_block
            # Обновляем регистр сдвига
            shift_register = encrypted_register
        
        return result

    def ofb_decrypt(self, data: bytes, key: bytes, iv: bytes) -> bytes:
        """Режим OFB (дешифрование) - идентичен шифрованию"""
        return self.ofb_encrypt(data, key, iv)

    def show_encryption_details(self, plaintext: str, key: str, ciphertext: str, mode: str):
        """Показывает детали шифрования"""
        st.markdown("---")
        st.markdown("**🔍 Детали процесса ГОСТ:**")

        # Информация о параметрах
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Алгоритм", "ГОСТ 28147-89")
        with col2:
            st.metric("Размер блока", "64 бита")
        with col3:
            st.metric("Режим", mode)
        with col4:
            st.metric("Раундов", "32")

        # Схема процесса
        st.markdown("**Схема базового раунда (сеть Фейстеля):**")
        st.markdown("""
        ```
        Lᵢ = Rᵢ₋₁
        Rᵢ = Lᵢ₋₁ ⊕ f(Rᵢ₋₁, Kᵢ)
        
        где f - функция Фейстеля:
        1. Сложение с ключом mod 2³²
        2. Замена через 8 S-блоков  
        3. Циклический сдвиг на 11 бит
        ```
        """)

    def visualize_gost_rounds(self, text: str, key: str):
        """Визуализирует процесс раундов ГОСТ"""
        st.markdown("### 🔄 Процесс раундов ГОСТ 28147-89")
        
        # Преобразуем текст в блок
        text_bytes = text.encode('utf-8')
        if len(text_bytes) < 8:
            text_bytes = text_bytes.ljust(8, b'\x00')
        elif len(text_bytes) > 8:
            text_bytes = text_bytes[:8]
        
        # Преобразуем блок в два 32-битных числа
        left, right = struct.unpack('<II', text_bytes)
        
        st.markdown(f"**Начальное состояние:**")
        st.markdown(f"L₀ = `{left:08X}`h, R₀ = `{right:08X}`h")
        
        # Генерируем раундовые ключи
        round_keys_hex = self.key_expansion(key)
        round_keys = [int(key, 16) for key in round_keys_hex]
        
        # Проходим через все 32 раунда
        for round_num in range(32):
            st.markdown(f"---")
            st.markdown(f"### 🔷 Раунд {round_num + 1}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**До раунда:**")
                st.text(f"L_{round_num} = {left:08X}h")
                st.text(f"R_{round_num} = {right:08X}h")
                st.text(f"K_{round_num + 1} = {round_keys[round_num]:08X}h")
                
                # Вычисляем функцию Фейстеля
                feistel_result = self.feistel_function(right, round_keys[round_num])
                st.text(f"f(R, K) = {feistel_result:08X}h")
            
            with col2:
                st.markdown("**После раунда:**")
                new_left = right
                new_right = left ^ feistel_result
                
                st.text(f"L_{round_num + 1} = R_{round_num} = {new_left:08X}h")
                st.text(f"R_{round_num + 1} = L_{round_num} ⊕ f(R, K)")
                st.text(f"R_{round_num + 1} = {new_right:08X}h")
                
                # Обновляем значения для следующего раунда
                left, right = new_left, new_right
            
            # Прогресс
            st.progress((round_num + 1) / 32)
        
        # Финальный результат
        st.markdown("---")
        st.markdown("**Финальная перестановка:**")
        final_block = struct.pack('<II', right, left)
        st.success(f"**Итоговый шифротекст:** {final_block.hex().upper()}")

# Для обратной совместимости
class GOST28147(GOST28147Module):
    pass