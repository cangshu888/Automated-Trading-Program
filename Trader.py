import re
import json
import os
import ast
from time import gmtime, strftime
from http import cookiejar
from urllib import request
import requests
import math

#import user-defined modules
from classes import Order, Candle, Ticker
import data
from writeData import writeTestResults
from checkForEMAStrategy import checkForEMAStrategy
from checkForReversalStrategy import checkForReversalStrategy
from checkForHighTightFlagStrategy import checkForHighTightFlagStrategy
from checkForStopLoss import checkForStopLoss, findOrder
from checkForFlatTopBreakoutStrategy import checkForFlatTopBreakoutStrategy, checkForValidBase
from checkForMorningBreakoutStrategy import checkForMorningBreakoutStrategy
from checkForOversoldReversalStrategy import checkForOversoldReversalStrategy
from checkFor3BarReversalStrategy import checkForBullish3BarReversalStrategy, checkForBearish3BarReversalStrategy
from checkForReversalOff25CentIntervalStrategy import checkForBullishReversalOff25CentIntervalStrategy, checkForBearishReversalOff25CentIntervalStrategy 

ACCESS_TOKEN = ''
ACCOUNT_NUMBER = '' #enter account number here
REFRESH_TOKEN = '' #enter refresh token here
CLIENT_ID = '' #enter client ID here
_SESSION = requests.session()

CALCULATED_EMAs = {} #maps symbol to dictionary that maps time to dictionary that maps EMA to value
CANDLES = {}
ORDERS = []

def calculateInitialEMAs(listOfClosingPrices, period):
    multiplier = 2 / (period + 1)
    initialEMA = 0
    EMA_period = 0
    for i in range(50 - period, 50):
        if (i == 50 - period):
            initialEMA = listOfClosingPrices[i]
            EMA_period = initialEMA
        else:
            #EMA_period = ((listOfClosingPrices[i] - initialEMA) * multiplier) + initialEMA
            EMA_period = (multiplier * listOfClosingPrices[i]) + ((1 - multiplier) * initialEMA)
            initialEMA = EMA_period
    
    return EMA_period

#calculates the initial EMAs for each ticker in AVAILABLE_TICKERS
def getInitialEMAs():
    initialEMAs = {}
    for i in range(len(data.AVAILABLE_TICKERS)):
        closingPrices = getDataFor50EMACalculation(data.AVAILABLE_TICKERS[i])
        initialEMA5 = calculateInitialEMAs(closingPrices, 5)
        initialEMA10 = calculateInitialEMAs(closingPrices, 10)
        initialEMA20 = calculateInitialEMAs(closingPrices, 20)
        
        #[test]
        print(data.AVAILABLE_TICKERS[i])
        #[test]

        initialEMAs[data.AVAILABLE_TICKERS[i]] = {'5EMA' : round(initialEMA5, 2), '10EMA' : round(initialEMA10, 2), '20EMA' : round(initialEMA20, 2)}
        time.sleep(1)

    with open('initialEMAs.json', 'w') as outfile:
        json.dump(initialEMAs, outfile)

#gets price history for 50EMA calculation
def getDataFor50EMACalculation(symbol):
    global ACCESS_TOKEN

    header = {'Host': 'api.tdameritrade.com',
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + ACCESS_TOKEN, 
          'Cache-Control': 'no-cache',
          'Connection' : 'keep-alive'}

    payload = {
               'period': '1',
               'periodType': "day",
               'frequency': '1',
               'frequencyType': "minute",
               'needExtendedHoursData': 'false'
              } 

    r = _SESSION.get('https://api.tdameritrade.com/v1/marketdata/' + symbol + '/pricehistory?periodType=day&period=1&frequencyType=minute&frequency=1&needExtendedHoursData=false', headers=header)

    #parse closing price for each candle
    initial_close_prices = re.findall('"close":[0-9]+.[0-9]+', r.text)
    close_prices = []
    for i in range(1, 51):
        close_prices.append(float(initial_close_prices[i * -1].split(':')[1]))

    listOfClosingPrices = []
    for i in reversed(close_prices):
        listOfClosingPrices.append(i)

    print(listOfClosingPrices)

    return listOfClosingPrices

#performs a premarket scan for morning breakout candidates
def scanForMorningBreakouts():
    global ACCESS_TOKEN
    listOfMorningBreakouts = []

    header = {'Host': 'api.tdameritrade.com',
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + ACCESS_TOKEN, 
          'Cache-Control': 'no-cache',
          'Connection' : 'keep-alive'}

    #creates list of symbols for payload
    symbol_list = ''
    for i in range(len(data.MORNING_BREAKOUT_TICKERS)):
        symbol_list += data.MORNING_BREAKOUT_TICKERS[i]
        if(i < len(data.MORNING_BREAKOUT_TICKERS) - 1):
            symbol_list += ','

    payload = {
               'symbol': symbol_list
              }

    #converts list of symbols into URL format
    link = re.sub('[,]', '%2C', symbol_list)

    r = _SESSION.get('https://api.tdameritrade.com/v1/marketdata/quotes?symbol=' + link, data=payload, headers=header) #returns json list of dictionary
    quotes = {}

    #parse prices for each quote
    initial_close_prices = re.findall('"closePrice":[0-9]+.[0-9]+', r.text)
    close_prices = []
    for i in range(len(initial_close_prices)):
        close_prices.append(float(initial_close_prices[i].split(':')[1]))

    #parse prices for each quote
    initial_prices = re.findall('"lastPrice":[0-9]+.[0-9]+', r.text)
    prices = []
    for i in range(len(initial_prices)):
        prices.append(float(initial_prices[i].split(':')[1]))

    #parse volume for each quote
    initial_volumes = re.findall('"totalVolume":[0-9]+', r.text)
    volumes = []
    for i in range(len(initial_volumes)):
        volumes.append(int(initial_volumes[i].split(':')[1]))

    #parse symbol for each quote
    initial_symbols = re.findall('"symbol":"[A-Z]+"', r.text)
    symbols = []
    for i in range(len(initial_symbols)):
        symbol = initial_symbols[i].split(':')[1]
        symbol = re.sub('["]', '', symbol)
        symbols.append(symbol)

    #checks if the morning breakout candidate had a significant gap up
    for i in range(len(close_prices)):
        if (prices[i] > 1.03 * close_prices[i] and volumes[i] > 15000):
            listOfMorningBreakouts.append(symbols[i])

    return listOfMorningBreakouts
            

