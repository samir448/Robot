import requests
import time

capital = 1000.0
position_size = 100.0
leverage = 2
tp_pct = 0.05
sl_pct = 0.02
in_position = False
buy_price = 0.0

def get_price():
    r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
    return r.json()["bitcoin"]["usd"]

while True:
    try:
        price = get_price()
        print(f"BTC price: {price} | Capital: {capital:.2f}")
        if not in_position and price % 10 == 0:  # signal d’achat fictif
            buy_price = price
            in_position = True
            print(f"BUY at {buy_price}")
        elif in_position:
            if price >= buy_price * (1 + tp_pct):
                gain = position_size * tp_pct * leverage
                capital += gain
                print(f"TP at {price} | +{gain:.2f}")
                in_position = False
            elif price <= buy_price * (1 - sl_pct):
                loss = position_size * sl_pct * leverage
                capital -= loss
                print(f"SL at {price} | -{loss:.2f}")
                in_position = False
        time.sleep(30)
    except Exception as e:
        print("Erreur :", e)
        time.sleep(30)