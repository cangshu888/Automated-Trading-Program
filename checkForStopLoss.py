#finds the order by symbol and edits the order object
def findOrder(symbol, exitTime, exitPrice, ORDERS):
    for i in range(len(ORDERS)):
        if (ORDERS[i].symbol == symbol and ORDERS[i].exitPrice == 0):
            ORDERS[i].exit(exitTime, exitPrice)
            break

def checkForStopLoss(tickers, item, orderQueue, ORDERS, price, time, candleTime, quoteServerError):
    #checks for stop in bounce higher off 20EMA
    if (tickers[item].currentCandle.closePrice < round(tickers[item].EMA20, 2) and tickers[item].havePosition == True 
        and tickers[item].direction == 'long' and tickers[item].strategy == 'bounce higher off 20EMA' and quoteServerError == False
        and tickers[item].triggeredHardStop == False):
        
        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)

        #[test]
        print(time + '\t' + 'stop loss in ' + tickers[item].strategy)
        #[test]

    #checks for stop in bounce lower off 20EMA
    elif (tickers[item].currentCandle.closePrice > round(tickers[item].EMA20, 2) and tickers[item].havePosition == True 
            and tickers[item].direction == 'short' and tickers[item].strategy == 'bounce lower off 20EMA' and quoteServerError == False
            and tickers[item].triggeredHardStop == False):
        
        orderQueue.append({item : {'action' : 'BUY_TO_COVER', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)

        #[test]
        print(time + '\t' + 'stop loss in ' + tickers[item].strategy)
        #[test]

    #checks for stop in break below 20EMA
    elif (tickers[item].currentCandle.closePrice > round(tickers[item].EMA10, 2) and tickers[item].havePosition == True 
            and tickers[item].direction == 'short' and tickers[item].strategy == 'break below 20EMA' and quoteServerError == False
            and tickers[item].triggeredHardStop == False):
        
        orderQueue.append({item : {'action' : 'BUY_TO_COVER', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)

        #[test]
        print(time + '\t' + 'stop loss in ' + tickers[item].strategy)
        #[test]

    #checks for stop in break above 20EMA
    elif (tickers[item].currentCandle.closePrice < round(tickers[item].EMA10, 2) and tickers[item].havePosition == True 
            and tickers[item].direction == 'long' and tickers[item].strategy == 'break above 20EMA' and quoteServerError == False
            and tickers[item].triggeredHardStop == False):
        
        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)

        #[test]
        print(time + '\t' + 'stop loss in ' + tickers[item].strategy)
        #[test]

    #checks for stop in 'reversal' strategy when price hasn't broken above 10EMA
    elif (tickers[item].currentCandle.closePrice < tickers[item].breakoutBarLow and tickers[item].useEMA10AsStop == False and tickers[item].strategy == 'reversal'
        and tickers[item].havePosition == True and tickers[item].direction == 'long' and quoteServerError == False
        and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)

        #[test]
        print(time + '\t' + 'stop loss in ' + tickers[item].strategy)
        #[test]

    #checks for stop in 'reversal' strategy when price has broken above 10EMA
    elif (tickers[item].currentCandle.closePrice < round(tickers[item].EMA10, 2) and tickers[item].useEMA10AsStop == True and tickers[item].strategy == 'reversal'
        and tickers[item].havePosition == True and tickers[item].direction == 'long' and quoteServerError == False
        and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)
        tickers[item].useEMA10AsStop = False

        #[test]
        print(time + '\t' + 'stop loss in ' + tickers[item].strategy)
        #[test]

    #checks for stop in 'high tight flag' strategy when there have been 2 down bars after the breakout
    elif (tickers[item].numberOfDownBarsAfterBreakout == 2 and tickers[item].strategy == 'high tight flag' and tickers[item].havePosition == True and quoteServerError == False
            and tickers[item].useEMA5AsStop == False
            and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)
        tickers[item].numberOfDownBarsAfterBreakout = 0

        #[test]
        print(time + '\t' + 'stop loss in ' + tickers[item].strategy)
        #[test]

    #checks for stop at 5EMA in long position
    elif (tickers[item].currentCandle.closePrice < round(tickers[item].EMA5, 2) and tickers[item].useEMA5AsStop == True
        and tickers[item].havePosition == True and quoteServerError == False and tickers[item].direction == 'long'
        and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})

        findOrder(item, candleTime, price, ORDERS)
        tickers[item].useEMA5AsStop = False

        #[test]
        print(time + '\t' + '5EMA stop in ' + tickers[item].strategy)
        #[test]

    #checks for stop at 5EMA in short position
    elif (tickers[item].currentCandle.closePrice > round(tickers[item].EMA5, 2) and tickers[item].useEMA5AsStop == True
        and tickers[item].havePosition == True and quoteServerError == False and tickers[item].direction == 'short'
        and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'BUY_TO_COVER', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})

        findOrder(item, candleTime, price, ORDERS)
        tickers[item].useEMA5AsStop = False

        #[test]
        print(time + '\t' + '5EMA stop in ' + tickers[item].strategy)
        #[test]
    #check for 10EMA stop in flat-top-breakout strategy
    elif (tickers[item].currentCandle.closePrice < round(tickers[item].EMA10, 2) and tickers[item].strategy == 'flat top breakout'
        and tickers[item].havePosition == True and quoteServerError == False
        and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)

        #[test]
        print(time + '\t' + '10EMA stop loss in ' + tickers[item].strategy + ' for ' + item)
        #[test]
    #check for close below stop loss interval in flat-top-breakout strategy
    elif (tickers[item].currentCandle.closePrice < tickers[item].stopLossInterval and tickers[item].strategy == 'flat top breakout'
        and tickers[item].havePosition == True and quoteServerError == False
        and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)

        #[test]
        print(time + '\t' + 'close below stop loss interval in ' + tickers[item].strategy + ' for ' + item)
        #[test]
    #check for top tail above next interval and close below in flat-top-breakout strategy
    elif (tickers[item].currentCandle.closePrice < tickers[item].nextInterval and tickers[item].currentCandle.high > tickers[item].nextInterval 
        and tickers[item].strategy == 'flat top breakout' and tickers[item].havePosition == True and quoteServerError == False
        and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)

        #[test]
        print(time + '\t' + 'top tail above next interval and close below in ' + tickers[item].strategy + ' for ' + item)
        #[test]
    #check for top tail within 2 cents of next interval and close down in flat-top-breakout strategy
    elif ((tickers[item].currentCandle.high == tickers[item].nextInterval - 0.02 or tickers[item].currentCandle.high == tickers[item].nextInterval - 0.01 or tickers[item].currentCandle.high == tickers[item].nextInterval)
        and tickers[item].currentCandle.closePrice <= tickers[item].currentCandle.openPrice 
        and tickers[item].strategy == 'flat top breakout' and tickers[item].havePosition == True and quoteServerError == False
        and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)

        #[test]
        print(time + '\t' + 'top tail within 2 cents of next interval and close down in ' + tickers[item].strategy + ' for ' + item)
        #[test]
    #check for top tail within 2 cents of next interval and close at bottom of range in flat-top-breakout strategy
    elif ((tickers[item].currentCandle.high == tickers[item].nextInterval - 0.02 or tickers[item].currentCandle.high == tickers[item].nextInterval - 0.01 or tickers[item].currentCandle.high == tickers[item].nextInterval)
        and (tickers[item].currentCandle.high - tickers[item].currentCandle.openPrice) >= 0.5 * (tickers[item].currentCandle.high - tickers[item].currentCandle.low) 
        and tickers[item].strategy == 'flat top breakout' and tickers[item].havePosition == True and quoteServerError == False
        and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)

        #[test]
        print(time + '\t' + 'top tail within 2 cents of next interval and close at bottom of range in ' + tickers[item].strategy + ' for ' + item)
        #[test]
    #check for EMA50 stop in morning breakout strategy
    elif (tickers[item].currentCandle.closePrice < round(tickers[item].EMA50, 2) and tickers[item].strategy == 'morning breakout'
        and tickers[item].havePosition == True and quoteServerError == False and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)

        #[test]
        print(time + '\t' + 'stop loss in ' + tickers[item].strategy)
        #[test]
    #checks for stop in 'oversold reversal', 'bullish 3-bar reversal', and bullish 25-cent reversal strategies when stock hasn't broken above 20EMA
    elif (tickers[item].currentCandle.closePrice < tickers[item].breakoutBarLow and tickers[item].useEMA10AsStop == False and (tickers[item].strategy == 'oversold reversal' or tickers[item].strategy == 'bullish 3-bar reversal' or tickers[item].strategy == 'bullish 25-cent reversal')
        and tickers[item].havePosition == True and tickers[item].direction == 'long' and quoteServerError == False
        and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)

        #[test]
        print(time + '\t' + 'stop loss in ' + tickers[item].strategy + ' before breaking above 20EMA')
        #[test]

    #checks for stop in 'oversold reversal', 'bullish 3-bar reversal', and bullish 25-cent reversal strategies when price has broken above 20EMA
    elif (tickers[item].currentCandle.closePrice < round(tickers[item].EMA10, 2) and tickers[item].useEMA10AsStop == True and (tickers[item].strategy == 'oversold reversal' or tickers[item].strategy == 'bullish 3-bar reversal' or tickers[item].strategy == 'bullish 25-cent reversal')
        and tickers[item].havePosition == True and tickers[item].direction == 'long' and quoteServerError == False
        and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'SELL', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)
        tickers[item].useEMA10AsStop = False

        #[test]
        print(time + '\t' + 'stop loss in ' + tickers[item].strategy + ' after break above 20EMA')
        #[test]
    #checks for stop in 'bearish 3-bar reversal' and bearish 25-cent reversal strategies when stock hasn't broken above 20EMA
    elif (tickers[item].currentCandle.closePrice > tickers[item].breakoutBarHigh and tickers[item].useEMA10AsStop == False and (tickers[item].strategy == 'bearish 3-bar reversal' or tickers[item].strategy == 'bearish 25-cent reversal')
        and tickers[item].havePosition == True and tickers[item].direction == 'short' and quoteServerError == False
        and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'BUY_TO_COVER', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)

        #[test]
        print(time + '\t' + 'stop loss in ' + tickers[item].strategy + ' before breaking above 20EMA')
        #[test]
    #checks for stop in 'bearish 3-bar reversal' and bearish 25-cent reversal strategies when price has broken above 20EMA
    elif (tickers[item].currentCandle.closePrice > round(tickers[item].EMA10, 2) and tickers[item].useEMA10AsStop == True and (tickers[item].strategy == 'bearish 3-bar reversal' or tickers[item].strategy == 'bearish 25-cent reversal')
        and tickers[item].havePosition == True and tickers[item].direction == 'short' and quoteServerError == False
        and tickers[item].triggeredHardStop == False):

        orderQueue.append({item : {'action' : 'BUY_TO_COVER', 'symbol' : item, 'size' : tickers[item].positionSize, 'price' : price}})
        findOrder(item, candleTime, price, ORDERS)
        tickers[item].useEMA10AsStop = False

        #[test]
        print(time + '\t' + 'stop loss in ' + tickers[item].strategy + ' after break above 20EMA')
        #[test]
    