#returns the price and volume of the symbol
def getQuote(symbol, quotes):
    price = quotes[symbol]['price']   
    volume = quotes[symbol]['volume']  

    return price, volume

#posts to 'get quotes' API 
#returns dictionary that maps symbol to dictionary of price and volume
def getLastClosingPrices(quoteServerError):
    global ACCESS_TOKEN

    header = {'Host': 'api.tdameritrade.com',
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + ACCESS_TOKEN, 
          'Cache-Control': 'no-cache',
          'Connection' : 'keep-alive'}

    #creates list of symbols for payload
    symbol_list = ''
    for i in range(len(data.AVAILABLE_TICKERS)):
        symbol_list += data.AVAILABLE_TICKERS[i]
        if(i < len(data.AVAILABLE_TICKERS) - 1):
            symbol_list += ','

    payload = {
               'symbol': symbol_list
              }

    #converts list of symbols into URL format
    link = re.sub('[,]', '%2C', symbol_list)

    r = _SESSION.get('https://api.tdameritrade.com/v1/marketdata/quotes?symbol=' + link, data=payload, headers=header) #returns json list of dictionary
    quotes = {}

    #parse prices for each quote
    initial_close_prices = re.findall('"closePrice":[0-9]+.[0-9]+', r.text)
    close_prices = []
    for i in range(len(initial_close_prices)):
        close_prices.append(float(initial_close_prices[i].split(':')[1]))

    #parse symbol for each quote
    initial_symbols = re.findall('"symbol":"[A-Z]+"', r.text)
    symbols = []
    for i in range(len(initial_symbols)):
        symbol = initial_symbols[i].split(':')[1]
        symbol = re.sub('["]', '', symbol)
        symbols.append(symbol)

    for i in range(len(symbols)):
        quotes[symbols[i]] = {'close price' : close_prices[i]}

    #parse 'delayed' for each quote
    initial_delayed_status = re.findall('"delayed":[a-z]+', r.text)
    delayed_status = []
    for i in range(len(initial_delayed_status)):
        delayed_status.append(str(initial_delayed_status[i].split(':')[1]))
    for i in range(len(delayed_status)):
        if (delayed_status[i] == 'true'):
            quoteServerError = True
            break

    print(quotes)

    if (quoteServerError):
        print("QUOTE SERVER ERROR")
    else:
        print("NO ERROR")
    
    return quotes, quoteServerError

#posts to 'get quotes' API 
#returns dictionary that maps symbol to dictionary of price and volume
def getQuotes(quoteServerError):
    global ACCESS_TOKEN

    header = {'Host': 'api.tdameritrade.com',
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + ACCESS_TOKEN, 
          'Cache-Control': 'no-cache',
          'Connection' : 'keep-alive'}

    #creates list of symbols for payload
    symbol_list = ''
    for i in range(len(data.AVAILABLE_TICKERS)):
        symbol_list += data.AVAILABLE_TICKERS[i]
        if(i < len(data.AVAILABLE_TICKERS) - 1):
            symbol_list += ','

    payload = {
               'symbol': symbol_list
              }

    #converts list of symbols into URL format
    link = re.sub('[,]', '%2C', symbol_list)

    r = _SESSION.get('https://api.tdameritrade.com/v1/marketdata/quotes?symbol=' + link, data=payload, headers=header) #returns json list of dictionary
    quotes = {}

    #parse prices for each quote
    initial_prices = re.findall('"lastPrice":[0-9]+.[0-9]+', r.text)
    prices = []
    for i in range(len(initial_prices)):
        prices.append(float(initial_prices[i].split(':')[1]))

    #parse volume for each quote
    initial_volumes = re.findall('"totalVolume":[0-9]+', r.text)
    volumes = []
    for i in range(len(initial_volumes)):
        volumes.append(int(initial_volumes[i].split(':')[1]))

    #parse symbol for each quote
    initial_symbols = re.findall('"symbol":"[A-Z]+"', r.text)
    symbols = []
    for i in range(len(initial_symbols)):
        symbol = initial_symbols[i].split(':')[1]
        symbol = re.sub('["]', '', symbol)
        symbols.append(symbol)

    for i in range(len(symbols)):
        quotes[symbols[i]] = {'price' : prices[i], 'volume' : volumes[i]}

    #parse 'delayed' for each quote
    initial_delayed_status = re.findall('"delayed":[a-z]+', r.text)
    delayed_status = []
    for i in range(len(initial_delayed_status)):
        delayed_status.append(str(initial_delayed_status[i].split(':')[1]))
    for i in range(len(delayed_status)):
        if (delayed_status[i] == 'true'):
            quoteServerError = True
            break
    
    return quotes, quoteServerError

#posts to 'accounts' API and returns DTBP       
def getDTBP():
    global ACCESS_TOKEN
    header = {'Host': 'api.tdameritrade.com',
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + ACCESS_TOKEN, 
          'Cache-Control': 'no-cache',
          'Connection' : 'keep-alive'}

    r = _SESSION.get('https://api.tdameritrade.com/v1/accounts/' + ACCOUNT_NUMBER, headers=header) #returns dictionary

    DTBP = float(re.findall('"dayTradingBuyingPower" : [0-9]+.[0-9]+', r.text)[0].split(':')[1])

    return DTBP

#posts to 'authentication' API and gets access token
#needs to be called at 6:30, 6:59, and 7:28
#returns access token
def getAccessToken():
    global ACCESS_TOKEN
    payload = {'grant_type': 'refresh_token',
               'refresh_token' : REFRESH_TOKEN,
               'client_id' : CLIENT_ID} 
    r = _SESSION.post('https://api.tdameritrade.com/v1/oauth2/token', data=payload, headers = { 'Content-Type': 'application/x-www-form-urlencoded' }) 

    ACCESS_TOKEN = ast.literal_eval(r.text)['access_token']

    #[test]
    print(ACCESS_TOKEN)
    #[test]

    return ast.literal_eval(r.text)['access_token']

