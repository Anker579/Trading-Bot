import pandas as pd

from backtest import calculate_metrics, calc_sltp_p_l


def test_calculate_metrics():
    profit_stream = pd.DataFrame({
        "profit": [100, -50, 25, -100]
    })

    metrics = calculate_metrics(profit_stream)

    assert metrics["total_profit"] == -25
    assert metrics["number_of_trades"] == 4
    assert metrics["win_rate"] == 50
    assert metrics["max_drawdown"] == 125

def test_sltp_long_take_profit():
    df = pd.DataFrame({
        "Datetime": pd.date_range(
            "2026-01-01",
            periods=3,
            freq="15min"
        ),
        "Open": [100, 100, 103],
        "High": [101, 104.5, 105],
        "Low": [99, 99, 102],
        "signal": [2, 0, 0]
    })

    profit, trades = calc_sltp_p_l(
        df,
        sl_tp_ratio=2,
        trade_units=1000
    )

    assert len(trades) == 1
    assert trades["direction"].iloc[0] == "long"
    assert trades["exit_reason"].iloc[0] == "take_profit"
    assert trades["entry_price"].iloc[0] == 100
    assert trades["exit_price"].iloc[0] == 104
    assert profit == 4000

def test_sltp_long_stop_loss():
    df = pd.DataFrame({
        "Datetime": pd.date_range(
            "2026-01-01",
            periods=3,
            freq="15min"
        ),
        "Open": [100, 100, 97],
        "High": [101, 101, 98],
        "Low": [99, 97.5, 96],
        "signal": [2, 0, 0]
    })

    profit, trades = calc_sltp_p_l(
        df,
        sl_tp_ratio=2,
        trade_units=1000
    )

    assert len(trades) == 1
    assert trades["exit_reason"].iloc[0] == "stop_loss"
    assert trades["exit_price"].iloc[0] == 98
    assert profit == -2000

def test_sltp_both_hit_uses_stop_loss():
    df = pd.DataFrame({
        "Datetime": pd.date_range(
            "2026-01-01",
            periods=2,
            freq="15min"
        ),
        "Open": [100, 100],
        "High": [101, 105],
        "Low": [99, 97],
        "signal": [2, 0]
    })

    profit, trades = calc_sltp_p_l(
        df,
        sl_tp_ratio=2,
        trade_units=1000
    )

    assert len(trades) == 1
    assert trades["exit_reason"].iloc[0] == "stop_loss"
    assert profit == -2000

def test_sltp_short_take_profit():
    df = pd.DataFrame({
        "Datetime": pd.date_range(
            "2026-01-01",
            periods=3,
            freq="15min"
        ),
        "Open": [100, 100, 97],
        "High": [101, 101, 98],
        "Low": [99, 95.5, 94],
        "signal": [1, 0, 0]
    })

    profit, trades = calc_sltp_p_l(
        df,
        sl_tp_ratio=2,
        trade_units=1000
    )

    assert len(trades) == 1
    assert trades["direction"].iloc[0] == "short"
    assert trades["exit_reason"].iloc[0] == "take_profit"
    assert trades["exit_price"].iloc[0] == 96
    assert profit == 4000
