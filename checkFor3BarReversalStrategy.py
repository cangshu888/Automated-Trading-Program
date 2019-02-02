from classes import Order

def checkLowOfDay(tickers, item, direction):
    stock = tickers[item]
    
    if (direction == "bullish"):
        if (stock.priceHistory[-2].low == stock.lowOfDay or stock.priceHistory[-3].low == stock.lowOfDay or stock.priceHistory[-1].low == stock.lowOfDay):
            return True
        else:
            return False
    elif (direction == "bearish"):
        if (stock.priceHistory[-2].high == stock.highOfDay or stock.priceHistory[-3].high == stock.highOfDay or stock.priceHistory[-1].high == stock.highOfDay):
            return True
        else:
            return False
    else:
        #[test]
        print("invalid direction in checkLowOfDay()")
        #[test]

def checkTrend(tickers, item, direction):
    stock = tickers[item]

    if (direction == "bullish"):
        if (stock.trend == "downtrend"):
            return True
        else:
            return False
    elif (direction == "bearish"):
        if (stock.trend == "uptrend"):
            return True
        else: 
            return False
    else:
        #[test]
        print("invalid direction in checkTrend()")
        #[test]

def checkLastTwoBars(tickers, item, direction):
    stock = tickers[item]

    if (direction == "bullish"):
        if (not(stock.priceHistory[-2].closePrice < stock.priceHistory[-2].EMA5 and stock.priceHistory[-3].closePrice < stock.priceHistory[-3].EMA5)):
            return False
        if (not(stock.priceHistory[-2].closePrice < stock.priceHistory[-2].openPrice and stock.priceHistory[-3].closePrice < stock.priceHistory[-3].openPrice)):
            return False
    elif (direction == "bearish"):
        if (not(stock.priceHistory[-2].closePrice > stock.priceHistory[-2].EMA5 and stock.priceHistory[-3].closePrice > stock.priceHistory[-3].EMA5)):
            return False
        if (not(stock.priceHistory[-2].closePrice > stock.priceHistory[-2].openPrice and stock.priceHistory[-3].closePrice > stock.priceHistory[-3].openPrice)):
            return False
    else:
        #[test]
        print("invalid direction in checkLastTwoBars()")
        #[test]

    return True

def checkReversalBar(tickers, item, direction):
    stock = tickers[item]

    #check volume of reversal bar
    if (not(stock.priceHistory[-1].volume > stock.priceHistory[-2].volume)):
        return False

    #check range of reversal bar
    if (not((stock.priceHistory[-1].high - stock.priceHistory[-1].low)) > (stock.priceHistory[-2].high - stock.priceHistory[-2].low)):
        return False

    if (direction == "bullish"):
        #check for close above pattern high
        if (not(stock.priceHistory[-1].closePrice > stock.priceHistory[-2].high and stock.priceHistory[-1].closePrice > stock.priceHistory[-3].high)):
            return False

        #check for close above 5EMA
        if (not(stock.priceHistory[-1].closePrice > stock.priceHistory[-1].EMA5)):
            return False

        #checks if reversal bar is up bar
        if (stock.priceHistory[-1].closePrice <= stock.priceHistory[-1].openPrice):
            return False

        #checks if reversal bar does not have long top tail
        if ((stock.priceHistory[-1].high - stock.priceHistory[-1].closePrice) > 0.25 * (stock.priceHistory[-1].high - stock.priceHistory[-1].low)):
            return False

    elif (direction == "bearish"):
        #check for close below pattern low
        if (not(stock.priceHistory[-1].closePrice < stock.priceHistory[-2].low and stock.priceHistory[-1].closePrice < stock.priceHistory[-3].low)):
            return False

        #check for close below 5EMA
        if (not(stock.priceHistory[-1].closePrice < stock.priceHistory[-1].EMA5)):
            return False

        #checks if reversal bar is down bar
        if (stock.priceHistory[-1].closePrice >= stock.priceHistory[-1].openPrice):
            return False

        #checks if reversal bar does not have long bottom tail
        if ((stock.priceHistory[-1].openPrice - stock.priceHistory[-1].low) > 0.25 * (stock.priceHistory[-1].high - stock.priceHistory[-1].low)):
            return False

    return True


