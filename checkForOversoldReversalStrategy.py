from classes import Order

def determineOversold(tickers, item):
    stock = tickers[item]
    if (len(stock.priceHistory) < 5):
            return False
    else:
        #checks for 4 consecutive down bars
        if (not(stock.priceHistory[-2].closePrice < stock.priceHistory[-2].openPrice and stock.priceHistory[-3].closePrice < stock.priceHistory[-3].openPrice and stock.priceHistory[-4].closePrice < stock.priceHistory[-4].openPrice and stock.priceHistory[-5].closePrice < stock.priceHistory[-5].openPrice)):
            return False
        #checks for increasing volume across the last 4 bars
        if (not(stock.priceHistory[-4].volume > stock.priceHistory[-5].volume and stock.priceHistory[-3].volume > stock.priceHistory[-4].volume and stock.priceHistory[-2].volume > stock.priceHistory[-3].volume)):
            return False
        #checks for increasing range across the last 4 bars
        if (not((stock.priceHistory[-4].high - stock.priceHistory[-4].low > stock.priceHistory[-5].high - stock.priceHistory[-5].low) and (stock.priceHistory[-3].high - stock.priceHistory[-3].low > stock.priceHistory[-4].high - stock.priceHistory[-4].low) and (stock.priceHistory[-2].high - stock.priceHistory[-2].low > stock.priceHistory[-3].high - stock.priceHistory[-3].low))):
            return False

        #checks if last 4 bars opened below 5EMA
        if (not(stock.priceHistory[-5].openPrice < stock.priceHistory[-5].EMA5 and stock.priceHistory[-4].openPrice < stock.priceHistory[-4].EMA5 and stock.priceHistory[-3].openPrice < stock.priceHistory[-3].EMA5 and stock.priceHistory[-2].openPrice < stock.priceHistory[-2].EMA5)):
            return False

        #[test]
        print("oversold conditions in " + item)
        #[test]
        

        return True

def checkLowOfDay(tickers, item):
    stock = tickers[item]
    
    if (stock.priceHistory[-2].low == stock.lowOfDay):
        return True
    elif (stock.priceHistory[-3].low == stock.lowOfDay):
        return True
    else:
        return False

def checkReversalBar(tickers, item):
    stock = tickers[item]

    #checks if reversal bar is up bar
    if (stock.priceHistory[-1].closePrice <= stock.priceHistory[-1].openPrice):
        return False

    #checks if reversal bar does not have long top tail
    if ((stock.priceHistory[-1].high - stock.priceHistory[-1].closePrice) > 0.25 * (stock.priceHistory[-1].high - stock.priceHistory[-1].low)):
        return False

    return True


def checkForOversoldReversalStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime):
    #checks for 'oversold reversal' strategy
    if (determineOversold(tickers, item) and checkLowOfDay(tickers, item) and checkReversalBar(tickers, item)
        and tickers[item].trend == 'downtrend' and tickers[item].percentageOfDownBarsInDowntrend >= 50 
        and tickers[item].canTrade == True and tickers[item].havePosition == False):

        #[test]
        print(time + '\t' + 'oversold reversal in' + item)
        #[test]

        #checks if DTBP is exceeded
        if (currentInvested + (price * size) < DTBP - 1000):

            print('DTBP not exceeded')

            #[test]
            orderQueue.append({item : {'action' : 'BUY', 'symbol' : item, 'size' : size, 'price' : price}})

            #update ticker info
            tickers[item].direction = "long"
            tickers[item].strategy = 'oversold reversal'
            tickers[item].breakoutBarLow = tickers[item].priceHistory[-2].low
            #add order to list
            order = Order(item, candleTime, price, 'oversold reversal', size, 'long')
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
            tickers[item].strategy = 'oversold reversal'
            tickers[item].breakoutBarLow = tickers[item].priceHistory[-2].low
            #add order to list
            order = Order(item, candleTime, price, 'oversold reversal', smallerSize, 'long')
            ORDERS.append(order)

            return True
    else:
        return False

    