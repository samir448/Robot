import requests
import time
import pandas as pd

capital = 1000.0
position_size = 100.0
leverage = 2
tp_pct = 0.05
sl_pct = 0.02
in_position = False
buy_price = 0.0

def get_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return float(data['bitcoin']['usd'])

def simulate_price_history(current_price):
    # Génère une fausse série de prix autour du prix actuel pour calculer le RSI
    return pd.Series([current_price * (1 + (i - 50) / 1000) for i in range(100)])

def compute_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

print("Bot started...\n")

while True:
    try:
        price = get_price()
        history = simulate_price_history(price)
        rsi = compute_rsi(history)

        print(f"[{time.strftime('%H:%M:%S')}] BTC: {price:.2f} | RSI: {rsi:.2f} | Capital: {capital:.2f}")

        if not in_position and rsi < 30:
            buy_price = price
            in_position = True
            print(f">>> BUY at {buy_price:.2f}")

        elif in_position:
            tp_price = buy_price * (1 + tp_pct)
            sl_price = buy_price * (1 - sl_pct)

            if price >= tp_price:
                gain = position_size * tp_pct * leverage
                capital += gain
                in_position = False
                print(f"<<< TAKE PROFIT at {price:.2f} | +{gain:.2f} | Capital: {capital:.2f}")
            elif price <= sl_price:
                loss = position_size * sl_pct * leverage
                capital -= loss
                in_position = False
                print(f"<<< STOP LOSS at {price:.2f} | -{loss:.2f} | Capital: {capital:.2f}")

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)