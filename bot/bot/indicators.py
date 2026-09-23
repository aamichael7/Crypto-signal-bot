def ema(values, period):
    if len(values) < period:
        return [None] * len(values)

    k = 2 / (period + 1)

    out = [None] * (period - 1)

    current = sum(values[:period]) / period
    out.append(current)

    for value in values[period:]:
        current = value * k + current * (1 - k)
        out.append(current)

    return out


def rsi(values, period=14):
    if len(values) <= period:
        return [None] * len(values)

    gains = []
    losses = []

    for i in range(1, len(values)):
        change = values[i] - values[i - 1]

        gains.append(max(change, 0))
        losses.append(max(-change, 0))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    out = [None] * period

    def calculate_rsi(gain, loss):
        if loss == 0:
            return 100.0

        rs = gain / loss

        return 100 - (100 / (1 + rs))

    out.append(calculate_rsi(avg_gain, avg_loss))

    for i in range(period, len(gains)):
        avg_gain = (
            (avg_gain * (period - 1)) + gains[i]
        ) / period

        avg_loss = (
            (avg_loss * (period - 1)) + losses[i]
        ) / period

        out.append(calculate_rsi(avg_gain, avg_loss))

    return out


def macd(values, fast=12, slow=26, signal=9):
    fast_ema = ema(values, fast)
    slow_ema = ema(values, slow)

    line = [
        None if a is None or b is None else a - b
        for a, b in zip(fast_ema, slow_ema)
    ]

    valid = [
        value for value in line
        if value is not None
    ]

    signal_values = ema(valid, signal)

    signal_line = (
        [None] * (len(line) - len(signal_values))
        + signal_values
    )

    histogram = [
        None if a is None or b is None else a - b
        for a, b in zip(line, signal_line)
    ]

    return line, signal_line, histogram


def atr(highs, lows, closes, period=14):
    if len(closes) < period + 1:
        return [None] * len(closes)

    true_ranges = [None]

    for i in range(1, len(closes)):
        true_range = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )

        true_ranges.append(true_range)

    out = [None] * period

    current = (
        sum(true_ranges[1:period + 1])
        / period
    )

    out.append(current)

    for i in range(period + 1, len(true_ranges)):
        current = (
            (current * (period - 1))
            + true_ranges[i]
        ) / period

        out.append(current)

    return out


def sma(values, period):
    out = [None] * (period - 1)

    for i in range(period - 1, len(values)):
        average = sum(
            values[i - period + 1:i + 1]
        ) / period

        out.append(average)

    return out
