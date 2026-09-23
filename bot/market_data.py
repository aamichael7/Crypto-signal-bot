import requests

BASE_URL = "https://api.binance.com/api/v3/klines"


def get_klines(symbol, interval="15m", limit=120):
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit,
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    rows = response.json()

    if not rows:
        raise ValueError(f"No candle data returned for {symbol}")

    candles = []

    for r in rows:
        candles.append({
            "open_time": int(r[0]),
            "open": float(r[1]),
            "high": float(r[2]),
            "low": float(r[3]),
            "close": float(r[4]),
            "volume": float(r[5]),
            "close_time": int(r[6]),
        })

    return candles