def checkForBullish3BarReversalStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime):
    #checks for 'bullish 3-bar reversal' strategy
    if (checkLowOfDay(tickers, item, 'bullish') and checkTrend(tickers, item, 'bullish') and checkLastTwoBars(tickers, item, 'bullish') and checkReversalBar(tickers, item, 'bullish')
        and tickers[item].percentageOfDownBarsInDowntrend >= 50 and tickers[item].canTrade == True and tickers[item].havePosition == False):

        #[test]
        print(time + '\t' + 'bullish 3-bar reversal in' + item)
        #[test]

        #checks if DTBP is exceeded
        if (currentInvested + (price * size) < DTBP - 1000):

            print('DTBP not exceeded')

            #[test]
            orderQueue.append({item : {'action' : 'BUY', 'symbol' : item, 'size' : size, 'price' : price}})

            #update ticker info
            tickers[item].direction = "long"
            tickers[item].strategy = 'bullish 3-bar reversal'
            tickers[item].breakoutBarLow = tickers[item].priceHistory[-2].low
            #add order to list
            order = Order(item, candleTime, price, 'bullish 3-bar reversal', size, 'long')
            ORDERS.append(order)

            return True
        #use smaller position size if DTBP would otherwise be exceeded
        elif ((DTBP - 1000 - currentInvested) / price >= 300):
            #[test]
            print('Using smaller size')
            #[test]

            smallerSize = DTBP - 1000 - currentInvested / price

            #[test]
            orderQueue.append({item : {'action' : 'BUY', 'symbol' : item, 'size' : smallerSize, 'price' : price}})

            #update ticker info
            tickers[item].direction = "long"
            tickers[item].strategy = 'bullish 3-bar reversal'
            tickers[item].breakoutBarLow = tickers[item].priceHistory[-2].low
            #add order to list
            order = Order(item, candleTime, price, 'bullish 3-bar reversal', smallerSize, 'long')
            ORDERS.append(order)
            
            return True
    else:
        return False
def checkForBearish3BarReversalStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime):
    #checks for 'bullish 3-bar reversal' strategy
    if (checkLowOfDay(tickers, item, 'bearish') and checkTrend(tickers, item, 'bearish') and checkLastTwoBars(tickers, item, 'bearish') and checkReversalBar(tickers, item, 'bearish')
        and tickers[item].canTrade == True and tickers[item].havePosition == False):

        #[test]
        print(time + '\t' + 'bearish 3-bar reversal in' + item)
        #[test]

        #checks if DTBP is exceeded
        if (currentInvested + (price * size) < DTBP - 1000):

            print('DTBP not exceeded')

            #[test]
            orderQueue.append({item : {'action' : 'SELL_SHORT', 'symbol' : item, 'size' : size, 'price' : price}})

            #update ticker info
            tickers[item].direction = "short"
            tickers[item].strategy = 'bearish 3-bar reversal'
            tickers[item].breakoutBarHigh = tickers[item].priceHistory[-2].high
            #add order to list
            order = Order(item, candleTime, price, 'bearish 3-bar reversal', size, 'short')
            ORDERS.append(order)

            return True

        #use smaller position size if DTBP would otherwise be exceeded
        elif ((DTBP - 1000 - currentInvested) / price >= 300):
            #[test]
            print('Using smaller size')
            #[test]

            smallerSize = DTBP - 1000 - currentInvested / price

            #[test]
            orderQueue.append({item : {'action' : 'SELL_SHORT', 'symbol' : item, 'size' : smallerSize, 'price' : price}})

            #update ticker info
            tickers[item].direction = "short"
            tickers[item].strategy = 'bearish 3-bar reversal'
            tickers[item].breakoutBarHigh = tickers[item].priceHistory[-2].high
            #add order to list
            order = Order(item, candleTime, price, 'bearish 3-bar reversal', smallerSize, 'short')
            ORDERS.append(order)

            return True
    else:
        return False