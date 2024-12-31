from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union
import pandas as pd
import numpy as np

class BaseStrategy(ABC):
    """Base class for all trading strategies."""
    
    def __init__(self, params: Dict = None):
        """
        Initialize the strategy with optional parameters.
        
        Args:
            params (Dict): Strategy parameters
        """
        self.params = params or {}
        self.position = 0
        self.signals = []
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate trading signals based on the strategy logic.
        
        Args:
            data (pd.DataFrame): Market data with OHLCV columns
            
        Returns:
            pd.DataFrame: Data with added signal column
        """
        pass
    
    @abstractmethod
    def calculate_position_size(self, data: pd.DataFrame, capital: float) -> float:
        """
        Calculate the position size based on available capital and risk parameters.
        
        Args:
            data (pd.DataFrame): Market data
            capital (float): Available capital
            
        Returns:
            float: Position size
        """
        pass
    
    def validate_parameters(self) -> bool:
        """
        Validate strategy parameters.
        
        Returns:
            bool: True if parameters are valid
        """
        return True
    
    def set_parameters(self, params: Dict) -> None:
        """
        Update strategy parameters.
        
        Args:
            params (Dict): New parameters
        """
        self.params.update(params)
        self.validate_parameters()
    
    def get_required_data(self) -> List[str]:
        """
        Get list of required data fields.
        
        Returns:
            List[str]: Required data fields
        """
        return ['open', 'high', 'low', 'close', 'volume']
    
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess input data before signal generation.
        
        Args:
            data (pd.DataFrame): Raw market data
            
        Returns:
            pd.DataFrame: Preprocessed data
        """
        return data
    
    def apply_risk_management(self, signal: float, data: pd.DataFrame) -> float:
        """
        Apply risk management rules to modify signals.
        
        Args:
            signal (float): Original signal
            data (pd.DataFrame): Market data
            
        Returns:
            float: Modified signal
        """
        return signal
    
    def get_strategy_info(self) -> Dict:
        """
        Get strategy information and current parameters.
        
        Returns:
            Dict: Strategy information
        """
        return {
            'name': self.__class__.__name__,
            'parameters': self.params,
            'position': self.position,
            'required_data': self.get_required_data()
        }
    
    def reset(self) -> None:
        """Reset strategy state."""
        self.position = 0
        self.signals = []
