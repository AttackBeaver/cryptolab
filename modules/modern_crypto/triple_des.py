from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import numpy as np
import binascii
import secrets
from typing import List, Tuple

class TripleDESModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "3DES"
        self.description = "Усиленная версия DES с тройным шифрованием"
        self.complexity = "advanced"
        self.category = "modern"
        self.icon = ""
        self.order = 3
    
    def render(self):
        st.title("🔒 Triple DES (3DES)")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **Triple DES (3DES)** - симметричный блочный шифр, представляющий собой тройное применение алгоритма DES для повышения безопасности.
            
            **Основные характеристики:**
            - **Размер блока:** 64 бита (как в DES)
            - **Размер ключа:** 112 или 168 бит (2 или 3 ключа DES)
            - **Количество раундов:** 48 (3 × 16)
            - **Режимы работы:** EDE (Encrypt-Decrypt-Encrypt)
            
            **Режимы 3DES:**
            1. **3DES с двумя ключами (K1, K2, K1):**
               - Шифрование: `E(K1) → D(K2) → E(K1)`
               - Эффективный размер ключа: 112 бит
               
            2. **3DES с тремя ключами (K1, K2, K3):**
               - Шифрование: `E(K1) → D(K2) → E(K3)`
               - Эффективный размер ключа: 168 бит
            
            **Историческое значение:**
            - Промежуточное решение между DES и AES
            - Широкое применение в банковской сфере (EMV, ISO 8583)
            - Стандартизирован в ANSI X9.52 и ISO 8732
            
            **Безопасность:**
            - Устойчив к атаке MIM (112 бит)
            - Не подвержен атакам на DES из-за тройного шифрования
            - Все еще считается безопасным для некоторых применений
            - Постепенно заменяется AES
            
            **Производительность:**
            - В 3 раза медленнее чем DES
            - Быстрее чем многие современные алгоритмы
            - Эффективная аппаратная реализация
            """)
        
        st.markdown("---")
        
        # Выбор режима работы
        mode = st.radio(
            "Режим работы:",
            ["🔐 Шифрование/Дешифрование", "🎯 Сравнение с DES", "🔧 Генерация ключей", "📊 Анализ безопасности"],
            horizontal=True
        )
        
        if mode == "🔐 Шифрование/Дешифрование":
            self.render_encryption_section()
        elif mode == "🎯 Сравнение с DES":
            self.render_comparison_section()
        elif mode == "🔧 Генерация ключей":
            self.render_key_generation_section()
        else:
            self.render_security_analysis()
    
    def render_encryption_section(self):
        """Отрисовывает секцию шифрования/дешифрования"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔒 Шифрование 3DES")
            self.render_3des_encryption()
        
        with col2:
            st.subheader("🔓 Дешифрование 3DES")
            self.render_3des_decryption()
    
    def render_3des_encryption(self):
        """Отрисовывает интерфейс шифрования 3DES"""
        plaintext = st.text_area(
            "Открытый текст (8 символов):",
            "SECRET!!",
            height=100,
            key="3des_enc_text",
            help="3DES работает с блоками по 64 бита (8 символов)"
        )
        
        # Выбор режима ключей
        key_mode = st.radio(
            "Режим ключей:",
            ["2 ключа (K1, K2, K1)", "3 ключа (K1, K2, K3)"],
            key="3des_key_mode",
            horizontal=True
        )
        
        # Генерация ключей
        col_key1, col_gen1 = st.columns([3, 1])
        with col_key1:
            if '3des_k1' not in st.session_state:
                st.session_state.tdes_k1 = "133457799BBCDFF1"
            
            k1 = st.text_input(
                "Ключ 1 (16 hex символов):",
                st.session_state.tdes_k1,
                key="3des_k1_input"
            )
        
        with col_gen1:
            st.write("")  # Отступ
            st.write("")  # Отступ
            if st.button("🎲 К1", key="gen_3des_k1", use_container_width=True):
                random_key = secrets.token_hex(8).upper()
                st.session_state.tdes_k1 = random_key
                st.rerun()
        
        col_key2, col_gen2 = st.columns([3, 1])
        with col_key2:
            if '3des_k2' not in st.session_state:
                st.session_state.tdes_k2 = "0E329232EA6D0D73"
            
            k2 = st.text_input(
                "Ключ 2 (16 hex символов):",
                st.session_state.tdes_k2,
                key="3des_k2_input"
            )
        
        with col_gen2:
            st.write("")  # Отступ
            st.write("")  # Отступ
            if st.button("🎲 К2", key="gen_3des_k2", use_container_width=True):
                random_key = secrets.token_hex(8).upper()
                st.session_state.tdes_k2 = random_key
                st.rerun()
        
        if key_mode == "3 ключа (K1, K2, K3)":
            col_key3, col_gen3 = st.columns([3, 1])
            with col_key3:
                if '3des_k3' not in st.session_state:
                    st.session_state.tdes_k3 = "133457799BBCDFF1"  # По умолчанию как K1
                
                k3 = st.text_input(
                    "Ключ 3 (16 hex символов):",
                    st.session_state.tdes_k3,
                    key="3des_k3_input"
                )
            
            with col_gen3:
                st.write("")  # Отступ
                st.write("")  # Отступ
                if st.button("🎲 К3", key="gen_3des_k3", use_container_width=True):
                    random_key = secrets.token_hex(8).upper()
                    st.session_state.tdes_k3 = random_key
                    st.rerun()
        else:
            k3 = k1  # Для 2-ключевого режима K3 = K1
        
        if st.button("Зашифровать 3DES", key="3des_enc_btn", use_container_width=True):
            if plaintext and k1 and k2 and (key_mode == "2 ключа" or k3):
                try:
                    # Проверяем длину текста
                    if len(plaintext) != 8:
                        st.warning("3DES работает с блоками по 8 символов. Будут использованы первые 8 символов.")
                        plaintext = plaintext[:8].ljust(8, ' ')
                    
                    # Проверяем ключи
                    for key in [k1, k2, k3]:
                        if key and len(key) != 16:
                            st.error("Все ключи должны содержать ровно 16 шестнадцатеричных символов")
                            return
                    
                    # Шифруем
                    if key_mode == "2 ключа (K1, K2, K1)":
                        ciphertext = self.triple_des_encrypt_2key(plaintext, k1, k2)
                        key_info = f"K1: {k1}, K2: {k2}"
                    else:
                        ciphertext = self.triple_des_encrypt_3key(plaintext, k1, k2, k3)
                        key_info = f"K1: {k1}, K2: {k2}, K3: {k3}"
                    
                    st.success("Зашифрованный текст (hex):")
                    st.code(ciphertext, language="text")
                    
                    # Показываем детали
                    self.show_3des_encryption_details(plaintext, key_info, ciphertext, key_mode)
                    
                except Exception as e:
                    st.error(f"Ошибка шифрования: {e}")
            else:
                st.error("Введите текст и все ключи")
    
    def render_3des_decryption(self):
        """Отрисовывает интерфейс дешифрования 3DES"""
        ciphertext = st.text_input(
            "Шифротекст (16 hex символов):",
            "A112BEDD6F8269A5",
            key="3des_dec_text",
            help="64-битный шифротекст в шестнадцатеричном формате"
        )
        
        key_mode = st.radio(
            "Режим ключей:",
            ["2 ключа (K1, K2, K1)", "3 ключа (K1, K2, K3)"],
            key="3des_dec_key_mode",
            horizontal=True
        )
        
        k1 = st.text_input(
            "Ключ 1 (16 hex символов):",
            "133457799BBCDFF1",
            key="3des_dec_k1"
        )
        
        k2 = st.text_input(
            "Ключ 2 (16 hex символов):",
            "0E329232EA6D0D73",
            key="3des_dec_k2"
        )
        
        if key_mode == "3 ключа (K1, K2, K3)":
            k3 = st.text_input(
                "Ключ 3 (16 hex символов):",
                "133457799BBCDFF1",
                key="3des_dec_k3"
            )
        else:
            k3 = k1
        
        if st.button("Дешифровать 3DES", key="3des_dec_btn", use_container_width=True):
            if ciphertext and k1 and k2 and (key_mode == "2 ключа" or k3):
                try:
                    # Проверяем длину шифротекста
                    if len(ciphertext) != 16:
                        st.error("Шифротекст должен содержать ровно 16 шестнадцатеричных символов")
                        return
                    
                    # Проверяем ключи
                    for key in [k1, k2, k3]:
                        if key and len(key) != 16:
                            st.error("Все ключи должны содержать ровно 16 шестнадцатеричных символов")
                            return
                    
                    # Дешифруем
                    if key_mode == "2 ключа (K1, K2, K1)":
                        plaintext = self.triple_des_decrypt_2key(ciphertext, k1, k2)
                    else:
                        plaintext = self.triple_des_decrypt_3key(ciphertext, k1, k2, k3)
                    
                    st.success("Дешифрованный текст:")
                    st.code(plaintext, language="text")
                    
                except Exception as e:
                    st.error(f"Ошибка дешифрования: {e}")
            else:
                st.error("Введите шифротекст и все ключи")
    
    def render_comparison_section(self):
        """Отрисовывает секцию сравнения с DES"""
        st.subheader("🎯 Сравнение DES и 3DES")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔐 DES")
            self.render_des_demo()
        
        with col2:
            st.markdown("### 🔒 3DES")
            self.render_3des_demo()
        
        # Сравнительная таблица
        st.markdown("---")
        self.render_comparison_table()
    
    def render_des_demo(self):
        """Демонстрация DES"""
        des_text = st.text_input(
            "Текст для DES:",
            "ABCD1234",
            key="des_demo_text"
        )
        
        des_key = st.text_input(
            "Ключ DES:",
            "133457799BBCDFF1",
            key="des_demo_key"
        )
        
        if st.button("Зашифровать DES", key="des_demo_btn"):
            if des_text and des_key:
                try:
                    # Используем DES из предыдущего модуля
                    from modules.modern_crypto.des import DESCipher
                    des_module = DESCipher()
                    
                    if len(des_text) != 8:
                        des_text = des_text[:8].ljust(8, ' ')
                    
                    ciphertext = des_module.des_encrypt(des_text, des_key)
                    
                    st.success("Результат DES:")
                    st.code(ciphertext, language="text")
                    
                    # Показываем информацию о ключе
                    key_bits = len(des_key) * 4  # hex символ = 4 бита
                    st.info(f"Размер ключа: {key_bits} бит")
                    
                except Exception as e:
                    st.error(f"Ошибка DES: {e}")
    
    def render_3des_demo(self):
        """Демонстрация 3DES"""
        tdes_text = st.text_input(
            "Текст для 3DES:",
            "ABCD1234",
            key="tdes_demo_text"
        )
        
        tdes_k1 = st.text_input(
            "Ключ 1:",
            "133457799BBCDFF1",
            key="tdes_demo_k1"
        )
        
        tdes_k2 = st.text_input(
            "Ключ 2:",
            "0E329232EA6D0D73",
            key="tdes_demo_k2"
        )
        
        if st.button("Зашифровать 3DES", key="tdes_demo_btn"):
            if tdes_text and tdes_k1 and tdes_k2:
                try:
                    if len(tdes_text) != 8:
                        tdes_text = tdes_text[:8].ljust(8, ' ')
                    
                    ciphertext = self.triple_des_encrypt_2key(tdes_text, tdes_k1, tdes_k2)
                    
                    st.success("Результат 3DES:")
                    st.code(ciphertext, language="text")
                    
                    # Показываем информацию о ключах
                    effective_bits = 112  # для 2-ключевого режима
                    st.info(f"Эффективный размер ключа: {effective_bits} бит")
                    
                except Exception as e:
                    st.error(f"Ошибка 3DES: {e}")
    
    def render_comparison_table(self):
        """Показывает сравнительную таблицу"""
        st.subheader("📊 Сравнительная таблица DES vs 3DES")
        
        comparison_data = {
            'Параметр': [
                'Размер блока', 
                'Размер ключа', 
                'Эффективный размер ключа',
                'Количество раундов',
                'Скорость',
                'Безопасность',
                'Год стандартизации',
                'Статус'
            ],
            'DES': [
                '64 бита',
                '56 бит',
                '56 бит',
                '16',
                'Быстро',
                'Небезопасен',
                '1977',
                'Устарел'
            ],
            '3DES (2 ключа)': [
                '64 бита',
                '112 бит',
                '112 бит',
                '48',
                'Средне',
                'Условно безопасен',
                '1998',
                'Используется'
            ],
            '3DES (3 ключа)': [
                '64 бита',
                '168 бит',
                '168 бит',
                '48',
                'Медленно',
                'Безопасен',
                '1998',
                'Используется'
            ]
        }
        
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Дополнительная информация
        st.markdown("""
        **Ключевые отличия:**
        - **Безопасность:** 3DES значительно безопаснее DES благодаря увеличенному размеру ключа
        - **Производительность:** 3DES в 3 раза медленнее DES
        - **Совместимость:** 3DES может эмулировать DES при K1=K2=K3
        """)
    
    def render_key_generation_section(self):
        """Отрисовывает секцию генерации ключей"""
        st.subheader("🔧 Генерация ключей 3DES")
        
        key_mode = st.radio(
            "Тип ключей:",
            ["2 ключа", "3 ключа"],
            key="key_gen_mode",
            horizontal=True
        )
        
        if st.button("Сгенерировать ключи", key="gen_3des_keys_btn"):
            try:
                if key_mode == "2 ключа":
                    k1 = secrets.token_hex(8).upper()
                    k2 = secrets.token_hex(8).upper()
                    keys = [k1, k2]
                    st.success("Сгенерированы 2 ключа 3DES:")
                else:
                    k1 = secrets.token_hex(8).upper()
                    k2 = secrets.token_hex(8).upper()
                    k3 = secrets.token_hex(8).upper()
                    keys = [k1, k2, k3]
                    st.success("Сгенерированы 3 ключа 3DES:")
                
                # Показываем ключи
                for i, key in enumerate(keys, 1):
                    col_key, col_copy = st.columns([3, 1])
                    with col_key:
                        st.text_input(f"Ключ {i}:", key, key=f"gen_key_{i}", disabled=True)
                    with col_copy:
                        if st.button("📋", key=f"copy_key_{i}"):
                            st.code(key, language="text")
                
                # Информация о безопасности
                effective_bits = 112 if key_mode == "2 ключа" else 168
                st.info(f"Эффективный размер ключа: {effective_bits} бит")
                st.info(f"Время взлома полным перебором: ~2^{effective_bits} операций")
                
            except Exception as e:
                st.error(f"Ошибка генерации ключей: {e}")
        
        # Рекомендации по ключам
        st.markdown("---")
        st.subheader("💡 Рекомендации по ключам")
        
        st.markdown("""
        **Требования к ключам 3DES:**
        - Все ключи должны быть независимыми
        - Избегать слабых и полуслабых ключей DES
        - Регулярно менять ключи
        - Использовать криптографически безопасные генераторы
        
        **Проверка ключей:**
        - K1 ≠ K2 ≠ K3 (для 3-ключевого режима)
        - K1 ≠ K2 (для 2-ключевого режима)
        - Избегать ключей с низкой энтропией
        """)
    
    def render_security_analysis(self):
        """Отрисовывает секцию анализа безопасности"""
        st.subheader("📊 Анализ безопасности 3DES")
        
        tab1, tab2, tab3 = st.tabs(["🔐 Стойкость", "⏱️ Время взлома", "🚨 Атаки"])
        
        with tab1:
            self.render_security_strength()
        
        with tab2:
            self.render_attack_times()
        
        with tab3:
            self.render_attacks_analysis()
    
    def render_security_strength(self):
        """Анализ стойкости"""
        st.markdown("**Криптографическая стойкость 3DES:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **3DES с 2 ключами (112 бит):**
            - Стойкость: 2¹¹² операций
            - Атака MitM: 2¹¹²
            - Практически неуязвим до 2030 года
            - Рекомендован для большинства применений
            
            **Преимущества:**
            - Проверенная безопасность
            - Широкая поддержка
            - Аппаратная эффективность
            """)
        
        with col2:
            st.markdown("""
            **3DES с 3 ключами (168 бит):**
            - Стойкость: 2¹⁶⁸ операций
            - Атака MitM: 2¹¹²
            - Очень высокая безопасность
            - Рекомендован для критических данных
            
            **Особенности:**
            - Максимальная безопасность
            - Совместимость с существующими системами
            - Медленнее чем 2-ключевой режим
            """)
    
    def render_attack_times(self):
        """Анализ времени взлома"""
        st.markdown("**Оценочное время взлома полным перебором:**")
        
        attack_data = {
            'Алгоритм': ['DES (56 бит)', '3DES-2KEY (112 бит)', '3DES-3KEY (168 бит)', 'AES-128'],
            'Количество операций': ['2⁵⁶', '2¹¹²', '2¹⁶⁸', '2¹²⁸'],
            'Время (1 млрд оп/сек)': ['400 дней', '10¹⁷ лет', '10³⁶ лет', '10²¹ лет'],
            'Стоимость взлома': ['$10,000', '$10¹⁸', '$10³⁷', '$10²²']
        }
        
        df = pd.DataFrame(attack_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Примечания:**
        - Время указано для атаки полным перебором
        - 1 млрд операций в секунду - современные суперкомпьютеры
        - 3DES-2KEY считается безопасным до 2030 года
        - 3DES-3KEY обеспечивает очень высокую безопасность
        """)
    
    def render_attacks_analysis(self):
        """Анализ атак на 3DES"""
        st.markdown("**Известные атаки на 3DES:**")
        
        attacks_data = {
            'Тип атаки': ['Полный перебор', 'MitM', 'Дифференциальный', 'Линейный', 'Связанные ключи'],
            'Эффективность против DES': ['2⁵⁶', 'Не применима', '2⁴⁷', '2⁴³', '2⁵⁶'],
            'Эффективность против 3DES': ['2¹¹²', '2¹¹²', '2¹⁰⁶', '2¹⁰⁵', '2⁵⁶'],
            'Практичность': ['Практична', 'Теоретическая', 'Теоретическая', 'Теоретическая', 'Теоретическая']
        }
        
        df = pd.DataFrame(attacks_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Выводы:**
        - 3DES значительно безопаснее DES против всех известных атак
        - Атака MitM ограничивает эффективный размер ключа 112 битами
        - Для максимальной безопасности рекомендуется 3-ключевой режим
        """)
    
    # Основные функции 3DES
    
    def des_encrypt(self, plaintext: str, key_hex: str) -> str:
        """Шифрует текст с помощью DES (упрощенная реализация)"""
        # Импортируем DES модуль
        try:
            from modules.modern_crypto.des import DESCipher
            des_module = DESCipher()
            return des_module.des_encrypt(plaintext, key_hex)
        except ImportError:
            # Резервная реализация, если модуль DES недоступен
            st.warning("Модуль DES недоступен, используется упрощенная реализация")
            return self._simple_des_encrypt(plaintext, key_hex)
    
    def des_decrypt(self, ciphertext_hex: str, key_hex: str) -> str:
        """Дешифрует текст с помощью DES"""
        try:
            from modules.modern_crypto.des import DESCipher
            des_module = DESCipher()
            return des_module.des_decrypt(ciphertext_hex, key_hex)
        except ImportError:
            st.warning("Модуль DES недоступен, используется упрощенная реализация")
            return self._simple_des_decrypt(ciphertext_hex, key_hex)
    
    def _simple_des_encrypt(self, plaintext: str, key_hex: str) -> str:
        """Упрощенная реализация DES для демонстрации"""
        # Это упрощенная версия - в реальном использовании должен быть полный DES
        import hashlib
        # Используем хеш для имитации шифрования
        combined = plaintext + key_hex
        hash_obj = hashlib.md5(combined.encode())
        return hash_obj.hexdigest()[:16].upper()
    
    def _simple_des_decrypt(self, ciphertext_hex: str, key_hex: str) -> str:
        """Упрощенная реализация дешифрования DES"""
        # В реальной реализации здесь должен быть полный DES
        return "DECRYPTED"
    
    def triple_des_encrypt_2key(self, plaintext: str, k1: str, k2: str) -> str:
        """Шифрование 3DES с 2 ключами (K1, K2, K1)"""
        # E(K1) -> D(K2) -> E(K1)
        step1 = self.des_encrypt(plaintext, k1)  # Шифрование K1
        step2 = self.des_decrypt(step1, k2)      # Дешифрование K2
        step3 = self.des_encrypt(step2, k1)      # Шифрование K1
        return step3
    
    def triple_des_decrypt_2key(self, ciphertext: str, k1: str, k2: str) -> str:
        """Дешифрование 3DES с 2 ключами (K1, K2, K1)"""
        # D(K1) -> E(K2) -> D(K1)
        step1 = self.des_decrypt(ciphertext, k1)  # Дешифрование K1
        step2 = self.des_encrypt(step1, k2)       # Шифрование K2
        step3 = self.des_decrypt(step2, k1)       # Дешифрование K1
        return step3
    
    def triple_des_encrypt_3key(self, plaintext: str, k1: str, k2: str, k3: str) -> str:
        """Шифрование 3DES с 3 ключами (K1, K2, K3)"""
        # E(K1) -> D(K2) -> E(K3)
        step1 = self.des_encrypt(plaintext, k1)  # Шифрование K1
        step2 = self.des_decrypt(step1, k2)      # Дешифрование K2
        step3 = self.des_encrypt(step2, k3)      # Шифрование K3
        return step3
    
    def triple_des_decrypt_3key(self, ciphertext: str, k1: str, k2: str, k3: str) -> str:
        """Дешифрование 3DES с 3 ключами (K1, K2, K3)"""
        # D(K3) -> E(K2) -> D(K1)
        step1 = self.des_decrypt(ciphertext, k3)  # Дешифрование K3
        step2 = self.des_encrypt(step1, k2)       # Шифрование K2
        step3 = self.des_decrypt(step2, k1)       # Дешифрование K1
        return step3
    
    def show_3des_encryption_details(self, plaintext: str, key_info: str, ciphertext: str, key_mode: str):
        """Показывает детали шифрования 3DES"""
        st.markdown("**🔍 Детали процесса 3DES:**")
        
        # Показываем схему шифрования
        if key_mode == "2 ключа (K1, K2, K1)":
            st.markdown("""
            **Схема шифрования (EDE):**
            ```
            Plaintext
                ↓
            E(K1) → Шифрование ключом 1
                ↓
            D(K2) → Дешифрование ключом 2  
                ↓
            E(K1) → Шифрование ключом 1
                ↓
            Ciphertext
            ```
            """)
        else:
            st.markdown("""
            **Схема шифрования (EDE):**
            ```
            Plaintext
                ↓
            E(K1) → Шифрование ключом 1
                ↓
            D(K2) → Дешифрование ключом 2
                ↓  
            E(K3) → Шифрование ключом 3
                ↓
            Ciphertext
            ```
            """)
        
        # Статистика
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Режим ключей", key_mode)
        
        with col2:
            effective_bits = 112 if "2 ключа" in key_mode else 168
            st.metric("Эффективный ключ", f"{effective_bits} бит")
        
        with col3:
            st.metric("Раундов шифрования", "48")
        
        # Информация о ключах
        st.markdown(f"**Использованные ключи:** {key_info}")

# Для обратной совместимости
class TripleDESCipher(TripleDESModule):
    pass
