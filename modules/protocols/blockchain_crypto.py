from modules.base_module import CryptoModule
import streamlit as st
import secrets
import hashlib
import time
import json
from typing import List, Tuple, Dict, Optional, Any
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import random
import datetime
from enum import Enum

class TransactionStatus(Enum):
    PENDING = "⏳ Ожидание"
    CONFIRMED = "✅ Подтверждена"
    FAILED = "❌ Отклонена"

class ConsensusAlgorithm(Enum):
    POW = "Proof of Work"
    POS = "Proof of Stake"
    DPOS = "Delegated Proof of Stake"
    PBFT = "Practical Byzantine Fault Tolerance"

@dataclass
class Block:
    index: int
    timestamp: float
    transactions: List[Dict]
    previous_hash: str
    hash: str
    nonce: int
    difficulty: int
    miner: str

@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float
    fee: float
    timestamp: float
    signature: str
    status: TransactionStatus
    tx_hash: str

@dataclass
class Blockchain:
    name: str
    blocks: List[Block]
    difficulty: int
    consensus: ConsensusAlgorithm
    total_supply: float

@dataclass
class Wallet:
    address: str
    private_key: str
    public_key: str
    balance: float
    transactions: List[Transaction]

class BlockchainCryptoModule(CryptoModule):
    def __init__(self):
        super().__init__()
        self.name = "Блокчейны и криптовалюты"
        self.description = "Принципы работы блокчейнов, криптовалют и смарт-контрактов"
        self.category = "protocols"
        self.icon = ""
        self.order = 11
        
        # Основные криптовалюты для сравнения
        self.cryptocurrencies = {
            "Bitcoin": {
                "symbol": "BTC",
                "launch_year": 2009,
                "consensus": ConsensusAlgorithm.POW,
                "block_time": 600,
                "max_supply": 21000000,
                "current_price": 45000,
                "market_cap": 880000000000
            },
            "Ethereum": {
                "symbol": "ETH", 
                "launch_year": 2015,
                "consensus": ConsensusAlgorithm.POS,
                "block_time": 12,
                "max_supply": None,
                "current_price": 2500,
                "market_cap": 300000000000
            },
            "Cardano": {
                "symbol": "ADA",
                "launch_year": 2017,
                "consensus": ConsensusAlgorithm.POS,
                "block_time": 20,
                "max_supply": 45000000000,
                "current_price": 0.45,
                "market_cap": 16000000000
            },
            "Solana": {
                "symbol": "SOL",
                "launch_year": 2020,
                "consensus": ConsensusAlgorithm.POS,
                "block_time": 0.4,
                "max_supply": None,
                "current_price": 100,
                "market_cap": 42000000000
            }
        }
        
        # Алгоритмы консенсуса
        self.consensus_algorithms = {
            "POW": {
                "name": "Proof of Work",
                "security": "Очень высокая",
                "energy": "Очень высокое",
                "decentralization": "Высокое",
                "examples": "Bitcoin, Litecoin"
            },
            "POS": {
                "name": "Proof of Stake",
                "security": "Высокая", 
                "energy": "Низкое",
                "decentralization": "Среднее",
                "examples": "Ethereum 2.0, Cardano"
            },
            "DPOS": {
                "name": "Delegated Proof of Stake",
                "security": "Средняя",
                "energy": "Низкое", 
                "decentralization": "Среднее",
                "examples": "EOS, TRON"
            },
            "PBFT": {
                "name": "Practical Byzantine Fault Tolerance",
                "security": "Высокая",
                "energy": "Низкое",
                "decentralization": "Низкое",
                "examples": "Hyperledger, Stellar"
            }
        }

    def render(self):
        st.title("⛓️ Блокчейны и Криптовалюты")
        
        # Теоретическая справка
        with st.expander("📚 Теоретическая справка", expanded=False):
            st.markdown("""
            **Блокчейн** - распределенная децентрализованная база данных, состоящая из цепочки блоков.
            
            ### 🏗️ Архитектура блокчейна:
            
            **Основные компоненты:**
            - **Блоки**: Контейнеры для транзакций с метаданными
            - **Транзакции**: Операции передачи стоимости или данных
            - **Хеши**: Цифровые отпечатки блоков для обеспечения целостности
            - **Майнеры/Валидаторы**: Узлы, создающие новые блоки
            - **Сеть P2P**: Распределенная сеть узлов
            
            **Ключевые свойства:**
            - **Децентрализация**: Отсутствие центрального контролирующего органа
            - **Неизменяемость**: Невозможность изменения подтвержденных данных
            - **Прозрачность**: Открытость данных для всех участников
            - **Безопасность**: Криптографическая защита от изменений
            
            ### 🔗 Структура блока:
            ```
            Block {
                index: номер блока,
                timestamp: время создания,
                transactions: список транзакций,
                previous_hash: хеш предыдущего блока,
                hash: хеш текущего блока,
                nonce: число для Proof of Work,
                difficulty: сложность майнинга
            }
            ```
            
            ### 💰 Криптовалюты:
            
            **Типы криптовалют:**
            - **Coin**: Нативная криптовалюта блокчейна (BTC, ETH)
            - **Token**: Цифровые активы на основе смарт-контрактов
            - **Stablecoin**: Криптовалюты с привязкой к фиату (USDT, USDC)
            - **NFT**: Уникальные невзаимозаменяемые токены
            
            **Технологии:**
            - **Смарт-контракты**: Самоисполняющиеся контракты
            - **DeFi**: Децентрализованные финансы
            - **DAO**: Децентрализованные автономные организации
            - **Web3**: Децентрализованный интернет
            """)

        st.markdown("---")
        
        # Основной интерфейс с вкладками
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🔗 Визуализация блокчейна", "💰 Криптовалюты", "⚡ Алгоритмы консенсуса", 
            "🖋️ Смарт-контракты", "🎮 Демонстрация", "🔮 Будущее"
        ])

        with tab1:
            self.render_blockchain_visualization()
        
        with tab2:
            self.render_cryptocurrencies_section()
            
        with tab3:
            self.render_consensus_algorithms()
            
        with tab4:
            self.render_smart_contracts()
            
        with tab5:
            self.render_demo_section()
            
        with tab6:
            self.render_future_trends()

    def render_blockchain_visualization(self):
        """Интерактивная визуализация блокчейна"""
        st.header("🔗 Визуализация блокчейна")
        
        # Инициализация блокчейна
        if 'blockchain' not in st.session_state:
            st.session_state.blockchain = self.create_genesis_blockchain()
        
        if 'wallets' not in st.session_state:
            st.session_state.wallets = self.create_demo_wallets()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("⛓️ Цепочка блоков")
            
            # Визуализация блокчейна
            blockchain = st.session_state.blockchain
            fig = self.create_blockchain_visualization(blockchain)
            st.plotly_chart(fig, use_container_width=True)
            
            # Детали выбранного блока
            selected_block_idx = st.selectbox(
                "Выберите блок для деталей:",
                range(len(blockchain.blocks)),
                format_func=lambda x: f"Блок #{x}",
                key="block_select"
            )
            
            if selected_block_idx < len(blockchain.blocks):
                block = blockchain.blocks[selected_block_idx]
                self.display_block_details(block)
        
        with col2:
            st.subheader("🔄 Создание транзакций")
            
            # Создание новой транзакции
            sender = st.selectbox(
                "Отправитель:",
                [wallet.address for wallet in st.session_state.wallets],
                key="tx_sender"
            )
            
            receiver = st.selectbox(
                "Получатель:",
                [wallet.address for wallet in st.session_state.wallets],
                key="tx_receiver"
            )
            
            amount = st.number_input(
                "Сумма:",
                min_value=0.1,
                max_value=1000.0,
                value=1.0,
                step=0.1,
                key="tx_amount"
            )
            
            fee = st.number_input(
                "Комиссия:",
                min_value=0.001,
                max_value=1.0,
                value=0.01,
                step=0.001,
                key="tx_fee"
            )
            
            if st.button("💸 Создать транзакцию", key="create_tx"):
                if sender != receiver:
                    transaction = self.create_transaction(sender, receiver, amount, fee)
                    if 'pending_transactions' not in st.session_state:
                        st.session_state.pending_transactions = []
                    st.session_state.pending_transactions.append(transaction)
                    st.success("✅ Транзакция создана!")
                else:
                    st.error("❌ Отправитель и получатель не могут быть одинаковыми")
            
            # Майнинг блока
            st.subheader("⛏️ Майнинг блока")
            
            if st.button("🔄 Добыть блок", key="mine_block"):
                if 'pending_transactions' in st.session_state and st.session_state.pending_transactions:
                    new_block = self.mine_block(
                        st.session_state.blockchain,
                        st.session_state.pending_transactions,
                        "Miner_1"
                    )
                    st.session_state.blockchain.blocks.append(new_block)
                    st.session_state.pending_transactions = []
                    
                    # Обновление балансов
                    self.update_wallet_balances(new_block)
                    
                    st.success(f"✅ Блок #{new_block.index} успешно добыт!")
                    st.balloons()
                else:
                    st.warning("⚠️ Нет транзакций для включения в блок")

    def render_cryptocurrencies_section(self):
        """Сравнение криптовалют"""
        st.header("💰 Криптовалюты")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Сравнение криптовалют")
            
            # Таблица сравнения
            crypto_data = []
            for name, info in self.cryptocurrencies.items():
                crypto_data.append({
                    "Криптовалюта": name,
                    "Символ": info["symbol"],
                    "Год запуска": info["launch_year"],
                    "Консенсус": info["consensus"].value,
                    "Время блока": f"{info['block_time']} сек",
                    "Макс. supply": f"{info['max_supply']:,.0f}" if info['max_supply'] else "∞",
                    "Цена ($)": f"${info['current_price']:,.2f}",
                    "Капитализация": f"${info['market_cap']:,.0f}"
                })
            
            df_crypto = pd.DataFrame(crypto_data)
            st.dataframe(df_crypto, use_container_width=True, hide_index=True)
            
            # Визуализация рыночной капитализации
            st.subheader("📈 Рыночная капитализация")
            
            names = list(self.cryptocurrencies.keys())
            market_caps = [info["market_cap"] for info in self.cryptocurrencies.values()]
            
            fig = px.pie(
                values=market_caps,
                names=names,
                title="Распределение рыночной капитализации"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🔍 Детали криптовалюты")
            
            selected_crypto = st.selectbox(
                "Выберите криптовалюту:",
                list(self.cryptocurrencies.keys()),
                key="crypto_select"
            )
            
            crypto_info = self.cryptocurrencies[selected_crypto]
            
            st.markdown(f"### {selected_crypto} ({crypto_info['symbol']})")
            
            # Основная информация
            info_cols = st.columns(2)
            with info_cols[0]:
                st.metric("Год запуска", crypto_info["launch_year"])
                st.metric("Алгоритм консенсуса", crypto_info["consensus"].value)
            with info_cols[1]:
                st.metric("Время блока", f"{crypto_info['block_time']} сек")
                st.metric("Текущая цена", f"${crypto_info['current_price']:,.2f}")
            
            # Историческая цена (демо данные)
            st.subheader("💹 Историческая цена")
            
            # Генерация демо данных цены
            dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
            base_price = crypto_info["current_price"]
            volatility = 0.02
            
            prices = []
            current_price = base_price
            for _ in range(len(dates)):
                change = random.uniform(-volatility, volatility)
                current_price *= (1 + change)
                prices.append(current_price)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=prices,
                mode='lines',
                name=f'{crypto_info["symbol"]} Price',
                line=dict(color='green' if prices[-1] > prices[0] else 'red')
            ))
            
            fig.update_layout(
                title=f"История цены {selected_crypto}",
                xaxis_title="Дата",
                yaxis_title="Цена (USD)",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)

    def render_consensus_algorithms(self):
        """Алгоритмы консенсуса"""
        st.header("⚡ Алгоритмы консенсуса")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Сравнение алгоритмов")
            
            # Таблица сравнения
            consensus_data = []
            for algo_id, algo_info in self.consensus_algorithms.items():
                consensus_data.append({
                    "Алгоритм": algo_info["name"],
                    "Безопасность": algo_info["security"],
                    "Энергопотребление": algo_info["energy"],
                    "Децентрализация": algo_info["decentralization"],
                    "Примеры": algo_info["examples"]
                })
            
            df_consensus = pd.DataFrame(consensus_data)
            st.dataframe(df_consensus, use_container_width=True, hide_index=True)
            
            # Визуализация характеристик
            st.subheader("📊 Сравнение характеристик")
            
            algorithms = [info["name"] for info in self.consensus_algorithms.values()]
            
            # Оценки по шкале 1-10
            security_scores = [9, 8, 6, 8]  # POW, POS, DPOS, PBFT
            energy_scores = [2, 8, 9, 9]    # обратная шкала для энергопотребления
            decentralization_scores = [9, 7, 6, 4]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=security_scores,
                theta=algorithms,
                fill='toself',
                name='Безопасность'
            ))
            fig.add_trace(go.Scatterpolar(
                r=energy_scores,
                theta=algorithms,
                fill='toself',
                name='Энергоэффективность'
            ))
            fig.add_trace(go.Scatterpolar(
                r=decentralization_scores,
                theta=algorithms,
                fill='toself',
                name='Децентрализация'
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                showlegend=True,
                title="Сравнение алгоритмов консенсуса",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🔍 Детали алгоритмов")
            
            selected_algo = st.selectbox(
                "Выберите алгоритм:",
                list(self.consensus_algorithms.keys()),
                key="algo_select"
            )
            
            algo_info = self.consensus_algorithms[selected_algo]
            
            st.markdown(f"### {algo_info['name']}")
            
            # Принцип работы
            if selected_algo == "POW":
                st.markdown("""
                **Proof of Work (Доказательство работы):**
                - Майнеры решают сложные математические задачи
                - Первый нашедший решение получает право создать блок
                - Требует значительных вычислительных ресурсов
                - Обеспечивает высокую безопасность через стоимость атаки
                """)
            elif selected_algo == "POS":
                st.markdown("""
                **Proof of Stake (Доказательство доли):**
                - Валидаторы блокируют монеты как залог
                - Шанс создания блока пропорционален доле
                - Энергоэффективная альтернатива PoW
                - Защита через экономические стимулы
                """)
            
            # Демонстрация майнинга
            st.subheader("⛏️ Демонстрация майнинга")
            
            if st.button("🎯 Запустить симуляцию майнинга", key="mine_sim"):
                mining_result = self.simulate_mining(selected_algo)
                st.session_state.mining_result = mining_result
            
            if 'mining_result' in st.session_state:
                result = st.session_state.mining_result
                
                st.write(f"**Алгоритм:** {result['algorithm']}")
                st.write(f"**Время:** {result['time']} сек")
                st.write(f"**Энергия:** {result['energy']} кВт·ч")
                st.write(f"**Награда:** {result['reward']} монет")
                
                # Визуализация эффективности
                efficiency = result['energy'] / result['reward'] if result['reward'] > 0 else 0
                st.metric("Эффективность", f"{efficiency:.2f} кВт·ч/монета")

    def render_smart_contracts(self):
        """Смарт-контракты"""
        st.header("🖋️ Смарт-контракты")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💡 Что такое смарт-контракты?")
            
            st.markdown("""
            **Смарт-контракт** - самоисполняющаяся программа, которая автоматически 
            выполняет условия контракта при наступлении определенных событий.
            
            **Преимущества:**
            - ✅ Автоматизация процессов
            - ✅ Прозрачность условий
            - ✅ Отсутствие посредников  
            - ✅ Невозможность цензуры
            - ✅ Снижение затрат
            
            **Применение:**
            - 💰 Децентрализованные финансы (DeFi)
            - 🎨 Цифровое искусство (NFT)
            - 🏢 Управление организациями (DAO)
            - ⛓️ Цепочки поставок
            - 🎮 Игровая индустрия
            """)
            
            # Пример простого смарт-контракта
            st.subheader("📝 Пример смарт-контракта")
            
            contract_code = """
// Простой смарт-контракт для краудфандинга
contract Crowdfunding {
    address public creator;
    uint public goal;
    uint public deadline;
    mapping(address => uint) public contributions;
    uint public totalContributions;
    bool public funded = false;
    
    constructor(uint _goal, uint _duration) {
        creator = msg.sender;
        goal = _goal;
        deadline = block.timestamp + _duration;
    }
    
    function contribute() public payable {
        require(block.timestamp < deadline, "Campaign ended");
        contributions[msg.sender] += msg.value;
        totalContributions += msg.value;
    }
    
    function withdraw() public {
        require(msg.sender == creator, "Only creator can withdraw");
        require(totalContributions >= goal, "Goal not reached");
        require(!funded, "Already funded");
        
        funded = true;
        payable(creator).transfer(address(this).balance);
    }
    
    function refund() public {
        require(block.timestamp >= deadline, "Campaign not ended");
        require(totalContributions < goal, "Goal reached");
        require(contributions[msg.sender] > 0, "No contributions");
        
        uint amount = contributions[msg.sender];
        contributions[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}
            """
            
            st.code(contract_code, language="javascript")
        
        with col2:
            st.subheader("🚀 Платформы смарт-контрактов")
            
            platforms = {
                "Ethereum": {
                    "language": "Solidity",
                    "tps": 15,
                    "gas_fees": "Высокие",
                    "ecosystem": "Очень большой"
                },
                "Cardano": {
                    "language": "Plutus",
                    "tps": 250,
                    "gas_fees": "Низкие", 
                    "ecosystem": "Растущий"
                },
                "Solana": {
                    "language": "Rust",
                    "tps": 65000,
                    "gas_fees": "Очень низкие",
                    "ecosystem": "Быстрорастущий"
                },
                "Polkadot": {
                    "language": "Rust/Ink!",
                    "tps": 1000,
                    "gas_fees": "Переменные",
                    "ecosystem": "Модульный"
                }
            }
            
            for platform, info in platforms.items():
                with st.expander(f"🔧 {platform}"):
                    st.write(f"**Язык:** {info['language']}")
                    st.write(f"**TPS:** {info['tps']}")
                    st.write(f"**Комиссии:** {info['gas_fees']}")
                    st.write(f"**Экосистема:** {info['ecosystem']}")
            
            # Демонстрация выполнения смарт-контракта
            st.subheader("🎮 Демонстрация смарт-контракта")
            
            contract_type = st.selectbox(
                "Тип контракта:",
                ["Краудфандинг", "Голосование", "Аукцион", "Токен"],
                key="contract_type"
            )
            
            if st.button("🔄 Выполнить контракт", key="execute_contract"):
                result = self.execute_smart_contract_demo(contract_type)
                st.session_state.contract_result = result
            
            if 'contract_result' in st.session_state:
                result = st.session_state.contract_result
                st.success(f"✅ Контракт выполнен: {result}")

    def render_demo_section(self):
        """Интерактивная демонстрация"""
        st.header("🎮 Интерактивная демонстрация")
        
        st.info("""
        💡 Эта демонстрация позволяет создать свой мини-блокчейн и поэкспериментировать 
        с транзакциями, майнингом и смарт-контрактами.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔄 Создание блокчейна")
            
            blockchain_name = st.text_input(
                "Название блокчейна:",
                "MyDemoChain",
                key="chain_name"
            )
            
            consensus = st.selectbox(
                "Алгоритм консенсуса:",
                [algo.value for algo in ConsensusAlgorithm],
                key="demo_consensus"
            )
            
            difficulty = st.slider(
                "Сложность майнинга:",
                min_value=1,
                max_value=5,
                value=2,
                key="demo_difficulty"
            )
            
            if st.button("🏗️ Создать блокчейн", key="create_chain"):
                new_blockchain = Blockchain(
                    name=blockchain_name,
                    blocks=[self.create_genesis_block()],
                    difficulty=difficulty,
                    consensus=ConsensusAlgorithm(consensus),
                    total_supply=1000000
                )
                st.session_state.demo_blockchain = new_blockchain
                st.success(f"✅ Блокчейн {blockchain_name} создан!")
        
        with col2:
            st.subheader("📊 Статистика блокчейна")
            
            if 'demo_blockchain' in st.session_state:
                chain = st.session_state.demo_blockchain
                
                st.metric("Название", chain.name)
                st.metric("Количество блоков", len(chain.blocks))
                st.metric("Алгоритм консенсуса", chain.consensus.value)
                st.metric("Сложность", chain.difficulty)
                
                # Визуализация роста блокчейна
                block_heights = list(range(len(chain.blocks)))
                transaction_counts = [len(block.transactions) for block in chain.blocks]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=block_heights,
                    y=transaction_counts,
                    mode='lines+markers',
                    name='Транзакции в блоке'
                ))
                
                fig.update_layout(
                    title="Рост блокчейна",
                    xaxis_title="Номер блока",
                    yaxis_title="Количество транзакций",
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("👆 Создайте блокчейн для просмотра статистики")

    def render_future_trends(self):
        """Будущие тенденции"""
        st.header("🔮 Будущее блокчейнов и криптовалют")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚀 Технологические тренды")
            
            trends = [
                ("Масштабируемость", "Layer 2 решения, шардинг", "📈"),
                ("Взаимодействие", "Мост между блокчейнами", "🔗"),
                ("Конфиденциальность", "Zero-knowledge proofs", "🕵️"),
                ("Управление", "Децентрализованные DAO", "🏛️"),
                ("Устойчивость", "Энергоэффективные алгоритмы", "🌱"),
                ("Регулирование", "Правовые frameworks", "⚖️")
            ]
            
            for trend, description, icon in trends:
                with st.expander(f"{icon} {trend}"):
                    st.write(description)
            
            # Roadmap развития
            st.subheader("🗓️ Дорожная карта развития")
            
            roadmap_data = {
                "Год": ["2024", "2025", "2026", "2027+"],
                "Тренд": [
                    "Массовое внедрение Layer 2",
                    "Зрелость DeFi и NFT", 
                    "Интеграция с традиционными финансами",
                    "Web3 и метавселенная"
                ],
                "Технология": [
                    "ZK-Rollups, Optimistic Rollups",
                    "Cross-chain bridges",
                    "CBDC и институциональное внедрение",
                    "Полная децентрализация интернета"
                ]
            }
            
            df_roadmap = pd.DataFrame(roadmap_data)
            st.dataframe(df_roadmap, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("💼 Применение в различных отраслях")
            
            industries = {
                "🏦 Финансы": "DeFi, платежи, трейдинг",
                "🎨 Искусство": "NFT, цифровое искусство",
                "🎮 Игры": "Play-to-earn, владение активами",
                "🏥 Здравоохранение": "Медицинские записи, исследования",
                "📦 Логистика": "Отслеживание цепочек поставок",
                "⚡ Энергетика": "P2P торговля энергией",
                "🏛️ Правительство": "Голосование, документооборот",
                "🎓 Образование": "Верификация дипломов, микро-кредиты"
            }
            
            for industry, application in industries.items():
                st.write(f"**{industry}** - {application}")
            
            st.subheader("📊 Прогноз развития")
            
            # Прогноз рыночной капитализации
            years = [2023, 2024, 2025, 2026, 2027]
            market_cap = [1.5, 2.5, 4.0, 6.5, 10.0]  # в триллионах USD
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=years,
                y=market_cap,
                mode='lines+markers',
                line=dict(color='green', width=3),
                name='Рыночная капитализация'
            ))
            
            fig.update_layout(
                title="Прогноз рыночной капитализации криптовалют (триллионы USD)",
                xaxis_title="Год",
                yaxis_title="Капитализация (трлн USD)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

    # Вспомогательные методы

    def create_genesis_blockchain(self) -> Blockchain:
        """Создание genesis блокчейна"""
        genesis_block = self.create_genesis_block()
        return Blockchain(
            name="DemoBlockchain",
            blocks=[genesis_block],
            difficulty=2,
            consensus=ConsensusAlgorithm.POW,
            total_supply=1000000
        )

    def create_genesis_block(self) -> Block:
        """Создание genesis блока"""
        return Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0" * 64,
            hash="0" * 64,
            nonce=0,
            difficulty=1,
            miner="Genesis"
        )

    def create_demo_wallets(self) -> List[Wallet]:
        """Создание демо кошельков"""
        wallets = []
        for i in range(3):
            private_key = secrets.token_hex(32)
            public_key = hashlib.sha256(private_key.encode()).hexdigest()
            address = public_key[:40]
            
            wallet = Wallet(
                address=address,
                private_key=private_key,
                public_key=public_key,
                balance=100.0,
                transactions=[]
            )
            wallets.append(wallet)
        
        return wallets

    def create_blockchain_visualization(self, blockchain: Blockchain) -> go.Figure:
        """Создание визуализации блокчейна"""
        fig = go.Figure()
        
        blocks = blockchain.blocks
        y_positions = list(range(len(blocks)))
        
        for i, block in enumerate(blocks):
            # Основной блок
            fig.add_trace(go.Scatter(
                x=[i],
                y=[y_positions[i]],
                mode='markers+text',
                marker=dict(size=50, color='lightblue'),
                text=[f"Блок #{block.index}"],
                textposition="middle center",
                name=f"Block {block.index}"
            ))
            
            # Соединение блоков
            if i > 0:
                fig.add_trace(go.Scatter(
                    x=[i-1, i],
                    y=[y_positions[i-1], y_positions[i]],
                    mode='lines',
                    line=dict(color='gray', width=2),
                    showlegend=False
                ))
        
        fig.update_layout(
            title="Визуализация блокчейна",
            xaxis_title="Позиция",
            yaxis_title="Высота блока",
            showlegend=False,
            height=400
        )
        
        return fig

    def display_block_details(self, block: Block):
        """Отображение деталей блока"""
        st.markdown(f"### Блок #{block.index}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Хеш:** {block.hash[:16]}...")
            st.write(f"**Предыдущий хеш:** {block.previous_hash[:16]}...")
            st.write(f"**Время:** {datetime.datetime.fromtimestamp(block.timestamp)}")
        with col2:
            st.write(f"**Nonce:** {block.nonce}")
            st.write(f"**Сложность:** {block.difficulty}")
            st.write(f"**Майнер:** {block.miner}")
        
        st.write(f"**Транзакции:** {len(block.transactions)}")
        if block.transactions:
            with st.expander("📋 Показать транзакции"):
                for tx in block.transactions:
                    st.write(f"- {tx['sender'][:8]} → {tx['receiver'][:8]}: {tx['amount']}")

    def create_transaction(self, sender: str, receiver: str, amount: float, fee: float) -> Dict:
        """Создание транзакции"""
        tx_data = {
            'sender': sender,
            'receiver': receiver,
            'amount': amount,
            'fee': fee,
            'timestamp': time.time(),
            'signature': secrets.token_hex(32),
            'tx_hash': secrets.token_hex(32)
        }
        return tx_data

    def mine_block(self, blockchain: Blockchain, transactions: List[Dict], miner: str) -> Block:
        """Майнинг нового блока"""
        previous_block = blockchain.blocks[-1]
        new_index = previous_block.index + 1
        
        # Упрощенный Proof of Work
        nonce = 0
        while True:
            block_data = f"{new_index}{previous_block.hash}{''.join([tx['tx_hash'] for tx in transactions])}{nonce}"
            block_hash = hashlib.sha256(block_data.encode()).hexdigest()
            
            # Проверка соответствия сложности
            if block_hash[:blockchain.difficulty] == "0" * blockchain.difficulty:
                break
            nonce += 1
        
        return Block(
            index=new_index,
            timestamp=time.time(),
            transactions=transactions.copy(),
            previous_hash=previous_block.hash,
            hash=block_hash,
            nonce=nonce,
            difficulty=blockchain.difficulty,
            miner=miner
        )

    def update_wallet_balances(self, block: Block):
        """Обновление балансов кошельков после майнинга"""
        for tx in block.transactions:
            sender_wallet = next((w for w in st.session_state.wallets if w.address == tx['sender']), None)
            receiver_wallet = next((w for w in st.session_state.wallets if w.address == tx['receiver']), None)
            
            if sender_wallet:
                sender_wallet.balance -= (tx['amount'] + tx['fee'])
            if receiver_wallet:
                receiver_wallet.balance += tx['amount']

    def simulate_mining(self, algorithm: str) -> Dict:
        """Симуляция процесса майнинга"""
        time.sleep(1)  # Имитация времени майнинга
        
        if algorithm == "POW":
            return {
                'algorithm': 'Proof of Work',
                'time': random.uniform(5, 15),
                'energy': random.uniform(50, 200),
                'reward': 6.25
            }
        elif algorithm == "POS":
            return {
                'algorithm': 'Proof of Stake',
                'time': random.uniform(1, 5),
                'energy': random.uniform(0.1, 1),
                'reward': random.uniform(1, 5)
            }
        else:
            return {
                'algorithm': algorithm,
                'time': random.uniform(2, 8),
                'energy': random.uniform(1, 10),
                'reward': random.uniform(2, 8)
            }

    def execute_smart_contract_demo(self, contract_type: str) -> str:
        """Демонстрация выполнения смарт-контракта"""
        time.sleep(1)  # Имитация выполнения
        
        results = {
            "Краудфандинг": "Сбор средств завершен успешно!",
            "Голосование": "Результаты голосования подсчитаны!",
            "Аукцион": "Товар продан победителю аукциона!",
            "Токен": "Новые токены выпущены успешно!"
        }
        
        return results.get(contract_type, "Контракт выполнен")

# Для обратной совместимости
class BlockchainCryptocurrencyModule(BlockchainCryptoModule):
    pass
