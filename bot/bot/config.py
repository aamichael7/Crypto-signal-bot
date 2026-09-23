import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COINS_FILE = ROOT / "config" / "coins.json"

TIMEFRAME = "15m"
CANDLE_LIMIT = 120

# Paper-trading reference levels only.
ATR_STOP_MULTIPLIER = 1.5
R1_MULTIPLIER = 1.5
R2_MULTIPLIER = 2.5


def load_symbols():
    return json.loads(COINS_FILE.read_text())
