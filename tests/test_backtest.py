import pandas as pd

from backtest import calculate_metrics


def test_calculate_metrics():
    profit_stream = pd.DataFrame({
        "profit": [100, -50, 25, -100]
    })

    metrics = calculate_metrics(profit_stream)

    assert metrics["total_profit"] == -25
    assert metrics["number_of_trades"] == 4
    assert metrics["win_rate"] == 50
    assert metrics["max_drawdown"] == 125