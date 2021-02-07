# An app to invest in (and sell) Dogecoin when Elon Musk tweets about it
# 1. Listen for "doge" 
# 2. If "doge" mentioned, buy $xx of DOGE
# 3. Optional part 1 - After purchase, set to sell when price begins to drop
# 4. Optional part 2 - Check if Robinhood daytrade limit at max before selling (or buying)

import robin_stocks as rh
import tweepy as t
import time
import config
import funcs

def from_creator(status):
    '''Filters out mentions and retweets'''
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

def stop_loss():
    '''Sells stock when it drops 5% or more from its lastest high'''
    buy_price = high_price = rh.get_crypto_quote('DOGE')['ask_price']
    up = True
    while up:
        current_price = rh.get_crypto_quote('DOGE')['ask_price']
        if current_price < high_price:
            loss_percentage = (current_price*100)/high_price
            if loss_percentage <= 95:
                sell_amount = (20*current_price)/buy_price
                rh.order_sell_crypto_by_price('DOGE', sell_amount)
                up = False
            else:
                time.sleep(60)
        else:
            time.sleep(60)

# Set up robin_stocks
rh.login(config.user, config.pw)

# Set up tweepy
auth = t.OAuthHandler(config.api_key, config.secret_key)
auth.set_access_token(config.token, config.token_secret)
api = t.API(auth,wait_on_rate_limit=True)

class MyStreamListener(t.StreamListener):

    def on_status(self, status):
        if from_creator(status):
            tweet = status.text.lower()
            if "doge" in tweet:
                if check_dt():
                    # Buy $20 DOGE
                    print(rh.order_buy_crypto_by_price('DOGE' , 20))
                    stop_loss()
            return True
        return True

    def on_error(self, status_code):
        if status_code == 420:
            print("Error 420")
            #returning False in on_error disconnects the stream
            return False
    
myStreamListener = MyStreamListener()
myStream = t.Stream(auth = api.auth, listener=myStreamListener)   
myStream.filter(follow=['44196397'])