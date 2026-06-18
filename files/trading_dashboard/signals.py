"""
C1 Trading Dashboard - Signal Generator
Analyzes market data and generates trading signals based on:
- Moving Average crossovers (Golden Cross / Death Cross)
- Price position in 52-week range (oversold/overbought)
- Analyst consensus vs current price (upside potential)
- Sentiment momentum from Bigdata.com
"""

from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class SignalType(Enum):
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_SELL = "STRONG_SELL"


@dataclass
class StockData:
    ticker: str
    name: str
    price: float
    ma_50: float
    ma_200: float
    year_high: float
    year_low: float
    analyst_target: float
    analyst_consensus: str
    buy_count: int
    hold_count: int
    sell_count: int
    sentiment_score: float
    sentiment_momentum: float
    beta: float
    change_1d_pct: float
    change_ytd_pct: float


@dataclass
class Signal:
    ticker: str
    signal_type: SignalType
    reason: str
    upside_pct: float
    confidence: float  # 0-1


def position_in_range(price: float, low: float, high: float) -> float:
    if high == low:
        return 0.5
    return (price - low) / (high - low)


def generate_signal(stock: StockData) -> Signal:
    score = 0
    reasons = []

    above_ma50 = stock.price > stock.ma_50
    above_ma200 = stock.price > stock.ma_200
    if above_ma50 and above_ma200:
        score += 2
        reasons.append("Golden Cross (price > 50MA > 200MA)")
    elif above_ma200 and not above_ma50:
        score += 1
        reasons.append("Above 200MA, consolidating near 50MA")
    elif not above_ma50 and not above_ma200:
        score -= 2
        reasons.append("Death Cross (price < 50MA < 200MA)")

    pos = position_in_range(stock.price, stock.year_low, stock.year_high)
    if pos < 0.2:
        score += 2
        reasons.append(f"Oversold - {pos:.0%} in 52-week range")
    elif pos > 0.8:
        score += 1
        reasons.append(f"Strong uptrend - {pos:.0%} in 52-week range")
    elif pos < 0.4:
        score += 1
        reasons.append(f"Near support - {pos:.0%} in 52-week range")

    upside = ((stock.analyst_target - stock.price) / stock.price) * 100
    if upside > 40:
        score += 2
        reasons.append(f"Major upside to target: +{upside:.1f}%")
    elif upside > 20:
        score += 1
        reasons.append(f"Significant upside: +{upside:.1f}%")
    elif upside < 0:
        score -= 1
        reasons.append(f"Below analyst target: {upside:.1f}%")

    if stock.analyst_consensus == "Buy":
        score += 1
    elif stock.analyst_consensus == "Sell":
        score -= 1

    if stock.sentiment_score > 0.1:
        score += 1
        reasons.append(f"Positive sentiment ({stock.sentiment_score:+.3f})")
    elif stock.sentiment_score < -0.05:
        score -= 1
        reasons.append(f"Negative sentiment ({stock.sentiment_score:+.3f})")

    if stock.sentiment_momentum > 0.02:
        score += 1
        reasons.append("Improving sentiment momentum")

    if score >= 4:
        signal_type = SignalType.STRONG_BUY
    elif score >= 2:
        signal_type = SignalType.BUY
    elif score >= 0:
        signal_type = SignalType.HOLD
    elif score >= -2:
        signal_type = SignalType.SELL
    else:
        signal_type = SignalType.STRONG_SELL

    confidence = min(1.0, max(0.2, 0.5 + abs(score) * 0.1))

    return Signal(
        ticker=stock.ticker,
        signal_type=signal_type,
        reason=" | ".join(reasons),
        upside_pct=upside,
        confidence=confidence,
    )


STOCKS = [
    StockData("AAPL", "Apple Inc.", 295.95, 287.96, 267.85, 317.4, 196.86,
              326.47, "Buy", 69, 33, 7, -0.02, -0.005, 1.086, -1.10, 8.86),
    StockData("NVDA", "NVIDIA Corp.", 204.65, 208.74, 189.70, 236.54, 142.03,
              309.46, "Buy", 58, 16, 3, 0.178, 0.014, 2.202, -1.33, 9.73),
    StockData("TSLA", "Tesla, Inc.", 396.38, 401.34, 416.61, 498.83, 288.77,
              450.45, "Hold", 32, 34, 15, -0.019, 0.039, 1.798, -2.05, -11.86),
    StockData("MSFT", "Microsoft Corp.", 378.91, 412.87, 451.98, 555.45, 356.28,
              551.96, "Buy", 66, 16, 0, 0.031, 0.003, 1.103, -3.79, -21.65),
]


def run_analysis():
    print("=" * 70)
    print(f"  C1 TRADING DASHBOARD - SIGNAL REPORT")
    print(f"  Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 70)

    signals = []
    for stock in STOCKS:
        signal = generate_signal(stock)
        signals.append(signal)

    buy_signals = [s for s in signals if s.signal_type in (SignalType.STRONG_BUY, SignalType.BUY)]
    sell_signals = [s for s in signals if s.signal_type in (SignalType.SELL, SignalType.STRONG_SELL)]
    hold_signals = [s for s in signals if s.signal_type == SignalType.HOLD]

    if buy_signals:
        print("\n  BUY SIGNALS:")
        for s in buy_signals:
            emoji = "***" if s.signal_type == SignalType.STRONG_BUY else " * "
            print(f"  {emoji} {s.ticker} [{s.signal_type.value}] Upside: +{s.upside_pct:.1f}% | Confidence: {s.confidence:.0%}")
            print(f"      {s.reason}")

    if hold_signals:
        print("\n  HOLD / NEUTRAL:")
        for s in hold_signals:
            print(f"   ~  {s.ticker} [{s.signal_type.value}] Upside: +{s.upside_pct:.1f}%")
            print(f"      {s.reason}")

    if sell_signals:
        print("\n  SELL SIGNALS:")
        for s in sell_signals:
            print(f"  !!  {s.ticker} [{s.signal_type.value}] Upside: {s.upside_pct:+.1f}%")
            print(f"      {s.reason}")

    print("\n" + "=" * 70)
    print("  DISCLAIMER: Not financial advice. Trade at your own risk.")
    print("  Data source: Bigdata.com")
    print("=" * 70)

    return signals


if __name__ == "__main__":
    run_analysis()
