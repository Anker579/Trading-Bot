import pandas as pd

from data.signal_generators import sig_gens


def test_bullish_sma_crossover():
    df = pd.DataFrame({
        "sma_50": [1.00, 1.20],
        "sma_200": [1.10, 1.10]
    })

    generator = sig_gens()

    signal = generator.sma_sig_gen(
        df,
        [50, 200]
    )

    assert signal == 2

def test_bearish_sma_crossover():
    df = pd.DataFrame({
        "sma_50": [1.20, 1.00],
        "sma_200": [1.10, 1.10]
    })

    generator = sig_gens()

    signal = generator.sma_sig_gen(
        df,
        [50, 200]
    )

    assert signal == 1

def test_no_sma_crossover():
    df = pd.DataFrame({
        "sma_50": [1.20, 1.25],
        "sma_200": [1.10, 1.10]
    })

    generator = sig_gens()

    signal = generator.sma_sig_gen(
        df,
        [50, 200]
    )

    assert signal == 0

def test_sma_nan_returns_no_signal():
    df = pd.DataFrame({
        "sma_50": [None, 1.20],
        "sma_200": [None, 1.10]
    })

    generator = sig_gens()

    signal = generator.sma_sig_gen(
        df,
        [50, 200]
    )

    assert signal == 0