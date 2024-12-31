# Trading Strategy and Backtesting System 📈

A Python-based trading strategy development and backtesting platform focused on quantitative approaches and modern portfolio theory.

## 🚀 Features

### Data Management
- Real-time and historical data fetching:
  - LMAX: Institutional-grade data
  - yfinance: Alternative data source
- Efficient data caching and storage mechanisms
- Automated data cleaning and normalization
- Custom data adapters for different data sources
- Preprocessing pipeline for feature engineering

### Strategy Development
- Modular strategy implementation framework
- Event-driven architecture for strategy execution
- Signal generation and filtering
- Focus on quantitative and statistical approaches

### Backtesting Engine
- Integration with Backtrader
- Historical performance simulation
- Key performance metrics:
  - Total Returns
  - Sharpe Ratio
  - Maximum Drawdown
  - Win/Loss Ratio
  - Transaction Costs Analysis
- Multi-asset class support

### Risk Management
- Integration with riskfolio-lib:
  - Portfolio optimization
  - Risk measures
  - Risk contribution
  - Risk allocation
- Stress testing and scenario analysis
- Real-time risk monitoring

### Portfolio Management
- Integration with skfolio:
  - Portfolio optimization
  - Risk-based allocation
  - Factor investing
  - Transaction costs
- Multi-currency support

### Analysis and Visualization
- Interactive performance dashboards
- Trade execution visualizations
- Custom report generation:
  - Equity curves
  - Drawdown charts
  - Trade logs
  - Risk metrics
- Export capabilities (PDF, CSV, Excel)
- Market regime analysis
- Factor analysis and attribution

### Optimization Framework
- Integration with scikit-optimize:
  - Bayesian optimization
  - Gaussian Processes
  - Random forests
- Walk-forward analysis
- Cross-validation techniques
- Performance persistence testing

## 🛠 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/trading-strategy-system.git

# Navigate to the project directory
cd trading-strategy-system

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 📋 Prerequisites

- Python 3.10+
- Required Python packages (see requirements.txt)
- Sufficient storage for historical data

## 🔧 Configuration

Create a `config.yaml` file in the root directory:

```yaml
data_providers:
  lmax:
    environment: paper  # or 'live'
  yfinance:
    cache_duration: 24h

backtesting:
  default_capital: 100000
  commission: 0.001
  slippage: 0.001

risk_management:
  risk_measure: 'MV'  # Mean-Variance
  risk_contrib: true
  rebalance_freq: 'M'  # Monthly

reporting:
  output_dir: ./reports
  save_trades: true
```

## 📁 Project Structure

```
trading-strategy-system/
├── data/
│   ├── adapters/
│   │   ├── lmax_adapter.py
│   │   ├── yfinance_adapter.py
│   │   └── base_adapter.py
│   ├── preprocessing/
│   ├── database/
│   └── api_configs/
├── strategies/
│   ├── quantitative/
│   │   ├── statistical_arbitrage.py
│   │   ├── factor_investing.py
│   │   └── risk_parity.py
│   ├── signals/
│   └── base_strategy.py
├── backtesting/
│   ├── backtester.py
│   ├── performance_metrics.py
│   └── transaction_costs.py
├── risk_management/
│   ├── riskfolio_wrapper.py
│   ├── stress_testing/
│   └── risk_metrics.py
├── portfolio/
│   ├── skfolio_wrapper.py
│   └── portfolio_metrics.py
├── optimization/
│   ├── skopt_wrapper.py
│   └── optimization_metrics.py
└── [rest of original structure remains unchanged]
```

## 🚦 Quick Start

```python
from trading_system import TradingSystem
from strategies.quantitative import StatisticalArbitrage
from riskfolio_lib import RiskFolio
from skfolio import SKFolio

# Initialize the system
ts = TradingSystem(config_path='config.yaml')

# Create and configure a strategy
strategy = StatisticalArbitrage(
    lookback_period=60,
    zscore_threshold=2.0
)

# Run backtesting
results = ts.backtest(
    strategy=strategy,
    symbols=['EURUSD', 'GBPUSD'],
    start_date='2020-01-01',
    end_date='2023-12-31'
)

# Generate and save reports
ts.generate_reports(results, output_dir='./reports')
```

[Rest of original content remains unchanged from License section onwards]