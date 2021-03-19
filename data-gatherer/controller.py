import tweepy, time
from twitter import CryptoStream
from market import MarketData


# Twitter API authentication info

def openStream(currency,keywords):
    
    auth = tweepy.OAuthHandler('', '')
    auth.set_access_token('', '')
    api = tweepy.API(auth)
    
    myStreamListener = CryptoStream(currency)
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener,tweet_mode='extended')
    myStream.filter(track=keywords, is_async=True,languages=['en'])
    
    return myStream

#Closes a twitter stream
    
def closeStream(stream):
    
    stream.disconnect()
    
def getMarketData(symbol):
    
        market = MarketData()
        session = market.startSession()
        quote = market.getQuote(session,symbol)
        market.storeQuote(quote,symbol)
    
#Main loop of program
    
while True:
    
    # Retrieve CMC data 
    
    try:
        getMarketData('BTC')
    
    except:
        pass
        
    time.sleep(5)
    
    try:
        getMarketData('ETH')
    
    except:
        pass
    
    # Open twitter streams
    
    btcstream = openStream('BTC',['bitcoin'])
    
    print('Bitcoin twitter stream opened.')
    
    ethstream = openStream('ETH',['ethereum'])
    
    print('Ethereum twitter stream opened.')
    
    # Waits 14.5 minutes
    time.sleep(870)

    # Closes and deletes streams
    
    closeStream(btcstream)
    print('Bitcoin twitter stream closed.')
    
    closeStream(ethstream)
    print('Ethereum twitter stream closed.')
    
    del(btcstream)
    del(ethstream)
    
    time.sleep(25)

        
    
    
    
    
    