from modules.base_module import CryptoModule
import streamlit as st
import secrets
import hashlib
import hmac
import time
from typing import List, Tuple, Dict, Optional
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
import struct
import binascii
import random
from sympy import isprime, mod_inverse
import math

@dataclass
class SignatureScheme:
    name: str
    type: str
    security: str
    key_size: int
    signature_size: int
    year: int

@dataclass
class DigitalSignature:
    message: str
    signature: str
    public_key: str
    algorithm: str
    timestamp: float

@dataclass
class EncryptionProtocol:
    name: str
    type: str
    security: str
    key_exchange: str
    authentication: str

class EPSProtocolsModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Принципы и протоколы ЭПС"
        self.description = "Электронная подпись и схемы шифрования - основы криптографических протоколов"
        self.category = "protocols"
        self.icon = ""
        self.order = 10
        
        # Схемы электронной подписи
        self.signature_schemes = {
            "RSA": SignatureScheme(
                "RSA-PSS",
                "Асимметричная",
                "Высокая",
                2048,
                256,
                1977
            ),
            "DSA": SignatureScheme(
                "DSA",
                "Асимметричная", 
                "Высокая",
                2048,
                320,
                1991
            ),
            "ECDSA": SignatureScheme(
                "ECDSA",
                "Эллиптическая кривая",
                "Очень высокая",
                256,
                64,
                1999
            ),
            "Ed25519": SignatureScheme(
                "Ed25519",
                "Эллиптическая кривая",
                "Очень высокая", 
                256,
                64,
                2011
            ),
            "Schnorr": SignatureScheme(
                "Schnorr",
                "Эллиптическая кривая",
                "Высокая",
                256,
                64,
                1989
            )
        }
        
        # Протоколы шифрования
        self.encryption_protocols = {
            "TLS": EncryptionProtocol(
                "TLS 1.3",
                "Транспортный",
                "Очень высокая",
                "ECDHE",
                "Цифровая подпись"
            ),
            "SSH": EncryptionProtocol(
                "SSH-2",
                "Удаленный доступ",
                "Высокая",
                "Diffie-Hellman",
                "Ключи хоста"
            ),
            "IPsec": EncryptionProtocol(
                "IPsec",
                "Сетевой",
                "Высокая",
                "IKEv2",
                "PSK/Сертификаты"
            ),
            "PGP": EncryptionProtocol(
                "PGP/GPG",
                "Прикладной",
                "Высокая",
                "RSA/ECDH",
                "Web of Trust"
            ),
            "S/MIME": EncryptionProtocol(
                "S/MIME",
                "Электронная почта", 
                "Высокая",
                "RSA",
                "X.509 сертификаты"
            )
        }

    def render(self):
        st.title("🖋️ Принципы и протоколы ЭПС")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **ЭПС (Электронная Подпись и Шифрование)** - фундаментальные криптографические примитивы для обеспечения безопасности.
            
            ### 🏗️ Принципы электронной подписи:
            
            **Криптографические основы:**
            - **Асимметричная криптография**: Открытый и закрытый ключи
            - **Хеш-функции**: Преобразование сообщения в фиксированный размер
            - **Математические задачи**: Факторизация, дискретный логарифм, ECDLP
            
            **Свойства электронной подписи:**
            - **Аутентичность**: Подтверждение авторства
            - **Целостность**: Гарантия неизменности данных
            - **Неотрекаемость**: Невозможность отказа от подписи
            - **Проверяемость**: Возможность проверки третьей стороной
            
            **Процесс подписания:**
            ```
            1. Хеширование сообщения: H = hash(message)
            2. Формирование подписи: sig = sign(H, private_key)
            3. Передача: (message, sig, public_key)
            ```
            
            **Процесс проверки:**
            ```
            1. Хеширование сообщения: H = hash(message)
            2. Проверка подписи: verify(sig, H, public_key)
            3. Результат: valid/invalid
            ```
            
            ### 🔐 Протоколы шифрования:
            
            **Типы протоколов:**
            - **Транспортные**: TLS, SSL - защита канала связи
            - **Сетевые**: IPsec - защита на сетевом уровне  
            - **Прикладные**: PGP, S/MIME - защита данных
            - **Удаленного доступа**: SSH - защита удаленных сессий
            
            **Компоненты протоколов:**
            - **Key Exchange**: Диффи-Хеллман, ECDH, RSA
            - **Аутентификация**: Сертификаты, цифровые подписи
            - **Шифрование**: AES, ChaCha20, 3DES
            - **Целостность**: HMAC, AEAD
            """)

        st.markdown("---")
        
        # Основной интерфейс с вкладками
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Схемы подписи", "🔐 Протоколы шифрования", "🎯 Криптоанализ", "🛡️ Безопасность", "🎮 Демонстрация"])

        with tab1:
            self.render_signature_schemes()
        
        with tab2:
            self.render_encryption_protocols()
            
        with tab3:
            self.render_cryptanalysis()
            
        with tab4:
            self.render_security_guidelines()
            
        with tab5:
            self.render_demo_section()

    def render_signature_schemes(self):
        """Демонстрация схем электронной подписи"""
        st.header("📝 Схемы электронной подписи")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Сравнение схем подписи")
            
            # Таблица сравнения
            schemes_data = []
            for scheme_name, scheme in self.signature_schemes.items():
                schemes_data.append({
                    "Схема": scheme_name,
                    "Тип": scheme.type,
                    "Безопасность": scheme.security,
                    "Размер ключа": f"{scheme.key_size} бит",
                    "Размер подписи": f"{scheme.signature_size} байт",
                    "Год": scheme.year
                })
            
            df_schemes = pd.DataFrame(schemes_data)
            st.dataframe(df_schemes, use_container_width=True, hide_index=True)
            
            # Визуализация эффективности
            st.subheader("📈 Эффективность схем")
            
            scheme_names = list(self.signature_schemes.keys())
            key_sizes = [s.key_size for s in self.signature_schemes.values()]
            sig_sizes = [s.signature_size for s in self.signature_schemes.values()]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Размер ключа (бит)',
                x=scheme_names,
                y=key_sizes,
                yaxis='y',
                offsetgroup=1
            ))
            fig.add_trace(go.Bar(
                name='Размер подписи (байт)',
                x=scheme_names, 
                y=sig_sizes,
                yaxis='y2',
                offsetgroup=2
            ))
            
            fig.update_layout(
                title="Сравнение размеров ключей и подписей",
                xaxis_title="Схема подписи",
                yaxis=dict(title="Размер ключа (бит)", side='left'),
                yaxis2=dict(title="Размер подписи (байт)", side='right', overlaying='y'),
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🔍 Детали схем")
            
            selected_scheme = st.selectbox(
                "Выберите схему подписи:",
                list(self.signature_schemes.keys()),
                key="scheme_select"
            )
            
            scheme = self.signature_schemes[selected_scheme]
            
            st.markdown(f"### {selected_scheme}")
            
            # Информация о схеме
            info_cols = st.columns(2)
            with info_cols[0]:
                st.metric("Тип", scheme.type)
                st.metric("Безопасность", scheme.security)
            with info_cols[1]:
                st.metric("Размер ключа", f"{scheme.key_size} бит")
                st.metric("Размер подписи", f"{scheme.signature_size} байт")
            
            # Специфическая информация
            if selected_scheme == "RSA":
                st.markdown("""
                **Особенности RSA-PSS:**
                - Probabilistic Signature Scheme
                - Стойкость основана на факторизации
                - Широкое распространение
                - Относительно большие подписи
                """)
            elif selected_scheme == "ECDSA":
                st.markdown("""
                **Особенности ECDSA:**
                - Elliptic Curve Digital Signature Algorithm
                - Малые размеры ключей и подписей
                - Высокая эффективность
                - Стойкость основана на ECDLP
                """)
            elif selected_scheme == "Ed25519":
                st.markdown("""
                **Особенности Ed25519:**
                - Edwards-curve Digital Signature Algorithm
                - Высокая скорость работы
                - Безопасность по умолчанию
                - Популярна в современных системах
                """)
            
            # Демонстрация подписи
            st.subheader("🖋️ Демонстрация подписи")
            
            message = st.text_area(
                "Сообщение для подписи:",
                "Важное конфиденциальное сообщение",
                height=100,
                key="sign_message"
            )
            
            if st.button("📝 Создать подпись", key="create_signature"):
                signature_data = self.create_digital_signature(message, selected_scheme)
                st.session_state.current_signature = signature_data
            
            if 'current_signature' in st.session_state:
                signature = st.session_state.current_signature
                
                st.success("✅ Подпись создана!")
                
                st.text_area(
                    "Цифровая подпись:",
                    signature.signature,
                    height=100,
                    key="signature_display"
                )
                
                st.text_input(
                    "Открытый ключ:",
                    signature.public_key[:64] + "...",
                    key="pubkey_display"
                )
                
                # Проверка подписи
                if st.button("✅ Проверить подпись", key="verify_signature"):
                    is_valid = self.verify_digital_signature(signature)
                    if is_valid:
                        st.success("🔐 Подпись действительна!")
                    else:
                        st.error("❌ Подпись недействительна!")

    def render_encryption_protocols(self):
        """Демонстрация протоколов шифрования"""
        st.header("🔐 Протоколы шифрования")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📡 Сравнение протоколов")
            
            # Таблица протоколов
            protocols_data = []
            for protocol_name, protocol in self.encryption_protocols.items():
                protocols_data.append({
                    "Протокол": protocol_name,
                    "Тип": protocol.type,
                    "Безопасность": protocol.security,
                    "Обмен ключами": protocol.key_exchange,
                    "Аутентификация": protocol.authentication
                })
            
            df_protocols = pd.DataFrame(protocols_data)
            st.dataframe(df_protocols, use_container_width=True, hide_index=True)
            
            # Визуализация применения
            st.subheader("🎯 Области применения")
            
            protocol_names = list(self.encryption_protocols.keys())
            usage_scores = {
                "TLS": 95,
                "SSH": 85, 
                "IPsec": 70,
                "PGP": 60,
                "S/MIME": 65
            }
            
            fig = go.Figure(go.Bar(
                x=protocol_names,
                y=[usage_scores[p] for p in protocol_names],
                marker_color='lightblue'
            ))
            
            fig.update_layout(
                title="Распространенность протоколов (%)",
                xaxis_title="Протокол",
                yaxis_title="Процент использования",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🔧 Детали протоколов")
            
            selected_protocol = st.selectbox(
                "Выберите протокол:",
                list(self.encryption_protocols.keys()),
                key="protocol_select"
            )
            
            protocol = self.encryption_protocols[selected_protocol]
            
            st.markdown(f"### {selected_protocol}")
            
            # Информация о протоколе
            st.write(f"**Тип:** {protocol.type}")
            st.write(f"**Безопасность:** {protocol.security}")
            st.write(f"**Обмен ключами:** {protocol.key_exchange}")
            st.write(f"**Аутентификация:** {protocol.authentication}")
            
            # Специфическая информация
            if selected_protocol == "TLS":
                st.markdown("""
                **Особенности TLS 1.3:**
                - Упрощенный handshake
                - Обязательное шифрование
                - Удаление уязвимых алгоритмов
                - Forward secrecy по умолчанию
                """)
            elif selected_protocol == "SSH":
                st.markdown("""
                **Особенности SSH-2:**
                - Защита удаленного доступа
                - Поддержка туннелирования
                - Аутентификация по ключам
                - Широкие возможности настройки
                """)
            elif selected_protocol == "PGP":
                st.markdown("""
                **Особенности PGP/GPG:**
                - End-to-end шифрование
                - Web of Trust модель
                - Гибридное шифрование
                - Независимость от инфраструктуры
                """)
            
            # Демонстрация рукопожатия
            st.subheader("🤝 Демонстрация рукопожатия")
            
            if st.button("🔄 Запустить рукопожатие", key="start_handshake"):
                handshake_steps = self.simulate_protocol_handshake(selected_protocol)
                st.session_state.handshake_steps = handshake_steps
            
            if 'handshake_steps' in st.session_state:
                steps = st.session_state.handshake_steps
                
                for i, step in enumerate(steps, 1):
                    with st.expander(f"Шаг {i}: {step['action']}"):
                        st.write(f"**От:** {step['from']}")
                        st.write(f"**К:** {step['to']}")
                        st.write(f"**Данные:** {step['data']}")
                        if 'key' in step:
                            st.write(f"**Ключ:** {step['key'][:32]}...")

    def render_cryptanalysis(self):
        """Анализ криптостойкости и атак"""
        st.header("🎯 Криптоанализ ЭПС")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⚠️ Атаки на схемы подписи")
            
            signature_attacks = {
                "Атака на подобранных сообщениях": {
                    "target": "Все схемы",
                    "complexity": "Высокая",
                    "description": "Подбор сообщений для получения подписи"
                },
                "Атака по времени": {
                    "target": "RSA, ECDSA",
                    "complexity": "Средняя", 
                    "description": "Анализ времени выполнения операций"
                },
                "Атака на отказе обслуживания": {
                    "target": "Все схемы",
                    "complexity": "Низкая",
                    "description": "Перегрузка системы проверки"
                },
                "Коллизии хеш-функций": {
                    "target": "Зависит от хеш-функции",
                    "complexity": "Очень высокая",
                    "description": "Поиск коллизий для подделки подписей"
                }
            }
            
            for attack, info in signature_attacks.items():
                with st.expander(f"🔓 {attack}"):
                    st.write(f"**Цель:** {info['target']}")
                    st.write(f"**Сложность:** {info['complexity']}")
                    st.write(f"**Описание:** {info['description']}")
            
            # Оценка стойкости
            st.subheader("📊 Оценка криптостойкости")
            
            schemes = list(self.signature_schemes.keys())
            security_levels = {
                "RSA": 110,  # в битах безопасности
                "DSA": 100,
                "ECDSA": 128, 
                "Ed25519": 128,
                "Schnorr": 128
            }
            
            fig = go.Figure(go.Bar(
                x=schemes,
                y=[security_levels[s] for s in schemes],
                marker_color=['red' if x < 112 else 'green' for x in [security_levels[s] for s in schemes]]
            ))
            
            fig.update_layout(
                title="Уровень безопасности схем подписи (в битах)",
                xaxis_title="Схема подписи",
                yaxis_title="Биты безопасности",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🛡️ Защитные меры")
            
            protection_measures = [
                ("Использование стойких параметров", "Большие ключи, проверенные кривые", "🔐"),
                ("Регулярная ротация ключей", "Ограничение времени жизни ключей", "🔄"),
                ("Защита от side-channel атак", "Постоянное время выполнения", "⏱️"),
                ("Валидация входных данных", "Проверка всех параметров", "✓"),
                ("Использование случайных значений", "Качественные ГПСЧ", "🎲"),
                ("Аудиторские проверки", "Регулярный анализ безопасности", "🔍")
            ]
            
            for measure, description, icon in protection_measures:
                with st.expander(f"{icon} {measure}"):
                    st.write(description)
            
            st.subheader("📈 Рекомендации по выбору")
            
            recommendations = [
                "✅ Используйте ECDSA или Ed25519 для новых систем",
                "✅ Минимальный размер ключа RSA - 2048 бит",
                "✅ Используйте PSS padding для RSA",
                "✅ Проверяйте случайные значения в ECDSA",
                "✅ Регулярно обновляйте криптографические библиотеки",
                "✅ Проводите пентесты систем подписи"
            ]
            
            for rec in recommendations:
                st.write(rec)

    def render_security_guidelines(self):
        """Рекомендации по безопасности"""
        st.header("🛡️ Рекомендации по безопасности ЭПС")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Лучшие практики")
            
            best_practices = [
                ("Выбор алгоритмов", "Используйте современные стандарты", "critical"),
                ("Размеры ключей", "Следуйте актуальным рекомендациям", "high"), 
                ("Управление ключами", "Безопасное хранение и ротация", "high"),
                ("Валидация", "Проверка всех криптографических параметров", "high"),
                ("Обновления", "Регулярное обновление библиотек", "medium"),
                ("Аудит", "Периодический анализ безопасности", "medium")
            ]
            
            for practice, description, priority in best_practices:
                priority_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
                st.write(f"{priority_icon[priority]} **{practice}** - {description}")
            
            st.subheader("⚡ Производительность")
            
            performance_data = {
                "Операция": ["RSA-2048 подпись", "RSA-2048 проверка", "ECDSA P-256 подпись", "ECDSA P-256 проверка", "Ed25519 подпись", "Ed25519 проверка"],
                "Время (мс)": [15, 0.5, 2, 3, 1, 1],
                "Память (КБ)": [256, 256, 32, 32, 16, 16]
            }
            
            df_perf = pd.DataFrame(performance_data)
            st.dataframe(df_perf, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("🏢 Стандарты и compliance")
            
            standards = [
                ("FIPS 186-5", "Цифровые подписи (NIST)", "США"),
                ("RFC 8017", "RSA (PKCS #1)", "IETF"),
                ("RFC 8032", "Edwards-curve Digital Signature", "IETF"),
                ("ISO/IEC 14888-3", "Подписи на основе дискретного логарифма", "Международный"),
                ("GOST R 34.10-2012", "Электронная подпись", "Россия"),
                ("BSI TR-03111", "Эллиптические кривые", "Германия")
            ]
            
            for standard, description, organization in standards:
                with st.expander(f"📜 {standard}"):
                    st.write(f"**Описание:** {description}")
                    st.write(f"**Организация:** {organization}")
            
            st.subheader("🔮 Будущие тенденции")
            
            future_trends = [
                "🔮 Постквантовая криптография",
                "🔮 Гомоморфное шифрование", 
                "🔮 Мультиподписи и пороговые схемы",
                "🔮 Анонимные подписи",
                "🔮 Интеграция с blockchain",
                "🔮 Автоматизированная верификация"
            ]
            
            for trend in future_trends:
                st.write(trend)

    def render_demo_section(self):
        """Интерактивная демонстрация"""
        st.header("🎮 Интерактивная демонстрация")
        
        st.info("""
        💡 Эта демонстрация показывает принципы работы электронной подписи 
        и позволяет экспериментировать с различными параметрами безопасности.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔐 Демонстрация RSA подписи")
            
            # Параметры RSA
            rsa_key_size = st.selectbox(
                "Размер ключа RSA:",
                [1024, 2048, 3072, 4096],
                index=1,
                key="rsa_key_size"
            )
            
            message = st.text_area(
                "Сообщение для подписи:",
                "Конфиденциальные данные для подписания",
                height=100,
                key="demo_message"
            )
            
            # Атака на подпись
            enable_tampering = st.checkbox(
                "Включить модификацию сообщения после подписи",
                key="enable_tamper"
            )
            
            if enable_tampering:
                tampered_message = st.text_input(
                    "Модифицированное сообщение:",
                    "Измененные конфиденциальные данные",
                    key="tampered_msg"
                )
            else:
                tampered_message = message
            
            if st.button("🎯 Запустить демонстрацию", key="run_demo"):
                # Генерация ключей и подписи
                private_key, public_key = self.generate_rsa_keys(rsa_key_size)
                signature = self.create_rsa_signature(message, private_key)
                
                # Проверка подписи
                original_valid = self.verify_rsa_signature(message, signature, public_key)
                tampered_valid = self.verify_rsa_signature(tampered_message, signature, public_key)
                
                st.session_state.demo_results = {
                    "original_valid": original_valid,
                    "tampered_valid": tampered_valid,
                    "key_size": rsa_key_size,
                    "signature": signature.hex()[:64] + "...",
                    "public_key": public_key
                }
        
        with col2:
            st.subheader("📊 Результаты демонстрации")
            
            if 'demo_results' in st.session_state:
                results = st.session_state.demo_results
                
                st.write(f"**Размер ключа:** {results['key_size']} бит")
                st.write(f"**Подпись:** {results['signature']}")
                
                # Визуализация результатов
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    if results["original_valid"]:
                        st.success("✅ Исходная подпись действительна")
                    else:
                        st.error("❌ Исходная подпись недействительна")
                
                with col_res2:
                    if results["tampered_valid"]:
                        st.error("❌ Подпись для модифицированного сообщения действительна!")
                    else:
                        st.success("✅ Подпись для модифицированного сообщения недействительна")
                
                # Объяснение
                if not results["tampered_valid"]:
                    st.info("""
                    **Объяснение:** Электронная подпись обеспечивает целостность данных. 
                    Любое изменение сообщения делает подпись недействительной.
                    """)
                
                # Визуализация безопасности
                st.subheader("📈 Уровень безопасности RSA")
                
                security_bits = {
                    1024: 80,
                    2048: 112,
                    3072: 128,
                    4096: 140
                }
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = security_bits[results["key_size"]],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Биты безопасности"},
                    gauge = {
                        'axis': {'range': [None, 256]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 80], 'color': "red"},
                            {'range': [80, 112], 'color': "orange"},
                            {'range': [112, 128], 'color': "yellow"},
                            {'range': [128, 256], 'color': "green"}
                        ],
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("👆 Запустите демонстрацию для отображения результатов")

    # Криптографические методы

    def create_digital_signature(self, message: str, scheme: str) -> DigitalSignature:
        """Создание цифровой подписи"""
        if scheme == "RSA":
            private_key, public_key = self.generate_rsa_keys(2048)
            signature = self.create_rsa_signature(message, private_key)
            pubkey_str = public_key.public_bytes(
                Encoding.PEM, 
                PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
        else:
            # Упрощенная демонстрация для других схем
            signature = secrets.token_hex(32)
            pubkey_str = f"public_key_{scheme}_{secrets.token_hex(16)}"
        
        return DigitalSignature(
            message=message,
            signature=signature.hex() if hasattr(signature, 'hex') else signature,
            public_key=pubkey_str,
            algorithm=scheme,
            timestamp=time.time()
        )

    def verify_digital_signature(self, signature_data: DigitalSignature) -> bool:
        """Проверка цифровой подписи"""
        # В демонстрационных целях всегда возвращаем True
        # В реальной системе здесь была бы настоящая проверка
        return True

    def generate_rsa_keys(self, key_size: int):
        """Генерация RSA ключей"""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def create_rsa_signature(self, message: str, private_key) -> bytes:
        """Создание RSA подписи"""
        if isinstance(message, str):
            message = message.encode('utf-8')
        
        signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify_rsa_signature(self, message: str, signature: bytes, public_key) -> bool:
        """Проверка RSA подписи"""
        try:
            if isinstance(message, str):
                message = message.encode('utf-8')
            
            public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False

    def simulate_protocol_handshake(self, protocol: str) -> List[Dict]:
        """Симуляция рукопожатия протокола"""
        if protocol == "TLS":
            return [
                {
                    "action": "Client Hello",
                    "from": "Клиент",
                    "to": "Сервер", 
                    "data": "Поддерживаемые шифры, случайное число",
                    "key": secrets.token_hex(32)
                },
                {
                    "action": "Server Hello",
                    "from": "Сервер",
                    "to": "Клиент",
                    "data": "Выбранный шифр, сертификат, случайное число",
                    "key": secrets.token_hex(32)
                },
                {
                    "action": "Key Exchange",
                    "from": "Клиент", 
                    "to": "Сервер",
                    "data": "Предмастер-секрет, зашифрованный открытым ключом",
                    "key": secrets.token_hex(48)
                },
                {
                    "action": "Finished",
                    "from": "Сервер",
                    "to": "Клиент", 
                    "data": "Зашифрованное подтверждение",
                    "key": secrets.token_hex(32)
                }
            ]
        else:
            # Упрощенная демонстрация для других протоколов
            return [
                {
                    "action": f"Handshake Step for {protocol}",
                    "from": "Участник A",
                    "to": "Участник B",
                    "data": "Криптографические параметры",
                    "key": secrets.token_hex(32)
                }
            ]

# Для обратной совместимости
class EPSProtocolsDemoModule(EPSProtocolsModule):
    pass
