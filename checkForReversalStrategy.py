from classes import Order

def checkForReversalStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime):
    #checks for 'reversal' strategy without climactic volume
    if (tickers[item].numberOfBarsBelowEMAs >= 9 and tickers[item].currentCandle.openPrice < round(tickers[item].EMA5, 2) and tickers[item].currentCandle.closePrice > round(tickers[item].EMA5, 2)
        and tickers[item].trend == 'downtrend' and tickers[item].percentageOfDownBarsInDowntrend >= 50 and tickers[item].priceHistory[-2].closePrice < tickers[item].priceHistory[-2].openPrice
        and tickers[item].currentCandle.closePrice >= (0.75 * (tickers[item].currentCandle.high - tickers[item].currentCandle.low) + tickers[item].currentCandle.low) 
        and tickers[item].canTrade == True and tickers[item].havePosition == False
        and tickers[item].currentCandle.closePrice >= tickers[item].priceHistory[-2].high - 0.01
        and tickers[item].priceHistory[-2].openPrice <= tickers[item].priceHistory[-2].EMA5 + 0.02
        and (tickers[item].priceHistory[-2].high - tickers[item].priceHistory[-2].openPrice) <= 0.4 * (tickers[item].priceHistory[-2].high - tickers[item].priceHistory[-2].low)):

        #[test]
        print(time + '\t' + 'reversal without climactic volume in' + item )

        if (item == 'M'):
            size = 1500

        if (item == 'AMAT' or item == 'MU'):
            size = 800

        if (item == 'C'):
            size = 1000
        
        if (item == 'INTC'):
            size = 700

        #checks if DTBP is exceeded
        if (currentInvested + (price * size) < DTBP - 1000):

            print('DTBP not exceeded')

            #[test]
            orderQueue.append({item : {'action' : 'BUY', 'symbol' : item, 'size' : size, 'price' : price}})

            #update ticker info
            tickers[item].direction = "long"
            tickers[item].strategy = 'reversal'
            tickers[item].breakoutBarLow = tickers[item].currentCandle.low
            #add order to list
            order = Order(item, candleTime, price, 'reversal', size, 'long')
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
            tickers[item].strategy = 'reversal'
            tickers[item].breakoutBarLow = tickers[item].currentCandle.low
            #add order to list
            order = Order(item, candleTime, price, 'reversal', smallerSize, 'long')
            ORDERS.append(order)

    #checks for 'reversal' strategy with several consecutive down bars
    elif (tickers[item].numberOfBarsBelowEMAs >= 9
            and tickers[item].trend == 'downtrend' and tickers[item].percentageOfDownBarsInDowntrend >= 50 and tickers[item].numberOfConsecutiveBars >= 6
            and tickers[item].currentCandle.closePrice >= (0.75 * (tickers[item].currentCandle.high - tickers[item].currentCandle.low) + tickers[item].currentCandle.low) 
            and tickers[item].canTrade == True and tickers[item].havePosition == False and tickers[item].currentCandle.closePrice >= tickers[item].priceHistory[-2].high - 0.01
            and tickers[item].priceHistory[-2].closePrice < tickers[item].priceHistory[-2].openPrice
            and tickers[item].priceHistory[-2].openPrice <= tickers[item].priceHistory[-2].EMA5 + 0.02
            and (tickers[item].priceHistory[-2].high - tickers[item].priceHistory[-2].openPrice) <= 0.4 * (tickers[item].priceHistory[-2].high - tickers[item].priceHistory[-2].low)):
        
        #[test]
        print(time + '\t' + 'reversal with several consecutive down bars in' + item )

        if (item == 'M'):
            size = 1500

        if (item == 'AMAT' or item == 'MU'):
            size = 800

        if (item == 'C'):
            size = 1000
        
        if (item == 'INTC'):
            size = 700
        
        #checks if DTBP is exceeded
        if (currentInvested + (price * size) < DTBP - 1000):

            #[test]
            print('DTBP not exceeded')

            #[test]
            orderQueue.append({item : {'action' : 'BUY', 'symbol' : item, 'size' : size, 'price' : price}})

            #update ticker info
            tickers[item].direction = "long"
            tickers[item].strategy = 'reversal'
            tickers[item].breakoutBarLow = tickers[item].currentCandle.low

            #add order to list
            order = Order(item, candleTime, price, 'reversal', size, 'long')
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
            tickers[item].strategy = 'reversal'
            tickers[item].breakoutBarLow = tickers[item].currentCandle.low
            #add order to list
            order = Order(item, candleTime, price, 'reversal', smallerSize, 'long')
            ORDERS.append(order)
