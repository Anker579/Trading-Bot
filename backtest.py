from data import process_data, signal_generators
from tests.profit_loss import calc_p_l
import pandas as pd

def calculate_metrics(profit_stream):
    if profit_stream.empty:
        return {
            "total_profit": 0,
            "number_of_trades": 0,
            "win_rate": 0,
            "max_drawdown": 0
        }

    cumulative_profit = profit_stream["profit"].cumsum()

    # Include starting P/L of zero when calculating drawdown
    running_max = cumulative_profit.cummax().clip(lower=0)
    drawdown = cumulative_profit - running_max

    return {
        "total_profit": profit_stream["profit"].sum(),
        "number_of_trades": len(profit_stream),
        "win_rate": (profit_stream["profit"] > 0).mean() * 100,
        "max_drawdown": abs(drawdown.min())
    }

def calc_sltp_p_l(df, sl_tp_ratio, trade_units):
    if "Datetime" in df.columns:
        time_column = "Datetime"
    elif "Date" in df.columns:
        time_column = "Date"
    else:
        raise ValueError("Data must contain a Date or Datetime column")

    trades = {
        "time": [],
        "entry_time": [],
        "direction": [],
        "entry_price": [],
        "exit_price": [],
        "exit_reason": [],
        "profit": []
    }

    i = 0

    while i < len(df) - 1:
        signal = df["signal"].iloc[i]

        # No entry signal
        if signal not in (1, 2):
            i += 1
            continue

        # Signal occurs after candle i closes,
        # so enter at the next candle's open.
        entry_index = i + 1

        entry_price = df["Open"].iloc[entry_index]
        entry_time = df[time_column].iloc[entry_index]

        candle_range = (
            df["High"].iloc[i]
            - df["Low"].iloc[i]
        )

        if candle_range <= 0:
            i += 1
            continue

        if signal == 2:
            direction = "long"

            stop_loss = entry_price - candle_range
            take_profit = (
                entry_price
                + candle_range * sl_tp_ratio
            )

        else:
            direction = "short"

            stop_loss = entry_price + candle_range
            take_profit = (
                entry_price
                - candle_range * sl_tp_ratio
            )

        exit_found = False

        for j in range(entry_index, len(df)):
            high = df["High"].iloc[j]
            low = df["Low"].iloc[j]

            if direction == "long":
                sl_hit = low <= stop_loss
                tp_hit = high >= take_profit

            else:
                sl_hit = high >= stop_loss
                tp_hit = low <= take_profit

            # If both occur in one candle,
            # use the conservative assumption that SL occurred first.
            if sl_hit:
                exit_price = stop_loss
                exit_reason = "stop_loss"
                exit_found = True

            elif tp_hit:
                exit_price = take_profit
                exit_reason = "take_profit"
                exit_found = True

            if exit_found:
                if direction == "long":
                    profit = (
                        exit_price - entry_price
                    ) * trade_units
                else:
                    profit = (
                        entry_price - exit_price
                    ) * trade_units

                trades["time"].append(
                    df[time_column].iloc[j]
                )
                trades["entry_time"].append(entry_time)
                trades["direction"].append(direction)
                trades["entry_price"].append(entry_price)
                trades["exit_price"].append(exit_price)
                trades["exit_reason"].append(exit_reason)
                trades["profit"].append(profit)

                # Continue searching for new signals
                # after this trade has closed.
                i = j
                break

        if not exit_found:
            break

        i += 1

    profit_stream = pd.DataFrame(trades)

    return profit_stream["profit"].sum(), profit_stream

def run_sma_backtest(
    data,
    sma_windows,
    exit_strategy="crossover",
    sl_tp_ratio=None,
    trade_units=None
):
    my_processor = process_data.processor()
    my_sig_gens = signal_generators.sig_gens()

    formatted_data = data.copy()
    formatted_data = formatted_data.reset_index()

    formatted_data = my_processor.add_sma(
        formatted_data,
        sma_windows
    )

    signals = [0]

    for i in range(1, len(formatted_data)):
        df = formatted_data[i-1:i+1]

        signals.append(
            my_sig_gens.sma_sig_gen(
                df,
                sma_windows
            )
        )

    formatted_data["signal"] = signals

    if exit_strategy == "crossover":
        profit, profit_stream = calc_p_l(
            formatted_data
        )
    
    elif exit_strategy == "sltp":
        if sl_tp_ratio is None or trade_units is None:
            raise ValueError(
                "SL/TP backtest requires sl_tp_ratio and trade_units"
            )
    
        profit, profit_stream = calc_sltp_p_l(
            formatted_data,
            sl_tp_ratio,
            trade_units
        )
    
    else:
        raise ValueError(
            f"Unknown exit strategy: {exit_strategy}"
        )

    formatted_data = formatted_data.iloc[max(sma_windows):]

    metrics = calculate_metrics(profit_stream)

    return formatted_data, profit_stream, metrics