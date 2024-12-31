import pandas as pd
import numpy as np
from typing import Dict, Union
import logging
from .base_strategy import BaseStrategy

logger = logging.getLogger(__name__)

class MovingAverageCrossover(BaseStrategy):
    """
    Moving Average Crossover strategy.
    Generates buy signals when the fast MA crosses above the slow MA,
    and sell signals when the fast MA crosses below the slow MA.
    """
    
    def _validate_parameters(self) -> None:
        """
        Validate strategy parameters.
        Required parameters:
        - fast_ma_period: Period for fast moving average
        - slow_ma_period: Period for slow moving average
        - ma_type: Type of moving average ('simple' or 'exponential')
        """
        required_params = ['fast_ma_period', 'slow_ma_period', 'ma_type']
        if not all(param in self.parameters for param in required_params):
            raise ValueError(f"Missing required parameters. Required: {required_params}")
        
        if self.parameters['fast_ma_period'] >= self.parameters['slow_ma_period']:
            raise ValueError("Fast MA period must be less than slow MA period")
        
        if self.parameters['ma_type'] not in ['simple', 'exponential']:
            raise ValueError("MA type must be either 'simple' or 'exponential'")
        
        if self.parameters['fast_ma_period'] < 1 or self.parameters['slow_ma_period'] < 1:
            raise ValueError("MA periods must be positive integers")
    
    def _calculate_moving_averages(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate moving averages based on parameters.
        
        Args:
            data (pd.DataFrame): Market data with 'close' prices
            
        Returns:
            pd.DataFrame: Data with moving averages added
        """
        df = data.copy()
        
        if self.parameters['ma_type'] == 'simple':
            df['fast_ma'] = df['close'].rolling(
                window=self.parameters['fast_ma_period']
            ).mean()
            df['slow_ma'] = df['close'].rolling(
                window=self.parameters['slow_ma_period']
            ).mean()
        else:  # exponential
            df['fast_ma'] = df['close'].ewm(
                span=self.parameters['fast_ma_period'],
                adjust=False
            ).mean()
            df['slow_ma'] = df['close'].ewm(
                span=self.parameters['slow_ma_period'],
                adjust=False
            ).mean()
        
        return df
    
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on moving average crossovers.
        
        Args:
            data (pd.DataFrame): Market data with OHLCV columns
            
        Returns:
            pd.Series: Trading signals (1: buy, -1: sell, 0: hold)
        """
        try:
            # Calculate moving averages
            df = self._calculate_moving_averages(data)
            
            # Initialize signals
            signals = pd.Series(0, index=df.index)
            
            # Generate crossover signals
            fast_ma = df['fast_ma']
            slow_ma = df['slow_ma']
            
            # Buy signal: fast MA crosses above slow MA
            buy_signals = (fast_ma > slow_ma) & (fast_ma.shift(1) <= slow_ma.shift(1))
            
            # Sell signal: fast MA crosses below slow MA
            sell_signals = (fast_ma < slow_ma) & (fast_ma.shift(1) >= slow_ma.shift(1))
            
            # Set signals
            signals[buy_signals] = 1
            signals[sell_signals] = -1
            
            return signals
            
        except Exception as e:
            logger.error(f"Error generating signals: {e}")
            # Return no signals in case of error
            return pd.Series(0, index=data.index)
    
    def get_strategy_state(self) -> Dict[str, Union[float, str]]:
        """
        Get current strategy state including MA values.
        
        Returns:
            dict: Current strategy state
        """
        return {
            'position': self.position,
            'fast_ma_period': self.parameters['fast_ma_period'],
            'slow_ma_period': self.parameters['slow_ma_period'],
            'ma_type': self.parameters['ma_type']
        }
