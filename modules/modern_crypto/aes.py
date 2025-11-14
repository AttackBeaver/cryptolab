from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import numpy as np
import secrets
import binascii
from typing import List, Tuple
import struct

class AESModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "AES"
        self.description = "Advanced Encryption Standard - современный симметричный блочный шифр"
        self.complexity = "advanced"
        self.category = "modern"
        self.icon = ""
        self.order = 4
        
        # Константы AES
        self.SBOX = [
            0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
            0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
            0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
            0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
            0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
            0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
            0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
            0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
            0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
            0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
            0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
            0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
            0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
            0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
            0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
        ]
        
        self.INV_SBOX = [
            0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
            0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
            0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
            0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
            0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
            0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
            0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
            0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
            0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
            0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
            0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
            0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
            0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
            0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
            0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
            0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
        ]
        
        self.RCON = [
            0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
        ]
    
    def render(self):
        st.title("🛡️ AES (Advanced Encryption Standard)")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **AES (Advanced Encryption Standard)** - симметричный блочный шифр, выбранный NIST в 2001 году как преемник DES.
            
            **Основные характеристики:**
            - **Размер блока:** 128 бит (16 байт)
            - **Размеры ключа:** 128, 192, 256 бит
            - **Количество раундов:** 10 (128-бит ключ), 12 (192-бит), 14 (256-бит)
            - **Структура:** Подстановочно-перестановочная сеть (SPN)
            
            **Историческое значение:**
            - Победитель конкурса NIST (Rijndael алгоритм)
            - Мировой стандарт шифрования с 2001 года
            - Используется в SSL/TLS, VPN, Wi-Fi, и многих других протоколах
            - Открытый и тщательно изученный алгоритм
            
            **Принцип работы:**
            1. **Key Expansion** - генерация раундовых ключей
            2. **Initial Round** - AddRoundKey
            3. **Main Rounds** (9/11/13 раундов):
               - SubBytes (S-блоки)
               - ShiftRows (сдвиг строк)
               - MixColumns (смешивание столбцов)
               - AddRoundKey (XOR с ключом)
            4. **Final Round** (без MixColumns)
            
            **Безопасность:**
            - Устойчив ко всем известным атакам
            - Эффективный против дифференциального и линейного криптоанализа
            - Нет известных практических атак лучше полного перебора
            - Рекомендован для защиты информации до уровня "Совершенно секретно"
            """)
        
        st.markdown("---")
        
        # Выбор режима работы
        mode = st.radio(
            "Режим работы:",
            ["🔐 Шифрование/Дешифрование", "🎯 Визуализация раундов", "🔧 Генерация ключей", "📊 Сравнение с DES/3DES"],
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
        """Отрисовывает секцию шифрования/дешифрования"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔒 Шифрование AES")
            self.render_aes_encryption()
        
        with col2:
            st.subheader("🔓 Дешифрование AES")
            self.render_aes_decryption()
    
    def render_aes_encryption(self):
        """Отрисовывает интерфейс шифрования AES"""
        plaintext = st.text_area(
            "Открытый текст (16 символов):",
            "Hello AES World!!",
            height=100,
            key="aes_enc_text",
            help="AES работает с блоками по 128 бит (16 символов)"
        )
        
        # Выбор размера ключа
        key_size = st.radio(
            "Размер ключа:",
            ["128 бит", "192 бита", "256 бит"],
            key="aes_key_size",
            horizontal=True
        )
        
        # Генерация ключа
        col_key, col_gen = st.columns([3, 1])
        
        with col_key:
            if 'aes_enc_key' not in st.session_state:
                st.session_state.aes_enc_key = "2b7e151628aed2a6abf7158809cf4f3c"
            
            key_length = 32 if key_size == "128 бит" else 48 if key_size == "192 бита" else 64
            key = st.text_input(
                f"Ключ ({key_length} hex символов):",
                st.session_state.aes_enc_key[:key_length],
                key="aes_enc_key_input"
            )
        
        with col_gen:
            st.write("")  # Отступ
            st.write("")  # Отступ
            if st.button("🎲 Ключ", key="gen_aes_key", use_container_width=True):
                key_length_bytes = 16 if key_size == "128 бит" else 24 if key_size == "192 бита" else 32
                random_key = secrets.token_hex(key_length_bytes).upper()
                st.session_state.aes_enc_key = random_key
                st.rerun()
        
        if st.button("Зашифровать AES", key="aes_enc_btn", use_container_width=True):
            if plaintext and key:
                try:
                    # Проверяем длину текста
                    if len(plaintext) != 16:
                        st.warning("AES работает с блоками по 16 символов. Будут использованы первые 16 символов.")
                        plaintext = plaintext[:16].ljust(16, ' ')
                    
                    # Проверяем ключ
                    expected_length = 32 if key_size == "128 бит" else 48 if key_size == "192 бита" else 64
                    if len(key) != expected_length:
                        st.error(f"Ключ должен содержать ровно {expected_length} шестнадцатеричных символов")
                        return
                    
                    # Шифруем
                    ciphertext = self.aes_encrypt(plaintext, key, key_size)
                    
                    st.success("Зашифрованный текст (hex):")
                    st.code(ciphertext, language="text")
                    
                    # Показываем детали
                    self.show_encryption_details(plaintext, key, ciphertext, key_size)
                    
                except Exception as e:
                    st.error(f"Ошибка шифрования: {e}")
            else:
                st.error("Введите текст и ключ")
    
    def render_aes_decryption(self):
        """Отрисовывает интерфейс дешифрования AES"""
        ciphertext = st.text_input(
            "Шифротекст (32 hex символа):",
            "3925841d02dc09fbdc118597196a0b32",
            key="aes_dec_text",
            help="128-битный шифротекст в шестнадцатеричном формате"
        )
        
        key_size = st.radio(
            "Размер ключа:",
            ["128 бит", "192 бита", "256 бит"],
            key="aes_dec_key_size",
            horizontal=True
        )
        
        key_length = 32 if key_size == "128 бит" else 48 if key_size == "192 бита" else 64
        key = st.text_input(
            f"Ключ ({key_length} hex символов):",
            "2b7e151628aed2a6abf7158809cf4f3c",
            key="aes_dec_key"
        )
        
        if st.button("Дешифровать AES", key="aes_dec_btn", use_container_width=True):
            if ciphertext and key:
                try:
                    # Проверяем длину шифротекста
                    if len(ciphertext) != 32:
                        st.error("Шифротекст должен содержать ровно 32 шестнадцатеричных символа")
                        return
                    
                    # Проверяем ключ
                    expected_length = 32 if key_size == "128 бит" else 48 if key_size == "192 бита" else 64
                    if len(key) != expected_length:
                        st.error(f"Ключ должен содержать ровно {expected_length} шестнадцатеричных символов")
                        return
                    
                    # Дешифруем
                    plaintext = self.aes_decrypt(ciphertext, key, key_size)
                    
                    st.success("Дешифрованный текст:")
                    st.code(plaintext, language="text")
                    
                except Exception as e:
                    st.error(f"Ошибка дешифрования: {e}")
            else:
                st.error("Введите шифротекст и ключ")
    
    def render_round_visualization(self):
        """Отрисовывает визуализацию раундов AES"""
        st.subheader("🎯 Визуализация раундов AES")
        
        demo_text = st.text_input(
            "Текст для демонстрации (16 символов):",
            "Hello AES World!!",
            key="demo_aes_text"
        )
        
        demo_key = st.text_input(
            "Ключ для демонстрации (32 hex):",
            "2b7e151628aed2a6abf7158809cf4f3c",
            key="demo_aes_key"
        )
        
        key_size = st.selectbox(
            "Размер ключа:",
            ["128 бит", "192 бита", "256 бит"],
            key="demo_key_size"
        )
        
        if st.button("Показать раунды", key="demo_rounds_btn"):
            if demo_text and demo_key:
                try:
                    if len(demo_text) != 16:
                        demo_text = demo_text[:16].ljust(16, ' ')
                    
                    self.visualize_aes_rounds(demo_text, demo_key, key_size)
                    
                except Exception as e:
                    st.error(f"Ошибка визуализации: {e}")
            else:
                st.error("Введите текст и ключ")
    
    def render_key_generation(self):
        """Отрисовывает секцию генерации ключей"""
        st.subheader("🔧 Генерация раундовых ключей AES")
        
        key_size = st.radio(
            "Размер мастер-ключа:",
            ["128 бит", "192 бита", "256 бит"],
            key="key_gen_size",
            horizontal=True
        )
        
        master_key = st.text_input(
            "Мастер-ключ:",
            "2b7e151628aed2a6abf7158809cf4f3c",
            key="key_gen_input"
        )
        
        if st.button("Сгенерировать раундовые ключи", key="key_gen_btn"):
            if master_key:
                try:
                    key_bytes = len(master_key) // 2
                    if key_bytes not in [16, 24, 32]:
                        st.error("Некорректный размер ключа. Используйте 32, 48 или 64 hex символа.")
                        return
                    
                    round_keys = self.key_expansion(master_key, key_size)
                    
                    st.success("Сгенерированные раундовые ключи:")
                    
                    # Показываем таблицу ключей
                    keys_data = []
                    for i, key in enumerate(round_keys):
                        keys_data.append({
                            'Раунд': i,
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
        """Отрисовывает секцию сравнения"""
        st.subheader("📊 Сравнение AES с DES и 3DES")
        
        # Сравнительная таблица
        comparison_data = {
            'Параметр': [
                'Год стандартизации',
                'Размер блока',
                'Размеры ключа',
                'Количество раундов',
                'Структура',
                'Стойкость',
                'Скорость',
                'Статус'
            ],
            'DES': [
                '1977',
                '64 бита',
                '56 бит',
                '16',
                'Сеть Фейстеля',
                'Небезопасен',
                'Быстро',
                'Устарел'
            ],
            '3DES': [
                '1998',
                '64 бита',
                '112/168 бит',
                '48',
                'Сеть Фейстеля',
                'Условно безопасен',
                'Медленно',
                'Используется'
            ],
            'AES-128': [
                '2001',
                '128 бит',
                '128 бит',
                '10',
                'SP-сеть',
                'Безопасен',
                'Очень быстро',
                'Стандарт'
            ],
            'AES-256': [
                '2001',
                '128 бит',
                '256 бит',
                '14',
                'SP-сеть',
                'Очень безопасен',
                'Быстро',
                'Стандарт'
            ]
        }
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Дополнительная информация
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Преимущества AES:**
            - Больший размер блока (128 бит)
            - Переменный размер ключа
            - Эффективная реализация
            - Устойчивость к атакам
            - Открытый стандарт
            
            **Производительность:**
            - Аппаратное ускорение (AES-NI)
            - Быстрее чем 3DES
            - Эффективное использование памяти
            """)
        
        with col2:
            st.markdown("""
            **Безопасность:**
            - Нет известных практических атак
            - Устойчив к дифференциальному анализу
            - Устойчив к линейному анализу
            - Рекомендован для государственных секретов
            
            **Применение:**
            - SSL/TLS
            - VPN
            - Wi-Fi (WPA2)
            - Файловые системы
            - Базы данных
            """)
    
    # Основные функции AES
    
    def text_to_hex(self, text: str) -> str:
        """Преобразует текст в hex строку"""
        return text.encode('utf-8').hex()
    
    def hex_to_text(self, hex_string: str) -> str:
        """Преобразует hex строку в текст"""
        return bytes.fromhex(hex_string).decode('utf-8', errors='ignore')
    
    def bytes_to_matrix(self, data: bytes) -> List[List[int]]:
        """Преобразует байты в матрицу состояния 4x4"""
        return [list(data[i:i+4]) for i in range(0, len(data), 4)]
    
    def matrix_to_bytes(self, matrix: List[List[int]]) -> bytes:
        """Преобразует матрицу состояния в байты"""
        return bytes([item for row in matrix for item in row])
    
    def sub_bytes(self, state: List[List[int]]) -> List[List[int]]:
        """Операция SubBytes (S-блоки)"""
        return [[self.SBOX[b] for b in row] for row in state]
    
    def inv_sub_bytes(self, state: List[List[int]]) -> List[List[int]]:
        """Обратная операция SubBytes"""
        return [[self.INV_SBOX[b] for b in row] for row in state]
    
    def shift_rows(self, state: List[List[int]]) -> List[List[int]]:
        """Операция ShiftRows"""
        return [
            [state[0][0], state[1][1], state[2][2], state[3][3]],
            [state[1][0], state[2][1], state[3][2], state[0][3]],
            [state[2][0], state[3][1], state[0][2], state[1][3]],
            [state[3][0], state[0][1], state[1][2], state[2][3]]
        ]
    
    def inv_shift_rows(self, state: List[List[int]]) -> List[List[int]]:
        """Обратная операция ShiftRows"""
        return [
            [state[0][0], state[3][1], state[2][2], state[1][3]],
            [state[1][0], state[0][1], state[3][2], state[2][3]],
            [state[2][0], state[1][1], state[0][2], state[3][3]],
            [state[3][0], state[2][1], state[1][2], state[0][3]]
        ]
    
    def gmul(self, a: int, b: int) -> int:
        """Умножение в поле GF(2^8)"""
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            hi_bit_set = a & 0x80
            a <<= 1
            if hi_bit_set:
                a ^= 0x1b
            b >>= 1
        return p & 0xff
    
    def mix_columns(self, state: List[List[int]]) -> List[List[int]]:
        """Операция MixColumns"""
        new_state = [[0]*4 for _ in range(4)]
        for i in range(4):
            new_state[0][i] = self.gmul(0x02, state[0][i]) ^ self.gmul(0x03, state[1][i]) ^ state[2][i] ^ state[3][i]
            new_state[1][i] = state[0][i] ^ self.gmul(0x02, state[1][i]) ^ self.gmul(0x03, state[2][i]) ^ state[3][i]
            new_state[2][i] = state[0][i] ^ state[1][i] ^ self.gmul(0x02, state[2][i]) ^ self.gmul(0x03, state[3][i])
            new_state[3][i] = self.gmul(0x03, state[0][i]) ^ state[1][i] ^ state[2][i] ^ self.gmul(0x02, state[3][i])
        return new_state
    
    def inv_mix_columns(self, state: List[List[int]]) -> List[List[int]]:
        """Обратная операция MixColumns"""
        new_state = [[0]*4 for _ in range(4)]
        for i in range(4):
            new_state[0][i] = self.gmul(0x0e, state[0][i]) ^ self.gmul(0x0b, state[1][i]) ^ self.gmul(0x0d, state[2][i]) ^ self.gmul(0x09, state[3][i])
            new_state[1][i] = self.gmul(0x09, state[0][i]) ^ self.gmul(0x0e, state[1][i]) ^ self.gmul(0x0b, state[2][i]) ^ self.gmul(0x0d, state[3][i])
            new_state[2][i] = self.gmul(0x0d, state[0][i]) ^ self.gmul(0x09, state[1][i]) ^ self.gmul(0x0e, state[2][i]) ^ self.gmul(0x0b, state[3][i])
            new_state[3][i] = self.gmul(0x0b, state[0][i]) ^ self.gmul(0x0d, state[1][i]) ^ self.gmul(0x09, state[2][i]) ^ self.gmul(0x0e, state[3][i])
        return new_state
    
    def add_round_key(self, state: List[List[int]], round_key: List[List[int]]) -> List[List[int]]:
        """Операция AddRoundKey"""
        return [[state[i][j] ^ round_key[i][j] for j in range(4)] for i in range(4)]
    
    def key_expansion(self, key_hex: str, key_size: str) -> List[str]:
        """Генерация раундовых ключей"""
        # Упрощенная реализация для демонстрации
        key_bytes = bytes.fromhex(key_hex)
        nk = len(key_bytes) // 4  # Number of 32-bit words in initial key
        
        if key_size == "128 бит":
            nr = 10
        elif key_size == "192 бита":
            nr = 12
        else:  # 256 бит
            nr = 14
        
        round_keys = []
        
        # Первый раундовый ключ - исходный ключ
        round_keys.append(key_hex)
        
        # Генерируем остальные ключи (упрощенно)
        for i in range(1, nr + 1):
            # В реальной реализации здесь был бы полный алгоритм Key Expansion
            # Для демонстрации используем упрощенную версию
            prev_key = bytes.fromhex(round_keys[-1])
            new_key = bytes([(b + i) % 256 for b in prev_key])
            round_keys.append(new_key.hex())
        
        return round_keys
    
    def aes_encrypt(self, plaintext: str, key_hex: str, key_size: str) -> str:
        """Шифрует текст с помощью AES"""
        # Преобразуем текст и ключ в байты
        plaintext_bytes = plaintext.encode('utf-8')
        key_bytes = bytes.fromhex(key_hex)
        
        # Определяем количество раундов
        if key_size == "128 бит":
            nr = 10
        elif key_size == "192 бита":
            nr = 12
        else:  # 256 бит
            nr = 14
        
        # Генерируем раундовые ключи
        round_keys_hex = self.key_expansion(key_hex, key_size)
        round_keys = [self.bytes_to_matrix(bytes.fromhex(rk)) for rk in round_keys_hex]
        
        # Преобразуем текст в матрицу состояния
        state = self.bytes_to_matrix(plaintext_bytes)
        
        # Начальный раунд - AddRoundKey
        state = self.add_round_key(state, round_keys[0])
        
        # Основные раунды
        for i in range(1, nr):
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            state = self.add_round_key(state, round_keys[i])
        
        # Финальный раунд (без MixColumns)
        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        state = self.add_round_key(state, round_keys[nr])
        
        # Преобразуем обратно в байты и hex
        ciphertext_bytes = self.matrix_to_bytes(state)
        return ciphertext_bytes.hex()
    
    def aes_decrypt(self, ciphertext_hex: str, key_hex: str, key_size: str) -> str:
        """Дешифрует текст с помощью AES"""
        # Преобразуем шифротекст и ключ в байты
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
        key_bytes = bytes.fromhex(key_hex)
        
        # Определяем количество раундов
        if key_size == "128 бит":
            nr = 10
        elif key_size == "192 бита":
            nr = 12
        else:  # 256 бит
            nr = 14
        
        # Генерируем раундовые ключи
        round_keys_hex = self.key_expansion(key_hex, key_size)
        round_keys = [self.bytes_to_matrix(bytes.fromhex(rk)) for rk in round_keys_hex]
        
        # Преобразуем шифротекст в матрицу состояния
        state = self.bytes_to_matrix(ciphertext_bytes)
        
        # Финальный раунд в обратном порядке
        state = self.add_round_key(state, round_keys[nr])
        state = self.inv_shift_rows(state)
        state = self.inv_sub_bytes(state)
        
        # Основные раунды в обратном порядке
        for i in range(nr-1, 0, -1):
            state = self.add_round_key(state, round_keys[i])
            state = self.inv_mix_columns(state)
            state = self.inv_shift_rows(state)
            state = self.inv_sub_bytes(state)
        
        # Начальный раунд
        state = self.add_round_key(state, round_keys[0])
        
        # Преобразуем обратно в текст
        plaintext_bytes = self.matrix_to_bytes(state)
        return plaintext_bytes.decode('utf-8', errors='ignore')
    
    def show_encryption_details(self, plaintext: str, key: str, ciphertext: str, key_size: str):
        """Показывает детали шифрования"""
        st.markdown("**🔍 Детали процесса AES:**")
        
        # Определяем количество раундов
        if key_size == "128 бит":
            nr = 10
        elif key_size == "192 бита":
            nr = 12
        else:  # 256 бит
            nr = 14
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Размер блока", "128 бит")
        with col2:
            st.metric("Размер ключа", key_size)
        with col3:
            st.metric("Количество раундов", nr)
        with col4:
            st.metric("Структура", "SP-сеть")
        
        # Показываем схему шифрования
        st.markdown("**Схема шифрования:**")
        st.markdown("""
        ```
        Plaintext
            ↓
        AddRoundKey (начальный ключ)
            ↓
        [Повторяется 9/11/13 раз]:
            SubBytes → ShiftRows → MixColumns → AddRoundKey
            ↓
        Финальный раунд:
            SubBytes → ShiftRows → AddRoundKey
            ↓
        Ciphertext
        ```
        """)
    
    def visualize_aes_rounds(self, text: str, key: str, key_size: str):
        """Визуализирует процесс раундов AES"""
        st.markdown("### 🔄 Процесс раундов AES")
        
        # Определяем количество раундов
        if key_size == "128 бит":
            nr = 10
        elif key_size == "192 бита":
            nr = 12
        else:  # 256 бит
            nr = 14
        
        # Преобразуем текст и ключ
        text_bytes = text.encode('utf-8')
        key_bytes = bytes.fromhex(key)
        
        # Генерируем раундовые ключи
        round_keys_hex = self.key_expansion(key, key_size)
        
        st.markdown("**Начальное состояние:**")
        state = self.bytes_to_matrix(text_bytes)
        self.display_state_matrix(state, "Исходный текст")
        
        # Начальный раунд
        st.markdown("**Раунд 0 - AddRoundKey:**")
        state = self.add_round_key(state, self.bytes_to_matrix(key_bytes))
        self.display_state_matrix(state, "После AddRoundKey")
        
        # Основные раунды
        for i in range(1, nr):
            st.markdown(f"**Раунд {i}:**")
            
            st.markdown("*SubBytes:*")
            state = self.sub_bytes(state)
            self.display_state_matrix(state, "После SubBytes")
            
            st.markdown("*ShiftRows:*")
            state = self.shift_rows(state)
            self.display_state_matrix(state, "После ShiftRows")
            
            st.markdown("*MixColumns:*")
            state = self.mix_columns(state)
            self.display_state_matrix(state, "После MixColumns")
            
            st.markdown(f"*AddRoundKey (ключ раунда {i}):*")
            state = self.add_round_key(state, self.bytes_to_matrix(bytes.fromhex(round_keys_hex[i])))
            self.display_state_matrix(state, "После AddRoundKey")
            
            st.progress(i / nr)
        
        # Финальный раунд
        st.markdown(f"**Раунд {nr} (финальный):**")
        
        st.markdown("*SubBytes:*")
        state = self.sub_bytes(state)
        self.display_state_matrix(state, "После SubBytes")
        
        st.markdown("*ShiftRows:*")
        state = self.shift_rows(state)
        self.display_state_matrix(state, "После ShiftRows")
        
        st.markdown(f"*AddRoundKey (ключ раунда {nr}):*")
        state = self.add_round_key(state, self.bytes_to_matrix(bytes.fromhex(round_keys_hex[nr])))
        self.display_state_matrix(state, "Финальное состояние")
        
        # Показываем результат
        ciphertext_bytes = self.matrix_to_bytes(state)
        st.success(f"**Итоговый шифротекст:** {ciphertext_bytes.hex()}")
    
    def display_state_matrix(self, state: List[List[int]], title: str):
        """Отображает матрицу состояния"""
        st.markdown(f"**{title}:**")
        
        # Создаем DataFrame для красивого отображения
        df = pd.DataFrame(state)
        df.columns = ['Col 0', 'Col 1', 'Col 2', 'Col 3']
        df.index = ['Row 0', 'Row 1', 'Row 2', 'Row 3']
        
        # Форматируем значения как hex
        styled_df = df.map(lambda x: f"{x:02x}")
        st.dataframe(styled_df, use_container_width=True)

# Для обратной совместимости
class AESCipher(AESModule):
    pass
