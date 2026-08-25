from data import process_data, signal_generators
from tests.profit_loss import calc_p_l


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

    return formatted_data, profit_stream