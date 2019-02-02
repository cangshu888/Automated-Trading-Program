from classes import Order

def checkDistanceFromInterval(tickers, item, direction):
    stock = tickers[item]
    lowOfDayDigits = (round(stock.lowOfDay, 2) * 100) % 100
    reversalBarLowDigits = (round(stock.priceHistory[-1].low, 2) * 100) % 100
    highOfDayDigits = (round(stock.highOfDay, 2) * 100) % 100
    reversalBarHighDigits = (round(stock.priceHistory[-1].high, 2) * 100) % 100

    #[test]
    print("checkDistanceFromInterval() in " + item + "; the low of day is " + str(stock.lowOfDay) + "; the high of day is " + str(stock.highOfDay))
    print("high of day digits: " + str(highOfDayDigits))
    print("reversal bar high digits: " + str(reversalBarHighDigits))
    print("low of day digits: " + str(lowOfDayDigits))
    print("reversal bar low digits: " + str(reversalBarLowDigits))
    #[test]


    if (direction == 'bullish'):
        #25-cent mark
        if ((lowOfDayDigits == 22 or lowOfDayDigits == 23 or lowOfDayDigits == 24 or lowOfDayDigits == 25 or lowOfDayDigits == 26)
            and (reversalBarLowDigits == 24 or reversalBarLowDigits == 25 or reversalBarLowDigits == 26)):
            #[test]
            print("low at 25-cent mark in " + item)
            #[test]
            return True
        #50-cent mark
        if ((lowOfDayDigits == 47 or lowOfDayDigits == 48 or lowOfDayDigits == 49 or lowOfDayDigits == 50 or lowOfDayDigits == 51)
            and (reversalBarLowDigits == 49 or reversalBarLowDigits == 50 or reversalBarLowDigits == 51)):
            #[test]
            print("low at 50-cent mark in " + item)
            #[test]
            return True
        #75-cent mark
        if ((lowOfDayDigits == 72 or lowOfDayDigits == 73 or lowOfDayDigits == 74 or lowOfDayDigits == 75 or lowOfDayDigits == 76)
            and (reversalBarLowDigits == 74 or reversalBarLowDigits == 75 or reversalBarLowDigits == 76)):
            #[test]
            print("low at 75-cent mark in " + item)
            #[test]
            return True
        #dollar mark
        if ((lowOfDayDigits == 97 or lowOfDayDigits == 98 or lowOfDayDigits == 99 or lowOfDayDigits == 0 or lowOfDayDigits == 1)
            and (reversalBarLowDigits == 99 or reversalBarLowDigits == 0 or reversalBarLowDigits == 1)):
            #[test]
            print("low at dollar mark in " + item)
            #[test]
            return True
    elif (direction == 'bearish'):
        #25-cent mark
        if ((highOfDayDigits == 22 or highOfDayDigits == 23 or highOfDayDigits == 24 or highOfDayDigits == 25 or highOfDayDigits == 26)
            and (reversalBarHighDigits == 24 or reversalBarHighDigits == 25 or reversalBarHighDigits == 26)):
            #[test]
            print("high at 25-cent mark in " + item)
            #[test]
            return True
        #50-cent mark
        if ((highOfDayDigits == 47 or highOfDayDigits == 48 or highOfDayDigits == 49 or highOfDayDigits == 50 or highOfDayDigits == 51)
            and (reversalBarHighDigits == 49 or reversalBarHighDigits == 50 or reversalBarHighDigits == 51)):
            #[test]
            print("high at 50-cent mark in " + item)
            #[test]
            return True
        #75-cent mark
        if ((highOfDayDigits == 72 or highOfDayDigits == 73 or highOfDayDigits == 74 or highOfDayDigits == 75 or highOfDayDigits == 76)
            and (reversalBarHighDigits == 74 or reversalBarHighDigits == 75 or reversalBarHighDigits == 76)):
            #[test]
            print("high at 75-cent mark in " + item)
            #[test]
            return True
        #dollar mark
        if ((highOfDayDigits == 97 or highOfDayDigits == 98 or highOfDayDigits == 99 or highOfDayDigits == 0 or highOfDayDigits == 1)
            and (reversalBarHighDigits == 99 or reversalBarHighDigits == 0 or reversalBarHighDigits == 1)):
            #[test]
            print("high at dollar mark in " + item)
            #[test]
            return True
    else:
        #[test]
        print("invalid direction in checkDistanceFromInterval()")
        #[test]

    return False

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

