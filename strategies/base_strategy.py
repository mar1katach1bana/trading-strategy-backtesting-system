from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime
import pandas as pd

class BaseStrategy(ABC):
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.positions = {}
        self.historical_data = pd.DataFrame()
        self.initialized = False

    @abstractmethod
    def initialize(self):
        """
        Initialize strategy with any required setup
        """
        self.initialized = True

    @abstractmethod
    def update(self, timestamp: datetime, data: pd.Series):
        """
        Update strategy with new market data
        """
        pass

    @abstractmethod
    def generate_signals(self) -> Dict[str, str]:
        """
        Generate trading signals based on current state
        Returns: Dictionary of {symbol: signal} where signal is 'buy', 'sell', or 'hold'
        """
        pass

    def calculate_position_size(self, symbol: str, price: float) -> float:
        """
        Calculate position size based on risk management rules
        """
        # Default implementation uses fixed position size
        return self.config.get('position_size', 100)

    def manage_risk(self, signals: Dict[str, str]) -> Dict[str, str]:
        """
        Apply risk management rules to signals
        """
        # Default implementation passes through signals unchanged
        return signals

    def on_order_filled(self, symbol: str, action: str, 
                       quantity: float, price: float):
        """
        Callback when an order is filled
        """
        if action == 'buy':
            self.positions[symbol] = {
                'quantity': quantity,
                'entry_price': price
            }
        elif action == 'sell':
            if symbol in self.positions:
                del self.positions[symbol]

    def get_position(self, symbol: str) -> Dict[str, Any]:
        """
        Get current position for a symbol
        """
        return self.positions.get(symbol, None)

    def get_all_positions(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all current positions
        """
        return self.positions

    def get_historical_data(self) -> pd.DataFrame:
        """
        Get historical data used by the strategy
        """
        return self.historical_data

    def set_historical_data(self, data: pd.DataFrame):
        """
        Set historical data for the strategy
        """
        self.historical_data = data
