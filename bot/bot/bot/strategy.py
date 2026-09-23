from .indicators import ema, rsi, macd, atr, sma

from .config import (
    ATR_STOP_MULTIPLIER,
    R1_MULTIPLIER,
    R2_MULTIPLIER,
)


def analyze(candles):
    # Ignore the newest candle because it may
    # still be forming.
    c = candles[:-1]

    closes = [x["close"] for x in c]
    highs = [x["high"] for x in c]
    lows = [x["low"] for x in c]
    volumes = [x["volume"] for x in c]

    ema9 = ema(closes, 9)[-1]
    ema21 = ema(closes, 21)[-1]

    rsi_value = rsi(closes, 14)[-1]

    _, _, macd_histogram = macd(closes)

    macd_value = macd_histogram[-1]

    atr_value = atr(
        highs,
        lows,
        closes,
        14,
    )[-1]

    volume_average = sma(
        volumes,
        20,
    )[-1]

    price = closes[-1]

    if volume_average:
        volume_ratio = (
            volumes[-1] / volume_average
        )
    else:
        volume_ratio = 1.0

    long_points = 0
    short_points = 0

    # Trend
    if ema9 > ema21:
        long_points += 1

    if ema9 < ema21:
        short_points += 1

    # Price versus EMA 21
    if price > ema21:
        long_points += 1

    if price < ema21:
        short_points += 1

    # MACD
    if macd_value > 0:
        long_points += 1

    if macd_value < 0:
        short_points += 1

    # RSI
    if 50 <= rsi_value <= 68:
        long_points += 1

    if 32 <= rsi_value <= 50:
        short_points += 1

    # Volume confirmation
    if volume_ratio >= 1.10:

        if long_points > short_points:
            long_points += 1

        elif short_points > long_points:
            short_points += 1

    # Confidence is a rule-agreement score.
    # It is NOT a probability of profit.
    score = max(
        long_points,
        short_points,
    )

    confidence = min(
        95,
        50 + score * 9,
    )

    # Signal decision
    if (
        long_points >= 4
        and long_points > short_points
    ):
        signal = "LONG"

    elif (
        short_points >= 4
        and short_points > long_points
    ):
        signal = "SHORT"

    else:
        signal = "WAIT"

    # Paper-trading levels only
    if signal == "LONG":

        stop = (
            price
            - ATR_STOP_MULTIPLIER * atr_value
        )

        risk = price - stop

        target1 = (
            price
            + R1_MULTIPLIER * risk
        )

        target2 = (
            price
            + R2_MULTIPLIER * risk
        )

    elif signal == "SHORT":

        stop = (
            price
            + ATR_STOP_MULTIPLIER * atr_value
        )

        risk = stop - price

        target1 = (
            price
            - R1_MULTIPLIER * risk
        )

        target2 = (
            price
            - R2_MULTIPLIER * risk
        )

    else:

        stop = None
        target1 = None
        target2 = None

    return {
        "signal": signal,
        "confidence": confidence,
        "price": price,
        "ema9": ema9,
        "ema21": ema21,
        "rsi": rsi_value,
        "macd_hist": macd_value,
        "atr": atr_value,
        "volume_ratio": volume_ratio,
        "long_points": long_points,
        "short_points": short_points,
        "stop": stop,
        "target1": target1,
        "target2": target2,
  }
