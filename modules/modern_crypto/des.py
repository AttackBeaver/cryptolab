from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import numpy as np
import binascii
import secrets
from typing import List, Tuple
import struct

class DESModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "DES"
        self.description = "Data Encryption Standard - классический блочный шифр"
        self.complexity = "advanced"
        self.category = "modern"
        self.icon = ""
        self.order = 2
        
        # Таблицы для DES
        self.IP = [
            58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7
        ]
        
        self.FP = [
            40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25
        ]
        
        self.PC1 = [
            57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4
        ]
        
        self.PC2 = [
            14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32
        ]
        
        self.E = [
            32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1
        ]
        
        self.P = [
            16, 7, 20, 21,
            29, 12, 28, 17,
            1, 15, 23, 26,
            5, 18, 31, 10,
            2, 8, 24, 14,
            32, 27, 3, 9,
            19, 13, 30, 6,
            22, 11, 4, 25
        ]
        
        self.S_BOX = [
            # S1
            [
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
            ],
            # S2
            [
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
                [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
                [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
                [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
            ],
            # S3
            [
                [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
                [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
                [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
            ],
            # S4
            [
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
                [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
                [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
            ],
            # S5
            [
                [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
                [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
                [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
                [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
            ],
            # S6
            [
                [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
                [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
                [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
                [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
            ],
            # S7
            [
                [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
                [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
                [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
                [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
            ],
            # S8
            [
                [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
                [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
                [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
                [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
            ]
        ]
        
        self.SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    
    def render(self):
        st.title("🔐 DES (Data Encryption Standard)")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **DES (Data Encryption Standard)** - симметричный блочный шифр, разработанный в 1970-х годах и ставший стандартом шифрования на decades.
            
            **Основные характеристики:**
            - **Размер блока:** 64 бита
            - **Размер ключа:** 56 бит (64 бита с паритетом)
            - **Количество раундов:** 16
            - **Структура:** Сеть Фейстеля
            
            **Историческое значение:**
            - Первый открытый криптографический стандарт
            - Широкое применение в банковской сфере и правительстве
            - Основа для понимания современных блочных шифров
            - Заменен на AES в 2001 году
            
            **Принцип работы:**
            1. **Начальная перестановка (IP)** - перестановка битов блока
            2. **16 раундов Фейстеля** - каждый раунд использует разные подключи
            3. **Функция Фейстеля (f)** - включает расширение, подстановку S-блоками и перестановку
            4. **Конечная перестановка (FP)** - обратная начальной
            
            **Безопасность:**
            - Уязвим к атаке полным перебором (2⁵⁶ операций)
            - Уязвим к дифференциальному и линейному криптоанализу
            - Современные вычисления позволяют взломать DES за часы
            """)
        
        st.markdown("---")
        
        # Выбор режима работы
        mode = st.radio(
            "Режим работы:",
            ["🔐 Шифрование/Дешифрование", "🎯 Визуализация раундов", "🔧 Генерация ключей", "📊 Анализ алгоритма"],
            horizontal=True
        )
        
        if mode == "🔐 Шифрование/Дешифрование":
            self.render_encryption_section()
        elif mode == "🎯 Визуализация раундов":
            self.render_round_visualization()
        elif mode == "🔧 Генерация ключей":
            self.render_key_generation()
        else:
            self.render_algorithm_analysis()
    
    def render_encryption_section(self):
        """Отрисовывает секцию шифрования/дешифрования"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔒 Шифрование DES")
            self.render_des_encryption()
        
        with col2:
            st.subheader("🔓 Дешифрование DES")
            self.render_des_decryption()
    
    def render_des_encryption(self):
        """Отрисовывает интерфейс шифрования DES"""
        plaintext = st.text_area(
            "Открытый текст (8 символов):",
            "ABCDEFGH",
            height=100,
            key="des_enc_text",
            help="DES работает с блоками по 64 бита (8 символов)"
        )
        
        # Генерация ключа
        col_key, col_gen = st.columns([3, 1])
        
        with col_key:
            if 'des_enc_key' not in st.session_state:
                st.session_state.des_enc_key = "133457799BBCDFF1"
            
            key = st.text_input(
                "Ключ (16 hex символов):",
                st.session_state.des_enc_key,
                key="des_enc_key_input",
                help="64-битный ключ в шестнадцатеричном формате"
            )
        
        with col_gen:
            st.write("")  # Отступ
            st.write("")  # Отступ
            if st.button("🎲 Сгенерировать ключ", key="gen_des_key", use_container_width=True):
                random_key = secrets.token_hex(8).upper()  # 8 байт = 64 бита
                st.session_state.des_enc_key = random_key
                st.rerun()
        
        if st.button("Зашифровать DES", key="des_enc_btn", use_container_width=True):
            if plaintext and key:
                try:
                    # Проверяем длину текста
                    if len(plaintext) != 8:
                        st.warning("DES работает с блоками по 8 символов. Будут использованы первые 8 символов.")
                        plaintext = plaintext[:8].ljust(8, ' ')  # Дополняем пробелами
                    
                    # Проверяем ключ
                    if len(key) != 16:
                        st.error("Ключ должен содержать ровно 16 шестнадцатеричных символов")
                        return
                    
                    # Шифруем
                    ciphertext = self.des_encrypt(plaintext, key)
                    
                    st.success("Зашифрованный текст (hex):")
                    st.code(ciphertext, language="text")
                    
                    # Показываем детали
                    self.show_encryption_details(plaintext, key, ciphertext)
                    
                except Exception as e:
                    st.error(f"Ошибка шифрования: {e}")
            else:
                st.error("Введите текст и ключ")
    
    def render_des_decryption(self):
        """Отрисовывает интерфейс дешифрования DES"""
        ciphertext = st.text_input(
            "Шифротекст (16 hex символов):",
            "85E813540F0AB405",
            key="des_dec_text",
            help="64-битный шифротекст в шестнадцатеричном формате"
        )
        
        key = st.text_input(
            "Ключ (16 hex символов):",
            "133457799BBCDFF1",
            key="des_dec_key",
            help="Тот же ключ, что использовался для шифрования"
        )
        
        if st.button("Дешифровать DES", key="des_dec_btn", use_container_width=True):
            if ciphertext and key:
                try:
                    # Проверяем длину шифротекста
                    if len(ciphertext) != 16:
                        st.error("Шифротекст должен содержать ровно 16 шестнадцатеричных символов")
                        return
                    
                    # Проверяем ключ
                    if len(key) != 16:
                        st.error("Ключ должен содержать ровно 16 шестнадцатеричных символов")
                        return
                    
                    # Дешифруем
                    plaintext = self.des_decrypt(ciphertext, key)
                    
                    st.success("Дешифрованный текст:")
                    st.code(plaintext, language="text")
                    
                except Exception as e:
                    st.error(f"Ошибка дешифрования: {e}")
            else:
                st.error("Введите шифротекст и ключ")
    
    def render_round_visualization(self):
        """Отрисовывает визуализацию раундов DES"""
        st.subheader("🎯 Визуализация раундов DES")
        
        demo_text = st.text_input(
            "Текст для демонстрации (8 символов):",
            "ABCDEFGH",
            key="demo_des_text"
        )
        
        demo_key = st.text_input(
            "Ключ для демонстрации (16 hex):",
            "133457799BBCDFF1",
            key="demo_des_key"
        )
        
        if st.button("Показать раунды", key="demo_rounds_btn"):
            if demo_text and demo_key:
                try:
                    if len(demo_text) != 8:
                        demo_text = demo_text[:8].ljust(8, ' ')
                    
                    self.visualize_des_rounds(demo_text, demo_key)
                    
                except Exception as e:
                    st.error(f"Ошибка визуализации: {e}")
            else:
                st.error("Введите текст и ключ")
    
    def render_key_generation(self):
        """Отрисовывает секцию генерации ключей"""
        st.subheader("🔧 Генерация подключей DES")
        
        master_key = st.text_input(
            "Мастер-ключ (16 hex символов):",
            "133457799BBCDFF1",
            key="key_gen_input"
        )
        
        if st.button("Сгенерировать подключи", key="key_gen_btn"):
            if master_key and len(master_key) == 16:
                try:
                    subkeys = self.generate_subkeys(master_key)
                    
                    st.success("Сгенерированные подключи:")
                    
                    # Показываем таблицу подключей
                    keys_data = []
                    for i, key in enumerate(subkeys, 1):
                        keys_data.append({
                            'Раунд': i,
                            'Подключ (hex)': key,
                            'Подключ (бинарно)': self.hex_to_binary(key)
                        })
                    
                    df_keys = pd.DataFrame(keys_data)
                    st.dataframe(df_keys, use_container_width=True, height=400)
                    
                    # Детали генерации ключей
                    self.show_key_generation_details(master_key, subkeys)
                    
                except Exception as e:
                    st.error(f"Ошибка генерации ключей: {e}")
            else:
                st.error("Введите корректный 64-битный ключ")
    
    def render_algorithm_analysis(self):
        """Отрисовывает секцию анализа алгоритма"""
        st.subheader("📊 Анализ алгоритма DES")
        
        tab1, tab2, tab3 = st.tabs(["🔄 Перестановки", "📦 S-блоки", "⚡ Производительность"])
        
        with tab1:
            self.render_permutations_analysis()
        
        with tab2:
            self.render_sbox_analysis()
        
        with tab3:
            self.render_performance_analysis()
    
    def render_permutations_analysis(self):
        """Анализ перестановок DES"""
        st.markdown("**Начальная перестановка (IP):**")
        
        # Показываем таблицу IP
        ip_data = []
        for i in range(8):
            row = []
            for j in range(8):
                index = i * 8 + j
                ip_data.append({
                    'Позиция': index + 1,
                    'Новая позиция': self.IP[index],
                    'Бит': f"b{self.IP[index]}"
                })
        
        df_ip = pd.DataFrame(ip_data)
        st.dataframe(df_ip, use_container_width=True, height=300)
        
        st.markdown("**Конечная перестановка (FP):**")
        
        # Показываем таблицу FP
        fp_data = []
        for i in range(8):
            for j in range(8):
                index = i * 8 + j
                fp_data.append({
                    'Позиция': index + 1,
                    'Исходная позиция': self.FP[index],
                    'Бит': f"b{self.FP[index]}"
                })
        
        df_fp = pd.DataFrame(fp_data)
        st.dataframe(df_fp, use_container_width=True, height=300)
    
    def render_sbox_analysis(self):
        """Анализ S-блоков"""
        st.markdown("**S-блоки DES:**")
        
        sbox_number = st.selectbox("Выберите S-блок:", list(range(1, 9)), key="sbox_select")
        
        sbox = self.S_BOX[sbox_number - 1]
        
        # Создаем таблицу S-блока
        sbox_data = []
        st.markdown(f"**S-блок {sbox_number}:**")
        
        # Заголовок таблицы
        cols = st.columns(17)
        with cols[0]:
            st.write("Row\\Col")
        for j in range(16):
            with cols[j + 1]:
                st.write(f"{j:X}")
        
        # Данные таблицы
        for i in range(4):
            cols = st.columns(17)
            with cols[0]:
                st.write(f"{i:02b}")
            for j in range(16):
                with cols[j + 1]:
                    st.write(f"{sbox[i][j]:X}")
        
        st.markdown("**Принцип работы S-блока:**")
        st.markdown("""
        - 6-битный вход делится на 2-битный номер строки и 4-битный номер столбца
        - Например, вход `011011`:
          - Строка: `01` = 1
          - Столбец: `1101` = 13
          - Результат: значение из S-блока[1][13]
        """)
    
    def render_performance_analysis(self):
        """Анализ производительности DES"""
        st.markdown("**Характеристики DES:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Сильные стороны:**
            - Быстрое аппаратное исполнение
            - Простая реализация
            - Хорошо изученная безопасность
            - Широкая стандартизация
            
            **Слабые стороны:**
            - Короткий ключ (56 бит)
            - Уязвимость к атакам
            - Устаревшая структура
            """)
        
        with col2:
            st.markdown("""
            **Время взлома полным перебором:**
            - 1993: 150 дней
            - 1997: 39 дней  
            - 1998: 56 часов
            - 1999: 22 часа
            - 2006: 9 дней (стоимость: $10,000)
            - 2012: 1 день
            - 2020: несколько часов
            
            **Модернизации:**
            - Triple DES (3DES)
            - DESX
            """)
    
    # Основные функции DES
    
    def string_to_bit_array(self, text: str) -> List[int]:
        """Преобразует строку в массив битов"""
        array = []
        for char in text:
            # Получаем ASCII код и преобразуем в 8 бит
            binval = bin(ord(char))[2:].zfill(8)
            array.extend([int(x) for x in list(binval)])
        return array
    
    def bit_array_to_string(self, array: List[int]) -> str:
        """Преобразует массив битов в строку"""
        res = []
        for i in range(0, len(array), 8):
            byte = array[i:i+8]
            char = chr(int(''.join(map(str, byte)), 2))
            res.append(char)
        return ''.join(res)
    
    def hex_to_bit_array(self, hex_string: str) -> List[int]:
        """Преобразует hex строку в массив битов"""
        # Преобразуем hex в байты, затем в биты
        byte_array = bytes.fromhex(hex_string)
        bit_array = []
        for byte in byte_array:
            bit_array.extend([int(bit) for bit in format(byte, '08b')])
        return bit_array
    
    def bit_array_to_hex(self, bit_array: List[int]) -> str:
        """Преобразует массив битов в hex строку"""
        # Группируем по 8 бит
        bytes_list = []
        for i in range(0, len(bit_array), 8):
            byte_bits = bit_array[i:i+8]
            byte_val = int(''.join(map(str, byte_bits)), 2)
            bytes_list.append(byte_val)
        
        # Преобразуем в hex
        return ''.join([format(byte, '02X') for byte in bytes_list])
    
    def permute(self, block: List[int], table: List[int]) -> List[int]:
        """Выполняет перестановку битов согласно таблице"""
        return [block[i-1] for i in table]
    
    def left_shift(self, block: List[int], n: int) -> List[int]:
        """Циклический сдвиг влево"""
        return block[n:] + block[:n]
    
    def generate_subkeys(self, key_hex: str) -> List[str]:
        """Генерирует 16 подключей для DES"""
        # Преобразуем ключ в битовый массив
        key_bits = self.hex_to_bit_array(key_hex)
        
        # Применяем PC1
        key_pc1 = self.permute(key_bits, self.PC1)
        
        # Разделяем на две половины
        left = key_pc1[:28]
        right = key_pc1[28:]
        
        subkeys = []
        
        for i in range(16):
            # Сдвигаем половины
            shift = self.SHIFTS[i]
            left = self.left_shift(left, shift)
            right = self.left_shift(right, shift)
            
            # Объединяем и применяем PC2
            combined = left + right
            subkey = self.permute(combined, self.PC2)
            
            # Преобразуем в hex
            subkey_hex = self.bit_array_to_hex(subkey)
            subkeys.append(subkey_hex)
        
        return subkeys
    
    def f_function(self, right: List[int], subkey: List[int]) -> List[int]:
        """Функция Фейстеля f"""
        # Расширение E
        expanded = self.permute(right, self.E)
        
        # XOR с подключом
        xor_result = [expanded[i] ^ subkey[i] for i in range(48)]
        
        # S-блоки
        sbox_result = []
        for i in range(8):
            # Берем 6 бит для каждого S-блока
            block = xor_result[i*6:(i+1)*6]
            row = (block[0] << 1) + block[5]  # Первый и последний бит
            col = (block[1] << 3) + (block[2] << 2) + (block[3] << 1) + block[4]  # Средние 4 бита
            
            # Получаем значение из S-блока
            sbox_val = self.S_BOX[i][row][col]
            
            # Преобразуем в 4 бита
            sbox_result.extend([int(bit) for bit in format(sbox_val, '04b')])
        
        # Перестановка P
        return self.permute(sbox_result, self.P)
    
    def des_encrypt(self, plaintext: str, key_hex: str) -> str:
        """Шифрует текст с помощью DES"""
        # Преобразуем текст и ключ в битовые массивы
        text_bits = self.string_to_bit_array(plaintext)
        key_bits = self.hex_to_bit_array(key_hex)
        
        # Генерируем подключи
        subkeys_hex = self.generate_subkeys(key_hex)
        subkeys_bits = [self.hex_to_bit_array(sk) for sk in subkeys_hex]
        
        # Начальная перестановка
        ip_result = self.permute(text_bits, self.IP)
        
        # Разделяем на две половины
        left = ip_result[:32]
        right = ip_result[32:]
        
        # 16 раундов Фейстеля
        for i in range(16):
            new_left = right
            f_result = self.f_function(right, subkeys_bits[i])
            new_right = [left[j] ^ f_result[j] for j in range(32)]
            
            left = new_left
            right = new_right
        
        # Финальное объединение (меняем половины местами)
        combined = right + left
        
        # Конечная перестановка
        fp_result = self.permute(combined, self.FP)
        
        # Преобразуем в hex
        return self.bit_array_to_hex(fp_result)
    
    def des_decrypt(self, ciphertext_hex: str, key_hex: str) -> str:
        """Дешифрует текст с помощью DES"""
        # Преобразуем шифротекст и ключ в битовые массивы
        cipher_bits = self.hex_to_bit_array(ciphertext_hex)
        key_bits = self.hex_to_bit_array(key_hex)
        
        # Генерируем подключи
        subkeys_hex = self.generate_subkeys(key_hex)
        subkeys_bits = [self.hex_to_bit_array(sk) for sk in subkeys_hex]
        
        # Начальная перестановка
        ip_result = self.permute(cipher_bits, self.IP)
        
        # Разделяем на две половины
        left = ip_result[:32]
        right = ip_result[32:]
        
        # 16 раундов Фейстеля в обратном порядке
        for i in range(15, -1, -1):
            new_right = left
            f_result = self.f_function(left, subkeys_bits[i])
            new_left = [right[j] ^ f_result[j] for j in range(32)]
            
            left = new_left
            right = new_right
        
        # Финальное объединение
        combined = left + right
        
        # Конечная перестановка
        fp_result = self.permute(combined, self.FP)
        
        # Преобразуем в строку
        return self.bit_array_to_string(fp_result)
    
    def hex_to_binary(self, hex_string: str) -> str:
        """Преобразует hex строку в бинарное представление"""
        return bin(int(hex_string, 16))[2:].zfill(64)
    
    def show_encryption_details(self, plaintext: str, key: str, ciphertext: str):
        """Показывает детали шифрования"""
        st.markdown("**Детали шифрования:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Открытый текст", plaintext)
            st.text(f"Бинарно: {self.string_to_bit_array(plaintext)}")
        
        with col2:
            st.metric("Ключ", key)
            st.text(f"Бинарно: {self.hex_to_binary(key)}")
        
        with col3:
            st.metric("Шифротекст", ciphertext)
            st.text(f"Бинарно: {self.hex_to_binary(ciphertext)}")
    
    def visualize_des_rounds(self, text: str, key: str):
        """Визуализирует процесс раундов DES"""
        st.markdown("### 🔄 Процесс раундов DES")
        
        # Преобразуем текст и ключ
        text_bits = self.string_to_bit_array(text)
        subkeys_hex = self.generate_subkeys(key)
        
        # Начальная перестановка
        ip_result = self.permute(text_bits, self.IP)
        left = ip_result[:32]
        right = ip_result[32:]
        
        st.markdown("**Начальная перестановка (IP):**")
        st.text(f"Результат IP: {''.join(map(str, ip_result))}")
        
        # Показываем каждый раунд
        for round_num in range(16):
            st.markdown(f"**Раунд {round_num + 1}:**")
            
            new_left = right
            f_result = self.f_function(right, self.hex_to_bit_array(subkeys_hex[round_num]))
            new_right = [left[j] ^ f_result[j] for j in range(32)]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("L", f"{''.join(map(str, left))[:8]}...")
            with col2:
                st.metric("R", f"{''.join(map(str, right))[:8]}...")
            with col3:
                st.metric("Подключ", subkeys_hex[round_num])
            
            left = new_left
            right = new_right
            
            st.progress((round_num + 1) / 16)
    
    def show_key_generation_details(self, master_key: str, subkeys: List[str]):
        """Показывает детали генерации ключей"""
        st.markdown("**Детали генерации ключей:**")
        
        # Показываем PC1 перестановку
        key_bits = self.hex_to_bit_array(master_key)
        pc1_result = self.permute(key_bits, self.PC1)
        
        st.text(f"Ключ после PC1: {''.join(map(str, pc1_result))}")
        st.text(f"Левая половина: {''.join(map(str, pc1_result[:28]))}")
        st.text(f"Правая половина: {''.join(map(str, pc1_result[28:]))}")

# Для обратной совместимости
class DESCipher(DESModule):
    pass