#posts to 'trading' API and places an order
def placeOrder(orderType, symbol, size):
    #[test]
    print("ORDER PLACED")
    print("The order type is: " + orderType)
    print("The symbol is: " + symbol)
    print("The size is: " + str(size))
    #[test]

    global ACCESS_TOKEN
    header = {'Host': 'api.tdameritrade.com',
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Bearer ' + ACCESS_TOKEN, 
          'Cache-Control': 'no-cache',
          'Connection' : 'keep-alive'}

    payload = {
    "orderType": "MARKET",
    "session": "NORMAL",
    "duration": "DAY",
    "orderStrategyType": "SINGLE",
    "orderLegCollection": [
        {
        "instruction": orderType,
        "quantity": size,
        "instrument": {
            "symbol": symbol,
            "assetType": "EQUITY"
        }
        }
    ]
    }

    #place order
    r = _SESSION.post('https://api.tdameritrade.com/v1/accounts/' + ACCOUNT_NUMBER + '/orders', json=payload, headers=header)

    #[test]
    print("The status code is: " + str(r.status_code))
    #[test]

#runs between 6:30 and 7:59
def main():
    canContinue = True
    canGetAccessToken = True
    canGetLastClosingPrice = True
    updatedCanTradeStatus = False
    quoteServerError = False
    numberOfIncorrectPrices = 0
    tickers = {}
    lastClosingPrices = {}
    morningBreakouts = []
    DTBP = 0

    #[test]
    printTime1 = True
    printTime2 = True
    printTime3 = True
    printTime4 = True
    printTime5 = True
    #[test]

    #keeps the program running continuously until 7:59AM
    #need to start program manually before market opens or night before
    while(canContinue):
        global ACCESS_TOKEN
        global ACCESS_TOKENS
        global CALCULATED_EMAs
        global CANDLES

        currentInvested = 0
        positions = {}
        orderQueue = []
        currentTime = strftime("%M:%S", gmtime())
        hours = int(strftime("%H", gmtime())) - 8
        time = str(hours) + ':' + currentTime
        previousSecond = '59'

        #[test]
        if (time == '1:00:00' and printTime1):
            print("connection maintained at 1AM")
            printTime1 = False
        if (time == '2:00:00' and printTime2):
            print("connection maintained at 2AM")
            printTime2 = False
        if (time == '3:00:00' and printTime3):
            print("connection maintained at 3AM")
            printTime3 = False
        if (time == '4:00:00' and printTime4):
            print("connection maintained at 4AM")
            printTime4 = False
        if (time == '5:00:00' and printTime5):
            print("connection maintained at 5AM")
            printTime5 = False
        #[test]
        
        '''
        if (time == '6:25:00' and canGetAccessToken):
            ACCESS_TOKEN = getAccessToken()
            morningBreakouts = scanForMorningBreakouts()
            count = 0

            #initializes a dictionary of ticker objects
            for i in range(len(data.AVAILABLE_TICKERS)):
                tickers[data.AVAILABLE_TICKERS[i]] = Ticker(data.AVAILABLE_TICKERS[i]) #maps symbol to ticker object
                CALCULATED_EMAs[data.AVAILABLE_TICKERS[i]] = []
                CANDLES[data.AVAILABLE_TICKERS[i]] = []
                tickers[data.AVAILABLE_TICKERS[i]].canTrade = True

            for i in range(len(morningBreakouts)):
                closingPrices = []
                if (count > 298):
                    break
                else:
                    closingPrices = getDataFor50EMACalculation(morningBreakouts[i])
                    tickers[item].calculateEMA50(closingPrices)
                time.sleep(1)
        '''
        
        if (time == '6:29:59' and canGetAccessToken): 
            ACCESS_TOKEN = getAccessToken()
            DTBP = getDTBP()
            canGetAccessToken = False

            if (canGetLastClosingPrice):
                lastClosingPrices, quoteServerError = getLastClosingPrices(quoteServerError)
                canGetLastClosingPrice = False

            if (quoteServerError == True):
                canContinue = False
                print("QUOTE SEVRVER ERROR - DELAYED DATA")
                print("Program not allowed to start")


            #initializes a dictionary of ticker objects
            for i in range(len(data.AVAILABLE_TICKERS)):
                tickers[data.AVAILABLE_TICKERS[i]] = Ticker(data.AVAILABLE_TICKERS[i]) #maps symbol to ticker object
                CALCULATED_EMAs[data.AVAILABLE_TICKERS[i]] = []
                CANDLES[data.AVAILABLE_TICKERS[i]] = []
                tickers[data.AVAILABLE_TICKERS[i]].canTrade = True

        '''
        #[test]
        if (canGetAccessToken):
            ACCESS_TOKEN = getAccessToken()
            tickers = {}
            canGetAccessToken = False
            for i in range(len(data.AVAILABLE_TICKERS)):
                tickers[data.AVAILABLE_TICKERS[i]] = Ticker(data.AVAILABLE_TICKERS[i])
                tickers[data.AVAILABLE_TICKERS[i]].canTrade = True
                CALCULATED_EMAs[data.AVAILABLE_TICKERS[i]] = []
                CANDLES[data.AVAILABLE_TICKERS[i]] = []

            if (canGetLastClosingPrice):
                lastClosingPrices, quoteServerError = getLastClosingPrices(quoteServerError)
                canGetLastClosingPrice = False
        #[test]
        '''

        quotes = {}
        previousQuotes = {}
        condition = True
               
        #assumes each iteration of the loop takes less than 1 second
        while ((time >= '6:30:00') and (time <= '7:59:00') and canContinue): 
            global ORDERS
            #gets the current time and converts it to PST
            currentTime = strftime("%M:%S", gmtime())
            hours = str(int(strftime("%H", gmtime())) - 8)
            time = hours + ':' + currentTime
            seconds = strftime("%S", gmtime())
            minutes = strftime("%M", gmtime())
            candleTime = hours + ':' + minutes


            #gets quotes for available tickers for current second
            if (seconds != previousSecond):
                quotes, quoteServerError = getQuotes(quoteServerError)

                try:
                    testQuote, testVolume = getQuote('MU', quotes)
                except KeyError:
                    if (len(previousQuotes.keys()) == 0 and time != '6:00:00'):
                        print("Key error detected and previous quotes do not exist - exiting program at " + time)
                        canContinue = False
                        break
                    else:
                        print("Key error detected - using previous quotes at " + time)
                        quotes = previousQuotes
                        
                previousQuotes = quotes
                previousSecond = seconds
            else:
                quotes = previousQuotes
            

            #prevent multiple API calls to getQuotes() within the same second
            previousSecond = seconds

            #prevents program from trying to get access token multiple times in the same second
            if (time != '6:30:00' and time != '6:59:00' and time != '7:28:00' and canGetAccessToken == False):
                canGetAccessToken = True

            #gets new access token one minute before the expiry time
            if ((time == '6:59:00' or time == '7:28:00') and canGetAccessToken == True): 
                ACCESS_TOKEN = getAccessToken()
                canGetAccessToken = False

            #stops all new trades at 7:45
            if (time == '7:45:00'): 
                for item in tickers.keys():
                    tickers[item].canTrade = False

            #exits all current positions at 7:57
            #writes all test data to JSON files
            if (time == '7:57:00'):
                for item in positions.keys():
                    if (tickers[item].havePosition == True):
                        price, volume = getQuote(item, quotes)
                        if (tickers[item].direction == 'long'):
                            orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                            findOrder(item, candleTime, price, ORDERS)
                        elif (tickers[item].direction == 'short'):
                            orderQueue.append({item : {'action' : 'BUY_TO_COVER', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                            findOrder(item, candleTime, price, ORDERS)

                #write test results to respective JSON files
                writeTestResults(CALCULATED_EMAs, CANDLES, ORDERS, True)

                #stops the program from continuing
                canContinue = False

            #allow trades for stocks that haven't interacted with 20EMA yet
            if (time == '6:39:00' and not updatedCanTradeStatus): 
                updatedCanTradeStatus = True
                for item in tickers.keys():
                    tickers[item].canTrade = True
                    if (tickers[item].lastInteraction == '00:00'):
                        tickers[item].canUseEMAStrategy = True

            for item in tickers.keys():
                price, volume = getQuote(item, quotes)

                #calculates the size and profit target to use for the symbol
                size = 0
                profitTarget = 0
                if item in data.SMALL_POSITION:
                    size = data.SMALL_POSITION_SIZE
                    profitTarget = data.SMALL_POSITION_PT
                elif item in data.VERY_SMALL_POSITION:
                    size = data.VERY_SMALL_POSITION_SIZE
                    profitTarget = data.SMALL_POSITION_PT
                else:
                    size = data.LARGE_POSITION_SIZE
                    profitTarget = data.LARGE_POSITION_PT        
                
                #allows 00-second code to run after the 0th second has passed
                if (seconds != '00' and not tickers[item].canRun00SecondCode):
                    tickers[item].canRun00SecondCode = True
                    numberOfIncorrectPrices = 0

                if (condition): 
                    candle = Candle(item)
                    tickers[item].currentCandle = candle
                    tickers[item].currentCandle.openPrice = price
                    tickers[item].currentCandle.closePrice = price
                    tickers[item].currentCandle.low = price
                    tickers[item].currentCandle.high = price
                    tickers[item].currentCandle.volume = 0
                    tickers[item].currentCandle.time = candleTime 
                    #[test]
                    print("initialized first candle at: " + time)
                    #[test]

                #checks if profit target in a long position has been reached
                if (price >= tickers[item].profitTarget and tickers[item].havePosition == True and tickers[item].direction == 'long' and quoteServerError == False and tickers[item].useEMA5AsStop == False
                    and tickers[item].strategy != 'flat top breakout' and tickers[item].triggeredHardStop == False and False): #[test]
                    if (data.useEMAstop):
                        if (price >= tickers[item].EMA5):
                            tickers[item].useEMA5AsStop = True
                            #[test]
                            print(time + '\t' + 'profit target reached in ' + item + '. Using 5EMA as stop now')
                            #[test]
                        else:
                            orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                            findOrder(item, candleTime, price, ORDERS)
                            tickers[item].triggeredHardStop = True
                    else:
                        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                        findOrder(item, candleTime, price, ORDERS)
                        tickers[item].triggeredHardStop = True

                #checks if profit target in a short position has been reached
                elif (price <= tickers[item].profitTarget and tickers[item].havePosition == True and tickers[item].direction == 'short' and quoteServerError == False and tickers[item].useEMA5AsStop == False
                     and tickers[item].triggeredHardStop == False and False): #[test]
                    if (data.useEMAstop):
                        if (price <= tickers[item].EMA5):
                            tickers[item].useEMA5AsStop = True
                            #[test]
                            print(time + '\t' + 'profit target reached in ' + item + '. Using 5EMA as stop now')
                            #[test]
                        else:
                            orderQueue.append({item : {'action' : 'BUY_TO_COVER', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                            findOrder(item, candleTime, price, ORDERS)
                            tickers[item].triggeredHardStop = True
                    else:
                        orderQueue.append({item : {'action' : 'BUY_TO_COVER', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                        findOrder(item, candleTime, price, ORDERS)
                        tickers[item].triggeredHardStop = True

                #checks for stop in 'high tight flag' strategy when price has broken below breakout bar low
                if (price < tickers[item].breakoutBarLow and tickers[item].strategy == 'high tight flag' and tickers[item].havePosition == True and quoteServerError == False
                    and tickers[item].triggeredHardStop == False):

                    orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                    findOrder(item, candleTime, price, ORDERS)
                    tickers[item].numberOfDownBarsAfterBreakout = 0
                    tickers[item].triggeredHardStop = True

                    #[test]
                    print(time + '\t' + 'stop loss in ' + tickers[item].strategy)
                    #[test]

                #hard stop in reversal, oversold reversal, bullish 3-bar reversal, and bullish 25-cent reversal strategies if price is 4 cents below reversal bar low
                if (price <= tickers[item].breakoutBarLow - 0.04 and (tickers[item].strategy == 'reversal' or tickers[item].strategy == 'oversold reversal' or tickers[item].strategy == 'bullish 3-bar reversal' or tickers[item].strategy == 'bullish 25-cent reversal') and tickers[item].havePosition == True
                    and quoteServerError == False and tickers[item].triggeredHardStop == False):

                    orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                    findOrder(item, candleTime, price, ORDERS)
                    tickers[item].triggeredHardStop = True

                    #[test]
                    print('Triggered hard stop in reversal/oversold reversal strategy in ' + item + ' because of price 4 cents below reversal bar low')
                    #[test]

                #hard stop in reversal/oversold reversal strategy if price is 5 cents below 10EMA and the 10EMA is being used as a stop
                elif (price < round(tickers[item].EMA10, 2) - 0.05 and (tickers[item].strategy == 'reversal' or tickers[item].strategy == 'oversold reversal' or tickers[item].strategy == 'bullish 3-bar reversal' or tickers[item].strategy == 'bullish 25-cent reversal') and tickers[item].havePosition == True
                    and quoteServerError == False and tickers[item].triggeredHardStop == False and tickers[item].useEMA10AsStop == True and tickers[item].currentCandle.openPrice >= tickers[item].EMA10):

                    orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                    findOrder(item, candleTime, price, ORDERS)
                    tickers[item].triggeredHardStop = True
                    tickers[item].useEMA10AsStop = False

                    #[test]
                    print("Triggered hard stop in reversal/oversold/bullish 3-bar reversal strategy in " + item + " because of price 5 cents below 10EMA when 10EMA is used as a stop")
                    #[test]

                #hard stop in bearish 3-bar reversal and bearish 25-cent reversal strategies if price is 4 cents above reversal bar high
                if (price <= tickers[item].breakoutBarHigh + 0.04 and (tickers[item].strategy == 'bearish 3-bar reversal' or tickers[item].strategy == 'bearish 25-cent reversal') and tickers[item].havePosition == True
                    and quoteServerError == False and tickers[item].triggeredHardStop == False):

                    orderQueue.append({item : {'action' : 'BUY_TO_COVER', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                    findOrder(item, candleTime, price, ORDERS)
                    tickers[item].triggeredHardStop = True

                    #[test]
                    print('Triggered hard stop in bearish 3-bar/25-cent reversal strategy in ' + item + ' because of price 4 cents above reversal bar high')
                    #[test]

                #hard stop in bearish 3-bar reversal and bearish 25-cent reversal strategies if price is 5 cents above 10EMA and the 10EMA is being used as a stop
                elif (price > round(tickers[item].EMA10, 2) + 0.05 and (tickers[item].strategy == 'bearish 3-bar reversal' or tickers[item].strategy == 'bearish 25-cent reversal') and tickers[item].havePosition == True
                    and quoteServerError == False and tickers[item].triggeredHardStop == False and tickers[item].useEMA10AsStop == True and tickers[item].currentCandle.openPrice <= tickers[item].EMA10):

                    orderQueue.append({item : {'action' : 'BUY_TO_COVER', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                    findOrder(item, candleTime, price, ORDERS)
                    tickers[item].triggeredHardStop = True
                    tickers[item].useEMA10AsStop = False

                    #[test]
                    print("Triggered hard stop in bearish 3-bar/25-cent reversal strategy in " + item + " because of price 5 cents above 10EMA when 10EMA is used as a stop")
                    #[test]

                #hard stop in bullish EMA strategy if price is 5 cents below 10EMA
                if (price <= round(tickers[item].EMA10, 2) - 0.05 and (tickers[item].strategy == 'break above 20EMA' or tickers[item].strategy == 'bounce higher off 20EMA') and tickers[item].havePosition == True
                    and quoteServerError == False and tickers[item].triggeredHardStop == False and tickers[item].currentCandle.openPrice >= tickers[item].EMA10):

                    orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                    findOrder(item, candleTime, price, ORDERS)
                    tickers[item].triggeredHardStop = True

                    #[test]
                    print("Triggered hard stop in bullish EMA strategy in " + item + " because of price 5 cents below 10EMA")
                    #[test]

                #hard stop in bearish EMA strategy if price is 5 cents above 10EMA
                elif (price >= round(tickers[item].EMA10, 2) + 0.05 and (tickers[item].strategy == 'break below 20EMA' or tickers[item].strategy == 'bounce lower off 20EMA') and tickers[item].havePosition == True
                    and quoteServerError == False and tickers[item].triggeredHardStop == False and tickers[item].currentCandle.openPrice <= tickers[item].EMA10):

                    orderQueue.append({item : {'action' : 'BUY_TO_COVER', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                    findOrder(item, candleTime, price, ORDERS)
                    tickers[item].triggeredHardStop = True

                    #[test]
                    print("Triggered hard stop in bullish EMA strategy in " + item + " because of price 5 cents below 10EMA")
                    #[test]

                #hard stop in bullish EMA strategy if price is 5 cents below 10EMA
                elif (price <= round(tickers[item].EMA20, 2) - 0.05 and tickers[item].strategy == 'bounce higher off 20EMA' and tickers[item].havePosition == True
                    and quoteServerError == False and tickers[item].triggeredHardStop == False and tickers[item].currentCandle.openPrice >= tickers[item].EMA20):

                    orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                    findOrder(item, candleTime, price, ORDERS)
                    tickers[item].triggeredHardStop = True

                    #[test]
                    print("Triggered hard stop in bullish EMA strategy in " + item + " because of price 5 cents below 20EMA")
                    #[test]

                #hard stop in bearish EMA strategy if price is 5 cents above 10EMA
                elif (price >= round(tickers[item].EMA20, 2) + 0.05 and tickers[item].strategy == 'bounce lower off 20EMA' and tickers[item].havePosition == True
                    and quoteServerError == False and tickers[item].triggeredHardStop == False and tickers[item].currentCandle.openPrice <= tickers[item].EMA20):

                    orderQueue.append({item : {'action' : 'BUY_TO_COVER', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                    findOrder(item, candleTime, price, ORDERS)
                    tickers[item].triggeredHardStop = True

                    #[test]
                    print("Triggered hard stop in bullish EMA strategy in " + item + " because of price 5 cents below 20EMA")
                    #[test]

                #uncomment the following code when using morning breakout strategy
                '''
                #checks for 2% stop loss in morning breakout strategy
                if (tickers[item].strategy == 'morning breakout' and price < tickers[item].morningHigh * 0.98 and not tickers[item].useEMA50AsStop
                    and tickers[item].havePosition == True and quoteServerError == False):
                    
                    orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                    findOrder(item, candleTime, price, ORDERS)

                    #[test]
                    print(time + '\t' + 'stop loss in ' + tickers[item].strategy)
                    #[test]

                #checks for 1.62% profit target in morning breakout strategy
                if (tickers[item].strategy == 'morning breakout' and price > tickers[item].morningHigh * 1.0162 and tickers[item].havePosition == True and quoteServerError == False)

                    orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
                    findOrder(item, candleTime, price, ORDERS)

                    #[test]
                    print(time + '\t' + 'profit target in ' + tickers[item].strategy)
                    #[test]
                

                #checks when to raise stop to EMA50 for morning breakout strategy
                if (price * 0.98 < tickers[item].EMA50 and not tickers[item].useEMA50AsStop and tickers[item].strategy = 'morning breakout'):
                    tickers[item].useEMA50AsStop = True
                '''

                #checks for a new low price in the current candle
                if (price < tickers[item].currentCandle.low and item == tickers[item].currentCandle.symbol):
                    tickers[item].currentCandle.low = price

                #checks for a new high price in the current candle
                if (price > tickers[item].currentCandle.high and item == tickers[item].currentCandle.symbol):
                    tickers[item].currentCandle.high = price

                #uncomment the following code when using morning breakout strategy
                '''
                #checks for a new morning high
                if (item in morningBreakouts and price > tickers[item].morningHigh and time <= '6:50:00'):
                    tickers[item].morningHigh = price
                '''

                #checks for a new intraday high 
                if (price > tickers[item].highOfDay):
                    tickers[item].highOfDay = price

                #checks for a new intraday low
                if (price < tickers[item].lowOfDay):
                    tickers[item].lowOfDay = price

                #checks if the stock interacted with the 20EMA
                #checks if stock broke above 20EMA 
                if (round(tickers[item].EMA20, 2) >= tickers[item].currentCandle.openPrice):
                    if (tickers[item].currentCandle.high >= round(tickers[item].EMA20, 2) and time >= '6:31:00'):

                        tickers[item].lastInteraction = candleTime
                        tickers[item].interactedWithEMA = True 

                        
                        if (item in data.EMA_STRATEGY_TICKERS):
                            #[test]
                            if (tickers[item].canPrintInteractionStatus):
                                print(time + '\t' + item + ' broke above 20EMA')
                                print("The high price is: " + str(tickers[item].currentCandle.high))
                                print("The open price is: " + str(tickers[item].currentCandle.openPrice))
                                print("The 20EMA is: " + str(round(tickers[item].EMA20, 2)))
                                print("It has been " + str(tickers[item].minutesSinceLastInteraction) + " minutes since " + item + " interacted with 20EMA")
                                tickers[item].canPrintInteractionStatus = False
                            #[test]
                        
                        
                #checks if stock broke below 20EMA
                elif (round(tickers[item].EMA20, 2) <= tickers[item].currentCandle.openPrice):
                    if (tickers[item].currentCandle.low <= round(tickers[item].EMA20, 2) and time >= '6:31:00'):
                        
                        tickers[item].lastInteraction = candleTime 
                        tickers[item].interactedWithEMA = True 

                        if (tickers[item].withinFlatTopBreakoutPattern):
                            #immediate invalidation of flat-top-breakout pattern
                            tickers[item].withinFlatTopBreakoutPattern = False
                            tickers[item].closedBelow10EMA = False
                            tickers[item].sizeOfFlatTopBreakoutPattern = 0
                            tickers[item].prohibitedIntervals.append(tickers[item].intervalUnderConsideration)
                            tickers[item].firstCandleOfBase = False

                            #[test]
                            print("Flat top breakout in " + item + " invalidated because of break below 20EMA")
                            #[test]

                        
                        if (item in data.EMA_STRATEGY_TICKERS):
                            #[test]
                            if (tickers[item].canPrintInteractionStatus):
                                print(time + '\t' + item + ' broke below 20EMA')
                                print("The low price is: " + str(tickers[item].currentCandle.low))
                                print("The open price is: " + str(tickers[item].currentCandle.openPrice))
                                print("The 20EMA is: " + str(round(tickers[item].EMA20, 2)))
                                print("It has been " + str(tickers[item].minutesSinceLastInteraction) + " minutes since " + item + " interacted with 20EMA")
                                tickers[item].canPrintInteractionStatus = False
                            #[test]
                        
                        
                if (seconds == '00' and tickers[item].canRun00SecondCode):
                    #checks if it has been at least 15 minutes since the stock has interacted with the 20EMA
                    if (tickers[item].havePosition == False and (tickers[item].minutesSinceLastInteraction >= 14 
                        or (time == '6:39:00' and tickers[item].minutesSinceLastInteraction == 8)
                        or (time == '6:40:00' and tickers[item].minutesSinceLastInteraction == 9)
                        or (time == '6:41:00' and tickers[item].minutesSinceLastInteraction == 10)
                        or (time == '6:42:00' and tickers[item].minutesSinceLastInteraction == 11)
                        or (time == '6:43:00' and tickers[item].minutesSinceLastInteraction == 12)
                        or (time == '6:44:00' and tickers[item].minutesSinceLastInteraction == 13)
                        or (time == '6:45:00' and tickers[item].minutesSinceLastInteraction == 14)) #8 minutes because it comes before code to update at 00 seconds
                        and time <= '7:45:00'): 

                        tickers[item].canUseEMAStrategy = True

                    #either the position already exists or it has been fewer than 15 minutes since the last interaction with the 20EMA
                    else: 
                        tickers[item].canUseEMAStrategy = False

                    if (tickers[item].interactedWithEMA == False and time != '6:30:00'):
                        tickers[item].minutesSinceLastInteraction += 1
                    
                    tickers[item].canRun00SecondCode = False

                    #updates the trend for the ticker
                    tickers[item].determineTrend()  

                    #determines number of consecutive up or down bars for the ticker
                    tickers[item].determineNumberOfConsecutiveBars()

                    #determines number of consecutive bars below 10EMA and 20EMA
                    tickers[item].determineNumberOfBarsBelowEMAs()

                    #calculates the percentage of bars that are down bars, if the stock is in a downtrend
                    if (tickers[item].numberOfBarsBelowEMAs > 0):
                        tickers[item].calculatePercentageOfDownBarsInDowntrend()

                    #determines if the stock is in a sideways trend over the last 6 minutes
                    tickers[item].detectSidewaysTrend()

                    #finishes building candle for current minute and adds it to ticker's price history
                    if (time != '6:30:00'):

                        tickers[item].currentCandle.volume = volume - tickers[item].previousTotalVolume

                        #calculates the EMAs based on the closing price
                        tickers[item].calculateEMA(price)

                        #checks for quote server error
                        if (tickers[item].currentCandle.volume < 0):# and (item in data.EMA_STRATEGY_TICKERS)):
                            quoteServerError = True
                            print("NEGATIVE VOLUME FOR: " + item)
                            print("QUOTE SERVER ERROR - NEGATIVE VOLUME")

                        #checks for quote server error
                        if (tickers[item].currentCandle.high == lastClosingPrices[item]['close price'] or tickers[item].currentCandle.low == lastClosingPrices[item]['close price']):
                            numberOfIncorrectPrices += 1

                        #checks for quote server error
                        if (numberOfIncorrectPrices == len(data.AVAILABLE_TICKERS)):
                            quoteServerError = True
                            print("QUOTE SERVER ERROR - INCORRECT PRICES RETURNED FROM SERVER")

                        tickers[item].currentCandle.closePrice = price
                        tickers[item].previousTotalVolume = volume
                                           
                        #exits all existing positions if there is a quote server error
                        if (quoteServerError == True):
                            for symbol in positions.keys():
                                if (tickers[symbol].direction == 'short'):
                                    orderQueue.append({symbol : {'action' : 'BUY_TO_COVER', 'symbol' : symbol, 'size' : tickers[symbol].positionSize, 'price' : tickers[symbol].currentCandle.closePrice}})
                                elif (tickers[symbol].direction == 'long'):
                                    orderQueue.append({symbol : {'action' : 'SELL', 'symbol' : symbol, 'size' : tickers[symbol].positionSize, 'price' : tickers[symbol].currentCandle.closePrice}})
                                findOrder(symbol, candleTime, price, ORDERS)
                                print("Exited " + symbol + " because of quote server error")


                        #updates the EMAs for the ticker's current candle
                        tickers[item].currentCandle.EMA5 = round(tickers[item].EMA5, 2)
                        tickers[item].currentCandle.EMA10 = round(tickers[item].EMA10, 2)
                        tickers[item].currentCandle.EMA20 = round(tickers[item].EMA20, 2)

                        #adds calculated EMAs to dictionary
                        CALCULATED_EMAs[item].append({tickers[item].currentCandle.time : {'5EMA' : round(tickers[item].EMA5, 2), '10EMA' : round(tickers[item].EMA10, 2), '20EMA' : round(tickers[item].EMA20, 2)}})
                        #adds current candle to dictionary
                        CANDLES[item].append({tickers[item].currentCandle.time : {'open' : tickers[item].currentCandle.openPrice, 'close' : tickers[item].currentCandle.closePrice, 'high' : tickers[item].currentCandle.high, 
                                                            'low' : tickers[item].currentCandle.low, 'volume' : tickers[item].currentCandle.volume, 'EMA5' : tickers[item].currentCandle.EMA5,
                                                            'EMA10' : tickers[item].currentCandle.EMA10, 'EMA20' : tickers[item].currentCandle.EMA20}})

                        #writes test results to respective JSON files
                        writeTestResults(CALCULATED_EMAs, CANDLES, ORDERS, False)

                        #updates the price history of the ticker
                        if (len(tickers[item].priceHistory) == 20):
                            tickers[item].priceHistory.pop(0)
                            tickers[item].priceHistory.append(tickers[item].currentCandle)
                        else:
                            tickers[item].priceHistory.append(tickers[item].currentCandle)

                        #checks for a valid flat-top-breakout pattern
                        checkForValidBase(tickers, item, time)

                    #determines if the current bar is a down bar after a breakout from a high tight flag
                    if (tickers[item].currentCandle.closePrice <= tickers[item].currentCandle.openPrice and tickers[item].strategy == 'high tight flag'):
                        tickers[item].numberOfDownBarsAfterBreakout += 1
                    
                    #only can consider trades after 6:39
                    #checks for entry points for trading strategies or stop loss points
                    if (time >= '6:39:00' and quoteServerError == False): 
                        #checks if the conditions for the EMA strategy were met, thereby preventing multiple strategies from triggering 
                        #for the same symbol at the same time
                        conditionsForEMAStrategyMet = False
                        conditionsForHighTightFlagMet = False

                        #prevents trades if the average candle size is too large
                        tickers[item].calculateAverageRange()
                        if (tickers[item].averageRange > 20):
                            #[test]
                            if (tickers[item].canTrade == True):
                                print("Prevented trades in " + item + " because the average candle range is too high")
                            #[test]
                            tickers[item].canTrade = False

                        if (data.tradeEMAStrategy):
                            if (item in data.EMA_STRATEGY_TICKERS):
                                conditionsForEMAStrategyMet = checkForEMAStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime)
                        
                        if (data.tradeReversalStrategy and not conditionsForEMAStrategyMet):
                            if (item in data.REVERSAL_STRATEGY_TICKERS):
                                checkForReversalStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime)
                        
                        if (data.tradeHighTightFlagStrategy):
                            if (item in data.HIGH_TIGHT_FLAG_STRATEGY_TICKERS):
                                conditionsForHighTightFlagMet = checkForHighTightFlagStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime)
                        
                        if (data.tradeFlatTopBreakoutStrategy and not conditionsForHighTightFlagMet):
                            if (item in data.FLAT_TOP_BREAKOUT_TICKERS):
                                checkForFlatTopBreakoutStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime)

                        oversoldReversalConditionsMet = False
                        bullish3BarReversalConditionsMet = False
                        bearish3BarReversalConditionsMet = False

                        if (data.tradeOversoldReversalStrategy):
                            oversoldReversalConditionsMet = checkForOversoldReversalStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime)
                        if (data.trade3BarReversalStrategy and not oversoldReversalConditionsMet):
                            bullish3BarReversalConditionsMet = checkForBullish3BarReversalStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime)
                            bearish3BarReversalConditionsMet = checkForBearish3BarReversalStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime)
                        if (data.trade25CentReversalStrategy):
                            if (not bullish3BarReversalConditionsMet):
                                checkForBullishReversalOff25CentIntervalStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime)
                            if (not (bearish3BarReversalConditionsMet or oversoldReversalConditionsMet)):
                                checkForBearishReversalOff25CentIntervalStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime)
                       
                       #uncomment the following code when using morning breakout strategy
                        '''
                        if (data.tradeMorningBreakoutStrategy and (item in morningBreakouts)):
                            checkForFlatTopBreakoutStrategy(tickers, item, orderQueue, ORDERS, price, time, currentInvested, DTBP, candleTime)
                        '''

                    #determines whether to use the 10EMA as the stop loss point for reversal strategy
                    if (tickers[item].strategy == 'reversal' and tickers[item].currentCandle.closePrice >= round(tickers[item].EMA10, 2)):
                        tickers[item].useEMA10AsStop = True

                    #determines whether to use the 10EMA as the stop loss point for oversold reversal, bullish 3-bar reversal, and bullish 25-cent reversal strategies
                    if ((tickers[item].strategy == 'oversold reversal' or tickers[item].strategy == 'bullish 3-bar reversal' or tickers[item].strategy == 'bullish 25-cent reversal') and tickers[item].currentCandle.closePrice > round(tickers[item].EMA20, 2)):
                        tickers[item].useEMA10AsStop = True

                    #determines whether to use the 10EMA as the stop loss point for bearish 3-bar reversal and bearish 25-cent reversal strategies
                    if ((tickers[item].strategy == 'bearish 3-bar reversal' or tickers[item].strategy == 'bearish 25-cent reversal') and tickers[item].currentCandle.closePrice < round(tickers[item].EMA20, 2)):
                        tickers[item].useEMA10AsStop = True

                    #checks for stop losses
                    checkForStopLoss(tickers, item, orderQueue, ORDERS, price, time, candleTime, quoteServerError)

                    #resets time elapsed since last interaction with EMA if stock interacted with EMA the prior minute
                    if (tickers[item].interactedWithEMA == True):
                        tickers[item].minutesSinceLastInteraction = 0
                        tickers[item].interactedWithEMA = False

                    #initialize the current candle of the ticker
                    if (time >= '6:31:00'):    
                        candle = Candle(item)
                        tickers[item].currentCandle = candle
                        tickers[item].currentCandle.openPrice = price
                        tickers[item].currentCandle.closePrice = price
                        tickers[item].currentCandle.low = price
                        tickers[item].currentCandle.high = price
                        tickers[item].currentCandle.volume = 0
                        tickers[item].currentCandle.time = candleTime 
                        tickers[item].canRun00SecondCode = False
                        tickers[item].canPrintInteractionStatus = True

            condition = False

            #place all orders at one time
            if (len(orderQueue) != 0):
                for i in range(len(orderQueue)):
                    item = ''
                    action = ''
                    size = 0
                    price = 0
                    profitTarget = 0
                    for index in orderQueue[i].keys():
                        item = orderQueue[i][index]['symbol']
                        action = orderQueue[i][index]['action']
                        size = orderQueue[i][index]['size']
                        price = orderQueue[i][index]['price']

                    #places order if user allows it
                    if (data.canPlaceOrders):
                        placeOrder(action, item, size)

                    if (action == 'SELL' or action == 'BUY_TO_COVER'):
                        currentInvested -= positions[item]
                        del positions[item]

                        #update ticker info
                        tickers[item].positionSize = 0
                        tickers[item].havePosition = False
                        tickers[item].direction = "none"
                        tickers[item].strategy = ''
                        tickers[item].positionSize = 0
                        tickers[item].useEMA10AsStop = False
                        tickers[item].useEMA5AsStop = False
                        tickers[item].stopLossInterval = 0
                        tickers[item].nextInterval = 0
                        tickers[item].triggeredHardStop = False

                        #[test]
                        print('time: ' + time + '\t' + item + '\t' + action + '\t' + 'price: ' + str(price) + '\t' + 'size: ' + str(size) + '\t' + 'strategy: ' + tickers[item].strategy)
                        print('the current positions are: ')
                        print(positions)
                        print("The current amount invested is: " + str(currentInvested))
                        #[test]

                    elif (action == 'BUY' or action == 'SELL_SHORT'):
                        positions[item] = (price * size)
                        currentInvested += (price * size)

                        if (item in data.SMALL_POSITION):
                            profitTarget = data.SMALL_POSITION_PT
                        elif (item in data.LARGE_POSITION):
                            profitTarget = data.LARGE_POSITION_PT

                        tickers[item].positionSize = size
                        tickers[item].havePosition = True

                        if (action == 'BUY'):
                            tickers[item].profitTarget = price + profitTarget
                        elif (action == 'SELL_SHORT'):
                            tickers[item].profitTarget = price - profitTarget

                        #[test]
                        print('time: ' + time + '\t' + item + '\t' + action + '\t' + 'price: ' + str(price) + '\t' + 'size: ' + str(tickers[item].positionSize) + '\t' + 'strategy: ' + tickers[item].strategy)
                        print('the profit target for ' + item + ' is ' + str(tickers[item].profitTarget))
                        print('the current positions are: ')
                        print(positions)
                        print("The current amount invested is: " + str(currentInvested))
                        #[test]

            orderQueue = []

            #exits program if there is a quote server error
            if (quoteServerError == True):
                canContinue = False
                print("QUOTE SERVER ERROR DETECTED - PROGRAM STOPPED")

def test():
    token = getAccessToken()
    scanForMorningBreakouts()

if __name__ == '__main__':
    main()
    #test()
