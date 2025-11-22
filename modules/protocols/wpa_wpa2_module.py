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
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct
import binascii
import random

@dataclass
class WPASecurity:
    protocol: str
    encryption: str
    key_management: str
    security_level: str
    year_introduced: int

@dataclass
class WPAHandshake:
    anonce: str  # Authenticator Nonce
    snonce: str  # Supplicant Nonce
    mic: str     # Message Integrity Code
    ptk: str     # Pairwise Transient Key
    gtk: str     # Group Temporal Key

@dataclass
class WPAAttack:
    name: str
    description: str
    complexity: str
    success_rate: float
    time_required: str
    requirements: List[str]

class WPAWPA2Module(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Протоколы WPA/WPA2"
        self.description = "Wi-Fi Protected Access - современные протоколы безопасности Wi-Fi"
        self.category = "protocols"
        self.icon = ""
        self.order = 9
        
        # Сравнение протоколов
        self.protocols_comparison = {
            "WPA": WPASecurity(
                "WPA",
                "TKIP (RC4-based)",
                "PSK/Enterprise",
                "Средний",
                2003
            ),
            "WPA2": WPASecurity(
                "WPA2", 
                "AES-CCMP",
                "PSK/Enterprise",
                "Высокий",
                2004
            ),
            "WPA3": WPASecurity(
                "WPA3",
                "AES-GCMP-256",
                "SAE/Enterprise",
                "Очень высокий",
                2018
            )
        }
        
        # Атаки на WPA/WPA2
        self.attacks = {
            "wpa_psk": WPAAttack(
                "Атака на WPA-PSK",
                "Словарная атака на предварительный общий ключ",
                "Средняя",
                60.0,
                "Часы-дни",
                ["Захват handshake", "Словарь паролей", "Вычислительные ресурсы"]
            ),
            "wpa_enterprise": WPAAttack(
                "Атака на WPA-Enterprise", 
                "Атака на инфраструктуру RADIUS",
                "Высокая",
                30.0,
                "Дни-недели",
                ["Сетевой доступ", "Сертификаты", "Знание инфраструктуры"]
            ),
            "kr00k": WPAAttack(
                "Атака Kr00k",
                "Уязвимость в разобщении сессии",
                "Низкая",
                95.0,
                "Минуты",
                ["Уязвимое устройство", "Активный трафик"]
            ),
            "krack": WPAAttack(
                "Атака KRACK",
                "Key Reinstallation Attacks",
                "Средняя",
                100.0,
                "Минуты",
                ["Близость к сети", "Активное вмешательство"]
            ),
            "wpa_pmkid": WPAAttack(
                "Атака PMKID",
                "Восстановление PMKID без handshake",
                "Средняя",
                70.0,
                "Часы-дни", 
                ["Поддержка PMKID", "Словарь паролей"]
            )
        }

    def render(self):
        st.title("📶 Протоколы WPA и WPA2")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **WPA (Wi-Fi Protected Access)** - протокол безопасности, разработанный как замена уязвимого WEP.
            
            ### 🏗️ Архитектура WPA/WPA2:
            
            **Компоненты безопасности:**
            - **TKIP (Temporal Key Integrity Protocol)**: Улучшенный RC4 для WPA
            - **AES-CCMP**: Advanced Encryption Standard для WPA2
            - **4-way Handshake**: Взаимная аутентификация и генерация ключей
            - **PMK (Pairwise Master Key)**: Основной ключ, производный от пароля
            - **PTK (Pairwise Transient Key)**: Сессионный ключ для шифрования
            - **GTK (Group Temporal Key)**: Групповой ключ для multicast
            
            **Процесс 4-way Handshake:**
            ```
            1. AP → Client: ANonce (случайное число от точки доступа)
            2. Client → AP: SNonce + MIC (случайное число клиента + проверка)
            3. AP → Client: GTK + MIC (групповой ключ + проверка)  
            4. Client → AP: Подтверждение
            ```
            
            ### 🔐 Ключевые улучшения по сравнению с WEP:
            
            **1. Динамические ключи:**
            - Новые ключи для каждой сессии
            - Perfect Forward Secrecy
            - Защита от перехвата трафика
            
            **2. Надежная аутентификация:**
            - 802.1X для корпоративных сетей
            - PSK для домашних сетей
            - Взаимная аутентификация
            
            **3. Целостность данных:**
            - MIC (Message Integrity Check)
            - Защита от подделки пакетов
            - Sequence counters
            
            **4. Управление ключами:**
            - Иерархия ключей
            - Регулярная ротация ключей
            - Secure key derivation
            
            ### 📜 Эволюция стандартов:
            - **2003**: WPA как временное решение
            - **2004**: WPA2 как полный стандарт 802.11i
            - **2018**: WPA3 с дополнительной защитой
            """)

        st.markdown("---")
        
        # Основной интерфейс с вкладками
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔐 Сравнение протоколов", "🎯 Атаки на WPA/WPA2", "📊 Анализ безопасности", "🛡️ Рекомендации", "🎮 Демонстрация"])

        with tab1:
            self.render_protocols_comparison()
        
        with tab2:
            self.render_attacks_section()
            
        with tab3:
            self.render_security_analysis()
            
        with tab4:
            self.render_recommendations()
            
        with tab5:
            self.render_demo_section()

    def render_protocols_comparison(self):
        """Сравнение протоколов WPA, WPA2, WPA3"""
        st.header("🔐 Сравнение протоколов безопасности Wi-Fi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Характеристики протоколов")
            
            # Таблица сравнения
            comparison_data = []
            for protocol_name, protocol in self.protocols_comparison.items():
                comparison_data.append({
                    "Протокол": protocol_name,
                    "Шифрование": protocol.encryption,
                    "Управление ключами": protocol.key_management,
                    "Уровень безопасности": protocol.security_level,
                    "Год внедрения": protocol.year_introduced
                })
            
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True, hide_index=True)
            
            # Визуализация эволюции
            st.subheader("📈 Эволюция безопасности")
            
            protocols = list(self.protocols_comparison.keys())
            security_scores = {
                "WPA": 6,
                "WPA2": 8, 
                "WPA3": 9
            }
            years = [p.year_introduced for p in self.protocols_comparison.values()]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=protocols,
                y=[security_scores[p] for p in protocols],
                mode='lines+markers+text',
                line=dict(color='green', width=4),
                marker=dict(size=12),
                text=[f"{security_scores[p]}/10" for p in protocols],
                textposition="top center"
            ))
            
            fig.update_layout(
                title="Эволюция уровня безопасности Wi-Fi",
                xaxis_title="Протокол",
                yaxis_title="Уровень безопасности (1-10)",
                yaxis_range=[0, 10],
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🔍 Детали протоколов")
            
            selected_protocol = st.selectbox(
                "Выберите протокол для деталей:",
                list(self.protocols_comparison.keys()),
                key="protocol_select"
            )
            
            protocol = self.protocols_comparison[selected_protocol]
            
            st.markdown(f"### {selected_protocol}")
            
            # Детальная информация о протоколе
            info_cols = st.columns(2)
            with info_cols[0]:
                st.metric("Шифрование", protocol.encryption)
                st.metric("Уровень безопасности", protocol.security_level)
            with info_cols[1]:
                st.metric("Управление ключами", protocol.key_management)
                st.metric("Год внедрения", protocol.year_introduced)
            
            # Специфическая информация для каждого протокола
            if selected_protocol == "WPA":
                st.markdown("""
                **Особенности WPA:**
                - TKIP (Temporal Key Integrity Protocol)
                - MIC (Message Integrity Check)
                - Sequence counters
                - Временное решение до WPA2
                """)
            elif selected_protocol == "WPA2":
                st.markdown("""
                **Особенности WPA2:**
                - AES-CCMP encryption
                - 4-way handshake
                - PMK/PTK key hierarchy  
                - Полная реализация 802.11i
                """)
            elif selected_protocol == "WPA3":
                st.markdown("""
                **Особенности WPA3:**
                - SAE (Simultaneous Authentication of Equals)
                - Forward secrecy
                - Enhanced Open для публичных сетей
                - 192-битная безопасность для enterprise
                """)
            
            # Демонстрация handshake
            st.subheader("🤝 Демонстрация 4-way Handshake")
            
            if st.button("🔄 Сгенерировать Handshake", key="gen_handshake"):
                handshake = self.generate_handshake_demo()
                st.session_state.wpa_handshake = handshake
            
            if 'wpa_handshake' in st.session_state:
                handshake = st.session_state.wpa_handshake
                
                steps = [
                    ("1. AP → Client", f"ANonce: {handshake.anonce[:16]}..."),
                    ("2. Client → AP", f"SNonce: {handshake.snonce[:16]}... + MIC"),
                    ("3. AP → Client", f"GTK + MIC"),
                    ("4. Client → AP", "Подтверждение")
                ]
                
                for step, description in steps:
                    st.write(f"**{step}** - {description}")
                
                with st.expander("🔑 Детали ключей"):
                    st.text(f"PTK: {handshake.ptk[:32]}...")
                    st.text(f"GTK: {handshake.gtk[:32]}...")
                    st.text(f"MIC: {handshake.mic}")

    def render_attacks_section(self):
        """Демонстрация атак на WPA/WPA2"""
        st.header("🎯 Атаки на WPA и WPA2")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📋 Методы атак")
            
            # Таблица атак
            attacks_data = []
            for attack_id, attack in self.attacks.items():
                attacks_data.append({
                    "Атака": attack.name,
                    "Описание": attack.description,
                    "Сложность": attack.complexity,
                    "Успешность": f"{attack.success_rate}%",
                    "Время": attack.time_required
                })
            
            df_attacks = pd.DataFrame(attacks_data)
            st.dataframe(df_attacks, use_container_width=True, hide_index=True)
            
            # Выбор атаки для деталей
            selected_attack = st.selectbox(
                "Выберите атаку для деталей:",
                list(self.attacks.keys()),
                key="wpa_attack_select"
            )
            
            attack = self.attacks[selected_attack]
            
            st.markdown(f"### {attack.name}")
            st.write(attack.description)
            
            # Детали атаки
            st.write("**Требования:**")
            for req in attack.requirements:
                st.write(f"- {req}")
            
            # Демонстрация выбранной атаки
            if selected_attack == "wpa_psk":
                self.demo_wpa_psk_attack()
            elif selected_attack == "krack":
                self.demo_krack_attack()
            elif selected_attack == "wpa_pmkid":
                self.demo_pmkid_attack()
        
        with col2:
            st.subheader("📊 Эффективность атак")
            
            # График успешности атак
            attack_names = [a.name for a in self.attacks.values()]
            success_rates = [a.success_rate for a in self.attacks.values()]
            complexity_scores = {
                "Низкая": 1,
                "Средняя": 2, 
                "Высокая": 3
            }
            complexities = [complexity_scores[a.complexity] for a in self.attacks.values()]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Успешность (%)',
                x=attack_names,
                y=success_rates,
                yaxis='y',
                offsetgroup=1
            ))
            fig.add_trace(go.Bar(
                name='Сложность',
                x=attack_names, 
                y=complexities,
                yaxis='y2',
                offsetgroup=2
            ))
            
            fig.update_layout(
                title="Сравнение атак на WPA/WPA2",
                xaxis_title="Атака",
                yaxis=dict(title="Успешность (%)", side='left'),
                yaxis2=dict(title="Сложность (1-3)", side='right', overlaying='y'),
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

    def render_security_analysis(self):
        """Анализ безопасности WPA/WPA2"""
        st.header("📊 Анализ безопасности WPA/WPA2")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🛡️ Сильные стороны")
            
            strengths = [
                ("Динамические ключи", "Новые ключи для каждой сессии", "🔄"),
                ("Взаимная аутентификация", "Обе стороны доказывают идентичность", "🤝"),
                ("Целостность данных", "MIC защищает от модификации", "✓"),
                ("Perfect Forward Secrecy", "Компрометация ключа не раскрывает прошлые сессии", "🔒"),
                ("Сертификация", "Wi-Fi Alliance тестирует совместимость", "🏆")
            ]
            
            for title, description, icon in strengths:
                with st.expander(f"{icon} {title}"):
                    st.write(description)
            
            # Оценка безопасности
            st.subheader("📈 Оценка безопасности")
            
            security_metrics = {
                "Аутентификация": 8,
                "Шифрование": 9,
                "Целостность": 8,
                "Управление ключами": 9,
                "Стойкость к атакам": 7
            }
            
            fig = go.Figure(go.Scatterpolar(
                r=list(security_metrics.values()),
                theta=list(security_metrics.keys()),
                fill='toself',
                name='WPA2 Security'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )),
                showlegend=False,
                title="Профиль безопасности WPA2",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⚠️ Слабые стороны и уязвимости")
            
            vulnerabilities = {
                "WPA-PSK словарные атаки": {
                    "severity": "Высокая",
                    "explanation": "Слабые пароли уязвимы к перебору",
                    "mitigation": "Использовать сложные пароли"
                },
                "Атака KRACK": {
                    "severity": "Критическая", 
                    "explanation": "Переустановка ключа в 4-way handshake",
                    "mitigation": "Обновление клиентов и точек доступа"
                },
                "Атака PMKID": {
                    "severity": "Средняя",
                    "explanation": "Восстановление хеша без handshake",
                    "mitigation": "Отключение PMKID кэширования"
                },
                "Атака Kr00k": {
                    "severity": "Высокая",
                    "explanation": "Уязвимость в разобщении сессии",
                    "mitigation": "Обновление firmware"
                },
                "Офлайн-атаки": {
                    "severity": "Средняя", 
                    "explanation": "Захваченный handshake можно атаковать офлайн",
                    "mitigation": "Использование WPA3"
                }
            }
            
            for vuln, info in vulnerabilities.items():
                with st.expander(f"🔓 {vuln} - {info['severity']}"):
                    st.write(f"**Объяснение:** {info['explanation']}")
                    st.write(f"**Защита:** {info['mitigation']}")

    def render_recommendations(self):
        """Рекомендации по безопасности"""
        st.header("🛡️ Рекомендации по безопасности")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔧 Конфигурация безопасности")
            
            config_recommendations = [
                ("WPA2/WPA3", "Используйте WPA2 или WPA3 вместо WPA", "critical"),
                ("Сложные пароли", "Минимум 12 символов, разные категории", "high"),
                ("Регулярные обновления", "Обновляйте firmware точек доступа", "high"),
                ("Отключение WPS", "WPS уязвим к brute-force", "high"),
                ("Фильтрация MAC", "Дополнительный уровень безопасности", "medium"),
                ("Скрытие SSID", "Ограниченная эффективность", "low")
            ]
            
            for rec, description, priority in config_recommendations:
                priority_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
                st.write(f"{priority_icon[priority]} **{rec}** - {description}")
            
            st.subheader("🏢 Для корпоративных сетей")
            
            enterprise_recs = [
                "✅ Используйте WPA2/WPA3-Enterprise",
                "✅ Внедрите 802.1X аутентификацию", 
                "✅ Используйте сертификаты вместо паролей",
                "✅ Настройте RADIUS сервер",
                "✅ Реализуйте сегментацию сети",
                "✅ Мониторьте подозрительную активность"
            ]
            
            for rec in enterprise_recs:
                st.write(rec)
        
        with col2:
            st.subheader("📋 План миграции на WPA3")
            
            migration_steps = [
                ("1. Аудит оборудования", "Проверьте поддержку WPA3"),
                ("2. Тестирование", "Протестируйте в изолированной среде"),
                ("3. Поэтапное внедрение", "Начните с менее критичных сетей"),
                ("4. Обучение пользователей", "Объясните преимущества WPA3"),
                ("5. Мониторинг", "Контролируйте работу после миграции"),
                ("6. Полный переход", "Завершите миграцию на всех устройствах")
            ]
            
            for step, description in migration_steps:
                st.write(f"**{step}** - {description}")
            
            st.subheader("🚨 Экстренные меры")
            
            emergency_measures = [
                "🔴 Немедленно обновить firmware при уязвимостях",
                "🔴 Изменить пароли при подозрении на компрометацию", 
                "🔴 Проверить логи на подозрительную активность",
                "🟠 Регулярно проводить пентесты",
                "🟠 Внедрить SIEM систему",
                "🟢 Обновлять политики безопасности"
            ]
            
            for measure in emergency_measures:
                st.write(measure)

    def render_demo_section(self):
        """Интерактивная демонстрация"""
        st.header("🎮 Интерактивная демонстрация")
        
        st.warning("""
        ⚠️ Эта демонстрация показывает образовательные цели безопасности WPA/WPA2.
        Использование этих техник без разрешения является незаконным.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔐 Демонстрация WPA-PSK атаки")
            
            # Настройка демонстрации
            ssid = st.text_input("SSID сети:", "HomeNetwork", key="wpa_ssid")
            password_strength = st.select_slider(
                "Сложность пароля:",
                options=["Очень слабый", "Слабый", "Средний", "Сложный", "Очень сложный"],
                value="Средний",
                key="pwd_strength"
            )
            
            # Генерация демонстрационного пароля
            if 'wpa_demo_password' not in st.session_state:
                st.session_state.wpa_demo_password = self.generate_demo_password("Средний")
            
            st.text_input(
                "Пароль WPA-PSK (известен для демонстрации):",
                st.session_state.wpa_demo_password,
                disabled=True,
                key="demo_pwd_display"
            )
            
            # Словарная атака
            dict_size = st.slider(
                "Размер словаря:",
                min_value=1000,
                max_value=1000000,
                value=10000,
                step=1000,
                key="dict_size"
            )
            
            computing_power = st.select_slider(
                "Вычислительная мощность:",
                options=["Слабый CPU", "Обычный CPU", "Мощный CPU", "GPU кластер"],
                value="Обычный CPU",
                key="computing_power"
            )
            
            if st.button("🎯 Начать словарную атаку", key="start_wpa_attack"):
                # Симуляция атаки
                success, time_taken, attempts = self.simulate_wpa_attack(
                    st.session_state.wpa_demo_password,
                    password_strength,
                    dict_size,
                    computing_power
                )
                
                st.session_state.wpa_attack_result = {
                    "success": success,
                    "time_taken": time_taken,
                    "attempts": attempts,
                    "password_strength": password_strength
                }
                st.rerun()
        
        with col2:
            st.subheader("📊 Результат атаки")
            
            if 'wpa_attack_result' in st.session_state:
                result = st.session_state.wpa_attack_result
                
                if result["success"]:
                    st.success("🎉 Пароль успешно взломан!")
                    
                    col_success1, col_success2 = st.columns(2)
                    with col_success1:
                        st.metric("Время атаки", f"{result['time_taken']}")
                        st.metric("Попыток", f"{result['attempts']:,}")
                    with col_success2:
                        st.metric("Сложность пароля", result["password_strength"])
                        st.metric("Восстановленный пароль", st.session_state.wpa_demo_password)
                    
                    st.balloons()
                else:
                    st.error("❌ Атака не удалась. Пароль слишком сложный.")
                    
                    col_fail1, col_fail2 = st.columns(2)
                    with col_fail1:
                        st.metric("Потраченное время", f"{result['time_taken']}")
                        st.metric("Попыток", f"{result['attempts']:,}")
                    with col_fail2:
                        st.metric("Сложность пароля", result["password_strength"])
                        st.metric("Рекомендация", "Увеличить словарь")
                
                # Визуализация прогресса
                st.subheader("📈 Прогресс подбора пароля")
                
                strength_scores = {
                    "Очень слабый": 20,
                    "Слабый": 40,
                    "Средний": 60, 
                    "Сложный": 80,
                    "Очень сложный": 95
                }
                
                progress = strength_scores[result["password_strength"]] if result["success"] else 0
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = progress,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Успешность подбора"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "green"}
                        ],
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("👆 Запустите атаку для отображения результатов")

    # Вспомогательные методы

    def generate_handshake_demo(self) -> WPAHandshake:
        """Генерация демонстрационного handshake"""
        return WPAHandshake(
            anonce=secrets.token_hex(32),
            snonce=secrets.token_hex(32),
            mic=secrets.token_hex(16),
            ptk=secrets.token_hex(48),
            gtk=secrets.token_hex(32)
        )

    def generate_demo_password(self, strength: str) -> str:
        """Генерация демонстрационного пароля"""
        if strength == "Очень слабый":
            return "password123"
        elif strength == "Слабый":
            return "summer2024"
        elif strength == "Средний":
            return "Blue42Sky!"
        elif strength == "Сложный":
            return "K8#pQ2$mN9!"
        else:  # Очень сложный
            return "G7@xP5&vR2#qW9*zM"

    def simulate_wpa_attack(self, target_password: str, strength: str, dict_size: int, computing_power: str) -> Tuple[bool, str, int]:
        """Симуляция WPA-PSK атаки"""
        import time
        
        # Вероятность успеха в зависимости от сложности пароля
        success_rates = {
            "Очень слабый": 0.95,
            "Слабый": 0.75, 
            "Средний": 0.40,
            "Сложный": 0.15,
            "Очень сложный": 0.02
        }
        
        # Время атаки в зависимости от вычислительной мощности
        time_multipliers = {
            "Слабый CPU": 10,
            "Обычный CPU": 1,
            "Мощный CPU": 0.3,
            "GPU кластер": 0.1
        }
        
        success_probability = success_rates[strength]
        success = random.random() < success_probability
        
        # Расчет времени и попыток
        base_time = 3600  # 1 час в секундах
        time_taken = base_time * time_multipliers[computing_power] * (1 / success_probability)
        
        # Форматирование времени
        if time_taken < 60:
            time_str = f"{int(time_taken)} сек"
        elif time_taken < 3600:
            time_str = f"{int(time_taken/60)} мин"
        else:
            time_str = f"{int(time_taken/3600)} час"
        
        attempts = int(dict_size * success_probability)
        
        time.sleep(0.5)  # Имитация обработки
        
        return success, time_str, attempts

    def demo_wpa_psk_attack(self):
        """Демонстрация WPA-PSK атаки"""
        st.markdown("""
        ### 🔓 Атака на WPA-PSK
        
        **Принцип работы:**
        - Захват 4-way handshake
        - Офлайн подбор PMK (Pairwise Master Key)
        - Проверка MIC для валидации пароля
        
        **Процесс:**
        ```
        1. Мониторинг сети и захват handshake
        2. Извлечение ANonce, SNonce, MAC адресов
        3. Вычисление PMK = PBKDF2(Password, SSID, 4096, 256)
        4. Вычисление PTK из PMK и nonces
        5. Проверка MIC для валидации пароля
        ```
        
        **Эффективность:**
        - Зависит от сложности пароля
        - Словари содержат миллионы распространенных паролей
        - GPU ускоряет перебор в 100+ раз
        """)

    def demo_krack_attack(self):
        """Демонстрация атаки KRACK"""
        st.markdown("""
        ### ⚡ Атака KRACK (Key Reinstallation Attacks)
        
        **Принцип работы:**
        - Принудительная переустановка ключа сессии
        - Обнуление nonce и повторное использование ключевого потока
        - Дешифрование и инъекция трафика
        
        **Уязвимость:**
        - 4-way handshake не гарантирует однократную установку ключа
        - Клиенты повторно используют ключи при получении дубликатов
        - Отсутствие защиты от replay-атак в handshake
        
        **Защита:**
        - Обновление клиентов и точек доступа
        - Проверка установки ключа только один раз
        - Использование WPA3
        """)

    def demo_pmkid_attack(self):
        """Демонстрация атаки PMKID"""
        st.markdown("""
        ### 🆕 Атака PMKID
        
        **Принцип работы:**
        - Извлечение PMKID из первого сообщения EAPOL
        - PMKID = HMAC-SHA1(PMK, "PMK Name" | MAC_AP | MAC_Client)
        - Офлайн подбор без захвата полного handshake
        
        **Преимущества:**
        - Не требует активного клиента
        - Не нужно ждать handshake
        - Работает против одиночных точек доступа
        
        **Ограничения:**
        - Требует поддержки PMKID кэширования
        - Эффективность зависит от сложности пароля
        """)

# Для обратной совместимости
class WPAWPA2AttackModule(WPAWPA2Module):
    pass
