from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
import time
import logging

class BaseDataAdapter(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._validate_config()
        self._initialize()

    def _validate_config(self):
        """
        Validate adapter configuration
        """
        required_keys = ['api_key', 'rate_limit']
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"Missing required config key: {key}")

    def _initialize(self):
        """
        Initialize adapter with any required setup
        """
        self.last_request_time = 0
        self.rate_limit = self.config['rate_limit']  # Requests per second

    def _enforce_rate_limit(self):
        """
        Enforce rate limiting between requests
        """
        elapsed = time.time() - self.last_request_time
        if elapsed < 1.0 / self.rate_limit:
            time.sleep(1.0 / self.rate_limit - elapsed)
        self.last_request_time = time.time()

    @abstractmethod
    def get_historical_data(self, symbols: List[str], 
                          start_date: datetime, 
                          end_date: datetime) -> pd.DataFrame:
        """
        Get historical data for given symbols and date range
        """
        pass

    @abstractmethod
    def stream_real_time_data(self, symbols: List[str], 
                            callback: callable):
        """
        Stream real-time data for given symbols
        """
        pass

    def _validate_symbols(self, symbols: List[str]):
        """
        Validate list of symbols
        """
        if not symbols:
            raise ValueError("Symbols list cannot be empty")
        if not all(isinstance(symbol, str) for symbol in symbols):
            raise ValueError("All symbols must be strings")

    def _validate_date_range(self, start_date: datetime, end_date: datetime):
        """
        Validate date range
        """
        if start_date >= end_date:
            raise ValueError("Start date must be before end date")
        if start_date > datetime.now():
            raise ValueError("Start date cannot be in the future")

    def _handle_error(self, error: Exception, retries: int = 3):
        """
        Handle errors with retry logic
        """
        self.logger.error(f"Error occurred: {str(error)}")
        if retries > 0:
            self.logger.info(f"Retrying... ({retries} attempts remaining)")
            time.sleep(1)
            return True
        return False
