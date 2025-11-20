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
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import struct
import binascii

@dataclass
class WEPKey:
    key: str
    length: int
    strength: str

@dataclass
class WEPPacket:
    iv: str  # Initialization Vector (24 бита)
    data: str  # Зашифрованные данные
    icv: str  # Integrity Check Value (32 бита)

@dataclass
class WEPAttack:
    name: str
    description: str
    complexity: str
    success_rate: float
    packets_required: int

class WEPModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Протокол WEP"
        self.description = "Wired Equivalent Privacy - уязвимый протокол безопасности Wi-Fi"
        self.category = "protocols"
        self.icon = ""
        self.order = 8
        
        # Стандартные длины ключей WEP
        self.key_lengths = {
            64: "40-битный ключ + 24-битный IV",
            128: "104-битный ключ + 24-битный IV", 
            152: "128-битный ключ + 24-битный IV",
            256: "232-битный ключ + 24-битный IV"
        }
        
        # Атаки на WEP
        self.attacks = {
            "fms": WEPAttack(
                "Атака FMS (Fluhrer, Mantin, Shamir)",
                "Использование слабых IV для восстановления ключа",
                "Низкая",
                95.0,
                5000000
            ),
            "korek": WEPAttack(
                "Атака Korek",
                "Улучшенная версия FMS с большим количеством слабых IV",
                "Средняя", 
                98.0,
                1000000
            ),
            "ptw": WEPAttack(
                "Атака PTW (Pyshkin, Tews, Weinmann)",
                "Современная атака с использованием ARP-пакетов",
                "Высокая",
                99.9,
                40000
            ),
            "fragmentation": WEPAttack(
                "Фрагментационная атака",
                "Восстановление ключа через фрагменты данных",
                "Средняя",
                85.0,
                100000
            ),
            "chopchop": WEPAttack(
                "Атака Chop-Chop",
                "Последовательное угадывание байтов пакета",
                "Высокая",
                90.0,
                1000
            )
        }
        
        # Слабые IV для демонстрации
        self.weak_ivs = self.generate_weak_ivs()
        
        # Демонстрационные ключи
        self.demo_keys = self.generate_demo_keys()

    def render(self):
        st.title("📡 Протокол WEP и его уязвимости")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **WEP (Wired Equivalent Privacy)** - первый протокол безопасности для Wi-Fi сетей, представленный в 1999 году.
            
            ### 🏗️ Архитектура WEP:
            
            **Компоненты шифрования:**
            - **Секретный ключ**: 40/104/128/232 бита (статический)
            - **Вектор инициализации (IV)**: 24 бита (открытый)
            - **RC4 алгоритм**: Потоковый шифр
            - **ICV (Integrity Check Value)**: CRC-32 checksum
            
            **Процесс шифрования:**
            ```
            1. IV (24 бита) + Секретный ключ = Ключ RC4
            2. RC4 генерирует ключевой поток
            3. Данные ⊕ ключевой поток = Шифротекст
            4. ICV = CRC32(Данные)
            5. ICV ⊕ ключевой поток = Зашифрованный ICV
            ```
            
            ### 🔓 Основные уязвимости:
            
            **1. Короткий IV (24 бита):**
            - Всего 16,777,216 возможных IV
            - Повторение IV через несколько часов активного использования
            - Коллизии позволяют криптоанализ
            
            **2. Слабые IV:**
            - Некоторые IV раскрывают информацию о ключе
            - Атаки FMS/Korek используют эту уязвимость
            
            **3. Статический ключ:**
            - Один ключ для всех пакетов
            - Нет Perfect Forward Secrecy
            
            **4. Небезопасная аутентификация:**
            - Shared Key Authentication уязвима
            - Отсутствие защиты от replay-атак
            
            **5. Слабая целостность (ICV):**
            - CRC-32 линейна и обратима
            - Возможность модификации пакетов
            
            ### 📜 Историческое значение:
            - **1999**: Внедрение WEP в стандарт 802.11
            - **2001**: Первые успешные атаки (Fluhrer, Mantin, Shamir)
            - **2005**: WEP официально объявлен небезопасным
            - **2009**: Взлом WEP за 1-5 минут с помощью PTW атаки
            """)

        st.markdown("---")
        
        # Основной интерфейс с вкладками
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔐 Шифрование WEP", "🎯 Атаки на WEP", "📊 Анализ уязвимостей", "🛡️ Защита и миграция", "🎮 Демонстрация взлома"])

        with tab1:
            self.render_encryption_section()
        
        with tab2:
            self.render_attacks_section()
            
        with tab3:
            self.render_vulnerability_analysis_section()
            
        with tab4:
            self.render_protection_section()
            
        with tab5:
            self.render_hack_demo_section()

    def render_encryption_section(self):
        """Демонстрация шифрования WEP"""
        st.header("🔐 Процесс шифрования WEP")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⚙️ Параметры шифрования")
            
            # Выбор ключа
            key_length = st.selectbox(
                "Длина ключа:",
                list(self.key_lengths.keys()),
                format_func=lambda x: f"{x} бит - {self.key_lengths[x]}",
                key="wep_key_length"
            )
            
            # Генерация или ввод ключа
            if st.button("🎲 Сгенерировать ключ WEP", key="gen_wep_key"):
                key = secrets.token_hex(key_length // 8)
                st.session_state.wep_key = key
                st.session_state.wep_key_length = key_length
            
            key_input = st.text_input(
                "Ключ WEP (hex):",
                st.session_state.get('wep_key', ''),
                key="wep_key_input"
            )
            
            # Данные для шифрования
            plaintext = st.text_area(
                "Данные для шифрования:",
                "Confidential wireless data",
                height=100,
                key="wep_plaintext"
            )
            
            if st.button("🔒 Зашифровать WEP", key="encrypt_wep_btn"):
                if key_input and plaintext:
                    # Генерируем IV
                    iv = secrets.token_hex(3)  # 24 бита = 3 байта
                    
                    # Шифруем данные
                    encrypted_data, icv = self.wep_encrypt(plaintext, key_input, iv)
                    
                    st.session_state.wep_packet = WEPPacket(
                        iv=iv,
                        data=encrypted_data,
                        icv=icv
                    )
                    st.session_state.wep_plaintext = plaintext
                    st.rerun()
        
        with col2:
            st.subheader("📄 Результат шифрования")
            
            if 'wep_packet' in st.session_state:
                packet = st.session_state.wep_packet
                
                st.success("✅ Данные зашифрованы с помощью WEP!")
                
                st.text_input(
                    "Вектор инициализации (IV):",
                    packet.iv,
                    key="iv_display"
                )
                
                st.text_area(
                    "Зашифрованные данные:",
                    packet.data,
                    height=100,
                    key="enc_data_display"
                )
                
                st.text_input(
                    "ICV (Integrity Check Value):",
                    packet.icv,
                    key="icv_display"
                )
                
                # Детали шифрования
                with st.expander("🔍 Детали процесса шифрования"):
                    self.display_encryption_details(st.session_state.wep_plaintext, packet)

    def render_attacks_section(self):
        """Демонстрация атак на WEP"""
        st.header("🎯 Атаки на протокол WEP")
        
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
                    "Пакетов требуется": f"{attack.packets_required:,}"
                })
            
            df_attacks = pd.DataFrame(attacks_data)
            st.dataframe(df_attacks, use_container_width=True, hide_index=True)
            
            # Выбор атаки для демонстрации
            selected_attack = st.selectbox(
                "Выберите атаку для деталей:",
                list(self.attacks.keys()),
                key="attack_select"
            )
            
            attack = self.attacks[selected_attack]
            
            st.markdown(f"### {attack.name}")
            st.write(attack.description)
            
            # Демонстрация выбранной атаки
            if selected_attack == "fms":
                self.demo_fms_attack()
            elif selected_attack == "ptw":
                self.demo_ptw_attack()
            elif selected_attack == "chopchop":
                self.demo_chopchop_attack()
        
        with col2:
            st.subheader("📊 Эффективность атак")
            
            # График успешности атак
            attack_names = [a.name for a in self.attacks.values()]
            success_rates = [a.success_rate for a in self.attacks.values()]
            packets_required = [a.packets_required for a in self.attacks.values()]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Успешность (%)',
                x=attack_names,
                y=success_rates,
                yaxis='y',
                offsetgroup=1
            ))
            fig.add_trace(go.Bar(
                name='Пакетов требуется',
                x=attack_names, 
                y=[p / 10000 for p in packets_required],  # Масштабируем для графика
                yaxis='y2',
                offsetgroup=2
            ))
            
            fig.update_layout(
                title="Сравнение эффективности атак на WEP",
                xaxis_title="Атака",
                yaxis=dict(title="Успешность (%)", side='left'),
                yaxis2=dict(title="Пакетов (x10,000)", side='right', overlaying='y'),
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

    def render_vulnerability_analysis_section(self):
        """Анализ уязвимостей WEP"""
        st.header("📊 Анализ уязвимостей WEP")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔓 Ключевые уязвимости")
            
            vulnerabilities = {
                "Короткий IV": {
                    "severity": "Критическая",
                    "explanation": "24-битный IV переиспользуется через несколько часов",
                    "impact": "Коллизии ключевых потоков"
                },
                "Слабые IV": {
                    "severity": "Критическая", 
                    "explanation": "Некоторые IV раскрывают биты ключа",
                    "impact": "Восстановление ключа через FMS/Korek"
                },
                "Статический ключ": {
                    "severity": "Высокая",
                    "explanation": "Один ключ для всех сессий",
                    "impact": "Нет Perfect Forward Secrecy"
                },
                "CRC-32 ICV": {
                    "severity": "Высокая",
                    "explanation": "Линейная проверка целостности",
                    "impact": "Возможность модификации пакетов"
                },
                "Shared Key Auth": {
                    "severity": "Средняя",
                    "explanation": "Уязвимая схема аутентификации", 
                    "impact": "Раскрытие ключевого потока"
                }
            }
            
            for vuln, info in vulnerabilities.items():
                with st.expander(f"🔓 {vuln} - {info['severity']}"):
                    st.write(f"**Объяснение:** {info['explanation']}")
                    st.write(f"**Воздействие:** {info['impact']}")
            
            # Визуализация уязвимостей
            st.subheader("📈 Оценка уязвимостей")
            
            vuln_names = list(vulnerabilities.keys())
            severity_scores = {
                "Критическая": 10,
                "Высокая": 8, 
                "Средняя": 5,
                "Низкая": 2
            }
            scores = [severity_scores[v["severity"]] for v in vulnerabilities.values()]
            
            fig = go.Figure(data=[go.Bar(x=vuln_names, y=scores)])
            fig.update_layout(
                title="Уровень критичности уязвимостей WEP",
                yaxis_title="Уровень критичности (1-10)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Эволюция взлома WEP")
            
            # Хронология взлома
            timeline_data = {
                "Год": [1999, 2001, 2002, 2004, 2005, 2007, 2009],
                "Событие": [
                    "Внедрение WEP",
                    "Атака FMS опубликована", 
                    "Атака Korek улучшает FMS",
                    "Фрагментационная атака",
                    "WEP объявлен небезопасным",
                    "Атака PTW опубликована",
                    "Взлом за 1-5 минут"
                ],
                "Время взлома": [None, "Недели", "Дни", "Часы", "Минуты", "Минуты", "1-5 минут"],
                "Пакетов требуется": [None, "10M+", "5M", "500K", "100K", "40K", "40K"]
            }
            
            df_timeline = pd.DataFrame(timeline_data)
            st.dataframe(df_timeline, use_container_width=True, hide_index=True)
            
            # График времени взлома
            st.subheader("⏱️ Снижение времени взлома")
            
            years = [2001, 2002, 2004, 2005, 2007, 2009]
            # Условное время в минутах для графика
            hack_times = [10080, 1440, 240, 60, 10, 3]  
            
            fig2 = go.Figure(data=[go.Scatter(
                x=years, y=hack_times, mode='lines+markers', line=dict(color='red', width=3)
            )])
            fig2.update_layout(
                title="Эволюция времени взлома WEP",
                xaxis_title="Год",
                yaxis_title="Время взлома (минуты, логарифмическая шкала)",
                yaxis_type="log",
                height=300
            )
            st.plotly_chart(fig2, use_container_width=True)

    def render_protection_section(self):
        """Рекомендации по защите и миграции"""
        st.header("🛡️ Защита и миграция с WEP")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚨 Почему WEP небезопасен?")
            
            st.error("""
            **WEP НЕ ДОЛЖЕН ИСПОЛЬЗОВАТЬСЯ!**
            
            Даже с максимальной длиной ключа (256 бит) WEP может быть взломан 
            за несколько минут с использованием современного оборудования.
            """)
            
            reasons = [
                "✅ Атаки работают против ЛЮБОЙ длины ключа WEP",
                "✅ Не требуется специальное оборудование", 
                "✅ Взлом возможен с обычного ноутбука",
                "✅ Автоматизированные инструменты доступны бесплатно",
                "✅ Защита через 'скрытие SSID' не эффективна"
            ]
            
            for reason in reasons:
                st.write(reason)
            
            st.subheader("🔄 Рекомендации по миграции")
            
            migration_paths = {
                "WPA": {
                    "security": "Базовый",
                    "recommendation": "Временное решение",
                    "notes": "Уязвим к словарным атакам"
                },
                "WPA2": {
                    "security": "Хороший", 
                    "recommendation": "Минимальный стандарт",
                    "notes": "Рекомендуется с AES-CCMP"
                },
                "WPA3": {
                    "security": "Отличный",
                    "recommendation": "Современный стандарт",
                    "notes": "Защита от офлайн-атак"
                }
            }
            
            for protocol, info in migration_paths.items():
                with st.expander(f"🛡️ {protocol}"):
                    st.write(f"**Уровень безопасности:** {info['security']}")
                    st.write(f"**Рекомендация:** {info['recommendation']}")
                    st.write(f"**Примечания:** {info['notes']}")
        
        with col2:
            st.subheader("📋 План миграции")
            
            migration_steps = [
                ("1. Аудит", "Выявить все устройства, использующие WEP"),
                ("2. Планирование", "Выбрать WPA2/WPA3 и настроить политики"),
                ("3. Тестирование", "Протестировать новые настройки в изолированной среде"),
                ("4. Коммуникация", "Уведомить пользователей о предстоящих изменениях"),
                ("5. Миграция", "Поэтапно переводить устройства на новый стандарт"),
                ("6. Мониторинг", "Контролировать работу после миграции"),
                ("7. Отключение", "Полностью отключить WEP после успешной миграции")
            ]
            
            for step, description in migration_steps:
                st.write(f"**{step}** - {description}")
            
            st.subheader("🔧 Технические рекомендации")
            
            technical_recs = [
                "✅ Используйте WPA2 с AES-CCMP",
                "✅ Применяйте сложные пароли (минимум 12 символов)",
                "✅ Регулярно обновляйте прошивки точек доступа",
                "✅ Рассмотрите переход на WPA3 для новой инфраструктуры",
                "✅ Используйте 802.1X для корпоративных сред",
                "✅ Реализуйте сегментацию сети",
                "✅ Мониторьте подозрительную активность"
            ]
            
            for rec in technical_recs:
                st.write(rec)

    def render_hack_demo_section(self):
        """Интерактивная демонстрация взлома WEP"""
        st.header("🎮 Интерактивная демонстрация взлома WEP")
        
        st.warning("""
        ⚠️ Эта демонстрация показывает образовательные цели взлома WEP.
        Использование этих техник без разрешения является незаконным.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⚙️ Настройка демонстрации")
            
            # Целевая сеть
            ssid = st.text_input("SSID целевой сети:", "HomeWiFi", key="target_ssid")
            key_length = st.select_slider(
                "Длина ключа WEP:",
                options=[64, 128, 152, 256],
                value=128,
                key="demo_key_length"
            )
            
            # Генерация целевого ключа
            if 'target_wep_key' not in st.session_state:
                st.session_state.target_wep_key = secrets.token_hex(key_length // 8)
            
            st.text_input(
                "Секретный ключ WEP (известен только для демонстрации):",
                st.session_state.target_wep_key,
                disabled=True,
                key="target_key_display"
            )
            
            # Захват пакетов
            packets_captured = st.slider(
                "Количество захваченных пакетов:",
                min_value=1000,
                max_value=1000000,
                value=50000,
                step=1000,
                key="packets_captured"
            )
            
            if st.button("🎯 Начать атаку PTW", key="start_attack_btn"):
                # Симуляция атаки
                success, recovered_key, time_taken = self.simulate_ptw_attack(
                    st.session_state.target_wep_key, 
                    packets_captured
                )
                
                st.session_state.attack_result = {
                    "success": success,
                    "recovered_key": recovered_key,
                    "time_taken": time_taken,
                    "packets_used": packets_captured
                }
                st.rerun()
        
        with col2:
            st.subheader("📊 Результат атаки")
            
            if 'attack_result' in st.session_state:
                result = st.session_state.attack_result
                
                if result["success"]:
                    st.success("🎉 Ключ WEP успешно взломан!")
                    
                    col_success1, col_success2 = st.columns(2)
                    with col_success1:
                        st.metric("Восстановленный ключ", result["recovered_key"][:16] + "...")
                        st.metric("Исходный ключ", st.session_state.target_wep_key[:16] + "...")
                    with col_success2:
                        st.metric("Время атаки", f"{result['time_taken']} сек")
                        st.metric("Пакетов использовано", f"{result['packets_used']:,}")
                    
                    # Проверка совпадения ключей
                    if result["recovered_key"] == st.session_state.target_wep_key:
                        st.balloons()
                        st.success("✅ Ключи полностью совпадают!")
                    else:
                        st.warning("⚠️ Ключи частично совпадают (демонстрация)")
                    
                    # Визуализация прогресса атаки
                    st.subheader("📈 Прогресс восстановления ключа")
                    
                    key_bytes = len(st.session_state.target_wep_key) // 2
                    recovered_bytes = min(key_bytes, int(key_bytes * (packets_captured / 40000)))
                    
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = recovered_bytes,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Байтов ключа восстановлено"},
                        delta = {'reference': key_bytes},
                        gauge = {
                            'axis': {'range': [None, key_bytes]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, key_bytes*0.7], 'color': "lightgray"},
                                {'range': [key_bytes*0.7, key_bytes], 'color': "gray"}
                            ],
                        }
                    ))
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                
                else:
                    st.error("❌ Атака не удалась. Требуется больше пакетов.")
                    st.info(f"Попробуйте увеличить количество пакетов до {result['packets_used'] * 2:,}")
            else:
                st.info("👆 Запустите атаку для отображения результатов")

    # Основные методы WEP

    def wep_encrypt(self, plaintext: str, key: str, iv: str) -> Tuple[str, str]:
        """Шифрование данных с помощью WEP"""
        # Преобразуем в байты
        key_bytes = bytes.fromhex(key)
        iv_bytes = bytes.fromhex(iv)
        plaintext_bytes = plaintext.encode('utf-8')
        
        # Вычисляем ICV (CRC-32)
        icv = binascii.crc32(plaintext_bytes) & 0xffffffff
        icv_bytes = struct.pack('<I', icv)
        
        # Объединяем данные и ICV
        data_with_icv = plaintext_bytes + icv_bytes
        
        # Генерируем ключ RC4: IV + Секретный ключ
        rc4_key = iv_bytes + key_bytes
        
        # Генерируем ключевой поток RC4 (упрощенная реализация)
        key_stream = self.rc4_generate(rc4_key, len(data_with_icv))
        
        # Шифруем XOR с ключевым потоком
        encrypted = bytes(a ^ b for a, b in zip(data_with_icv, key_stream))
        
        return encrypted.hex(), icv_bytes.hex()

    def rc4_generate(self, key: bytes, length: int) -> bytes:
        """Упрощенная генерация ключевого потока RC4"""
        # Инициализация S-блока
        S = list(range(256))
        j = 0
        
        # Key-scheduling algorithm (KSA)
        for i in range(256):
            j = (j + S[i] + key[i % len(key)]) % 256
            S[i], S[j] = S[j], S[i]
        
        # Pseudo-random generation algorithm (PRGA)
        i = j = 0
        key_stream = []
        
        for _ in range(length):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            key_stream.append(S[(S[i] + S[j]) % 256])
        
        return bytes(key_stream)

    def generate_weak_ivs(self) -> List[str]:
        """Генерация слабых IV для атак FMS/Korek"""
        weak_ivs = []
        
        # Слабые IV формата (A+3, N-1, X) для FMS атаки
        for a in range(256):
            for x in range(256):
                weak_ivs.append(f"{(a+3) % 256:02x}{255:02x}{x:02x}")
        
        return weak_ivs[:1000]  # Ограничиваем для демонстрации

    def generate_demo_keys(self) -> List[WEPKey]:
        """Генерация демонстрационных ключей"""
        return [
            WEPKey(secrets.token_hex(5), 64, "Очень слабый"),
            WEPKey(secrets.token_hex(13), 128, "Слабый"),
            WEPKey(secrets.token_hex(16), 152, "Средний"),
            WEPKey(secrets.token_hex(29), 256, "Сильный (но все равно уязвимый)")
        ]

    # Демонстрационные методы атак

    def demo_fms_attack(self):
        """Демонстрация атаки FMS"""
        st.markdown("""
        ### 🔓 Атака FMS (Fluhrer, Mantin, Shamir)
        
        **Принцип работы:**
        - Использует слабые векторы инициализации (IV)
        - Наблюдает за первыми байтами ключевого потока
        - Статистически восстанавливает байты секретного ключа
        
        **Слабые IV:**
        - Формат: `(A+3, 255, X)`
        - Раскрывают информацию о байте `K[A+3]` ключа
        - Требуется ~5,000,000 пакетов для 104-битного ключа
        
        **Процесс:**
        ```
        Для каждого слабого IV:
          1. Анализируем первый байт зашифрованных данных
          2. Вычисляем вероятное значение байта ключа
          3. Статистически подтверждаем правильность
          4. Повторяем для всех байтов ключа
        ```
        
        **Ограничения:**
        - Требует большого количества пакетов
        - Работает только со слабыми IV
        - Медленнее современных методов
        """)

    def demo_ptw_attack(self):
        """Демонстрация атаки PTW"""
        st.markdown("""
        ### ⚡ Атака PTW (Pyshkin, Tews, Weinmann)
        
        **Улучшения по сравнению с FMS:**
        - Использует все IV, а не только слабые
        - Требует всего ~40,000 пакетов
        - Работает за 1-5 минут
        - 99.9% успешность
        
        **Ключевые особенности:**
        - Атака на ключевую схему RC4
        - Использует атаку на основе корреляции
        - Не требует слабых IV
        - Работает с ARP-пакетами
        
        **Процесс:**
        ```
        1. Сбор ARP-пакетов (перехват или инъекция)
        2. Анализ ключевого потока RC4
        3. Статистическое восстановление ключа
        4. Проверка правильности ключа
        ```
        
        **Преимущества:**
        - Высокая скорость
        - Надежность
        - Автоматизация через инструменты (aircrack-ng)
        """)

    def demo_chopchop_attack(self):
        """Демонстрация атаки Chop-Chop"""
        st.markdown("""
        ### 🪓 Атака Chop-Chop
        
        **Принцип работы:**
        - Последовательное угадывание байтов пакета
        - Использует обратимый CRC-32 для проверки
        - Не требует знания ключа
        
        **Процесс:**
        ```
        1. Перехватываем зашифрованный пакет
        2. Угадываем последний байт plaintext
        3. Проверяем правильность через ICV
        4. Повторяем для всех байтов пакета
        5. Получаем расшифрованный пакет
        ```
        
        **Применение:**
        - Расшифровка ARP-пакетов для PTW атаки
        - Получение plaintext для дальнейшего анализа
        - Обход шифрования без знания ключа
        
        **Особенности:**
        - Работает против любого ключа WEP
        - Требует всего ~1000 пакетов
        - Может быть использован для инъекции пакетов
        """)

    def display_encryption_details(self, plaintext: str, packet: WEPPacket):
        """Отображение деталей шифрования"""
        st.markdown("**Детали процесса шифрования:**")
        
        st.text(f"Длина plaintext: {len(plaintext)} байт")
        st.text(f"IV: {packet.iv} (24 бита)")
        st.text(f"Длина зашифрованных данных: {len(packet.data) // 2} байт")
        st.text(f"ICV: {packet.icv} (CRC-32)")
        
        st.markdown("**Криптографические примитивы:**")
        st.text("✓ RC4 потоковый шифр")
        st.text("✓ CRC-32 для проверки целостности")
        st.text("✓ XOR с ключевым потоком")
        st.text("✗ Статический ключ")
        st.text("✗ Короткий IV (24 бита)")

    def simulate_ptw_attack(self, target_key: str, packets_available: int) -> Tuple[bool, str, float]:
        """Симуляция PTW атаки"""
        import time
        
        # Необходимое количество пакетов для успешной атаки
        required_packets = 40000
        
        # Имитация времени атаки (быстрее с большим количеством пакетов)
        base_time = 60  # секунд
        time_taken = base_time * (required_packets / max(packets_available, 1))
        time_taken = max(5, min(300, time_taken))  # Ограничиваем 5-300 секунд
        
        time.sleep(0.1)  # Имитация обработки
        
        # Успех зависит от количества пакетов
        success_probability = min(1.0, packets_available / required_packets)
        success = secrets.SystemRandom().random() < success_probability
        
        if success:
            # "Восстанавливаем" ключ (в демонстрации знаем его)
            # В реальности здесь был бы сложный криптоанализ
            recovered_key = target_key
        else:
            # Частично "восстановленный" ключ для демонстрации
            key_bytes = bytes.fromhex(target_key)
            recovered_bytes = bytearray(key_bytes)
            
            # "Восстанавливаем" только часть байтов
            bytes_to_recover = min(len(recovered_bytes), int(len(recovered_bytes) * success_probability))
            for i in range(bytes_to_recover, len(recovered_bytes)):
                recovered_bytes[i] = secrets.randbelow(256)
            
            recovered_key = recovered_bytes.hex()
        
        return success, recovered_key, round(time_taken, 1)

# Для обратной совместимости
class WEPAttackModule(WEPModule):
    pass