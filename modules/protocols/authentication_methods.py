from modules.base_module import CryptoModule
import streamlit as st
import secrets
import hashlib
import time
import hmac
import base64
import qrcode
from typing import List, Tuple, Dict, Optional
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass
from datetime import datetime, timedelta
import io
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.twofactor import totp, hotp
from cryptography.hazmat.backends import default_backend

@dataclass
class AuthenticationFactor:
    type: str
    description: str
    examples: List[str]
    security_level: int

@dataclass
class UserCredentials:
    username: str
    password_hash: str
    salt: str
    mfa_secret: str
    biometric_template: str

@dataclass
class AuthenticationAttempt:
    timestamp: float
    method: str
    success: bool
    factors_used: List[str]
    risk_score: float

class AuthenticationMethodsModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Методы аутентификации"
        self.description = "Протоколы и методы проверки подлинности пользователей"
        self.category = "protocols"
        self.icon = ""
        self.order = 7
        
        # Факторы аутентификации
        self.authentication_factors = {
            "knowledge": AuthenticationFactor(
                "Знание (Something you know)",
                "Секретная информация, известная только пользователю",
                ["Пароли", "PIN-коды", "Секретные вопросы", "Графические ключи"],
                3
            ),
            "possession": AuthenticationFactor(
                "Владение (Something you have)", 
                "Физический объект во владении пользователя",
                ["Смарт-карты", "USB-токены", "Мобильные устройства", "OTP-генераторы"],
                6
            ),
            "inherence": AuthenticationFactor(
                "Биометрия (Something you are)",
                "Уникальные биологические характеристики пользователя",
                ["Отпечатки пальцев", "Радужная оболочка", "Голос", "Лицо", "Поведение"],
                8
            ),
            "location": AuthenticationFactor(
                "Местоположение (Somewhere you are)",
                "Географическое положение пользователя",
                ["GPS координаты", "IP-адрес", "Сетевые характеристики"],
                4
            ),
            "behavior": AuthenticationFactor(
                "Поведение (Something you do)",
                "Уникальные поведенческие паттерны",
                ["Ритм печати", "Мышиные жесты", "Поведение при прокрутке"],
                5
            )
        }
        
        # Протоколы аутентификации
        self.auth_protocols = {
            "LDAP": {
                "name": "Lightweight Directory Access Protocol",
                "type": "Сетевая аутентификация",
                "security": "Средний",
                "use_cases": ["Корпоративные сети", "Active Directory"]
            },
            "RADIUS": {
                "name": "Remote Authentication Dial-In User Service", 
                "type": "Удаленная аутентификация",
                "security": "Высокий",
                "use_cases": ["VPN", "Wi-Fi сети", "Сетевые устройства"]
            },
            "OAuth2": {
                "name": "Open Authorization 2.0",
                "type": "Делегированная аутентификация",
                "security": "Высокий", 
                "use_cases": ["Вход через соцсети", "API авторизация"]
            },
            "OpenID Connect": {
                "name": "OpenID Connect",
                "type": "Федеративная аутентификация",
                "security": "Высокий",
                "use_cases": ["Единый вход (SSO)", "Веб-приложения"]
            },
            "SAML": {
                "name": "Security Assertion Markup Language",
                "type": "Федеративная аутентификация", 
                "security": "Высокий",
                "use_cases": ["Корпоративный SSO", "Госуслуги"]
            },
            "FIDO2": {
                "name": "Fast Identity Online 2",
                "type": "Беспарольная аутентификация",
                "security": "Очень высокий",
                "use_cases": ["Биометрия", "Аппаратные ключи"]
            }
        }
        
        # Демонстрационные пользователи
        self.demo_users = self.generate_demo_users()
        
        # История аутентификаций
        self.auth_history = []

    def render(self):
        st.title("🔐 Методы и протоколы аутентификации")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **Аутентификация** - процесс проверки подлинности пользователя или системы.
            
            ### 🎯 Факторы аутентификации:
            
            **1. Знание (Something you know)**
            - Пароли, PIN-коды, секретные вопросы
            - 🔸 Преимущества: Простота реализации
            - 🔹 Недостатки: Уязвимы к фишингу, слабые пароли
            
            **2. Владение (Something you have)**  
            - Токены, смарт-карты, мобильные устройства
            - 🔸 Преимущества: Устойчивость к фишингу
            - 🔹 Недостатки: Риск потери/кражи
            
            **3. Биометрия (Something you are)**
            - Отпечатки, лицо, голос, радужная оболочка
            - 🔸 Преимущества: Уникальность, удобство
            - 🔹 Недостатки: Конфиденциальность, спуфинг
            
            **4. Многофакторная аутентификация (MFA)**
            - Комбинация 2+ факторов
            - 🔸 Увеличивает безопасность в 99.9%
            - 🔹 Требует дополнительных усилий от пользователя
            
            ### 🛡️ Криптографические протоколы:
            
            **OAuth 2.0** - делегирование доступа без раскрытия паролей
            **OpenID Connect** - идентификация поверх OAuth 2.0  
            **SAML** - обмен утверждениями аутентификации между доменами
            **FIDO2** - стандарт беспарольной аутентификации
            
            ### 📊 Метрики безопасности:
            - **False Acceptance Rate (FAR)** - процент ложных принятий
            - **False Rejection Rate (FRR)** - процент ложных отказов
            - **CER** - точка равной ошибки (FAR = FRR)
            """)

        st.markdown("---")
        
        # Основной интерфейс с вкладками
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Факторы аутентификации", "🔐 MFA Демонстрация", "🔄 Протоколы", "📊 Анализ безопасности", "🛡️ Атаки и защита"])

        with tab1:
            self.render_factors_section()
        
        with tab2:
            self.render_mfa_demo_section()
            
        with tab3:
            self.render_protocols_section()
            
        with tab4:
            self.render_security_analysis_section()
            
        with tab5:
            self.render_attacks_protection_section()

    def render_factors_section(self):
        """Демонстрация факторов аутентификации"""
        st.header("🎯 Факторы аутентификации")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📊 Сравнение факторов")
            
            # Таблица факторов
            factors_data = []
            for factor_id, factor in self.authentication_factors.items():
                factors_data.append({
                    "Тип": factor.type,
                    "Описание": factor.description,
                    "Примеры": ", ".join(factor.examples[:2]),
                    "Уровень безопасности": factor.security_level
                })
            
            df_factors = pd.DataFrame(factors_data)
            st.dataframe(df_factors, use_container_width=True, hide_index=True)
            
            # График безопасности факторов
            st.subheader("📈 Уровень безопасности факторов")
            
            factor_names = [f.type for f in self.authentication_factors.values()]
            security_scores = [f.security_level for f in self.authentication_factors.values()]
            
            fig = go.Figure(data=[go.Bar(
                x=factor_names,
                y=security_scores,
                marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
            )])
            
            fig.update_layout(
                title="Уровень безопасности факторов аутентификации",
                xaxis_title="Фактор",
                yaxis_title="Уровень безопасности (1-10)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎮 Демонстрация факторов")
            
            selected_factor = st.selectbox(
                "Выберите фактор для демонстрации:",
                list(self.authentication_factors.keys()),
                format_func=lambda x: self.authentication_factors[x].type,
                key="factor_demo"
            )
            
            factor = self.authentication_factors[selected_factor]
            
            st.markdown(f"**{factor.type}**")
            st.write(factor.description)
            
            # Интерактивная демонстрация
            if selected_factor == "knowledge":
                self.demo_knowledge_factor()
            elif selected_factor == "possession":
                self.demo_possession_factor()
            elif selected_factor == "inherence":
                self.demo_biometric_factor()
            elif selected_factor == "location":
                self.demo_location_factor()
            elif selected_factor == "behavior":
                self.demo_behavior_factor()

    def render_mfa_demo_section(self):
        """Демонстрация многофакторной аутентификации"""
        st.header("🔐 Многофакторная аутентификация (MFA)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👤 Аутентификация пользователя")
            
            username = st.selectbox(
                "Пользователь:",
                list(self.demo_users.keys()),
                key="mfa_user"
            )
            
            # Фактор 1: Знание (пароль)
            st.markdown("**Фактор 1: Знание (Пароль)**")
            password = st.text_input("Пароль:", type="password", key="mfa_password")
            
            # Фактор 2: Владение (TOTP)
            st.markdown("**Фактор 2: Владение (TOTP код)**")
            
            # Генерация QR-кода для приложения аутентификации
            user = self.demo_users[username]
            totp_uri = self.generate_totp_uri(user, "Demo App")
            
            # Показываем QR-код
            qr_img = self.generate_qr_code(totp_uri)
            st.image(qr_img, caption="Отсканируйте QR-код в приложении аутентификации", width=200)
            
            totp_code = st.text_input("6-значный код из приложения:", key="totp_code")
            
            # Фактор 3: Биометрия (опционально)
            st.markdown("**Фактор 3: Биометрия (Демо)**")
            use_biometric = st.checkbox("Использовать биометрическую аутентификацию", key="use_bio")
            
            if use_biometric:
                biometric_match = st.slider("Совпадение биометрического шаблона (%):", 0, 100, 95, key="bio_match")
            
            if st.button("🔐 Выполнить аутентификацию", key="mfa_auth_btn"):
                # Проверяем факторы
                factors_used = ["Пароль", "TOTP"]
                success_factors = 0
                
                # Проверка пароля
                if self.verify_password(password, user.password_hash, user.salt):
                    success_factors += 1
                    st.success("✅ Пароль верный")
                else:
                    st.error("❌ Неверный пароль")
                
                # Проверка TOTP
                if self.verify_totp(totp_code, user.mfa_secret):
                    success_factors += 1
                    st.success("✅ TOTP код верный")
                else:
                    st.error("❌ Неверный TOTP код")
                
                # Проверка биометрии
                if use_biometric:
                    factors_used.append("Биометрия")
                    if biometric_match >= 90:  # Порог совпадения
                        success_factors += 1
                        st.success("✅ Биометрическая аутентификация успешна")
                    else:
                        st.error("❌ Биометрическая аутентификация не удалась")
                
                # Определяем результат
                required_factors = 2 + (1 if use_biometric else 0)
                is_success = success_factors >= required_factors
                
                # Записываем попытку
                attempt = AuthenticationAttempt(
                    timestamp=time.time(),
                    method="MFA",
                    success=is_success,
                    factors_used=factors_used,
                    risk_score=self.calculate_risk_score(success_factors, required_factors)
                )
                self.auth_history.append(attempt)
                
                if is_success:
                    st.success("🎉 Аутентификация успешна! Доступ предоставлен.")
                    st.balloons()
                else:
                    st.error("🚫 Аутентификация не удалась. Доступ запрещен.")
        
        with col2:
            st.subheader("📊 Эффективность MFA")
            
            # Статистика MFA
            st.metric("Увеличение безопасности", "99.9%", "с MFA")
            st.metric("Снижение успешных атак", "96%", "по данным Microsoft")
            st.metric("Ложные отказы", "1-3%", "типичный показатель")
            
            # Визуализация факторов MFA
            st.subheader("🛡️ Защита MFA от атак")
            
            attacks_data = {
                "Тип атаки": ["Фишинг", "Брутфорс", "Кража учетных данных", "Человек посередине"],
                "Без MFA": [85, 65, 90, 75],
                "С MFA": [5, 1, 10, 15]
            }
            
            df_attacks = pd.DataFrame(attacks_data)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Без MFA', x=df_attacks['Тип атаки'], y=df_attacks['Без MFA']))
            fig.add_trace(go.Bar(name='С MFA', x=df_attacks['Тип атаки'], y=df_attacks['С MFA']))
            
            fig.update_layout(
                title="Эффективность MFA против различных атак (%)",
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

    def render_protocols_section(self):
        """Демонстрация протоколов аутентификации"""
        st.header("🔄 Протоколы аутентификации")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📋 Сравнение протоколов")
            
            # Таблица протоколов
            protocols_data = []
            for protocol_id, protocol in self.auth_protocols.items():
                protocols_data.append({
                    "Протокол": protocol["name"],
                    "Тип": protocol["type"],
                    "Безопасность": protocol["security"],
                    "Области применения": ", ".join(protocol["use_cases"][:2])
                })
            
            df_protocols = pd.DataFrame(protocols_data)
            st.dataframe(df_protocols, use_container_width=True, hide_index=True)
            
            # Демонстрация OAuth 2.0 flow
            st.subheader("🎯 Демонстрация OAuth 2.0 Flow")
            
            if st.button("🔄 Запустить OAuth 2.0 демонстрацию", key="oauth_demo_btn"):
                self.demo_oauth2_flow()
        
        with col2:
            st.subheader("🔐 Выбор протокола")
            
            selected_protocol = st.selectbox(
                "Выберите протокол для деталей:",
                list(self.auth_protocols.keys()),
                key="protocol_detail"
            )
            
            protocol = self.auth_protocols[selected_protocol]
            
            st.markdown(f"### {protocol['name']}")
            st.write(f"**Тип:** {protocol['type']}")
            st.write(f"**Уровень безопасности:** {protocol['security']}")
            
            st.markdown("**Области применения:**")
            for use_case in protocol["use_cases"]:
                st.write(f"• {use_case}")
            
            # Визуализация использования протоколов
            st.subheader("📊 Популярность протоколов")
            
            protocols = list(self.auth_protocols.keys())
            adoption = [65, 45, 80, 70, 55, 30]  # Условные данные
            
            fig = go.Figure(data=[go.Pie(
                labels=protocols,
                values=adoption,
                hole=0.3
            )])
            
            fig.update_layout(title="Распространенность протоколов аутентификации")
            st.plotly_chart(fig, use_container_width=True)

    def render_security_analysis_section(self):
        """Анализ безопасности методов аутентификации"""
        st.header("📊 Анализ безопасности")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Сравнительный анализ")
            
            # Метрики безопасности
            methods = ["Пароль", "Пароль + SMS", "TOTP", "Биометрия", "FIDO2"]
            security_scores = [3, 6, 7, 8, 9]
            usability_scores = [9, 7, 6, 8, 7]
            cost_scores = [1, 3, 4, 6, 5]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=security_scores,
                theta=methods,
                fill='toself',
                name='Безопасность',
                line=dict(color='red')
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=usability_scores,
                theta=methods,
                fill='toself', 
                name='Удобство',
                line=dict(color='blue')
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=cost_scores,
                theta=methods,
                fill='toself',
                name='Стоимость',
                line=dict(color='green')
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                showlegend=True,
                title="Сравнение методов аутентификации",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Статистика аутентификации")
            
            if self.auth_history:
                # Анализ истории аутентификаций
                success_rate = len([a for a in self.auth_history if a.success]) / len(self.auth_history) * 100
                avg_factors = np.mean([len(a.factors_used) for a in self.auth_history])
                avg_risk = np.mean([a.risk_score for a in self.auth_history])
                
                col_metric1, col_metric2 = st.columns(2)
                with col_metric1:
                    st.metric("Успешные аутентификации", f"{success_rate:.1f}%")
                    st.metric("Среднее количество факторов", f"{avg_factors:.1f}")
                with col_metric2:
                    st.metric("Средняя оценка риска", f"{avg_risk:.1f}/10")
                    st.metric("Всего попыток", len(self.auth_history))
                
                # График истории аутентификаций
                dates = [datetime.fromtimestamp(a.timestamp) for a in self.auth_history]
                successes = [1 if a.success else 0 for a in self.auth_history]
                
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x=dates, y=successes,
                    mode='markers',
                    marker=dict(
                        size=10,
                        color=successes,
                        colorscale=['red', 'green']
                    ),
                    name='Результат аутентификации'
                ))
                
                fig2.update_layout(
                    title="История попыток аутентификации",
                    xaxis_title="Время",
                    yaxis_title="Успех (1=успех, 0=неудача)",
                    height=300
                )
                
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Нет данных об аутентификации. Выполните аутентификацию в разделе MFA.")

    def render_attacks_protection_section(self):
        """Атаки на аутентификацию и методы защиты"""
        st.header("🛡️ Атаки и защита")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⚔️ Распространенные атаки")
            
            attacks = {
                "Фишинг": {
                    "description": "Обман пользователя для раскрытия учетных данных",
                    "target": "Пароли, OTP коды",
                    "protection": ["MFA", "Антифишинг обучение", "Аппаратные ключи"]
                },
                "Брутфорс": {
                    "description": "Перебор паролей методом грубой силы",
                    "target": "Слабые пароли",
                    "protection": ["Сложные пароли", "Блокировка после попыток", "Капча"]
                },
                "Человек посередине": {
                    "description": "Перехват и модификация трафика аутентификации", 
                    "target": "Сессии, токены",
                    "protection": ["HTTPS", "Certificate pinning", "TLS"]
                },
                "Replay атака": {
                    "description": "Повторное использование перехваченных данных аутентификации",
                    "target": "Сессионные токены",
                    "protection": ["Nonce", "Временные метки", "Одноразовые токены"]
                },
                "Спуфинг биометрии": {
                    "description": "Подделка биометрических характеристик",
                    "target": "Системы распознавания",
                    "protection": ["Liveness detection", "Мультимодальная биометрия"]
                }
            }
            
            for attack, info in attacks.items():
                with st.expander(f"🔓 {attack}"):
                    st.write(f"**Описание:** {info['description']}")
                    st.write(f"**Цель:** {info['target']}")
                    st.write("**Методы защиты:**")
                    for protection in info['protection']:
                        st.write(f"• {protection}")
        
        with col2:
            st.subheader("🛡️ Рекомендации по защите")
            
            recommendations = [
                ("🔐 MFA", "Всегда используйте многофакторную аутентификацию", "Высокий"),
                ("🎯 FIDO2", "Внедряйте беспарольную аутентификацию", "Очень высокий"),
                ("📱 TOTP", "Используйте приложения аутентификации вместо SMS", "Высокий"),
                ("🔍 Мониторинг", "Отслеживайте подозрительные попытки входа", "Высокий"),
                ("🎓 Обучение", "Обучайте пользователей кибергигиене", "Средний"),
                ("⚙️ Политики", "Внедряйте строгие политики паролей", "Средний")
            ]
            
            for icon, rec, priority in recommendations:
                with st.expander(f"{icon} {rec}"):
                    st.write(f"**Приоритет:** {priority}")
                    st.write(f"**Эффективность:** Высокая")
            
            # Демонстрация защиты от фишинга
            st.subheader("🎯 Демонстрация защиты от фишинга")
            
            if st.button("🛡️ Показать защиту FIDO2", key="fido2_demo_btn"):
                self.demo_fido2_protection()

    # Демонстрационные методы для факторов

    def demo_knowledge_factor(self):
        """Демонстрация фактора знания"""
        st.markdown("**Демонстрация проверки пароля:**")
        
        password = st.text_input("Введите пароль для проверки:", type="password", key="demo_pass")
        
        if password:
            # Анализ пароля
            strength = self.analyze_password_strength(password)
            entropy = self.calculate_password_entropy(password)
            
            st.metric("Сложность пароля", strength)
            st.metric("Энтропия", f"{entropy:.1f} бит")
            
            # Рекомендации
            if strength == "Слабый":
                st.error("❌ Пароль слишком простой. Рекомендуется:")
                st.write("• Минимум 12 символов")
                st.write("• Буквы в разных регистрах")
                st.write("• Цифры и специальные символы")

    def demo_possession_factor(self):
        """Демонстрация фактора владения"""
        st.markdown("**Генерация TOTP кода:**")
        
        # Генерация демонстрационного TOTP
        secret = base64.b32encode(secrets.token_bytes(20)).decode('utf-8')
        current_time = int(time.time())
        totp_code = self.generate_totp_code(secret, current_time)
        
        st.text_input("Секрет TOTP:", secret, disabled=True)
        st.text_input("Текущий TOTP код:", totp_code, disabled=True)
        
        st.info("💡 TOTP коды обновляются каждые 30 секунд и требуют синхронизации времени")

    def demo_biometric_factor(self):
        """Демонстрация биометрического фактора"""
        st.markdown("**Демонстрация распознавания отпечатка:**")
        
        # Имитация сканирования отпечатка
        match_confidence = st.slider("Уверенность совпадения (%):", 0, 100, 85, key="finger_match")
        
        if match_confidence >= 90:
            st.success("✅ Отпечаток распознан успешно")
            st.metric("FAR", "0.001%")  # False Acceptance Rate
            st.metric("FRR", "2.5%")    # False Rejection Rate
        else:
            st.error("❌ Отпечаток не распознан")
            st.info("Попробуйте лучше разместить палец на сканере")

    def demo_location_factor(self):
        """Демонстрация фактора местоположения"""
        st.markdown("**Проверка географического положения:**")
        
        # Имитация проверки местоположения
        allowed_locations = ["Москва", "Санкт-Петербург", "Новосибирск"]
        current_location = st.selectbox("Текущее местоположение:", 
                                      ["Москва", "Санкт-Петербург", "Новосибирск", "Лондон", "Нью-Йорк"],
                                      key="location")
        
        if current_location in allowed_locations:
            st.success(f"✅ Доступ разрешен из {current_location}")
        else:
            st.error(f"❌ Доступ запрещен из {current_location}")

    def demo_behavior_factor(self):
        """Демонстрация поведенческого фактора"""
        st.markdown("**Анализ поведения при вводе пароля:**")
        
        # Имитация анализа поведения
        typing_speed = st.slider("Скорость печати (зн/мин):", 20, 120, 45, key="typing_speed")
        pause_pattern = st.selectbox("Паттерн пауз:", ["Нормальный", "Необычный"], key="pause_pattern")
        
        behavior_score = self.analyze_behavior(typing_speed, pause_pattern)
        
        st.metric("Оценка поведения", f"{behavior_score}/10")
        
        if behavior_score >= 7:
            st.success("✅ Поведение соответствует пользователю")
        else:
            st.warning("⚠️ Обнаружены аномалии в поведении")

    # Вспомогательные методы

    def generate_demo_users(self) -> Dict[str, UserCredentials]:
        """Генерация демонстрационных пользователей"""
        users = {}
        for username in ["alice", "bob", "charlie"]:
            salt = secrets.token_hex(16)
            password = "SecurePassword123!"
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
            mfa_secret = base64.b32encode(secrets.token_bytes(20)).decode('utf-8')
            
            users[username] = UserCredentials(
                username=username,
                password_hash=password_hash,
                salt=salt,
                mfa_secret=mfa_secret,
                biometric_template=secrets.token_hex(32)
            )
        return users

    def analyze_password_strength(self, password: str) -> str:
        """Анализ сложности пароля"""
        score = 0
        if len(password) >= 8: score += 1
        if len(password) >= 12: score += 1
        if any(c.islower() for c in password): score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(not c.isalnum() for c in password): score += 1
        
        if score >= 5: return "Очень сильный"
        elif score >= 4: return "Сильный"
        elif score >= 3: return "Средний"
        else: return "Слабый"

    def calculate_password_entropy(self, password: str) -> float:
        """Вычисление энтропии пароля"""
        char_set = 0
        if any(c.islower() for c in password): char_set += 26
        if any(c.isupper() for c in password): char_set += 26
        if any(c.isdigit() for c in password): char_set += 10
        if any(not c.isalnum() for c in password): char_set += 32
        
        if char_set == 0: return 0
        return len(password) * (char_set ** 0.5)

    def generate_totp_uri(self, user: UserCredentials, issuer: str) -> str:
        """Генерация URI для TOTP"""
        return f"otpauth://totp/{issuer}:{user.username}?secret={user.mfa_secret}&issuer={issuer}"

    def generate_qr_code(self, data: str):
        """Генерация QR-кода"""
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        return buf

    def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Проверка пароля"""
        computed_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
        return computed_hash == stored_hash

    def generate_totp_code(self, secret: str, timestamp: int) -> str:
        """Генерация TOTP кода"""
        import hmac
        import struct
        
        time_step = 30
        time_counter = timestamp // time_step
        
        key = base64.b32decode(secret)
        msg = struct.pack(">Q", time_counter)
        hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()
        
        offset = hmac_hash[-1] & 0x0F
        code = struct.unpack(">I", hmac_hash[offset:offset+4])[0] & 0x7FFFFFFF
        code = code % 1000000
        
        return f"{code:06d}"

    def verify_totp(self, code: str, secret: str) -> bool:
        """Проверка TOTP кода"""
        current_time = int(time.time())
        expected_code = self.generate_totp_code(secret, current_time)
        return code == expected_code

    def analyze_behavior(self, typing_speed: int, pause_pattern: str) -> float:
        """Анализ поведенческих характеристик"""
        score = 5.0  # Базовая оценка
        
        # Оценка скорости печати
        if 40 <= typing_speed <= 60:
            score += 2
        elif 30 <= typing_speed <= 70:
            score += 1
        
        # Оценка паттерна пауз
        if pause_pattern == "Нормальный":
            score += 3
        else:
            score -= 2
            
        return max(0, min(10, score))

    def calculate_risk_score(self, success_factors: int, required_factors: int) -> float:
        """Вычисление оценки риска аутентификации"""
        base_risk = 10.0 - (success_factors * 2.5)
        if success_factors < required_factors:
            base_risk += 5.0
        return max(0, min(10, base_risk))

    def demo_oauth2_flow(self):
        """Демонстрация OAuth 2.0 flow"""
        st.markdown("""
        ### 🔄 OAuth 2.0 Authorization Code Flow
        
        **1. Инициация запроса:**
        ```
        GET /authorize?
          response_type=code&
          client_id=CLIENT_ID&  
          redirect_uri=REDIRECT_URI&
          scope=read&
          state=RANDOM_STRING
        ```
        
        **2. Аутентификация пользователя:**
        - Пользователь вводит учетные данные
        - Сервер аутентификации проверяет их
        
        **3. Получение authorization code:**
        ```
        HTTP/1.1 302 Found
        Location: https://client.com/callback?
          code=AUTHORIZATION_CODE&
          state=RANDOM_STRING
        ```
        
        **4. Обмен code на access token:**
        ```
        POST /token
        Content-Type: application/x-www-form-urlencoded
        
        grant_type=authorization_code&
        code=AUTHORIZATION_CODE&
        redirect_uri=REDIRECT_URI&
        client_id=CLIENT_ID&
        client_secret=CLIENT_SECRET
        ```
        
        **5. Получение access token:**
        ```json
        {
          "access_token": "ACCESS_TOKEN",
          "token_type": "Bearer", 
          "expires_in": 3600,
          "refresh_token": "REFRESH_TOKEN"
        }
        ```
        
        **6. Использование access token для доступа к API**
        """)

    def demo_fido2_protection(self):
        """Демонстрация защиты FIDO2 от фишинга"""
        st.markdown("""
        ### 🛡️ Защита FIDO2 от фишинговых атак
        
        **Проблема фишинга:**
        - Пользователи вводят пароли на поддельных сайтах
        - OTP коды могут быть перехвачены
        - Сессии могут быть украдены
        
        **Решение FIDO2:**
        
        **1. Привязка к домену:**
        - Ключ FIDO2 привязан к конкретному домену
        - Нельзя использовать ключ с фишингового сайта
        
        **2. Биометрическая верификация:**
        - Требуется отпечаток/лицо для использования ключа
        - Защита от использования украденного ключа
        
        **3. Асимметричная криптография:**
        - Приватный ключ никогда не покидает устройство
        - Подпись создается локально
        
        **Процесс аутентификации:**
        ```
        1. Сервер отправляет challenge
        2. Устройство создает подпись с помощью приватного ключа
        3. Сервер проверяет подпись с помощью публичного ключа
        4. Аутентификация успешна только для правильного домена
        ```
        
        **Результат:** Даже если пользователь попадет на фишинговый сайт, 
        аутентификация не сработает, так как домен не совпадает!
        """)

# Для обратной совместимости
class AuthenticationMethods(AuthenticationMethodsModule):
    pass