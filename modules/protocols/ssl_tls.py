from modules.base_module import CryptoModule
import streamlit as st
import secrets
import hashlib
import time
from typing import List, Tuple, Dict, Optional
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import io

@dataclass
class TLSCipherSuite:
    name: str
    key_exchange: str
    authentication: str
    encryption: str
    mac: str
    bits: int

@dataclass
class TLSHandshakeMessage:
    type: str
    content: Dict
    timestamp: float

@dataclass
class TLSSession:
    version: str
    cipher_suite: TLSCipherSuite
    client_random: str
    server_random: str
    pre_master_secret: str
    master_secret: str
    client_write_key: str
    server_write_key: str
    client_write_iv: str
    server_write_iv: str

@dataclass
class Certificate:
    subject: str
    issuer: str
    public_key: str
    validity: Tuple[datetime, datetime]
    signature: str

class SSL_TLS_Module(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Протокол SSL/TLS"
        self.description = "Secure Sockets Layer / Transport Layer Security - защищенная коммуникация"
        self.category = "protocols"
        self.icon = ""
        self.order = 6
        
        # Поддерживаемые версии TLS
        self.tls_versions = {
            "SSL 3.0": {"year": 1996, "status": "Устарел", "security": "Небезопасен"},
            "TLS 1.0": {"year": 1999, "status": "Устарел", "security": "Слабый"},
            "TLS 1.1": {"year": 2006, "status": "Устаревший", "security": "Умеренный"},
            "TLS 1.2": {"year": 2008, "status": "Активный", "security": "Сильный"},
            "TLS 1.3": {"year": 2018, "status": "Современный", "security": "Очень сильный"}
        }
        
        # Наборы шифров
        self.cipher_suites = {
            "TLS_AES_256_GCM_SHA384": TLSCipherSuite(
                "TLS_AES_256_GCM_SHA384", "ECDHE", "RSA", "AES_256_GCM", "SHA384", 256
            ),
            "TLS_AES_128_GCM_SHA256": TLSCipherSuite(
                "TLS_AES_128_GCM_SHA256", "ECDHE", "RSA", "AES_128_GCM", "SHA256", 128
            ),
            "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384": TLSCipherSuite(
                "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384", "ECDHE", "RSA", "AES_256_GCM", "SHA384", 256
            ),
            "TLS_RSA_WITH_AES_256_CBC_SHA256": TLSCipherSuite(
                "TLS_RSA_WITH_AES_256_CBC_SHA256", "RSA", "RSA", "AES_256_CBC", "SHA256", 256
            )
        }
        
        # Демонстрационные сертификаты
        self.demo_certificates = self.generate_demo_certificates()
        
        # Активные сессии
        self.active_sessions = {}

    def render(self):
        st.title("🔒 Протокол SSL/TLS")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **SSL/TLS** - криптографические протоколы для защищенной коммуникации в компьютерных сетях.
            
            ### 🎯 Историческая эволюция:
            - **SSL 1.0** (1994) - никогда не выпущен
            - **SSL 2.0** (1995) - серьезные уязвимости
            - **SSL 3.0** (1996) - основа для TLS
            - **TLS 1.0** (1999) - первая стандартизированная версия
            - **TLS 1.1** (2006) - защита от CBC-атак
            - **TLS 1.2** (2008) - современные алгоритмы
            - **TLS 1.3** (2018) - улучшенная безопасность и производительность
            
            ### 🔐 Ключевые цели безопасности:
            - **Конфиденциальность** - шифрование данных
            - **Целостность** - защита от модификации
            - **Аутентификация** - проверка сторон
            - **Perfect Forward Secrecy** - защита прошлых сессий
            
            ### 🏗️ Архитектура TLS 1.2 Handshake:
            
            ```
            ClientHello           →  
                                  ←   ServerHello
                                  ←   Certificate*
                                  ←   ServerKeyExchange*
                                  ←   CertificateRequest*
                                  ←   ServerHelloDone
            Certificate*          →
            ClientKeyExchange     →
            CertificateVerify*    →
            ChangeCipherSpec      →
            Finished              →
                                  ←   ChangeCipherSpec
                                  ←   Finished
            Application Data      ↔   Application Data
            ```
            
            ### 🚀 Улучшения в TLS 1.3:
            - 1-RTT handshake (вместо 2-RTT)
            - Удалены небезопасные алгоритмы
            - Обязательный PFS (Perfect Forward Secrecy)
            - Улучшенная защита от downgrade-атак
            """)

        st.markdown("---")
        
        # Основной интерфейс с вкладками
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🤝 Handshake Process", "🔐 Шифрование данных", "📜 Сертификаты", "📊 Анализ безопасности", "🛡️ Атаки и защита"])

        with tab1:
            self.render_handshake_section()
        
        with tab2:
            self.render_encryption_section()
            
        with tab3:
            self.render_certificates_section()
            
        with tab4:
            self.render_security_analysis_section()
            
        with tab5:
            self.render_attacks_protection_section()

    def render_handshake_section(self):
        """Визуализация процесса TLS Handshake"""
        st.header("🤝 Процесс TLS Handshake")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("⚙️ Параметры соединения")
            
            version = st.selectbox(
                "Версия TLS:",
                list(self.tls_versions.keys()),
                format_func=lambda x: f"{x} ({self.tls_versions[x]['year']}) - {self.tls_versions[x]['status']}",
                key="tls_version"
            )
            
            cipher_suite = st.selectbox(
                "Набор шифров:",
                list(self.cipher_suites.keys()),
                key="cipher_suite"
            )
            
            client_name = st.text_input("Клиент:", "client.example.com", key="client_name")
            server_name = st.text_input("Сервер:", "server.example.com", key="server_name")
            
            if st.button("🚀 Запустить TLS Handshake", key="handshake_btn", use_container_width=True):
                # Запускаем процесс handshake
                session = self.simulate_tls_handshake(version, cipher_suite, client_name, server_name)
                st.session_state.tls_session = session
                st.session_state.handshake_messages = self.generate_handshake_messages(session)
                st.rerun()
        
        with col2:
            st.subheader("🔑 Ключи сессии")
            
            if 'tls_session' in st.session_state:
                session = st.session_state.tls_session
                
                st.success("✅ TLS Handshake завершен!")
                
                with st.expander("🔐 Ключевой материал"):
                    st.text(f"Client Random: {session.client_random[:32]}...")
                    st.text(f"Server Random: {session.server_random[:32]}...")
                    st.text(f"Pre-Master Secret: {session.pre_master_secret[:32]}...")
                    st.text(f"Master Secret: {session.master_secret[:32]}...")
                    st.text(f"Client Write Key: {session.client_write_key[:32]}...")
                    st.text(f"Server Write Key: {session.server_write_key[:32]}...")
            
        # Визуализация handshake процесса
        if 'handshake_messages' in st.session_state:
            st.subheader("🔄 Визуализация Handshake")
            self.visualize_handshake_process(st.session_state.handshake_messages)

    def render_encryption_section(self):
        """Шифрование данных в TLS"""
        st.header("🔐 Шифрование данных в TLS")
        
        if 'tls_session' not in st.session_state:
            st.warning("⚠️ Сначала выполните TLS Handshake")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📨 Отправка данных")
            
            message = st.text_area(
                "Сообщение для отправки:",
                "Confidential data that needs to be securely transmitted over TLS connection.",
                height=100,
                key="enc_message"
            )
            
            direction = st.radio(
                "Направление:",
                ["Клиент → Сервер", "Сервер → Клиент"],
                key="direction"
            )
            
            if st.button("🔒 Зашифровать и отправить", key="encrypt_btn"):
                session = st.session_state.tls_session
                
                # Шифруем сообщение
                encrypted_data, auth_tag = self.tls_encrypt(
                    message, 
                    session, 
                    direction == "Клиент → Сервер"
                )
                
                st.session_state.encrypted_data = {
                    "original": message,
                    "encrypted": encrypted_data,
                    "auth_tag": auth_tag,
                    "direction": direction
                }
                st.rerun()
        
        with col2:
            st.subheader("📄 Результат шифрования")
            
            if 'encrypted_data' in st.session_state:
                data = st.session_state.encrypted_data
                
                st.success(f"✅ Сообщение зашифровано ({data['direction']})!")
                
                st.text_area(
                    "Исходное сообщение:",
                    data["original"],
                    height=80,
                    key="original_display"
                )
                
                st.text_area(
                    "Зашифрованные данные (hex):",
                    data["encrypted"],
                    height=80,
                    key="encrypted_display"
                )
                
                st.text_input(
                    "Authentication Tag:",
                    data["auth_tag"],
                    key="auth_tag_display"
                )
                
                # Детали шифрования
                with st.expander("🔍 Детали шифрования"):
                    self.display_encryption_details(data, st.session_state.tls_session)

    def render_certificates_section(self):
        """Работа с сертификатами"""
        st.header("📜 Сертификаты X.509")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔐 Демонстрационные сертификаты")
            
            cert_choice = st.selectbox(
                "Выберите сертификат:",
                list(self.demo_certificates.keys()),
                key="cert_choice"
            )
            
            certificate = self.demo_certificates[cert_choice]
            
            st.text_input("Субъект:", certificate.subject, disabled=True)
            st.text_input("Издатель:", certificate.issuer, disabled=True)
            st.text_area("Публичный ключ:", certificate.public_key[:200] + "...", height=100, disabled=True)
            
            validity = f"{certificate.validity[0].strftime('%Y-%m-%d')} - {certificate.validity[1].strftime('%Y-%m-%d')}"
            st.text_input("Срок действия:", validity, disabled=True)
            
            # Проверка сертификата
            if st.button("✅ Проверить сертификат", key="verify_cert_btn"):
                is_valid = self.verify_certificate(certificate)
                if is_valid:
                    st.success("✅ Сертификат валиден!")
                else:
                    st.error("❌ Сертификат невалиден!")
        
        with col2:
            st.subheader("🏗️ Цепочка доверия")
            
            # Визуализация цепочки сертификатов
            cert_chain = [
                {"name": "Root CA", "type": "Корневой", "status": "Доверенный"},
                {"name": "Intermediate CA", "type": "Промежуточный", "status": "Доверенный"},
                {"name": "server.example.com", "type": "Конечный", "status": "Валидный"}
            ]
            
            df_chain = pd.DataFrame(cert_chain)
            st.dataframe(df_chain, use_container_width=True, hide_index=True)
            
            # График срока действия
            st.subheader("📅 Срок действия сертификата")
            
            dates = [certificate.validity[0], datetime.now(), certificate.validity[1]]
            status = ["Начало", "Сейчас", "Конец"]
            
            fig = go.Figure(data=[go.Scatter(
                x=dates,
                y=[1, 1, 1],
                mode='markers+text',
                marker=dict(size=20, color=['green', 'blue', 'red']),
                text=status,
                textposition="top center"
            )])
            
            fig.update_layout(
                title="Срок действия сертификата",
                xaxis_title="Дата",
                yaxis=dict(visible=False),
                height=200
            )
            
            st.plotly_chart(fig, use_container_width=True)

    def render_security_analysis_section(self):
        """Анализ безопасности TLS"""
        st.header("📊 Анализ безопасности TLS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔍 Сравнение версий TLS")
            
            # Таблица сравнения версий
            comparison_data = []
            for version, info in self.tls_versions.items():
                comparison_data.append({
                    "Версия": version,
                    "Год": info["year"],
                    "Статус": info["status"],
                    "Безопасность": info["security"]
                })
            
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True, hide_index=True)
            
            # График безопасности
            st.subheader("📈 Эволюция безопасности")
            
            versions = list(self.tls_versions.keys())
            security_scores = [1, 2, 4, 8, 10]  # Условные оценки безопасности
            
            fig = go.Figure(data=[go.Bar(x=versions, y=security_scores)])
            fig.update_layout(
                title="Сравнение безопасности версий TLS",
                xaxis_title="Версия",
                yaxis_title="Уровень безопасности"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Анализ наборов шифров")
            
            # Анализ шифров
            cipher_analysis = []
            for cipher_name, cipher in self.cipher_suites.items():
                score = self.analyze_cipher_suite(cipher)
                cipher_analysis.append({
                    "Набор шифров": cipher_name,
                    "Обмен ключами": cipher.key_exchange,
                    "Шифрование": cipher.encryption,
                    "Безопасность": score
                })
            
            df_ciphers = pd.DataFrame(cipher_analysis)
            st.dataframe(df_ciphers, use_container_width=True, hide_index=True)
            
            # Рекомендации
            st.subheader("💡 Рекомендации по безопасности")
            
            recommendations = [
                "✅ Используйте TLS 1.2 или выше",
                "✅ Включите Perfect Forward Secrecy",
                "✅ Используйте сильные наборы шифров",
                "✅ Регулярно обновляйте сертификаты",
                "❌ Отключите SSL 3.0 и TLS 1.0",
                "❌ Избегайте статических RSA ключей"
            ]
            
            for rec in recommendations:
                st.write(rec)

    def render_attacks_protection_section(self):
        """Атаки и защита в TLS"""
        st.header("🛡️ Атаки и защита в TLS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⚔️ Распространенные атаки")
            
            attacks = {
                "POODLE": {
                    "description": "Padding Oracle On Downgraded Legacy Encryption",
                    "target": "SSL 3.0, TLS 1.0",
                    "protection": "Отключить SSL 3.0"
                },
                "BEAST": {
                    "description": "Browser Exploit Against SSL/TLS", 
                    "target": "TLS 1.0",
                    "protection": "Использовать TLS 1.1+"
                },
                "CRIME": {
                    "description": "Compression Ratio Info-leak Made Easy",
                    "target": "TLS compression", 
                    "protection": "Отключить сжатие"
                },
                "BREACH": {
                    "description": "Browser Reconnaissance and Exfiltration via Adaptive Compression of Hypertext",
                    "target": "HTTP compression",
                    "protection": "Отключить HTTP сжатие"
                },
                "Heartbleed": {
                    "description": "Уязвимость в OpenSSL",
                    "target": "TLS реализации",
                    "protection": "Обновить OpenSSL"
                }
            }
            
            for attack, info in attacks.items():
                with st.expander(f"🔓 {attack}"):
                    st.write(f"**Описание:** {info['description']}")
                    st.write(f"**Цель:** {info['target']}")
                    st.write(f"**Защита:** {info['protection']}")
        
        with col2:
            st.subheader("🛡️ Методы защиты")
            
            protections = [
                ("HSTS", "HTTP Strict Transport Security", "Принудительное использование HTTPS"),
                ("Certificate Pinning", "Закрепление сертификатов", "Защита от MITM"),
                ("Perfect Forward Secrecy", "Временные ключи", "Защита прошлых сессий"),
                ("OCSP Stapling", "Online Certificate Status Protocol", "Проверка отзыва сертификатов"),
                ("CAA Records", "Certificate Authority Authorization", "Контроль выпуска сертификатов")
            ]
            
            for protection, name, description in protections:
                with st.expander(f"🛡️ {protection}"):
                    st.write(f"**Название:** {name}")
                    st.write(f"**Описание:** {description}")
            
            # Демонстрация атаки
            st.subheader("🎯 Демонстрация защиты")
            
            if st.button("🛡️ Показать защиту от Downgrade Attack", key="downgrade_btn"):
                self.demo_downgrade_protection()

    # Основные методы TLS

    def simulate_tls_handshake(self, version: str, cipher_suite: str, client: str, server: str) -> TLSSession:
        """Симуляция процесса TLS Handshake"""
        suite = self.cipher_suites[cipher_suite]
        
        # Генерируем случайные значения
        client_random = secrets.token_hex(32)
        server_random = secrets.token_hex(32)
        
        # Генерируем pre-master secret
        if "ECDHE" in suite.key_exchange:
            # Эфемерный ключ Диффи-Хеллмана
            pre_master_secret = secrets.token_hex(48)
        else:
            # RSA ключ
            pre_master_secret = secrets.token_hex(48)
        
        # Вычисляем master secret
        master_secret = self.derive_master_secret(pre_master_secret, client_random, server_random)
        
        # Генерируем ключи
        key_material = self.derive_key_material(master_secret, client_random, server_random, suite)
        
        return TLSSession(
            version=version,
            cipher_suite=suite,
            client_random=client_random,
            server_random=server_random,
            pre_master_secret=pre_master_secret,
            master_secret=master_secret,
            client_write_key=key_material["client_key"],
            server_write_key=key_material["server_key"],
            client_write_iv=key_material["client_iv"],
            server_write_iv=key_material["server_iv"]
        )

    def derive_master_secret(self, pre_master_secret: str, client_random: str, server_random: str) -> str:
        """Вычисление master secret"""
        seed = client_random + server_random
        # Упрощенная версия PRF
        combined = pre_master_secret + seed
        return hashlib.sha384(combined.encode()).hexdigest()

    def derive_key_material(self, master_secret: str, client_random: str, server_random: str, 
                          cipher_suite: TLSCipherSuite) -> Dict[str, str]:
        """Генерация ключевого материала"""
        seed = server_random + client_random
        combined = master_secret + seed
        
        # Генерируем достаточное количество ключевого материала
        key_block = hashlib.sha384(combined.encode()).hexdigest() * 4
        
        # Распределяем ключевой материал (упрощенно)
        key_length = cipher_suite.bits // 8
        iv_length = 12  # Для GCM
        
        return {
            "client_key": key_block[:key_length*2],
            "server_key": key_block[key_length*2:key_length*4],
            "client_iv": key_block[key_length*4:key_length*4+iv_length*2],
            "server_iv": key_block[key_length*4+iv_length*2:key_length*4+iv_length*4]
        }

    def tls_encrypt(self, message: str, session: TLSSession, is_client: bool) -> Tuple[str, str]:
        """Шифрование данных в TLS"""
        # Выбираем ключ в зависимости от направления
        if is_client:
            key = session.client_write_key
            iv = session.client_write_iv
        else:
            key = session.server_write_key
            iv = session.server_write_iv
        
        # Упрощенное шифрование (в реальности используется AES-GCM)
        key_bytes = bytes.fromhex(key[:32])
        iv_bytes = bytes.fromhex(iv[:24])
        
        # Имитация шифрования
        cipher = Cipher(algorithms.AES(key_bytes), modes.GCM(iv_bytes), backend=default_backend())
        encryptor = cipher.encryptor()
        
        message_bytes = message.encode('utf-8')
        encrypted = encryptor.update(message_bytes) + encryptor.finalize()
        
        return encrypted.hex(), encryptor.tag.hex()

    def generate_handshake_messages(self, session: TLSSession) -> List[TLSHandshakeMessage]:
        """Генерация сообщений handshake процесса"""
        messages = []
        current_time = time.time()
        
        messages.append(TLSHandshakeMessage(
            "ClientHello",
            {
                "version": session.version,
                "random": session.client_random,
                "cipher_suites": [session.cipher_suite.name],
                "compression_methods": ["null"],
                "extensions": ["supported_versions", "key_share"]
            },
            current_time
        ))
        
        messages.append(TLSHandshakeMessage(
            "ServerHello", 
            {
                "version": session.version,
                "random": session.server_random,
                "cipher_suite": session.cipher_suite.name,
                "compression_method": "null",
                "extensions": ["key_share"]
            },
            current_time + 0.1
        ))
        
        messages.append(TLSHandshakeMessage(
            "Certificate",
            {
                "certificates": ["server_certificate"],
                "chain": ["intermediate_ca", "root_ca"]
            },
            current_time + 0.2
        ))
        
        messages.append(TLSHandshakeMessage(
            "ServerKeyExchange",
            {
                "key_exchange": session.cipher_suite.key_exchange,
                "parameters": "ecdh_params" if "ECDHE" in session.cipher_suite.key_exchange else "rsa_params"
            },
            current_time + 0.3
        ))
        
        messages.append(TLSHandshakeMessage(
            "ServerHelloDone",
            {},
            current_time + 0.4
        ))
        
        messages.append(TLSHandshakeMessage(
            "ClientKeyExchange",
            {
                "pre_master_secret": session.pre_master_secret[:32] + "..."
            },
            current_time + 0.5
        ))
        
        messages.append(TLSHandshakeMessage(
            "ChangeCipherSpec",
            {},
            current_time + 0.6
        ))
        
        messages.append(TLSHandshakeMessage(
            "Finished",
            {
                "verify_data": "verified"
            },
            current_time + 0.7
        ))
        
        messages.append(TLSHandshakeMessage(
            "ChangeCipherSpec",
            {},
            current_time + 0.8
        ))
        
        messages.append(TLSHandshakeMessage(
            "Finished",
            {
                "verify_data": "verified"
            },
            current_time + 0.9
        ))
        
        return messages

    def generate_demo_certificates(self) -> Dict[str, Certificate]:
        """Генерация демонстрационных сертификатов"""
        return {
            "Root CA": Certificate(
                subject="CN=Root CA, O=Demo Certificate Authority",
                issuer="CN=Root CA, O=Demo Certificate Authority", 
                public_key=secrets.token_hex(128),
                validity=(datetime.now() - timedelta(days=365), datetime.now() + timedelta(days=3650)),
                signature=secrets.token_hex(64)
            ),
            "Intermediate CA": Certificate(
                subject="CN=Intermediate CA, O=Demo Certificate Authority",
                issuer="CN=Root CA, O=Demo Certificate Authority",
                public_key=secrets.token_hex(128),
                validity=(datetime.now() - timedelta(days=180), datetime.now() + timedelta(days=1825)),
                signature=secrets.token_hex(64)
            ),
            "server.example.com": Certificate(
                subject="CN=server.example.com, O=Demo Organization",
                issuer="CN=Intermediate CA, O=Demo Certificate Authority",
                public_key=secrets.token_hex(128),
                validity=(datetime.now() - timedelta(days=30), datetime.now() + timedelta(days=365)),
                signature=secrets.token_hex(64)
            )
        }

    def verify_certificate(self, certificate: Certificate) -> bool:
        """Проверка валидности сертификата"""
        now = datetime.now()
        return certificate.validity[0] <= now <= certificate.validity[1]

    def analyze_cipher_suite(self, cipher: TLSCipherSuite) -> str:
        """Анализ безопасности набора шифров"""
        score = 0
        
        if "ECDHE" in cipher.key_exchange:
            score += 3
        elif "DHE" in cipher.key_exchange:
            score += 2
        elif "RSA" in cipher.key_exchange:
            score += 1
            
        if "GCM" in cipher.encryption:
            score += 2
        elif "CBC" in cipher.encryption:
            score += 1
            
        if cipher.bits >= 256:
            score += 2
        elif cipher.bits >= 128:
            score += 1
            
        return "Высокий" if score >= 5 else "Средний" if score >= 3 else "Низкий"

    # Методы визуализации

    def visualize_handshake_process(self, messages: List[TLSHandshakeMessage]):
        """Визуализация процесса handshake"""
        fig = go.Figure()
        
        # Создаем timeline
        entities = ["Клиент", "Сервер"]
        colors = {'Клиент': 'blue', 'Сервер': 'green'}
        
        for i, message in enumerate(messages):
            if message.type in ["ClientHello", "ClientKeyExchange", "ChangeCipherSpec", "Finished"]:
                from_entity, to_entity = 0, 1  # Клиент → Сервер
            else:
                from_entity, to_entity = 1, 0  # Сервер → Клиент
            
            fig.add_trace(go.Scatter(
                x=[from_entity, to_entity],
                y=[i, i],
                mode='lines+markers+text',
                line=dict(width=3, color=colors[entities[from_entity]]),
                marker=dict(size=12),
                text=[message.type, ""],
                textposition="middle right",
                name=message.type
            ))
        
        fig.update_layout(
            title="TLS Handshake Process Timeline",
            xaxis=dict(
                tickvals=[0, 1],
                ticktext=entities,
                range=[-0.5, 1.5]
            ),
            yaxis=dict(
                tickvals=list(range(len(messages))),
                ticktext=[msg.type for msg in messages],
                autorange="reversed"
            ),
            showlegend=False,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Детали сообщений
        st.subheader("📋 Детали сообщений Handshake")
        
        for i, message in enumerate(messages):
            with st.expander(f"{i+1}. {message.type}"):
                for key, value in message.content.items():
                    if isinstance(value, list):
                        st.write(f"**{key}:** {', '.join(value)}")
                    else:
                        st.write(f"**{key}:** {value}")

    def display_encryption_details(self, encrypted_data: Dict, session: TLSSession):
        """Отображение деталей шифрования"""
        st.markdown("**Параметры шифрования:**")
        st.text(f"Алгоритм: {session.cipher_suite.encryption}")
        st.text(f"Длина ключа: {session.cipher_suite.bits} бит")
        st.text(f"Режим: GCM (Galois/Counter Mode)")
        st.text(f"Размер сообщения: {len(encrypted_data['original'])} байт")
        st.text(f"Размер шифротекста: {len(encrypted_data['encrypted']) // 2} байт")
        
        st.markdown("**Криптографические примитивы:**")
        st.text("✓ Аутентифицированное шифрование")
        st.text("✓ Гарантия целостности данных")
        st.text("✓ Защита от повторного воспроизведения")
        st.text("✓ Конфиденциальность передаваемых данных")

    def demo_downgrade_protection(self):
        """Демонстрация защиты от downgrade attack"""
        st.markdown("""
        ### 🛡️ Защита от Downgrade Attack в TLS 1.3
        
        **Атака:** Злоумышленник пытается заставить клиента и сервер использовать более старую, 
        менее безопасную версию TLS.
        
        **Защита в TLS 1.3:**
        - Сервер всегда проверяет supported_versions extension
        - Клиент отправляет версию 1.3 в ClientHello, даже при downgrade
        - ServerHello содержит подтверждение версии 1.3
        - Атаки обнаруживаются по несоответствию версий
        
        **Процесс:**
        ```
        Клиент (реальная поддержка: TLS 1.3):
          ClientHello (version = 1.2)  # Злоумышленник изменил
          supported_versions = [1.3, 1.2]  # Реальные возможности
        
        Сервер (поддерживает 1.3):
          Обнаруживает supported_versions
          Отвечает ServerHello с version = 1.3
          Атака обнаруживается!
        ```
        
        **Результат:** Соединение устанавливается с TLS 1.3, атака предотвращена!
        """)

# Для обратной совместимости
class SSL_TLS_Protocol(SSL_TLS_Module):
    pass