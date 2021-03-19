import json, csv, datetime
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os

class MarketData():

  def __init__(self):
    self.parameters = {'limit':10,'convert':'USD','cryptocurrency_type':'all'}
    self.headers = {'Accepts': 'application/json','X-CMC_PRO_API_KEY': ''}
    self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    
#Creates a session with CMC's API
  def startSession(self):
    session = Session()
    session.headers.update(self.headers)
    return session

#Retrieves the index in the response data of a symbol
  def getIndex(self,data, symbol):
      index = None
      for i in range(len(data['data'])):
          if data['data'][i]['symbol'] == symbol:
              index = i
      return index

#Gets quote for a coin
  def getQuote(self, session, symbol):

    quote = None

    try:
      response = session.get(self.url, params=self.parameters)
      quote = response.text
      quote = json.loads(quote)
      print('Quote successfully retrieved.')
      index = self.getIndex(quote,symbol)
      
      price = quote['data'][index]['quote']['USD']['price']
      volume = quote['data'][index]['quote']['USD']['volume_24h']
      hourdelta = quote['data'][index]['quote']['USD']['percent_change_1h']
      daydelta = quote['data'][index]['quote']['USD']['percent_change_24h']
      
      timestring = quote['status']['timestamp']
      time = datetime.datetime.strptime(timestring, '%Y-%m-%dT%H:%M:%S.%fZ')
      
      # Removes millisecond and 'Z'
      time = str(time)[:19]
      
      print(timestring)
      
      data = [time,price,volume,hourdelta,daydelta]
      
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)
      
    return data

#Stores the quote as a line in a csvfile
  def storeQuote(self,data,symbol):

    here = os.path.dirname(os.path.realpath('market.py'))
    
    filepath = os.path.join(here,'{}-quotes.csv'.format(symbol))

    with open(filepath,'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
        print('Quote successfully stored.')