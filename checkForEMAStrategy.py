import data
from classes import Order

def checkForEMAStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime):
    conditionsForEMAStrategyMet = False
    #checks for 'break above 20EMA' strategy
    if (tickers[item].currentCandle.openPrice < round(tickers[item].EMA20, 2) and tickers[item].currentCandle.closePrice > round(tickers[item].EMA20, 2)
        and ((tickers[item].priceHistory[-1].volume > 1.7 * tickers[item].priceHistory[-2].volume and tickers[item].priceHistory[-1].volume < 3 * tickers[item].priceHistory[-2].volume) or tickers[item].priceHistory[-1].volume > 4 * tickers[item].priceHistory[-2].volume)
        and tickers[item].canUseEMAStrategy == True and tickers[item].havePosition == False and tickers[item].tradedEMAStrategy == False
        and tickers[item].isInSidewaysTrend == False and tickers[item].canTrade == True):

        #[test]
        print(time + '\t' + 'break above 20EMA in' + item)
        #[test]

        conditionsForEMAStrategyMet = True

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
            orderQueue.append({item : {'action' : 'BUY', 'symbol' : item, 'size' : size, 'price' : price}})
            #update ticker info
            tickers[item].direction = "long"
            tickers[item].strategy = 'break above 20EMA'
            tickers[item].tradedEMAStrategy = True
            #add order to list
            order = Order(item, candleTime, price, 'break above 20EMA', size, 'long')
            ORDERS.append(order)

            #[test]
            print('DTBP not exceeded')
            #[test]
        #use smaller position size if DTBP would otherwise be exceeded
        elif ((DTBP - 1000 - currentInvested) / price >= 300):
            smallerSize = DTBP - 1000 - currentInvested / price
            orderQueue.append({item : {'action' : 'BUY', 'symbol' : item, 'size' : smallerSize, 'price' : price}})
            #update ticker info
            tickers[item].direction = "long"
            tickers[item].strategy = 'break above 20EMA'
            tickers[item].tradedEMAStrategy = True
            #add order to list
            order = Order(item, candleTime, price, 'break above 20EMA', smallerSize, 'long')
            ORDERS.append(order)

            #[test]
            print('Using smaller position size')
            #[test]

    #checks for 'break below 20EMA' strategy
    elif (tickers[item].currentCandle.openPrice > round(tickers[item].EMA20, 2) and tickers[item].currentCandle.closePrice < round(tickers[item].EMA20, 2)
        and ((tickers[item].priceHistory[-1].volume > 1.7 * tickers[item].priceHistory[-2].volume and tickers[item].priceHistory[-1].volume < 3 * tickers[item].priceHistory[-2].volume) or tickers[item].priceHistory[-1].volume > 4 * tickers[item].priceHistory[-2].volume)
        and tickers[item].canUseEMAStrategy == True and tickers[item].havePosition == False and tickers[item].tradedEMAStrategy == False
        and tickers[item].isInSidewaysTrend == False and tickers[item].canTrade == True):

        #[test]
        print(time + '\t' + 'break below 20EMA in' + item)
        #[test]

        conditionsForEMAStrategyMet = True

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
            
            if (item not in data.HARD_TO_BORROW):
                orderQueue.append({item : {'action' : 'SELL_SHORT', 'symbol' : item, 'size' : size, 'price' : price}})
                #update ticker info
                tickers[item].direction = "short"
                tickers[item].strategy = 'break below 20EMA'
                tickers[item].tradedEMAStrategy = True
                #add order to list
                order = Order(item, candleTime, price, 'break below 20EMA', size, 'short')
                ORDERS.append(order)

                #[test]
                print('stock can be shorted')
                #[test]
        #use smaller position size if DTBP would otherwise be exceeded
        elif ((DTBP - 1000 - currentInvested) / price >= 300):

            #[test]
            print('Using smaller position size')
            #[test]

            smallerSize = DTBP - 1000 - currentInvested / price
            if (item not in data.HARD_TO_BORROW):
                orderQueue.append({item : {'action' : 'SELL_SHORT', 'symbol' : item, 'size' : smallerSize, 'price' : price}})
                #update ticker info
                tickers[item].direction = "short"
                tickers[item].strategy = 'bounce lower off 20EMA'
                tickers[item].tradedEMAStrategy = True
                #add order to list
                order = Order(item, candleTime, price, 'bounce lower off 20EMA', smallerSize, 'short')
                ORDERS.append(order)

                #[test]
                print('stock can be shorted')
                #[test]
    
    #checks for 'bounce lower off 20EMA' strategy
    elif (tickers[item].currentCandle.openPrice < round(tickers[item].EMA20, 2) and tickers[item].currentCandle.high == round(tickers[item].EMA20, 2)
        and ((tickers[item].priceHistory[-1].volume > 1.7 * tickers[item].priceHistory[-2].volume and tickers[item].priceHistory[-1].volume < 3 * tickers[item].priceHistory[-2].volume) or tickers[item].priceHistory[-1].volume > 4 * tickers[item].priceHistory[-2].volume)
        and tickers[item].currentCandle.closePrice < tickers[item].currentCandle.openPrice and tickers[item].canUseEMAStrategy == True and tickers[item].havePosition == False
        and tickers[item].tradedEMAStrategy == False and tickers[item].isInSidewaysTrend == False and tickers[item].canTrade == True):
        
        #[test]
        print(time + '\t' + 'bounce lower off 20EMA in' + item)
        #[test]

        conditionsForEMAStrategyMet = True

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

            if (item not in data.HARD_TO_BORROW):
                orderQueue.append({item : {'action' : 'SELL_SHORT', 'symbol' : item, 'size' : size, 'price' : price}})
                #update ticker info
                tickers[item].direction = "short"
                tickers[item].strategy = 'bounce lower off 20EMA'
                tickers[item].tradedEMAStrategy = True
                #add order to list
                order = Order(item, candleTime, price, 'bounce lower off 20EMA', size, 'short')
                ORDERS.append(order)

                #[test]
                print('stock can be shorted')
                #[test]
        #use smaller position size if DTBP would otherwise be exceeded
        elif ((DTBP - 1000 - currentInvested) / price >= 300):

            #[test]
            print('Using smaller position size')
            #[test]

            smallerSize = DTBP - 1000 - currentInvested / price
            if (item not in data.HARD_TO_BORROW):
                orderQueue.append({item : {'action' : 'SELL_SHORT', 'symbol' : item, 'size' : smallerSize, 'price' : price}})
                #update ticker info
                tickers[item].direction = "short"
                tickers[item].strategy = 'bounce lower off 20EMA'
                tickers[item].tradedEMAStrategy = True
                #add order to list
                order = Order(item, candleTime, price, 'bounce lower off 20EMA', smallerSize, 'short')
                ORDERS.append(order)

                #[test]
                print('stock can be shorted')
                #[test]

    #checks for 'bounce higher off 20EMA' strategy
    elif (tickers[item].currentCandle.openPrice > round(tickers[item].EMA20, 2) and tickers[item].currentCandle.low == round(tickers[item].EMA20, 2)
        and ((tickers[item].priceHistory[-1].volume > 1.7 * tickers[item].priceHistory[-2].volume and tickers[item].priceHistory[-1].volume < 3 * tickers[item].priceHistory[-2].volume) or tickers[item].priceHistory[-1].volume > 4 * tickers[item].priceHistory[-2].volume)
        and tickers[item].currentCandle.closePrice > tickers[item].currentCandle.openPrice and tickers[item].canUseEMAStrategy == True and tickers[item].havePosition == False
        and tickers[item].tradedEMAStrategy == False and tickers[item].isInSidewaysTrend == False and tickers[item].canTrade == True):
        
        #[test]
        print(time + '\t' + 'bounce higher off 20EMA in' + item)
        #[test]

        conditionsForEMAStrategyMet = True

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
            tickers[item].strategy = 'bounce higher off 20EMA'
            tickers[item].tradedEMAStrategy = True
            #add order to list
            order = Order(item, candleTime, price, 'bounce higher off 20EMA', size, 'long')
            ORDERS.append(order)
        #use smaller position size if DTBP would otherwise be exceeded
        elif ((DTBP - 1000 - currentInvested) / price >= 300):
            smallerSize = DTBP - 1000 - currentInvested / price
            orderQueue.append({item : {'action' : 'BUY', 'symbol' : item, 'size' : smallerSize, 'price' : price}})
            #update ticker info
            tickers[item].direction = "long"
            tickers[item].strategy = 'break above 20EMA'
            tickers[item].tradedEMAStrategy = True
            #add order to list
            order = Order(item, candleTime, price, 'break above 20EMA', smallerSize, 'long')
            ORDERS.append(order)

            #[test]
            print('Using smaller position size')
            #[test]

    return conditionsForEMAStrategyMet