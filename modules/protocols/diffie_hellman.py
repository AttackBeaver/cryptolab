from modules.base_module import CryptoModule
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import math

class DiffieHellmanModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Протокол Диффи-Хеллмана"
        self.description = "Обмен ключами по открытому каналу"
        self.category = "protocols"
        self.icon = ""
        self.order = 2
        
        # Предустановленные параметры для демонстрации
        self.demo_parameters = {
            "Маленькие (для демонстрации)": {"p": 23, "g": 5},
            "Средние (учебные)": {"p": 101, "g": 7},
            "Большие (реальные)": {"p": 1009, "g": 11},
            "Свои параметры": "custom"
        }
    
    def render(self):
        st.title("🔄 Протокол Диффи-Хеллмана")
        st.subheader("Безопасный обмен ключами по открытому каналу")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            ### Протокол обмена ключами Диффи-Хеллмана
            
            **Проблема:** Как два участника (Алиса и Боб) могут установить общий секретный ключ 
            по открытому (небезопасному) каналу связи?
            
            **Решение Диффи-Хеллмана (1976):**
            1. **Общие параметры:** Выбираются большое простое число `p` и первообразный корень `g`
            2. **Секретные ключи:** Алиса и Боб выбирают свои секретные числа `a` и `b`
            3. **Открытые ключи:** 
               - Алиса вычисляет `A = gᵃ mod p` и отправляет Бобу
               - Боб вычисляет `B = gᵇ mod p` и отправляет Алисе
            4. **Общий секрет:**
               - Алиса вычисляет `S = Bᵃ mod p`
               - Боб вычисляет `S = Aᵇ mod p`
            
            **Математическая основа:**
            - `Bᵃ mod p = (gᵇ)ᵃ mod p = gᵇᵃ mod p`
            - `Aᵇ mod p = (gᵃ)ᵇ mod p = gᵃᵇ mod p`
            - `gᵇᵃ mod p = gᵃᵇ mod p`
            
            **Безопасность:** Основана на сложности задачи дискретного логарифмирования
            """)
        
        # Выбор режима работы
        mode = st.radio(
            "Режим работы:",
            ["🔒 Безопасный обмен", "👁️ Атака 'Человек посередине'"],
            horizontal=True
        )
        
        if mode == "🔒 Безопасный обмен":
            self.render_secure_exchange()
        else:
            self.render_mitm_attack()
    
    def render_secure_exchange(self):
        """Режим безопасного обмена ключами"""
        st.markdown("### 🔒 Безопасный обмен ключами")
        
        # Выбор параметров
        st.markdown("#### 1. Выбор общих параметров")
        
        param_choice = st.selectbox(
            "Выберите параметры:",
            list(self.demo_parameters.keys()),
            index=0
        )
        
        if self.demo_parameters[param_choice] == "custom":
            col1, col2 = st.columns(2)
            with col1:
                p = st.number_input("Простое число p:", min_value=11, max_value=10000, value=23)
            with col2:
                g = st.number_input("Первообразный корень g:", min_value=2, max_value=p-1, value=5)
        else:
            params = self.demo_parameters[param_choice]
            p, g = params["p"], params["g"]
            st.info(f"**Используются параметры:** p = {p}, g = {g}")
        
        # Проверяем что p простое
        if not self.is_prime(p):
            st.error(f"Число p = {p} должно быть простым!")
            return
        
        # Генерация ключей
        st.markdown("#### 2. Генерация секретных ключей")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**👩 Алиса**")
            a = st.slider("Секретный ключ Алисы (a):", 2, p-2, 6, key="alice_secret")
            A = pow(g, a, p)
            st.success(f"**Открытый ключ Алисы:** A = gᵃ mod p = {g}**{a} mod {p} = {A}")
        
        with col2:
            st.markdown("**👨 Боб**")
            b = st.slider("Секретный ключ Боба (b):", 2, p-2, 15, key="bob_secret")
            B = pow(g, b, p)
            st.success(f"**Открытый ключ Боба:** B = gᵇ mod p = {g}**{b} mod {p} = {B}")
        
        # Обмен ключами
        st.markdown("#### 3. Обмен открытыми ключами")
        
        st.info("📨 Алиса отправляет Бобу: A = " + str(A))
        st.info("📨 Боб отправляет Алисе: B = " + str(B))
        
        # Вычисление общего секрета
        st.markdown("#### 4. Вычисление общего секрета")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**👩 Алиса вычисляет:**")
            S_alice = pow(B, a, p)
            st.latex(f"S = B^a \\mod p = {B}^{{{a}}} \\mod {p} = {S_alice}")
        
        with col2:
            st.markdown("**👨 Боб вычисляет:**")
            S_bob = pow(A, b, p)
            st.latex(f"S = A^b \\mod p = {A}^{{{b}}} \\mod {p} = {S_bob}")
        
        # Проверка
        if S_alice == S_bob:
            st.success(f"🎉 **Общий секретный ключ установлен:** S = {S_alice}")
        else:
            st.error("❌ Ошибка: ключи не совпадают!")
        
        # Визуализация процесса
        st.markdown("---")
        self.plot_exchange_process(g, p, a, b, A, B, S_alice)
    
    def render_mitm_attack(self):
        """Режим атаки 'Человек посередине'"""
        st.markdown("### 👁️ Атака 'Человек посередине' (MITM)")
        st.warning("В этом режиме Ева перехватывает и подменяет сообщения!")
        
        # Выбор параметров
        st.markdown("#### 1. Выбор общих параметров")
        
        param_choice = st.selectbox(
            "Выберите параметры:",
            list(self.demo_parameters.keys()),
            index=0,
            key="mitm_params"
        )
        
        if self.demo_parameters[param_choice] == "custom":
            col1, col2 = st.columns(2)
            with col1:
                p = st.number_input("Простое число p:", min_value=11, max_value=10000, value=23, key="mitm_p")
            with col2:
                g = st.number_input("Первообразный корень g:", min_value=2, max_value=p-1, value=5, key="mitm_g")
        else:
            params = self.demo_parameters[param_choice]
            p, g = params["p"], params["g"]
            st.info(f"**Используются параметры:** p = {p}, g = {g}")
        
        # Проверяем что p простое
        if not self.is_prime(p):
            st.error(f"Число p = {p} должно быть простым!")
            return
        
        # Генерация ключей
        st.markdown("#### 2. Генерация секретных ключей")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**👩 Алиса**")
            a = st.slider("Секретный ключ Алисы (a):", 2, p-2, 6, key="mitm_alice")
            A = pow(g, a, p)
            st.success(f"**Открытый ключ Алисы:** A = {A}")
        
        with col2:
            st.markdown("**👨 Боб**")
            b = st.slider("Секретный ключ Боба (b):", 2, p-2, 15, key="mitm_bob")
            B = pow(g, b, p)
            st.success(f"**Открытый ключ Боба:** B = {B}")
        
        with col3:
            st.markdown("**👤 Ева (атакующий)**")
            e = st.slider("Секретный ключ Евы (e):", 2, p-2, 9, key="eve_secret")
            E = pow(g, e, p)
            st.error(f"**Открытый ключ Евы:** E = {E}")
        
        # Процесс атаки
        st.markdown("#### 3. Процесс атаки MITM")
        
        st.markdown("**📨 Исходный обмен:**")
        st.info(f"Алиса → Боб: A = {A}")
        st.info(f"Боб → Алиса: B = {B}")
        
        st.markdown("**🕵️ Ева перехватывает и подменяет:**")
        st.error(f"Ева перехватывает A и отправляет Бобу: E = {E}")
        st.error(f"Ева перехватывает B и отправляет Алисе: E = {E}")
        
        # Вычисление ключей после атаки
        st.markdown("#### 4. Вычисление ключей после атаки")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**👩 Алиса думает, что общается с Бобом:**")
            S_alice_eve = pow(E, a, p)
            st.latex(f"S_{{A}} = E^a \\mod p = {E}^{{{a}}} \\mod {p} = {S_alice_eve}")
        
        with col2:
            st.markdown("**👨 Боб думает, что общается с Алисой:**")
            S_bob_eve = pow(E, b, p)
            st.latex(f"S_{{B}} = E^b \\mod p = {E}^{{{b}}} \\mod {p} = {S_bob_eve}")
        
        with col3:
            st.markdown("**👤 Ева знает оба ключа:**")
            S_eve_alice = pow(A, e, p)
            S_eve_bob = pow(B, e, p)
            st.latex(f"S_{{E→A}} = A^e \\mod p = {A}^{{{e}}} \\mod {p} = {S_eve_alice}")
            st.latex(f"S_{{E→B}} = B^e \\mod p = {B}^{{{e}}} \\mod {p} = {S_eve_bob}")
        
        # Проверка атаки
        st.markdown("#### 5. Результат атаки")
        
        if S_alice_eve == S_eve_alice and S_bob_eve == S_eve_bob:
            st.error("🎭 **Атака успешна!** Ева может читать и изменять все сообщения!")
            st.error(f"🔑 Ключ Алиса-Ева: {S_alice_eve}")
            st.error(f"🔑 Ключ Боб-Ева: {S_bob_eve}")
        else:
            st.warning("⚠️ Атака не удалась")
        
        # Визуализация атаки
        st.markdown("---")
        self.plot_mitm_attack(g, p, a, b, e, A, B, E, S_alice_eve, S_bob_eve, S_eve_alice, S_eve_bob)
    
    def plot_exchange_process(self, g, p, a, b, A, B, S):
        """Визуализирует процесс обмена ключами"""
        st.markdown("### 📊 Визуализация процесса")
        
        # Создаем график
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # График 1: Вычисление открытых ключей
        steps1 = ['g', 'a', 'A = gᵃ mod p', 'b', 'B = gᵇ mod p']
        values1 = [g, a, A, b, B]
        colors1 = ['blue', 'red', 'red', 'green', 'green']
        
        bars1 = ax1.bar(steps1, values1, color=colors1, alpha=0.7)
        ax1.set_title('Генерация открытых ключей')
        ax1.set_ylabel('Значение')
        ax1.tick_params(axis='x', rotation=45)
        
        for i, v in enumerate(values1):
            ax1.text(i, v, str(v), ha='center', va='bottom')
        
        # График 2: Вычисление общего секрета
        steps2 = ['A → Бобу', 'B → Алисе', 'S = Bᵃ mod p', 'S = Aᵇ mod p', 'Общий ключ']
        values2 = [A, B, S, S, S]
        colors2 = ['red', 'green', 'red', 'green', 'purple']
        
        bars2 = ax2.bar(steps2, values2, color=colors2, alpha=0.7)
        ax2.set_title('Обмен и вычисление общего секрета')
        ax2.set_ylabel('Значение')
        ax2.tick_params(axis='x', rotation=45)
        
        for i, v in enumerate(values2):
            ax2.text(i, v, str(v), ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Тацательная информация
        st.markdown("#### 📋 Детали процесса:")
        process_data = {
            'Этап': [
                'Общие параметры',
                'Секрет Алисы', 
                'Открытый ключ Алисы',
                'Секрет Боба',
                'Открытый ключ Боба',
                'Общий секрет'
            ],
            'Значение': [
                f'p={p}, g={g}',
                f'a={a}',
                f'A={g}**{a} mod {p} = {A}',
                f'b={b}', 
                f'B={g}**{b} mod {p} = {B}',
                f'S={S}'
            ]
        }
        
        st.table(pd.DataFrame(process_data))
    
    def plot_mitm_attack(self, g, p, a, b, e, A, B, E, S_ae, S_be, S_ea, S_eb):
        """Визуализирует атаку MITM"""
        st.markdown("### 📊 Визуализация атаки MITM")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # График 1: Исходные ключи
        participants1 = ['Алиса (a)', 'Боб (b)', 'Ева (e)']
        secrets1 = [a, b, e]
        public1 = [A, B, E]
        
        x = np.arange(len(participants1))
        width = 0.35
        
        bars1_1 = ax1.bar(x - width/2, secrets1, width, label='Секретные ключи', alpha=0.7)
        bars1_2 = ax1.bar(x + width/2, public1, width, label='Открытые ключи', alpha=0.7)
        
        ax1.set_title('Секретные и открытые ключи участников')
        ax1.set_ylabel('Значение')
        ax1.set_xticks(x)
        ax1.set_xticklabels(participants1)
        ax1.legend()
        
        for i, v in enumerate(secrets1):
            ax1.text(i - width/2, v, str(v), ha='center', va='bottom')
        for i, v in enumerate(public1):
            ax1.text(i + width/2, v, str(v), ha='center', va='bottom')
        
        # График 2: Ключи после атаки
        connections = ['Алиса-Ева', 'Боб-Ева']
        alice_keys = [S_ae, 0]
        bob_keys = [0, S_be]
        eve_keys = [S_ea, S_eb]
        
        x2 = np.arange(len(connections))
        
        bars2_1 = ax2.bar(x2 - width, alice_keys, width, label='Ключ Алисы', alpha=0.7)
        bars2_2 = ax2.bar(x2, bob_keys, width, label='Ключ Боба', alpha=0.7)
        bars2_3 = ax2.bar(x2 + width, eve_keys, width, label='Ключ Евы', alpha=0.7)
        
        ax2.set_title('Ключи после атаки MITM')
        ax2.set_ylabel('Значение ключа')
        ax2.set_xticks(x2)
        ax2.set_xticklabels(connections)
        ax2.legend()
        
        for i, (v1, v2, v3) in enumerate(zip(alice_keys, bob_keys, eve_keys)):
            if v1 > 0:
                ax2.text(i - width, v1, str(v1), ha='center', va='bottom')
            if v2 > 0:
                ax2.text(i, v2, str(v2), ha='center', va='bottom')
            if v3 > 0:
                ax2.text(i + width, v3, str(v3), ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Информация об атаке
        st.markdown("#### ⚠️ Результат атаки:")
        attack_data = {
            'Соединение': ['Алиса ↔ Ева', 'Боб ↔ Ева', 'Алиса ↔ Боб'],
            'Ключ Алисы': [S_ae, '-', '-'],
            'Ключ Боба': ['-', S_be, '-'],
            'Ключ Евы': [S_ea, S_eb, '-'],
            'Статус': ['✅ Ева читает', '✅ Ева читает', '❌ Нет связи']
        }
        
        st.table(pd.DataFrame(attack_data))
    
    def is_prime(self, n):
        """Проверяет, является ли число простым"""
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True