import pyupbit
import KeyFile
import time
import datetime

print("Start Real-time Trading Program.")

# 1) Login Upbit
Access_key = KeyFile.Access_key
Secret_key = KeyFile.Secret_key
upbit = pyupbit.Upbit(Access_key, Secret_key)

print("Login successfully.")


# 2) Get coin name information to purchase from the user
tickets = pyupbit.get_tickers("KRW")
while True:
    print("Input what Coin_name you want to buy.")
    coin_name = input()
    if coin_name in tickets:
        break
    else:
        print("Input Coin_name Error.")
        print("You have to input correct coin_name. Input again please.\n")

print("Start Trading {}".format(coin_name))


# 3) Start real-time Trading
while True:
    try:
        df = pyupbit.get_ohlcv(coin_name, interval = "day", count = 1)

        now = datetime.datetime.now()
        start_time = df.index[0]
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            df = pyupbit.get_ohlcv(coin_name, interval="day", count=2)
            target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * 0.7
            current_price = pyupbit.get_orderbook(tickers=coin_name)[0]["orderbook_units"][0]["ask_price"]

            if target_price < current_price:
                krw = upbit.get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
        else:
            btc = upbit.get_balance("KRW-BTC")
            if btc >= 10000 / current_price:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)

    except Exception as e:
        print(e)
        time.sleep(1)