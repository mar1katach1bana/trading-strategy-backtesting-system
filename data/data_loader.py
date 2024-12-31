import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import os
import yfinance as yf
import requests
import json
from data.adapters.base_adapter import BaseDataAdapter

class DataLoader:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cache_dir = self.config.get('cache_dir', './data/cache')
        self.adapters = self._initialize_adapters()
        self._ensure_cache_directory()

    def _initialize_adapters(self) -> Dict[str, BaseDataAdapter]:
        """
        Initialize data adapters based on configuration
        """
        adapters = {}
        # Initialize adapters from config
        for source, adapter_config in self.config.get('data_sources', {}).items():
            adapter_class = self._get_adapter_class(adapter_config['adapter'])
            adapters[source] = adapter_class(adapter_config)
        return adapters

    def _get_adapter_class(self, adapter_name: str) -> type:
        """
        Get adapter class by name
        """
        # Map adapter names to actual classes
        adapter_map = {
            'yfinance': 'YFinanceAdapter',
            'lmax': 'LMAXAdapter'
        }
        # Import and return the appropriate adapter class
        module = __import__(f'data.adapters.{adapter_name.lower()}_adapter', 
                          fromlist=[adapter_map[adapter_name]])
        return getattr(module, adapter_map[adapter_name])

    def _ensure_cache_directory(self):
        """
        Ensure cache directory exists
        """
        os.makedirs(self.cache_dir, exist_ok=True)

    def load_historical_data(self, symbols: list, 
                           start_date: datetime, 
                           end_date: datetime,
                           source: str = 'yfinance') -> pd.DataFrame:
        """
        Load historical data for given symbols and date range
        """
        cache_key = self._generate_cache_key(symbols, start_date, end_date, source)
        cached_data = self._load_from_cache(cache_key)
        
        if cached_data is not None:
            return cached_data

        # Load data from adapter
        adapter = self.adapters.get(source)
        if adapter is None:
            raise ValueError(f"Unknown data source: {source}")

        data = adapter.get_historical_data(symbols, start_date, end_date)
        
        # Cache the data
        self._save_to_cache(cache_key, data)
        
        return data

    def _generate_cache_key(self, symbols: list, 
                          start_date: datetime, 
                          end_date: datetime,
                          source: str) -> str:
        """
        Generate cache key for given parameters
        """
        symbol_str = '_'.join(sorted(symbols))
        date_range = f"{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}"
        return f"{source}_{symbol_str}_{date_range}.parquet"

    def _load_from_cache(self, cache_key: str) -> Optional[pd.DataFrame]:
        """
        Load data from cache if available
        """
        cache_path = os.path.join(self.cache_dir, cache_key)
        if os.path.exists(cache_path):
            try:
                return pd.read_parquet(cache_path)
            except Exception as e:
                print(f"Error loading from cache: {e}")
                return None
        return None

    def _save_to_cache(self, cache_key: str, data: pd.DataFrame):
        """
        Save data to cache
        """
        cache_path = os.path.join(self.cache_dir, cache_key)
        try:
            data.to_parquet(cache_path)
        except Exception as e:
            print(f"Error saving to cache: {e}")

    def stream_real_time_data(self, symbols: list, 
                            callback: callable,
                            source: str = 'yfinance'):
        """
        Stream real-time data for given symbols
        """
        adapter = self.adapters.get(source)
        if adapter is None:
            raise ValueError(f"Unknown data source: {source}")
        
        return adapter.stream_real_time_data(symbols, callback)
