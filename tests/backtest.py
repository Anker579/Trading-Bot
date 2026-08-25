from data import process_data, signal_generators
from tests.profit_loss import calc_p_l

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

def run_sma_backtest(data, sma_windows):
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

    profit, profit_stream = calc_p_l(formatted_data)

    formatted_data = formatted_data.iloc[max(sma_windows):]

    metrics = calculate_metrics(profit_stream)

    return formatted_data, profit_stream, metrics