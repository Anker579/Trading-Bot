# Algo Trading Bot

A Python-based algorithmic forex trading project using OANDA for (currently practice) execution for historical backtesting, this information is then shown on a free streamlit website [here](https://algo-trading-bot-angus.streamlit.app/).

## Features
- Simple Moving Average crossover trading strategy
- OANDA practice/live API integration
- Automatic stop-loss and take-profit orders
- Existing-position checks before opening trades
- Historical backtesting using Oanda data
- Backtest performance metrics:
  - Total profit
  - Number of trades
  - Win rate
  - Maximum drawdown
- Streamlit interface
- Configurable trading and strategy parameters
- Automated tests with pytest and GitHub Actions

## Project Structure
```text
Trading-Bot/
├── data/               # Market data retrieval and signal generation
├── trader/             # OANDA trade execution and transaction history
├── pages/              # Streamlit pages
├── tests/              # Automated tests
├── backtest.py         # Reusable backtesting logic
├── config.py           # Trading and strategy configuration
├── main.py             # Live trading entry point
└── app.py              # Streamlit application
```

## Installation & Use
### Installation
If you do want to, bogstandard process to clone the repo then install dependencies from requirements.txt.
### Use
Change config.py to tailor the relevant parameters like the currency pair, candle timeframe and window, oanda environment (practice or not), backtesting details etc.

Create an [Oanda account](https://developer.oanda.com/) and save your access token and account ID into a .env file. Add to this also "DRY_RUN=*true/false*", which is another safety measure on top of the oanda environment selection. Note: This application uses the REST-V20 oanda API .