def checkPriorBar(tickers, item, direction):
    stock = tickers[item]

    if (direction == "bullish"):
        if (not(stock.priceHistory[-2].closePrice < stock.priceHistory[-2].openPrice and stock.priceHistory[-2].openPrice <= stock.priceHistory[-2].EMA5 + 0.01)):
            return False
    elif (direction == "bearish"):
        if (not(stock.priceHistory[-2].closePrice > stock.priceHistory[-2].openPrice and stock.priceHistory[-2].openPrice >= stock.priceHistory[-2].EMA5 - 0.01)):
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
        #[test]
        print("lower volume on reversal bar")
        #[test]
        return False

    #check range of reversal bar
    if (not((stock.priceHistory[-1].high - stock.priceHistory[-1].low)) > (0.8 * (stock.priceHistory[-2].high - stock.priceHistory[-2].low))):
        #[test]
        print("lower range on reversal bar")
        #[test]
        return False

    if (direction == "bullish"):
        #check for close above prior bar high
        if (not(stock.priceHistory[-1].closePrice > stock.priceHistory[-2].high)):
            #[test]
            print("closed below prior bar high in potential bullish reversal")
            #[test]
            return False

        #check for close above 5EMA
        if (not(stock.priceHistory[-1].closePrice > stock.priceHistory[-1].EMA5)):
            #[test]
            print("closed below 5EMA in potential bullish reversal")
            #[test]
            return False

        #checks if reversal bar is up bar
        if (stock.priceHistory[-1].closePrice <= stock.priceHistory[-1].openPrice):
            #[test]
            print("reversal bar not up bar in potential bullish reversal")
            #[test]
            return False

        #checks if reversal bar does not have long top tail
        if ((stock.priceHistory[-1].high - stock.priceHistory[-1].closePrice) > (0.4 * (stock.priceHistory[-1].high - stock.priceHistory[-1].low))):
            #[test]
            print("reversal bar has long top tail in potential bullish reversal")
            #[test]
            return False

    elif (direction == "bearish"):
        #check for close below pattern low
        if (not(stock.priceHistory[-1].closePrice < stock.priceHistory[-2].low)):
            #[test]
            print("did not close below pattern low in potential bearish reversal")
            #[test]
            return False

        #check for close below 5EMA
        if (not(stock.priceHistory[-1].closePrice < stock.priceHistory[-1].EMA5)):
            #[test]
            print("did not close below 5EMA in potential bearish reversal")
            #[test]
            return False

        #checks if reversal bar is down bar
        if (stock.priceHistory[-1].closePrice >= stock.priceHistory[-1].openPrice):
            #[test]
            print("reversal bar was up bar in potential bearish reversal")
            #[test]
            return False

        #checks if reversal bar does not have long bottom tail
        if ((stock.priceHistory[-1].openPrice - stock.priceHistory[-1].low) > (0.4 * (stock.priceHistory[-1].high - stock.priceHistory[-1].low))):
            #[test]
            print("reversal bar had long bottom tail in potential bearish reversal")
            #[test]
            return False

    return True


def checkForBullishReversalOff25CentIntervalStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime):
    #checks for 'bullish reversal off 25-cent interval' strategy
    if (checkLowOfDay(tickers, item, 'bullish') and checkTrend(tickers, item, 'bullish') and checkPriorBar(tickers, item, 'bullish') and checkReversalBar(tickers, item, 'bullish') and checkDistanceFromInterval(tickers, item, 'bullish')
        and tickers[item].percentageOfDownBarsInDowntrend >= 50 and tickers[item].canTrade == True and tickers[item].havePosition == False):

        #[test]
        print(time + '\t' + 'bullish reversal off 25-cent interval in' + item)
        #[test]

        #checks if DTBP is exceeded
        if (currentInvested + (price * size) < DTBP - 1000):

            print('DTBP not exceeded')

            #[test]
            orderQueue.append({item : {'action' : 'BUY', 'symbol' : item, 'size' : size, 'price' : price}})

            #update ticker info
            tickers[item].direction = "long"
            tickers[item].strategy = 'bullish 25-cent reversal'
            tickers[item].breakoutBarLow = tickers[item].priceHistory[-2].low
            #add order to list
            order = Order(item, candleTime, price, 'bullish 25-cent reversal', size, 'long')
            ORDERS.append(order)
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
            tickers[item].strategy = 'bullish 25-cent reversal'
            tickers[item].breakoutBarLow = tickers[item].priceHistory[-2].low
            #add order to list
            order = Order(item, candleTime, price, 'bullish 25-cent reversal', smallerSize, 'long')
            ORDERS.append(order)

def checkForBearishReversalOff25CentIntervalStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime):
    #checks for 'bearish reversal off 25-cent interval' strategy
    if (checkLowOfDay(tickers, item, 'bearish') and checkTrend(tickers, item, 'bearish') and checkPriorBar(tickers, item, 'bearish') and checkReversalBar(tickers, item, 'bearish') and checkDistanceFromInterval(tickers, item, 'bearish')
        and tickers[item].canTrade == True and tickers[item].havePosition == False):

        #[test]
        print(time + '\t' + 'bearish reversal off 25-cent interval in' + item)
        #[test]

        #checks if DTBP is exceeded
        if (currentInvested + (price * size) < DTBP - 1000):

            print('DTBP not exceeded')

            #[test]
            orderQueue.append({item : {'action' : 'SELL_SHORT', 'symbol' : item, 'size' : size, 'price' : price}})

            #update ticker info
            tickers[item].direction = "short"
            tickers[item].strategy = 'bearish 25-cent reversal'
            tickers[item].breakoutBarHigh = tickers[item].priceHistory[-2].high
            #add order to list
            order = Order(item, candleTime, price, 'bearish 25-cent reversal', size, 'short')
            ORDERS.append(order)
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
            tickers[item].strategy = 'bearish 25-cent reversal'
            tickers[item].breakoutBarHigh = tickers[item].priceHistory[-2].high
            #add order to list
            order = Order(item, candleTime, price, 'bearish 25-cent reversal', smallerSize, 'short')
            ORDERS.append(order)