from classes import Order

def checkForHighTightFlagStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime):
    conditionsForHighTightFlagMet = False
    #checks for 'high tight flag' strategy with 1 down bar
    if (tickers[item].isInSteepUptrend(1) == True and tickers[item].priceHistory[-2].volume < tickers[item].priceHistory[-3].volume
            and tickers[item].priceHistory[-2].high <= tickers[item].priceHistory[-3].closePrice + 0.04
            and ((tickers[item].priceHistory[-2].high - tickers[item].priceHistory[-2].low) <= 0.8 * (tickers[item].priceHistory[-3].high - tickers[item].priceHistory[-3].low) or (tickers[item].priceHistory[-2].high - tickers[item].priceHistory[-2].low) <= 0.05)
            and tickers[item].priceHistory[-2].low >= tickers[item].priceHistory[-2].EMA5 - 0.02 
            and tickers[item].priceHistory[-2].closePrice <= tickers[item].priceHistory[-2].openPrice
            and tickers[item].priceHistory[-1].closePrice > tickers[item].priceHistory[-2].high
            and tickers[item].priceHistory[-1].closePrice > tickers[item].priceHistory[-3].closePrice
            and (tickers[item].priceHistory[-1].closePrice <= tickers[item].priceHistory[-3].closePrice + 0.08 or tickers[item].priceHistory[-1].closePrice <= tickers[item].priceHistory[-2].high + 0.08)
            and tickers[item].priceHistory[-1].closePrice >= (tickers[item].priceHistory[-1].low + (0.8 * (tickers[item].priceHistory[-1].high - tickers[item].priceHistory[-1].low)))
            and tickers[item].priceHistory[-3].closePrice >= (tickers[item].priceHistory[-3].low + (0.7 * (tickers[item].priceHistory[-3].high - tickers[item].priceHistory[-3].low)))
            and tickers[item].canTrade == True and tickers[item].havePosition == False):

        #[test]
        print(time + '\t' + 'high tight flag with 1 down bar in ' + item)
        #[test]

        conditionsForHighTightFlagMet = True

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
            tickers[item].strategy = 'high tight flag'
            tickers[item].breakoutBarLow = tickers[item].currentCandle.low
            #add order to list
            order = Order(item, candleTime, price, 'high tight flag', size, 'long')
            ORDERS.append(order)

    #checks for 'high tight flag' strategy with 2 down bars
    elif (tickers[item].isInSteepUptrend(2) == True and tickers[item].priceHistory[-3].volume < tickers[item].priceHistory[-4].volume
            and tickers[item].priceHistory[-3].high <= tickers[item].priceHistory[-4].closePrice + 0.04
            and (tickers[item].priceHistory[-3].high - tickers[item].priceHistory[-3].low) <= 0.8 * (tickers[item].priceHistory[-4].high - tickers[item].priceHistory[-4].low)
            and tickers[item].priceHistory[-3].low >= tickers[item].priceHistory[-3].EMA5 - 0.02 
            and tickers[item].priceHistory[-2].volume < tickers[item].priceHistory[-4].volume
            and tickers[item].priceHistory[-2].volume < 2 * tickers[item].priceHistory[-3].volume
            and (tickers[item].priceHistory[-2].high - tickers[item].priceHistory[-2].low) <= 1.2 * (tickers[item].priceHistory[-3].high - tickers[item].priceHistory[-3].low)
            and tickers[item].priceHistory[-2].high <= tickers[item].priceHistory[-3].high
            and tickers[item].priceHistory[-2].high <= tickers[item].priceHistory[-4].high
            and tickers[item].priceHistory[-2].low >= tickers[item].priceHistory[-2].EMA5 - 0.03
            and tickers[item].priceHistory[-2].closePrice < tickers[item].priceHistory[-2].openPrice
            and tickers[item].priceHistory[-3].closePrice < tickers[item].priceHistory[-3].openPrice
            and tickers[item].priceHistory[-1].closePrice > tickers[item].priceHistory[-2].high
            and tickers[item].priceHistory[-1].closePrice > tickers[item].priceHistory[-3].high
            and tickers[item].priceHistory[-1].closePrice > tickers[item].priceHistory[-4].closePrice
            and (tickers[item].priceHistory[-1].closePrice <= tickers[item].priceHistory[-4].closePrice + 0.07 or tickers[item].priceHistory[-1].closePrice <= tickers[item].priceHistory[-3].high + 0.07)
            and tickers[item].priceHistory[-1].closePrice >= (tickers[item].priceHistory[-1].low + (0.8 * (tickers[item].priceHistory[-1].high - tickers[item].priceHistory[-1].low)))
            and tickers[item].priceHistory[-4].closePrice >= (tickers[item].priceHistory[-4].low + (0.7 * (tickers[item].priceHistory[-4].high - tickers[item].priceHistory[-4].low)))
            and tickers[item].canTrade == True and tickers[item].havePosition == False):

        #[test]
        print(time + '\t' + 'high tight flag with 2 down bars in ' + item)
        #[test]

        conditionsForHighTightFlagMet = True

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
            tickers[item].strategy = 'high tight flag'
            tickers[item].breakoutBarLow = tickers[item].currentCandle.low
            #add order to list
            order = Order(item, candleTime, price, 'high tight flag', size, 'long')
            ORDERS.append(order)

    return conditionsForHighTightFlagMet