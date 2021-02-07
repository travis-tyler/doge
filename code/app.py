# An app to invest in (and sell) Dogecoin when Elon Musk tweets about it
# 1. Listen for "doge" 
# 2. If "doge" mentioned, buy $xx of DOGE
# 3. Optional part 1 - After purchase, set to sell when price begins to drop
# 4. Optional part 2 - Check if Robinhood daytrade limit at max before selling (or buying)

import robin_stocks as rh
import tweepy as t
import time
import config

# Set up tweepy
auth = t.OAuthHandler(config.api_key, config.secret_key)
auth.set_access_token(config.token, config.token_secret)
api = t.API(auth,wait_on_rate_limit=True)

#Filters out mentions and retweets
def from_creator(status):
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

class MyStreamListener(t.StreamListener):

    def on_status(self, status):
        if from_creator(status):
            tweet = status.text.lower()
            if "doge" in tweet:

                # Set number of day trades
                # TODO: needs to be for week, not all time
                # TODO: default to buying DOGE if last move was buying and vice versa
                day_trades = len(rh.get_day_trades())

                # Right number?
                if day_trades < 4:
                
                    # Set "up" status to 2 for while loop
                    up = 2

                    # Buy $20 DOGE
                    print(rh.order_buy_crypto_by_price('DOGE' , 20))

                    # Get current DOGE value at purchase
                    buy_price = rh.get_crypto_quote('DOGE')['ask_price']

                    # Wait for order to process
                    time.sleep(60)

                    # Get current DOGE value 60 seconds after purchase
                    old_price = rh.get_crypto_quote('DOGE')['ask_price']

                    # Loop to check price every minute
                    # Sell if price falls for two mins in a row
                    # If "up" drops to 0, exit loop
                    while up > 0:
                        time.sleep(60)
                        new_price = rh.get_crypto_quote('DOGE')['ask_price']
                        if new_price > old_price:
                            old_price = new_price
                            new_price = rh.get_crypto_quote('DOGE')['ask_price']
                            up = 2
                        else:
                            old_price = new_price
                            new_price = rh.get_crypto_quote('DOGE')['ask_price']
                            up -= 1

                        # Calculate amount to sell
                        sell_amount = ((20*current_price)/buy_price)

                        # Sell new amount of dogecoin
                        print(rh.order_sell_crypto_by_price('DOGE', sell_amount))

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