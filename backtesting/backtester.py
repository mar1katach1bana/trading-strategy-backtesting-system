import pandas as pd
from typing import Dict, Any
from datetime import datetime
from strategies.base_strategy import BaseStrategy

class Backtester:
    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = initial_capital
        self.portfolio = {'cash': initial_capital, 'positions': {}}
        self.trade_history = []
        self.performance_metrics = {}

    def run_backtest(self, strategy: BaseStrategy, data: pd.DataFrame,
                    start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """
        Run backtest for a given strategy and data
        """
        # Filter data for backtest period
        data = data[(data.index >= start_date) & (data.index <= end_date)]
        
        # Initialize strategy
        strategy.initialize()
        
        # Main backtest loop
        for timestamp, row in data.iterrows():
            # Update strategy with new data
            strategy.update(timestamp, row)
            
            # Generate signals
            signals = strategy.generate_signals()
            
            # Execute trades based on signals
            self.execute_trades(signals, row)
            
            # Update portfolio metrics
            self.update_portfolio(row)
        
        # Calculate final performance metrics
        self.calculate_performance_metrics(data)
        
        return {
            'portfolio': self.portfolio,
            'trade_history': self.trade_history,
            'performance_metrics': self.performance_metrics
        }

    def execute_trades(self, signals: Dict[str, str], market_data: pd.Series):
        """
        Execute trades based on generated signals
        """
        for symbol, signal in signals.items():
            if signal == 'buy' and self.portfolio['cash'] > 0:
                # Execute buy order
                self.portfolio['positions'][symbol] = {
                    'quantity': 100,  # Example fixed quantity
                    'entry_price': market_data[symbol]
                }
                self.portfolio['cash'] -= 100 * market_data[symbol]
                self.trade_history.append({
                    'timestamp': market_data.name,
                    'symbol': symbol,
                    'action': 'buy',
                    'price': market_data[symbol],
                    'quantity': 100
                })
            elif signal == 'sell' and symbol in self.portfolio['positions']:
                # Execute sell order
                position = self.portfolio['positions'].pop(symbol)
                self.portfolio['cash'] += position['quantity'] * market_data[symbol]
                self.trade_history.append({
                    'timestamp': market_data.name,
                    'symbol': symbol,
                    'action': 'sell',
                    'price': market_data[symbol],
                    'quantity': position['quantity']
                })

    def update_portfolio(self, market_data: pd.Series):
        """
        Update portfolio value based on current market data
        """
        total_value = self.portfolio['cash']
        for symbol, position in self.portfolio['positions'].items():
            total_value += position['quantity'] * market_data[symbol]
        self.portfolio['value'] = total_value

    def calculate_performance_metrics(self, data: pd.DataFrame):
        """
        Calculate key performance metrics
        """
        # Calculate returns
        self.performance_metrics['total_return'] = (
            (self.portfolio['value'] - self.initial_capital) / self.initial_capital
        )
        
        # Calculate Sharpe ratio (simplified)
        returns = data.pct_change().dropna()
        self.performance_metrics['sharpe_ratio'] = (
            returns.mean() / returns.std()
        )
        
        # Calculate maximum drawdown
        cumulative_max = data.cummax()
        drawdown = (data - cumulative_max) / cumulative_max
        self.performance_metrics['max_drawdown'] = drawdown.min()
