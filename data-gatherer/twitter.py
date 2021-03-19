import tweepy, os, json, csv

class CryptoStream(tweepy.StreamListener):

    def __init__(self,symbol):
        super(CryptoStream, self).__init__()
        self.symbol = symbol
        
    # Actions performed when a tweet enters the stream
    def on_status(self, status):
       
      time = status.created_at
      tweetid = status.id_str
      text = status.text
      userid = status.user.id_str
      username = status.user.name
      followers = status.user.followers_count
      retweets = status.retweet_count
      favorites = status.favorite_count
      
      if hasattr(status,'extended_tweet'):
          text = status.extended_tweet['full_text']
          
      data = [time,tweetid,text,userid,username,followers,retweets,favorites]
      
      print(status.text)
      
      here = os.path.dirname(os.path.realpath('twitter.py'))
      
      filepath = os.path.join(here,'{}-tweets.csv'.format(self.symbol))
      
      if('bitcoin') in text:
          with open(filepath,'a') as csvfile:
              writer = csv.writer(csvfile)
              writer.writerow(data)
        
    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False
        