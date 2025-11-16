from modules.base_module import CryptoModule
import streamlit as st
import secrets
import hashlib
import random
from typing import List, Tuple, Dict
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dataclasses import dataclass
from sympy import isprime, nextprime
import math

@dataclass
class Signature:
    r: int
    s: int

@dataclass
class DomainParameters:
    p: int  # модуль эллиптической кривой
    a: int  # коэффициент a
    b: int  # коэффициент b  
    q: int  # порядок подгруппы
    x: int  # x-координата базовой точки
    y: int  # y-координата базовой точки

class GOSTSignatureModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "ГОСТ Р 34.10"
        self.description = "Российские стандарты электронной подписи (1994, 2001, 2012)"
        self.category = "protocols"
        self.icon = ""
        self.order = 4
        
        # Параметры для разных версий ГОСТ
        self.versions = {
            "1994": {
                "name": "ГОСТ Р 34.10-94",
                "description": "На основе дискретного логарифмирования",
                "key_size": 512,
                "hash_size": 256
            },
            "2001": {
                "name": "ГОСТ Р 34.10-2001", 
                "description": "На основе эллиптических кривых",
                "key_size": 512,
                "hash_size": 256
            },
            "2012": {
                "name": "ГОСТ Р 34.10-2012",
                "description": "Современная версия с увеличенной стойкостью",
                "key_size": 512,
                "hash_size": 512
            }
        }
        
        # Стандартные параметры эллиптических кривых для ГОСТ Р 34.10-2001/2012
        self.curve_params = {
            "id-GostR3410-2001-CryptoPro-A-ParamSet": DomainParameters(
                p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD97,
                a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD94,
                b=0x00000000000000000000000000000000000000000000000000000000000000a6,
                q=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF6C611070995AD10045841B09B761B893,
                x=0x0000000000000000000000000000000000000000000000000000000000000001,
                y=0x8D91E471E0989CDA27DF505A453F2B7635294F2DDF23E3B122ACC99C9E9F1E14
            ),
            "id-tc26-gost-3410-12-512-paramSetA": DomainParameters(
                p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC7,
                a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDC4,
                b=0xE8C2505DEDFC86DDC1BD0B2B6667F1DA34B82574761CB0E879BD081CFD0B6265EE3CB090F30D27614CB4574010DA90DD862EF9D4EBEE4761503190785A71C760,
                q=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF27E69532F48D89116FF22B8D4E0560609B4B38ABFAD2B85DCACDB1411F10B275,
                x=0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003,
                y=0x7503CFE87A836AE3A61B8816E25450E6CE5E1C93ACF1ABC1778064FDCBEFA921DF1626BE4FD036E93D75E6A50E3A41E98028FE5FC235F5B889A589CB5215F2A4
            )
        }

    def render(self):
        st.title("📝 ГОСТ Р 34.10 - Электронная подпись")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **ГОСТ Р 34.10** - российский стандарт электронной цифровой подписи.
            
            ### 📜 Версии стандарта:
            
            **ГОСТ Р 34.10-94 (1994)**
            - Основан на проблеме дискретного логарифмирования
            - Длина ключа: 512-1024 бит
            - Использует простые числа специального вида
            
            **ГОСТ Р 34.10-2001 (2001)**
            - Основан на эллиптических кривых (ECC)
            - Повышенная стойкость при меньшей длине ключа
            - Использует отечественные параметры кривых
            
            **ГОСТ Р 34.10-2012 (2012)**
            - Увеличенная длина хеша до 512 бит
            - Усиленные параметры эллиптических кривых
            - Современные требования стойкости
            
            ### 🎯 Математические основы:
            
            **Дискретное логарифмирование (1994):**
            ```
            y = g^x mod p
            Подпись: (r, s), где:
            r = (g^k mod p) mod q
            s = (x*r + k*H) mod q
            ```
            
            **Эллиптические кривые (2001/2012):**
            ```
            y² = x³ + ax + b mod p
            Подпись: (r, s), где:
            r = x-координата(k*G) mod q  
            s = (r*d + k*H) mod q
            ```
            """)

        st.markdown("---")
        
        # Основной интерфейс с вкладками
        tab1, tab2, tab3, tab4 = st.tabs(["🔐 Генерация ключей", "📝 Создание подписи", "✅ Проверка подписи", "📊 Сравнение версий"])

        with tab1:
            self.render_key_generation()
        
        with tab2:
            self.render_signature_creation()
            
        with tab3:
            self.render_signature_verification()
            
        with tab4:
            self.render_comparison_section()

    def render_key_generation(self):
        """Генерация ключей для разных версий ГОСТ"""
        st.header("🔐 Генерация ключевых пар")
        
        # Выбор версии ГОСТ
        version = st.selectbox(
            "Версия ГОСТ Р 34.10:",
            list(self.versions.keys()),
            format_func=lambda x: f"{self.versions[x]['name']} - {self.versions[x]['description']}",
            key="key_gen_version"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Параметры")
            
            if version == "1994":
                self.render_gost94_parameters()
            else:
                self.render_ecc_parameters(version)
            
            # Генерация ключей
            if st.button("🎲 Сгенерировать ключевую пару", key="gen_key_pair_btn"):
                if version == "1994":
                    private_key, public_key = self.generate_gost94_keys()
                else:
                    private_key, public_key = self.generate_ecc_keys(version)
                
                st.session_state.private_key = private_key
                st.session_state.public_key = public_key
                st.session_state.key_version = version
                st.rerun()
        
        with col2:
            st.subheader("🔑 Результаты")
            
            if 'private_key' in st.session_state and st.session_state.key_version == version:
                st.success("✅ Ключевая пара сгенерирована!")
                
                st.text_area(
                    "Закрытый ключ:",
                    st.session_state.private_key,
                    height=100,
                    key="private_key_display"
                )
                
                st.text_area(
                    "Открытый ключ:",
                    st.session_state.public_key,
                    height=150,
                    key="public_key_display"
                )
                
                # Детали ключей
                with st.expander("🔍 Детали ключей"):
                    if version == "1994":
                        self.display_gost94_key_details(st.session_state.private_key, st.session_state.public_key)
                    else:
                        self.display_ecc_key_details(st.session_state.private_key, st.session_state.public_key, version)
            else:
                st.info("👆 Сгенерируйте ключевую пару для отображения")

    def render_gost94_parameters(self):
        """Параметры для ГОСТ Р 34.10-94"""
        st.markdown("**Параметры дискретного логарифмирования:**")
        
        if 'gost94_p' not in st.session_state:
            # Генерируем простые числа для демонстрации
            st.session_state.gost94_p = self.generate_gost94_prime()
            st.session_state.gost94_q = self.generate_gost94_subprime(st.session_state.gost94_p)
            st.session_state.gost94_g = self.find_generator(st.session_state.gost94_p, st.session_state.gost94_q)
        
        st.text_input("Модуль p:", hex(st.session_state.gost94_p), disabled=True)
        st.text_input("Порядок подгруппы q:", hex(st.session_state.gost94_q), disabled=True)
        st.text_input("Генератор g:", hex(st.session_state.gost94_g), disabled=True)
        
        st.markdown("""
        **Параметры ГОСТ Р 34.10-94:**
        - Длина p: 512-1024 бит
        - Длина q: 256 бит  
        - p = 2 * q + 1 (безопасное простое)
        - g - генератор подгруппы порядка q
        """)

    def render_ecc_parameters(self, version: str):
        """Параметры для ГОСТ Р 34.10-2001/2012"""
        st.markdown("**Параметры эллиптической кривой:**")
        
        curve_name = st.selectbox(
            "Набор параметров:",
            list(self.curve_params.keys()),
            key=f"curve_select_{version}"
        )
        
        params = self.curve_params[curve_name]
        
        st.text_input("Модуль p:", hex(params.p), disabled=True)
        st.text_input("Коэффициент a:", hex(params.a), disabled=True)
        st.text_input("Коэффициент b:", hex(params.b), disabled=True)
        st.text_input("Порядок q:", hex(params.q), disabled=True)
        st.text_input("Базовая точка Gx:", hex(params.x), disabled=True)
        st.text_input("Базовая точка Gy:", hex(params.y), disabled=True)
        
        st.session_state.current_curve = curve_name
        st.session_state.current_params = params

    def render_signature_creation(self):
        """Создание электронной подписи"""
        st.header("📝 Создание электронной подписи")
        
        version = st.selectbox(
            "Версия ГОСТ Р 34.10:",
            list(self.versions.keys()),
            key="sign_version"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Входные данные")
            
            message = st.text_area(
                "Сообщение для подписи:",
                "Важное сообщение для подписи по ГОСТ Р 34.10",
                height=100,
                key="sign_message"
            )
            
            private_key = st.text_input(
                "Закрытый ключ:",
                st.session_state.get('private_key', ''),
                key="sign_private_key"
            )
            
            if st.button("📝 Создать подпись", key="create_sign_btn"):
                if message and private_key:
                    try:
                        if version == "1994":
                            signature = self.gost94_sign(message, private_key)
                        else:
                            signature = self.ecc_sign(message, private_key, version)
                        
                        st.session_state.signature = signature
                        st.session_state.signed_message = message
                        st.session_state.sign_version = version
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Ошибка создания подписи: {e}")
                else:
                    st.error("⚠️ Введите сообщение и закрытый ключ")
        
        with col2:
            st.subheader("Результат подписи")
            
            if 'signature' in st.session_state and st.session_state.sign_version == version:
                st.success("✅ Подпись создана!")
                
                signature = st.session_state.signature
                
                st.text_input("Компонент r:", hex(signature.r), key="sign_r_display")
                st.text_input("Компонент s:", hex(signature.s), key="sign_s_display")
                
                st.text_area(
                    "Подпись (hex):",
                    f"{signature.r:064X}{signature.s:064X}",
                    height=100,
                    key="full_signature_display"
                )
                
                # Детали процесса подписи
                with st.expander("🔍 Детали процесса подписи"):
                    if version == "1994":
                        self.display_gost94_signature_details(st.session_state.signed_message, signature)
                    else:
                        self.display_ecc_signature_details(st.session_state.signed_message, signature, version)
            else:
                st.info("👆 Создайте подпись для отображения")

    def render_signature_verification(self):
        """Проверка электронной подписи"""
        st.header("✅ Проверка электронной подписи")
        
        version = st.selectbox(
            "Версия ГОСТ Р 34.10:",
            list(self.versions.keys()),
            key="verify_version"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Данные для проверки")
            
            message = st.text_area(
                "Сообщение:",
                st.session_state.get('signed_message', ''),
                height=100,
                key="verify_message"
            )
            
            public_key = st.text_input(
                "Открытый ключ:",
                st.session_state.get('public_key', ''),
                key="verify_public_key"
            )
            
            signature_r = st.text_input("Компонент r (hex):", key="verify_r")
            signature_s = st.text_input("Компонент s (hex):", key="verify_s")
            
            if st.button("✅ Проверить подпись", key="verify_sign_btn"):
                if message and public_key and signature_r and signature_s:
                    try:
                        signature = Signature(
                            r=int(signature_r, 16),
                            s=int(signature_s, 16)
                        )
                        
                        if version == "1994":
                            is_valid = self.gost94_verify(message, signature, public_key)
                        else:
                            is_valid = self.ecc_verify(message, signature, public_key, version)
                        
                        st.session_state.verification_result = is_valid
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Ошибка проверки подписи: {e}")
                else:
                    st.error("⚠️ Заполните все поля")
        
        with col2:
            st.subheader("Результат проверки")
            
            if 'verification_result' in st.session_state:
                if st.session_state.verification_result:
                    st.success("🎉 Подпись ВАЛИДНА!")
                    st.balloons()
                else:
                    st.error("❌ Подпись НЕВЕРНА!")
                
                # Детали проверки
                with st.expander("🔍 Детали проверки"):
                    st.markdown("""
                    **Процесс проверки подписи:**
                    
                    1. Вычисление хеша сообщения
                    2. Проверка диапазона значений r и s
                    3. Вычисление промежуточных значений
                    4. Сравнение с компонентами подписи
                    
                    **Критерии валидности:**
                    - r и s в диапазоне [1, q-1]
                    - Вычисленные значения совпадают
                    - Открытый ключ соответствует подписи
                    """)
            else:
                st.info("👆 Проверьте подпись для отображения результата")

    def render_comparison_section(self):
        """Сравнение версий ГОСТ"""
        st.header("📊 Сравнение версий ГОСТ Р 34.10")
        
        # Сравнительная таблица
        comparison_data = {
            'Параметр': [
                'Год принятия',
                'Математическая основа',
                'Длина ключа',
                'Длина хеша', 
                'Длина подписи',
                'Стойкость',
                'Производительность',
                'Применение'
            ],
            'ГОСТ 34.10-94': [
                '1994',
                'Дискретное логарифмирование',
                '512-1024 бит',
                '256 бит',
                '1024 бит',
                'Средняя',
                'Низкая',
                'Устаревшие системы'
            ],
            'ГОСТ 34.10-2001': [
                '2001',
                'Эллиптические кривые',
                '512 бит',
                '256 бит', 
                '1024 бит',
                'Высокая',
                'Средняя',
                'Активные системы'
            ],
            'ГОСТ 34.10-2012': [
                '2012',
                'Эллиптические кривые',
                '512 бит',
                '512 бит',
                '1024 бит',
                'Очень высокая',
                'Высокая',
                'Современные системы'
            ]
        }

        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Графическое сравнение
        st.subheader("📈 Сравнительные характеристики")
        
        metrics_data = {
            'Версия': ['ГОСТ 34.10-94', 'ГОСТ 34.10-2001', 'ГОСТ 34.10-2012'],
            'Стойкость': [6, 8, 10],
            'Скорость': [4, 7, 8],
            'Безопасность': [5, 8, 9],
            'Стандартизация': [7, 9, 10]
        }
        
        df_metrics = pd.DataFrame(metrics_data)
        
        fig = go.Figure()
        
        for version in df_metrics['Версия']:
            version_data = df_metrics[df_metrics['Версия'] == version]
            fig.add_trace(go.Scatterpolar(
                r=[version_data['Стойкость'].iloc[0], version_data['Скорость'].iloc[0], 
                   version_data['Безопасность'].iloc[0], version_data['Стандартизация'].iloc[0]],
                theta=['Стойкость', 'Скорость', 'Безопасность', 'Стандартизация'],
                fill='toself',
                name=version
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True,
            title="Сравнение характеристик версий ГОСТ Р 34.10"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Эволюция стандарта
        st.subheader("🔄 Эволюция стандарта")
        
        evolution_data = {
            'Год': [1994, 2001, 2012],
            'Стойкость (бит)': [80, 128, 256],
            'Длина ключа (бит)': [512, 512, 512],
            'Производительность': [1, 3, 5]
        }
        
        df_evolution = pd.DataFrame(evolution_data)
        
        fig2 = go.Figure()
        
        fig2.add_trace(go.Scatter(
            x=df_evolution['Год'], 
            y=df_evolution['Стойкость (бит)'],
            mode='lines+markers',
            name='Стойкость (бит)',
            line=dict(color='red', width=3)
        ))
        
        fig2.add_trace(go.Scatter(
            x=df_evolution['Год'],
            y=df_evolution['Производительность'] * 50,
            mode='lines+markers', 
            name='Производительность (отн. ед.)',
            line=dict(color='blue', width=3)
        ))
        
        fig2.update_layout(
            title="Эволюция стойкости и производительности ГОСТ Р 34.10",
            xaxis_title="Год",
            yaxis_title="Значение"
        )
        
        st.plotly_chart(fig2, use_container_width=True)

    # Реализация ГОСТ Р 34.10-94

    def generate_gost94_prime(self, bits=512) -> int:
        """Генерирует простое число для ГОСТ Р 34.10-94"""
        # Для демонстрации используем предварительно вычисленное простое число
        demo_primes = {
            512: 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF43,
            1024: 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF4F
        }
        return demo_primes.get(bits, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD97)

    def generate_gost94_subprime(self, p: int) -> int:
        """Генерирует порядок подгруппы q = (p-1)/2"""
        return (p - 1) // 2

    def find_generator(self, p: int, q: int) -> int:
        """Находит генератор подгруппы порядка q"""
        # Для демонстрации используем небольшой генератор
        return 2

    def generate_gost94_keys(self) -> Tuple[str, str]:
        """Генерирует ключевую пару для ГОСТ Р 34.10-94"""
        p = st.session_state.gost94_p
        q = st.session_state.gost94_q
        g = st.session_state.gost94_g
        
        # Закрытый ключ - случайное число от 1 до q-1
        private_key = random.randint(1, q-1)
        
        # Открытый ключ - y = g^x mod p
        public_key = pow(g, private_key, p)
        
        return hex(private_key), hex(public_key)

    def gost94_sign(self, message: str, private_key_hex: str) -> Signature:
        """Создает подпись по ГОСТ Р 34.10-94"""
        p = st.session_state.gost94_p
        q = st.session_state.gost94_q
        g = st.session_state.gost94_g
        
        private_key = int(private_key_hex, 16)
        
        # Вычисляем хеш сообщения (упрощенно)
        message_hash = self.gost_hash(message, 256)
        h = int(message_hash, 16) % q
        if h == 0:
            h = 1
        
        while True:
            # Случайное k от 1 до q-1
            k = random.randint(1, q-1)
            
            # r = (g^k mod p) mod q
            r = pow(g, k, p) % q
            if r == 0:
                continue
            
            # s = (x*r + k*h) mod q
            s = (private_key * r + k * h) % q
            if s != 0:
                break
        
        return Signature(r, s)

    def gost94_verify(self, message: str, signature: Signature, public_key_hex: str) -> bool:
        """Проверяет подпись по ГОСТ Р 34.10-94"""
        p = st.session_state.gost94_p
        q = st.session_state.gost94_q
        g = st.session_state.gost94_g
        
        public_key = int(public_key_hex, 16)
        
        # Проверка диапазона
        if not (0 < signature.r < q and 0 < signature.s < q):
            return False
        
        # Вычисляем хеш сообщения
        message_hash = self.gost_hash(message, 256)
        h = int(message_hash, 16) % q
        if h == 0:
            h = 1
        
        # v = h^(-1) mod q
        v = pow(h, -1, q)
        
        # z1 = s*v mod q
        z1 = (signature.s * v) % q
        
        # z2 = (-r)*v mod q
        z2 = (-signature.r * v) % q
        
        # u = (g^z1 * y^z2 mod p) mod q
        u = (pow(g, z1, p) * pow(public_key, z2, p)) % p % q
        
        return u == signature.r

    # Реализация ГОСТ Р 34.10-2001/2012 (ECC)

    def generate_ecc_keys(self, version: str) -> Tuple[str, str]:
        """Генерирует ключевую пару для ECC-версий ГОСТ"""
        params = st.session_state.current_params
        
        # Закрытый ключ - случайное число от 1 до q-1
        private_key = random.randint(1, params.q - 1)
        
        # Открытый ключ - точка d*G на эллиптической кривой
        public_key_point = self.ec_point_multiply(private_key, params)
        public_key_hex = f"{public_key_point[0]:064X}{public_key_point[1]:064X}"
        
        return hex(private_key), public_key_hex

    def ecc_sign(self, message: str, private_key_hex: str, version: str) -> Signature:
        """Создает подпись по ECC-версии ГОСТ"""
        params = st.session_state.current_params
        private_key = int(private_key_hex, 16)
        
        # Вычисляем хеш сообщения
        hash_size = 512 if version == "2012" else 256
        message_hash = self.gost_hash(message, hash_size)
        h = int(message_hash, 16) % params.q
        if h == 0:
            h = 1
        
        while True:
            # Случайное k от 1 до q-1
            k = random.randint(1, params.q - 1)
            
            # Точка k*G
            kG = self.ec_point_multiply(k, params)
            
            # r = x-координата(k*G) mod q
            r = kG[0] % params.q
            if r == 0:
                continue
            
            # s = (r*d + k*h) mod q
            s = (r * private_key + k * h) % params.q
            if s != 0:
                break
        
        return Signature(r, s)

    def ecc_verify(self, message: str, signature: Signature, public_key_hex: str, version: str) -> bool:
        """Проверяет подпись по ECC-версии ГОСТ"""
        params = st.session_state.current_params
        
        # Извлекаем открытый ключ (точку на кривой)
        public_key_x = int(public_key_hex[:64], 16)
        public_key_y = int(public_key_hex[64:], 16)
        public_key = (public_key_x, public_key_y)
        
        # Проверка диапазона
        if not (0 < signature.r < params.q and 0 < signature.s < params.q):
            return False
        
        # Вычисляем хеш сообщения
        hash_size = 512 if version == "2012" else 256
        message_hash = self.gost_hash(message, hash_size)
        h = int(message_hash, 16) % params.q
        if h == 0:
            h = 1
        
        # v = h^(-1) mod q
        v = pow(h, -1, params.q)
        
        # z1 = s*v mod q
        z1 = (signature.s * v) % params.q
        
        # z2 = (-r)*v mod q
        z2 = (-signature.r * v) % params.q
        
        # Точка C = z1*G + z2*Q
        z1G = self.ec_point_multiply(z1, params)
        z2Q = self.ec_point_multiply(z2, params, public_key)
        C = self.ec_point_add(z1G, z2Q, params)
        
        # R = x-координата(C) mod q
        R = C[0] % params.q
        
        return R == signature.r

    def ec_point_multiply(self, k: int, params: DomainParameters, point=None):
        """Умножение точки на скаляр (упрощенная реализация)"""
        if point is None:
            # Умножение базовой точки
            x, y = params.x, params.y
        else:
            x, y = point
        
        # Для демонстрации используем упрощенное вычисление
        # В реальной реализации нужно использовать алгоритмы эллиптических кривых
        result_x = (k * x) % params.p
        result_y = (k * y) % params.p
        
        return (result_x, result_y)

    def ec_point_add(self, P1, P2, params: DomainParameters):
        """Сложение двух точек на эллиптической кривой (упрощенная реализация)"""
        x1, y1 = P1
        x2, y2 = P2
        
        # Для демонстрации используем упрощенное вычисление
        # В реальной реализации нужно использовать формулы сложения точек
        result_x = (x1 + x2) % params.p
        result_y = (y1 + y2) % params.p
        
        return (result_x, result_y)

    def gost_hash(self, message: str, bits=256) -> str:
        """Вычисляет хеш по ГОСТ Р 34.11 (упрощенная реализация)"""
        message_bytes = message.encode('utf-8')
        
        if bits == 512:
            # ГОСТ Р 34.11-2012 (Стрибог)
            hash_obj = hashlib.sha512()
        else:
            # ГОСТ Р 34.11-94
            hash_obj = hashlib.sha256()
        
        hash_obj.update(message_bytes)
        return hash_obj.hexdigest()

    # Методы отображения деталей

    def display_gost94_key_details(self, private_key: str, public_key: str):
        """Отображает детали ключей ГОСТ Р 34.10-94"""
        st.markdown("**Детали ключевой пары:**")
        st.text(f"Закрытый ключ (x): {private_key}")
        st.text(f"Открытый ключ (y = g^x mod p): {public_key}")
        
        p = st.session_state.gost94_p
        q = st.session_state.gost94_q
        g = st.session_state.gost94_g
        
        st.markdown("**Параметры системы:**")
        st.text(f"Модуль p: {hex(p)}")
        st.text(f"Порядок подгруппы q: {hex(q)}")
        st.text(f"Генератор g: {hex(g)}")

    def display_ecc_key_details(self, private_key: str, public_key: str, version: str):
        """Отображает детали ключей ECC-версий ГОСТ"""
        st.markdown("**Детали ключевой пары:**")
        st.text(f"Закрытый ключ (d): {private_key}")
        st.text(f"Открытый ключ (Q = d*G): {public_key}")
        
        params = st.session_state.current_params
        
        st.markdown("**Параметры эллиптической кривой:**")
        st.text(f"Модуль p: {hex(params.p)}")
        st.text(f"Коэффициент a: {hex(params.a)}")
        st.text(f"Коэффициент b: {hex(params.b)}")
        st.text(f"Порядок q: {hex(params.q)}")
        st.text(f"Базовая точка G: ({hex(params.x)}, {hex(params.y)})")

    def display_gost94_signature_details(self, message: str, signature: Signature):
        """Отображает детали подписи ГОСТ Р 34.10-94"""
        st.markdown("**Процесс создания подписи:**")
        
        message_hash = self.gost_hash(message, 256)
        h = int(message_hash, 16) % st.session_state.gost94_q
        
        st.text(f"Хеш сообщения: {message_hash}")
        st.text(f"Нормализованный хеш: {hex(h)}")
        st.text(f"Компонент r: {hex(signature.r)}")
        st.text(f"Компонент s: {hex(signature.s)}")
        
        st.markdown("""
        **Формулы:**
        - r = (g^k mod p) mod q
        - s = (x*r + k*h) mod q
        """)

    def display_ecc_signature_details(self, message: str, signature: Signature, version: str):
        """Отображает детали подписи ECC-версий ГОСТ"""
        st.markdown("**Процесс создания подписи:**")
        
        hash_size = 512 if version == "2012" else 256
        message_hash = self.gost_hash(message, hash_size)
        h = int(message_hash, 16) % st.session_state.current_params.q
        
        st.text(f"Хеш сообщения: {message_hash}")
        st.text(f"Нормализованный хеш: {hex(h)}")
        st.text(f"Компонент r: {hex(signature.r)}")
        st.text(f"Компонент s: {hex(signature.s)}")
        
        st.markdown("""
        **Формулы:**
        - r = x-координата(k*G) mod q
        - s = (r*d + k*h) mod q
        """)

# Для обратной совместимости
class GOSTSignature(GOSTSignatureModule):
    pass