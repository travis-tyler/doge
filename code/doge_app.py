# An app to buy and set trailing stop loss for DOGECOIN
import robin_stocks as rh
import tweepy as t
import time
import config

investment = input('How much DOGECOIN would you like to buy? ')

def doge_buy_stop_loss(buy_amount):
    '''Buys amount of DOGE and sells when it drops 5% or more from its lastest high'''
    print(f'Buying {buy_amount} of DOGE!\n')
    print('------------\n')

    # Doge error workaround
    price = float(rh.get_crypto_quote('DOGE').get('ask_price'))
    shares = round(float(buy_amount)/price, 0)
    result = rh.order_buy_crypto_by_quantity('DOGE', shares)

    print(result)
    print('------------\n')
    buy_price = high_price = float(rh.get_crypto_quote('DOGE')['ask_price'])
    up=True
    while up:
        time.sleep(10)
        print('\n------------\n')
        print('Checking price....\n')
        current_price = float(rh.get_crypto_quote('DOGE')['ask_price'])
        print('------------\n')
        print(f'Current price: {current_price}')
        print(f'High price: {high_price}')
        print(f'High price: {buy_price}')
        if current_price < high_price:
            loss_percentage = (current_price*100)/high_price
            print(f'Loss percentage: {round(100-loss_percentage, 2)}%\n')
            if loss_percentage <= 95:
                sell_amount = (buy_amount*current_price)/buy_price
                # Doge error workaround
                price = float(rh.get_crypto_quote('DOGE').get('ask_price'))
                shares = round(sell_amount/price, 0)
                result = rh.order_buy_crypto_by_quantity('DOGE', shares)
                print('------------\n')
                print(f'Selling ${sell_amount} of DOGE!\n')
                print('------------\n')
                break
            else:
                continue
        else:
            continue

# Set up robin_stocks
rh.login(config.user, config.pw)

# Run function
doge_buy_stop_loss(investment)