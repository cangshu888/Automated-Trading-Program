from classes import Order

def checkForMorningBreakoutStrategy(tickers, item, orderQueue, ORDERS, price, time, currentInvested, DTBP, candleTime):
    #checks for 'morning breakout' strategy
    if (tickers[item].currentCandle.closePrice > tickers[item].morningHigh and tickers[item].currentCandle.closePrice < tickers[item].morningHigh * 1.003
        and time <= '7:30:00' and tickers[item].canTrade and not tickers[item].havePosition):
        #[test]
        print(time + '\t' + 'morning breakout in ' + item)
        #[test]

        size = round(10000 / price)

        #checks if DTBP is exceeded
        if (currentInvested + (price * size) < DTBP - 1000):
            orderQueue.append({item : {'action' : 'BUY', 'symbol' : item, 'size' : size, 'price' : price}})
            #update ticker info
            tickers[item].direction = "long"
            tickers[item].strategy = 'morning breakout breakout'
            #add order to list
            order = Order(item, candleTime, price, 'morning breakout', size, 'long')
            ORDERS.append(order)

            #[test]
            print('DTBP not exceeded')
            #[test]