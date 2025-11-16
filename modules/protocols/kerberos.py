from modules.base_module import CryptoModule
import streamlit as st
import secrets
import hashlib
import time
from typing import List, Tuple, Dict, Optional
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

@dataclass
class KerberosTicket:
    client: str
    server: str
    timestamp: float
    lifetime: int
    session_key: str

@dataclass
class KerberosAuthenticator:
    client: str
    timestamp: float

@dataclass
class TGTRequest:
    client: str
    server: str
    timestamp: float

@dataclass
class ServiceTicket:
    client: str
    server: str
    session_key: str
    timestamp: float
    lifetime: int

class KerberosModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Протокол Kerberos"
        self.description = "Сетевой протокол аутентификации с использованием билетов"
        self.category = "protocols"
        self.icon = ""
        self.order = 5
        
        # База данных пользователей и сервисов (для демонстрации)
        self.users_db = {
            "alice": {"password": "password123", "key": hashlib.sha256(b"password123").hexdigest()},
            "bob": {"password": "secret456", "key": hashlib.sha256(b"secret456").hexdigest()},
            "charlie": {"password": "qwerty789", "key": hashlib.sha256(b"qwerty789").hexdigest()}
        }
        
        self.services_db = {
            "fileserver": {"key": secrets.token_hex(32)},
            "printserver": {"key": secrets.token_hex(32)},
            "mailserver": {"key": secrets.token_hex(32)},
            "webserver": {"key": secrets.token_hex(32)}
        }
        
        # Центры распределения ключей (KDC)
        self.as_key = secrets.token_hex(32)  # Authentication Server key
        self.tgs_key = secrets.token_hex(32)  # Ticket Granting Server key
        
        # Активные сессии
        self.active_sessions = {}

    def render(self):
        st.title("🎫 Протокол Kerberos")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **Kerberos** - сетевой протокор аутентификации, разработанный в MIT.
            
            ### 🎯 Основные компоненты:
            
            **Участники протокола:**
            - **Client (C)** - пользователь, запрашивающий доступ
            - **Authentication Server (AS)** - сервер аутентификации  
            - **Ticket Granting Server (TGS)** - сервер выдачи билетов
            - **Service Server (SS)** - целевой сервис
            
            **Ключевые концепции:**
            - **Ticket (TGT)** - билет для получения сервисных билетов
            - **Service Ticket** - билет для доступа к конкретному сервису
            - **Session Key** - временный ключ для сессии
            - **Authenticator** - доказательство идентичности
            
            ### 🔐 Процесс аутентификации (упрощенный):
            
            **1. Аутентификация клиента (AS Exchange):**
            ```
            C → AS: Client, TGS, Timestamp
            AS → C: {Session_Key}K_C, {TGT}K_TGS
            ```
            
            **2. Получение сервисного билета (TGS Exchange):**
            ```
            C → TGS: Service, {Authenticator}Session_Key, {TGT}K_TGS
            TGS → C: {Service_Session_Key}Session_Key, {Service_Ticket}K_Service
            ```
            
            **3. Доступ к сервису (Client/Server Exchange):**
            ```
            C → SS: {Authenticator}Service_Session_Key, {Service_Ticket}K_Service
            SS → C: {Timestamp + 1}Service_Session_Key
            ```
            
            ### 🛡️ Преимущества безопасности:
            - Пароли никогда не передаются по сети
            - Временные билеты с ограниченным сроком действия
            - Взаимная аутентификация клиента и сервера
            - Защита от replay-атак
            """)

        st.markdown("---")
        
        # Основной интерфейс с вкладками
        tab1, tab2, tab3, tab4 = st.tabs(["👤 Аутентификация", "🎫 Получение билетов", "🔐 Доступ к сервису", "📊 Мониторинг"])

        with tab1:
            self.render_authentication_section()
        
        with tab2:
            self.render_ticket_granting_section()
            
        with tab3:
            self.render_service_access_section()
            
        with tab4:
            self.render_monitoring_section()

    def render_authentication_section(self):
        """Секция аутентификации клиента"""
        st.header("👤 Аутентификация клиента (AS Exchange)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔐 Входные данные")
            
            client = st.selectbox(
                "Клиент:",
                list(self.users_db.keys()),
                key="auth_client"
            )
            
            password = st.text_input(
                "Пароль:",
                type="password",
                key="auth_password"
            )
            
            if st.button("🔑 Аутентифицироваться", key="auth_btn", use_container_width=True):
                if self.authenticate_user(client, password):
                    # Генерируем TGT и сессионный ключ
                    session_key = secrets.token_hex(32)
                    tgt = self.generate_tgt(client, session_key)
                    
                    st.session_state.kerberos_session = {
                        "client": client,
                        "session_key": session_key,
                        "tgt": tgt,
                        "authenticated": True,
                        "auth_time": time.time()
                    }
                    
                    st.success("✅ Аутентификация успешна!")
                    st.rerun()
                else:
                    st.error("❌ Неверные учетные данные!")
        
        with col2:
            st.subheader("📄 Результаты аутентификации")
            
            if 'kerberos_session' in st.session_state and st.session_state.kerberos_session["authenticated"]:
                session = st.session_state.kerberos_session
                
                st.success(f"✅ Клиент '{session['client']}' аутентифицирован!")
                
                st.text_area(
                    "Сессионный ключ:",
                    session["session_key"],
                    height=80,
                    key="session_key_display"
                )
                
                # Детали TGT
                with st.expander("🔍 Детали TGT (Ticket Granting Ticket)"):
                    self.display_tgt_details(session["tgt"])
                
                # Визуализация процесса
                st.subheader("🔄 Процесс аутентификации")
                
                steps = ["Запрос аутентификации", "Проверка учетных данных", "Генерация TGT", "Отправка клиенту"]
                statuses = ["✅"] * 4
                
                for step, status in zip(steps, statuses):
                    st.write(f"{status} {step}")
            else:
                st.info("👆 Выполните аутентификацию для отображения результатов")

    def render_ticket_granting_section(self):
        """Секция получения сервисных билетов"""
        st.header("🎫 Получение сервисного билета (TGS Exchange)")
        
        if 'kerberos_session' not in st.session_state or not st.session_state.kerberos_session["authenticated"]:
            st.warning("⚠️ Сначала выполните аутентификацию клиента")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Запрос сервиса")
            
            service = st.selectbox(
                "Целевой сервис:",
                list(self.services_db.keys()),
                key="tgs_service"
            )
            
            lifetime = st.slider(
                "Время жизни билета (часы):",
                min_value=1,
                max_value=24,
                value=8,
                key="tgs_lifetime"
            )
            
            if st.button("🎫 Получить сервисный билет", key="tgs_btn", use_container_width=True):
                session = st.session_state.kerberos_session
                
                # Создаем аутентификатор
                authenticator = self.create_authenticator(session["client"])
                
                # Получаем сервисный билет
                service_session_key, service_ticket = self.grant_service_ticket(
                    session["tgt"], 
                    authenticator, 
                    service,
                    lifetime * 3600  # Конвертируем в секунды
                )
                
                # Сохраняем сервисный билет в сессии
                session["service_session_key"] = service_session_key
                session["service_ticket"] = service_ticket
                session["target_service"] = service
                
                st.success("✅ Сервисный билет получен!")
                st.rerun()
        
        with col2:
            st.subheader("📄 Сервисный билет")
            
            session = st.session_state.kerberos_session
            if 'service_ticket' in session:
                st.success(f"✅ Билет для сервиса '{session['target_service']}' получен!")
                
                st.text_area(
                    "Сессионный ключ сервиса:",
                    session["service_session_key"],
                    height=80,
                    key="service_session_key_display"
                )
                
                # Детали сервисного билета
                with st.expander("🔍 Детали сервисного билета"):
                    self.display_service_ticket_details(session["service_ticket"])
                
                # Визуализация процесса
                st.subheader("🔄 Процесс получения билета")
                
                steps = [
                    "Запрос сервисного билета",
                    "Проверка TGT", 
                    "Верификация аутентификатора",
                    "Генерация сервисного билета",
                    "Отправка клиенту"
                ]
                
                for step in steps:
                    st.write(f"✅ {step}")
            else:
                st.info("👆 Запросите сервисный билет для отображения")

    def render_service_access_section(self):
        """Секция доступа к сервису"""
        st.header("🔐 Доступ к сервису (Client/Server Exchange)")
        
        if 'kerberos_session' not in st.session_state or not st.session_state.kerberos_session["authenticated"]:
            st.warning("⚠️ Сначала выполните аутентификацию клиента")
            return
        
        if 'service_ticket' not in st.session_state.kerberos_session:
            st.warning("⚠️ Сначала получите сервисный билет")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚀 Запрос доступа к сервису")
            
            action = st.selectbox(
                "Действие:",
                ["Чтение файлов", "Печать документа", "Отправка почты", "Доступ к веб-приложению"],
                key="service_action"
            )
            
            if st.button("🔓 Получить доступ к сервису", key="service_btn", use_container_width=True):
                session = st.session_state.kerberos_session
                
                # Создаем аутентификатор для сервиса
                service_authenticator = self.create_authenticator(session["client"])
                
                # Аутентифицируемся на сервисе
                success, response = self.authenticate_to_service(
                    session["service_ticket"],
                    service_authenticator,
                    session["target_service"]
                )
                
                if success:
                    st.session_state.service_access_granted = True
                    st.session_state.service_response = response
                    st.success("✅ Доступ к сервису получен!")
                    st.rerun()
                else:
                    st.error("❌ Ошибка доступа к сервису!")
        
        with col2:
            st.subheader("📄 Результат доступа")
            
            if 'service_access_granted' in st.session_state and st.session_state.service_access_granted:
                session = st.session_state.kerberos_session
                
                st.success(f"✅ Успешный доступ к сервису '{session['target_service']}'!")
                
                # Информация о сессии
                st.markdown("**Информация о сессии:**")
                st.text(f"Клиент: {session['client']}")
                st.text(f"Сервис: {session['target_service']}")
                st.text(f"Время аутентификации: {datetime.fromtimestamp(session['auth_time']).strftime('%H:%M:%S')}")
                
                if 'service_response' in st.session_state:
                    st.text(f"Ответ сервиса: {st.session_state.service_response}")
                
                # Визуализация процесса
                st.subheader("🔄 Процесс доступа к сервису")
                
                steps = [
                    "Отправка сервисного билета",
                    "Отправка аутентификатора", 
                    "Проверка сервисным сервером",
                    "Верификация временной метки",
                    "Подтверждение аутентификации"
                ]
                
                for step in steps:
                    st.write(f"✅ {step}")
            else:
                st.info("👆 Запросите доступ к сервису для отображения")

    def render_monitoring_section(self):
        """Мониторинг и визуализация Kerberos"""
        st.header("📊 Мониторинг системы Kerberos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👥 Учетные записи")
            
            # Таблица пользователей
            users_data = []
            for username, info in self.users_db.items():
                users_data.append({
                    "Пользователь": username,
                    "Статус": "Активен",
                    "Последняя активность": "Сегодня"
                })
            
            df_users = pd.DataFrame(users_data)
            st.dataframe(df_users, use_container_width=True, hide_index=True)
            
            st.subheader("🖥️ Сервисы")
            
            # Таблица сервисов
            services_data = []
            for service, info in self.services_db.items():
                services_data.append({
                    "Сервис": service,
                    "Статус": "Доступен",
                    "Ключ": f"{info['key'][:16]}..."
                })
            
            df_services = pd.DataFrame(services_data)
            st.dataframe(df_services, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("📈 Статистика аутентификации")
            
            # График активности
            times = ["00:00", "06:00", "12:00", "18:00", "23:59"]
            auth_attempts = [5, 15, 45, 35, 20]
            
            fig = go.Figure(data=[go.Scatter(x=times, y=auth_attempts, mode='lines+markers')])
            fig.update_layout(
                title="Активность аутентификации по времени",
                xaxis_title="Время",
                yaxis_title="Количество запросов"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Статистика сервисов
            st.subheader("🎯 Популярность сервисов")
            
            services = list(self.services_db.keys())
            usage = [65, 45, 30, 25]  # Примерные данные
            
            fig2 = go.Figure(data=[go.Bar(x=services, y=usage)])
            fig2.update_layout(
                title="Использование сервисов",
                xaxis_title="Сервис",
                yaxis_title="Количество запросов"
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            # Информация о текущей сессии
            if 'kerberos_session' in st.session_state:
                st.subheader("🔐 Текущая сессия")
                session = st.session_state.kerberos_session
                
                session_info = {
                    "Клиент": session["client"],
                    "Статус": "Аутентифицирован" if session["authenticated"] else "Не аутентифицирован",
                    "TGT": "Получен" if "tgt" in session else "Отсутствует",
                    "Сервисный билет": "Получен" if "service_ticket" in session else "Отсутствует"
                }
                
                for key, value in session_info.items():
                    st.text(f"{key}: {value}")

    # Основные методы Kerberos

    def authenticate_user(self, client: str, password: str) -> bool:
        """Аутентификация пользователя"""
        if client in self.users_db:
            expected_hash = hashlib.sha256(password.encode()).hexdigest()
            return self.users_db[client]["key"] == expected_hash
        return False

    def generate_tgt(self, client: str, session_key: str) -> KerberosTicket:
        """Генерация TGT (Ticket Granting Ticket)"""
        return KerberosTicket(
            client=client,
            server="TGS",
            timestamp=time.time(),
            lifetime=86400,  # 24 часа
            session_key=session_key
        )

    def create_authenticator(self, client: str) -> KerberosAuthenticator:
        """Создание аутентификатора"""
        return KerberosAuthenticator(
            client=client,
            timestamp=time.time()
        )

    def grant_service_ticket(self, tgt: KerberosTicket, authenticator: KerberosAuthenticator, 
                           service: str, lifetime: int) -> Tuple[str, ServiceTicket]:
        """Выдача сервисного билета"""
        # Проверяем аутентификатор
        current_time = time.time()
        if abs(current_time - authenticator.timestamp) > 300:  # 5 минут
            raise ValueError("Аутентификатор устарел")
        
        # Проверяем TGT
        if tgt.timestamp + tgt.lifetime < current_time:
            raise ValueError("TGT истек")
        
        # Генерируем новый сессионный ключ для сервиса
        service_session_key = secrets.token_hex(32)
        
        # Создаем сервисный билет
        service_ticket = ServiceTicket(
            client=tgt.client,
            server=service,
            session_key=service_session_key,
            timestamp=current_time,
            lifetime=lifetime
        )
        
        return service_session_key, service_ticket

    def authenticate_to_service(self, service_ticket: ServiceTicket, 
                              authenticator: KerberosAuthenticator, service: str) -> Tuple[bool, str]:
        """Аутентификация на сервисном сервере"""
        # Проверяем сервисный билет
        current_time = time.time()
        if service_ticket.timestamp + service_ticket.lifetime < current_time:
            return False, "Сервисный билет истек"
        
        # Проверяем аутентификатор
        if abs(current_time - authenticator.timestamp) > 300:  # 5 минут
            return False, "Аутентификатор устарел"
        
        # Проверяем, что аутентификатор от правильного клиента
        if authenticator.client != service_ticket.client:
            return False, "Несоответствие клиента в аутентификаторе"
        
        # Имитируем успешную аутентификацию
        response = f"Аутентификация успешна для {authenticator.client}. Время: {current_time + 1}"
        
        # Сохраняем информацию о сессии
        session_id = f"{service_ticket.client}_{service}_{int(current_time)}"
        self.active_sessions[session_id] = {
            "client": service_ticket.client,
            "service": service,
            "start_time": current_time,
            "session_key": service_ticket.session_key
        }
        
        return True, response

    def display_tgt_details(self, tgt: KerberosTicket):
        """Отображает детали TGT"""
        st.markdown("**Содержимое TGT:**")
        st.text(f"Клиент: {tgt.client}")
        st.text(f"Сервер: {tgt.server}")
        st.text(f"Временная метка: {datetime.fromtimestamp(tgt.timestamp).strftime('%Y-%m-%d %H:%M:%S')}")
        st.text(f"Время жизни: {tgt.lifetime} секунд")
        st.text(f"Сессионный ключ: {tgt.session_key[:32]}...")
        
        st.markdown("**Шифрование:**")
        st.text("TGT зашифрован ключом TGS (Ticket Granting Server)")

    def display_service_ticket_details(self, service_ticket: ServiceTicket):
        """Отображает детали сервисного билета"""
        st.markdown("**Содержимое сервисного билета:**")
        st.text(f"Клиент: {service_ticket.client}")
        st.text(f"Сервер: {service_ticket.server}")
        st.text(f"Временная метка: {datetime.fromtimestamp(service_ticket.timestamp).strftime('%Y-%m-%d %H:%M:%S')}")
        st.text(f"Время жизни: {service_ticket.lifetime} секунд")
        st.text(f"Сессионный ключ: {service_ticket.session_key[:32]}...")
        
        st.markdown("**Шифрование:**")
        st.text("Сервисный билет зашифрован ключом целевого сервиса")

    def visualize_kerberos_flow(self):
        """Визуализация потока Kerberos"""
        st.subheader("🔄 Визуализация полного потока Kerberos")
        
        # Создаем график потока
        entities = ["Клиент", "AS", "TGS", "Сервис"]
        steps = [
            ("1. Запрос аутентификации", 0, 1),
            ("2. TGT + Session Key", 1, 0),
            ("3. Запрос сервисного билета", 0, 2),
            ("4. Сервисный билет", 2, 0),
            ("5. Запрос доступа к сервису", 0, 3),
            ("6. Подтверждение", 3, 0)
        ]
        
        fig = go.Figure()
        
        # Добавляем линии для шагов
        for i, (label, start, end) in enumerate(steps):
            fig.add_trace(go.Scatter(
                x=[start, end],
                y=[i, i],
                mode='lines+markers+text',
                line=dict(width=2),
                marker=dict(size=10),
                text=[label, ""],
                textposition="middle right",
                name=label
            ))
        
        fig.update_layout(
            title="Полный поток аутентификации Kerberos",
            xaxis=dict(
                tickvals=list(range(len(entities))),
                ticktext=entities,
                range=[-0.5, len(entities)-0.5]
            ),
            yaxis=dict(visible=False),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Для обратной совместимости
class KerberosProtocol(KerberosModule):
    pass