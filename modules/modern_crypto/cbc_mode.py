# modules/modern_crypto/cbc_mode.py
from modules.base_module import CryptoModule
import streamlit as st
import secrets
import binascii
from typing import List, Tuple
import pandas as pd
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class CBCModeModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Режим CBC"
        self.description = "Режим сцепления блоков шифра - распространенный режим для блочных шифров"
        self.category = "modern"
        self.icon = ""
        self.order = 7

    def render(self):
        st.title("🔄 Режим CBC (Cipher Block Chaining)")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **CBC (Cipher Block Chaining)** - режим сцепления блоков шифра, один из самых популярных режимов для блочных шифров.

            **Принцип работы:**
            - Каждый блок открытого текста XOR-ится с предыдущим зашифрованным блоком
            - Первый блок XOR-ится с вектором инициализации (IV)
            - Создается цепочка зависимостей между блоками

            **Шифрование в CBC:**
            ```
            C₀ = IV
            Cᵢ = Eₖ(Pᵢ ⊕ Cᵢ₋₁) для i = 1, 2, ..., n
            ```

            **Дешифрование в CBC:**
            ```
            C₀ = IV  
            Pᵢ = Dₖ(Cᵢ) ⊕ Cᵢ₋₁ для i = 1, 2, ..., n
            ```

            **Преимущества:**
            - Распространение ошибок (ошибка в одном блоке влияет на последующие)
            - Скрытие паттернов в открытом тексте
            - Устойчивость к некоторым атакам

            **Недостатки:**
            - Последовательная обработка (не параллелизуется)
            - Требует синхронизации IV

            **Применение:**
            - SSL/TLS
            - IPSec
            - Многие файловые системы
            - Базы данных
            """)

        st.markdown("---")

        # Выбор режима работы
        mode = st.radio(
            "Режим работы:",
            ["🔐 Шифрование/Дешифрование", "🎯 Визуализация процесса", "📊 Сравнение с ECB"],
            horizontal=True
        )

        if mode == "🔐 Шифрование/Дешифрование":
            self.render_encryption_section()
        elif mode == "🎯 Визуализация процесса":
            self.render_visualization_section()
        else:
            self.render_comparison_section()

    def render_encryption_section(self):
        """Секция шифрования/дешифрования в CBC режиме"""
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🔒 Шифрование CBC")
            self.render_cbc_encryption()

        with col2:
            st.subheader("🔓 Дешифрование CBC")
            self.render_cbc_decryption()

    def render_cbc_encryption(self):
        """Интерфейс шифрования CBC"""
        plaintext = st.text_area(
            "Открытый текст:",
            "Hello CBC Mode! This is a demonstration.",
            height=100,
            key="cbc_enc_text"
        )

        # Выбор алгоритма
        algorithm = st.selectbox(
            "Алгоритм шифрования:",
            ["AES", "DES"],
            key="cbc_enc_algo"
        )

        # Генерация ключа и IV
        col_key, col_iv = st.columns(2)

        with col_key:
            if 'cbc_enc_key' not in st.session_state:
                st.session_state.cbc_enc_key = secrets.token_hex(16)
            
            key_length = 32 if algorithm == "AES" else 16
            key = st.text_input(
                f"Ключ ({key_length} hex символов):",
                st.session_state.cbc_enc_key[:key_length],
                key="cbc_enc_key_input"
            )

        with col_iv:
            if 'cbc_enc_iv' not in st.session_state:
                st.session_state.cbc_enc_iv = secrets.token_hex(16)
            
            iv = st.text_input(
                "IV (32 hex символа):",
                st.session_state.cbc_enc_iv,
                key="cbc_enc_iv_input"
            )

        # Кнопки генерации
        col_gen1, col_gen2 = st.columns(2)
        with col_gen1:
            if st.button("🎲 Сгенерировать ключ", key="gen_cbc_key", use_container_width=True):
                key_length_bytes = 16 if algorithm == "AES" else 8
                st.session_state.cbc_enc_key = secrets.token_hex(key_length_bytes)
                st.rerun()

        with col_gen2:
            if st.button("🎲 Сгенерировать IV", key="gen_cbc_iv", use_container_width=True):
                st.session_state.cbc_enc_iv = secrets.token_hex(16)
                st.rerun()

        if st.button("Зашифровать CBC", key="cbc_enc_btn", use_container_width=True):
            if plaintext and key and iv:
                try:
                    # Проверки
                    if algorithm == "AES" and len(key) != 32:
                        st.error("Для AES ключ должен быть 32 hex символа (128 бит)")
                        return
                    elif algorithm == "DES" and len(key) != 16:
                        st.error("Для DES ключ должен быть 16 hex символа (64 бит)")
                        return
                    
                    if len(iv) != 32:
                        st.error("IV должен быть 32 hex символа (128 бит)")
                        return

                    # Шифрование
                    ciphertext = self.cbc_encrypt(plaintext, key, iv, algorithm)
                    
                    st.success("✅ Зашифрованный текст (hex):")
                    st.code(ciphertext, language="text")

                    # Детали процесса
                    self.show_encryption_details(plaintext, key, iv, ciphertext, algorithm)

                except Exception as e:
                    st.error(f"❌ Ошибка шифрования: {e}")
            else:
                st.error("⚠️ Заполните все поля")

    def render_cbc_decryption(self):
        """Интерфейс дешифрования CBC"""
        ciphertext = st.text_area(
            "Шифротекст (hex):",
            "",
            height=100,
            key="cbc_dec_text",
            placeholder="Введите hex-строку шифротекста"
        )

        algorithm = st.selectbox(
            "Алгоритм шифрования:",
            ["AES", "DES"],
            key="cbc_dec_algo"
        )

        key_length = 32 if algorithm == "AES" else 16
        key = st.text_input(
            f"Ключ ({key_length} hex символов):",
            key="cbc_dec_key"
        )

        iv = st.text_input(
            "IV (32 hex символа):",
            key="cbc_dec_iv"
        )

        if st.button("Дешифровать CBC", key="cbc_dec_btn", use_container_width=True):
            if ciphertext and key and iv:
                try:
                    # Проверки
                    if algorithm == "AES" and len(key) != 32:
                        st.error("Для AES ключ должен быть 32 hex символа")
                        return
                    elif algorithm == "DES" and len(key) != 16:
                        st.error("Для DES ключ должен быть 16 hex символа")
                        return
                    
                    if len(iv) != 32:
                        st.error("IV должен быть 32 hex символа")
                        return

                    # Дешифрование
                    plaintext = self.cbc_decrypt(ciphertext, key, iv, algorithm)
                    
                    st.success("✅ Дешифрованный текст:")
                    st.code(plaintext, language="text")

                except Exception as e:
                    st.error(f"❌ Ошибка дешифрования: {e}")
            else:
                st.error("⚠️ Заполните все поля")

    def render_visualization_section(self):
        """Визуализация процесса CBC"""
        st.subheader("🎯 Визуализация процесса CBC")

        demo_text = st.text_input(
            "Текст для демонстрации:",
            "CBC Demo",
            key="demo_cbc_text"
        )

        # Убедимся, что текст кратен 16 байтам для AES
        if len(demo_text) % 16 != 0:
            demo_text = demo_text.ljust((len(demo_text) // 16 + 1) * 16, ' ')

        demo_key = st.text_input(
            "Ключ (32 hex):",
            "2b7e151628aed2a6abf7158809cf4f3c",
            key="demo_cbc_key"
        )

        demo_iv = st.text_input(
            "IV (32 hex):",
            "000102030405060708090a0b0c0d0e0f",
            key="demo_cbc_iv"
        )

        if st.button("Визуализировать процесс", key="viz_cbc_btn"):
            if demo_text and demo_key and demo_iv:
                try:
                    self.visualize_cbc_process(demo_text, demo_key, demo_iv)
                except Exception as e:
                    st.error(f"Ошибка визуализации: {e}")
            else:
                st.error("Заполните все поля")

    def render_comparison_section(self):
        """Сравнение CBC с ECB"""
        st.subheader("📊 Сравнение CBC vs ECB")

        # Сравнительная таблица
        comparison_data = {
            'Параметр': [
                'Режим работы',
                'Зависимость блоков',
                'Параллелизация',
                'Распространение ошибок',
                'Стойкость к анализу',
                'Требует IV',
                'Применение'
            ],
            'ECB': [
                'Простая замена',
                'Нет',
                'Полная',
                'Только в одном блоке',
                'Низкая',
                'Нет',
                'Не рекомендуется'
            ],
            'CBC': [
                'Сцепление блоков',
                'Да',
                'Только дешифрование',
                'На все последующие блоки',
                'Высокая',
                'Да',
                'Широко используется'
            ]
        }

        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Визуальное сравнение
        st.markdown("### 🎨 Визуальное сравнение")

        test_image_text = "AAAAAAAABBBBBBBBAAAAAAAABBBBBBBB"
        
        col_ecb, col_cbc = st.columns(2)
        
        with col_ecb:
            st.markdown("**ECB Mode:**")
            st.markdown("""
            ```
            Plaintext:  AAAAAAAABBBBBBBBAAAAAAAABBBBBBBB
            Ciphertext: XXXXXXXXYYYYYYYYXXXXXXXXYYYYYYYY
            ```
            """)
            st.warning("Паттерны сохраняются!")

        with col_cbc:
            st.markdown("**CBC Mode:**")
            st.markdown("""
            ```
            Plaintext:  AAAAAAAABBBBBBBBAAAAAAAABBBBBBBB  
            Ciphertext: X1X2X3X4Y1Y2Y3Y4Z1Z2Z3Z4W1W2W3W4
            ```
            """)
            st.success("Паттерны скрыты!")

        # Демонстрация с одинаковыми блоками
        st.markdown("### 🔍 Демонстрация с одинаковыми блоками")

        identical_blocks = "BLOCK" * 8  # 8 одинаковых блоков
        
        if st.button("Показать разницу", key="compare_btn"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**ECB (проблема):**")
                # В ECB одинаковые блоки дают одинаковый шифротекст
                ecb_result = "ECB1 " * 8
                st.text(f"Шифротекст: {ecb_result}")
                st.error("Одинаковые блоки → одинаковый шифротекст!")
            
            with col2:
                st.markdown("**CBC (решение):**")
                # В CBC даже одинаковые блоки дают разный шифротекст
                cbc_result = "CBC1 CBC2 CBC3 CBC4 CBC5 CBC6 CBC7 CBC8"
                st.text(f"Шифротекст: {cbc_result}")
                st.success("Одинаковые блоки → разный шифротекст!")

    def cbc_encrypt(self, plaintext: str, key_hex: str, iv_hex: str, algorithm: str) -> str:
        """Шифрование в режиме CBC"""
        try:
            # Преобразуем в байты
            plaintext_bytes = plaintext.encode('utf-8')
            key_bytes = bytes.fromhex(key_hex)
            iv_bytes = bytes.fromhex(iv_hex)

            # Выбираем алгоритм
            if algorithm == "AES":
                cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())
            else:  # DES
                cipher = Cipher(algorithms.TripleDES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())

            # Дополняем данные до размера блока
            block_size = 16 if algorithm == "AES" else 8
            padded_data = self.pad_data(plaintext_bytes, block_size)

            # Шифруем
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

            return ciphertext.hex()

        except Exception as e:
            raise Exception(f"Ошибка CBC шифрования: {e}")

    def cbc_decrypt(self, ciphertext_hex: str, key_hex: str, iv_hex: str, algorithm: str) -> str:
        """Дешифрование в режиме CBC"""
        try:
            # Преобразуем в байты
            ciphertext_bytes = bytes.fromhex(ciphertext_hex)
            key_bytes = bytes.fromhex(key_hex)
            iv_bytes = bytes.fromhex(iv_hex)

            # Выбираем алгоритм
            if algorithm == "AES":
                cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())
            else:  # DES
                cipher = Cipher(algorithms.TripleDES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())

            # Дешифруем
            decryptor = cipher.decryptor()
            decrypted_padded = decryptor.update(ciphertext_bytes) + decryptor.finalize()

            # Убираем дополнение
            plaintext_bytes = self.unpad_data(decrypted_padded)

            return plaintext_bytes.decode('utf-8')

        except Exception as e:
            raise Exception(f"Ошибка CBC дешифрования: {e}")

    def pad_data(self, data: bytes, block_size: int) -> bytes:
        """Дополнение данных по стандарту PKCS7"""
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding

    def unpad_data(self, data: bytes) -> bytes:
        """Удаление дополнения PKCS7"""
        padding_length = data[-1]
        return data[:-padding_length]

    def show_encryption_details(self, plaintext: str, key: str, iv: str, ciphertext: str, algorithm: str):
        """Показывает детали процесса шифрования"""
        st.markdown("---")
        st.markdown("**🔍 Детали процесса CBC:**")

        # Информация о параметрах
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Алгоритм", algorithm)
        with col2:
            st.metric("Размер блока", "128 бит" if algorithm == "AES" else "64 бита")
        with col3:
            st.metric("Режим", "CBC")
        with col4:
            st.metric("Длина текста", f"{len(plaintext)} симв.")

        # Схема процесса
        st.markdown("**Схема шифрования CBC:**")
        st.markdown("""
        ```
        Plaintext: P₁ P₂ P₃ ... Pₙ
            ↓
        IV → XOR → Eₖ → C₁ → XOR → Eₖ → C₂ → ... → Cₙ
               ↑        ↑        ↑
               P₁       P₂       P₃
        ```
        """)

        # Показываем блоки
        plaintext_bytes = plaintext.encode('utf-8')
        block_size = 16 if algorithm == "AES" else 8
        blocks = [plaintext_bytes[i:i+block_size] for i in range(0, len(plaintext_bytes), block_size)]
        
        st.markdown(f"**Блоки открытого текста ({len(blocks)}):**")
        for i, block in enumerate(blocks):
            st.text(f"Блок {i+1}: {block.hex()} -> '{block.decode('utf-8', errors='replace')}'")

    def visualize_cbc_process(self, plaintext: str, key_hex: str, iv_hex: str):
        """Визуализирует процесс CBC шифрования по шагам"""
        st.markdown("### 🔄 Пошаговая визуализация CBC")

        # Преобразуем в байты
        plaintext_bytes = plaintext.encode('utf-8')
        key_bytes = bytes.fromhex(key_hex)
        iv_bytes = bytes.fromhex(iv_hex)
        
        block_size = 16  # AES
        blocks = [plaintext_bytes[i:i+block_size] for i in range(0, len(plaintext_bytes), block_size)]

        # Начальное состояние
        st.markdown("**Начальные параметры:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("IV:", iv_hex, disabled=True)
        with col2:
            st.text_input("Ключ:", key_hex, disabled=True)
        with col3:
            st.text_input("Блоков:", str(len(blocks)), disabled=True)

        # Процесс для каждого блока
        current_state = iv_bytes
        
        for i, block in enumerate(blocks):
            st.markdown(f"---")
            st.markdown(f"### 🔷 Обработка блока {i+1}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**До XOR с предыдущим блоком:**")
                st.text(f"Блок текста: {block.hex()}")
                st.text(f"Пред. блок: {current_state.hex()}")
                
                # XOR операция
                xor_result = bytes(a ^ b for a, b in zip(block, current_state))
                st.text(f"XOR результат: {xor_result.hex()}")
            
            with col2:
                st.markdown("**После шифрования:**")
                # Имитация шифрования (в реальности используем AES/DES)
                encrypted_block = self.simulate_encryption(xor_result, key_bytes)
                st.text(f"Зашифр. блок: {encrypted_block.hex()}")
                
                # Обновляем состояние для следующего блока
                current_state = encrypted_block
                
                st.success(f"Блок {i+1} завершен!")

            # Прогресс
            st.progress((i + 1) / len(blocks))

        # Финальный результат
        st.markdown("---")
        st.success(f"**Итоговый шифротекст:** {current_state.hex()}")

    def simulate_encryption(self, data: bytes, key: bytes) -> bytes:
        """Имитация шифрования блока (для визуализации)"""
        # В реальной реализации здесь было бы настоящее шифрование
        # Для демонстрации используем простую трансформацию
        return bytes((b + 1) % 256 for b in data)

# Для обратной совместимости
class CBCMode(CBCModeModule):
    pass