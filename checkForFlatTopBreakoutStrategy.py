import data
import math
from classes import Order

def searchForProhibitedInterval(price, tickers, item):
    digits = (100 * price) % 100
    interval = 0
    if (digits == 23 or digits == 24 or digits == 25 or digits == 26):
        interval = math.floor(price) + 0.25
    elif (digits == 48 or digits == 49 or digits == 50 or digits == 51):
        interval = math.floor(price) + 0.5
    elif (digits == 73 or digits == 74 or digits == 75 or digits == 76):
        interval = math.floor(price) + 0.75
    elif (digits == 98 or digits == 99):
        interval = math.ceil(price)
    elif(digits == 0 or digits == 1):
        interval = math.floor(price)

    if (interval in tickers[item].prohibitedIntervals):
        return True
    else:
        return False

def checkForValidBase(tickers, item, time):
    #check for start of flat-top-breakout pattern
    digitsHigh = (100 * tickers[item].currentCandle.high) % 100
    digitsClose = (100 * tickers[item].currentCandle.closePrice) % 100
    acceptableDigits = [23, 24, 25, 26, 48, 49, 50, 51, 73, 74, 75, 76, 98, 99, 0, 1]
    if (tickers[item].currentCandle.high == tickers[item].highOfDay and not tickers[item].withinFlatTopBreakoutPattern and (digitsHigh in acceptableDigits) and not searchForProhibitedInterval(tickers[item].currentCandle.high, tickers, item)
        and tickers[item].currentCandle.closePrice > tickers[item].EMA5 and tickers[item].currentCandle.openPrice > tickers[item].EMA20 and tickers[item].currentCandle.openPrice > tickers[item].EMA10
        and tickers[item].currentCandle.closePrice > tickers[item].EMA20):
        if (digitsHigh == 26):
            tickers[item].intervalUnderConsideration = math.floor(tickers[item].currentCandle.high) + 0.25
            if (digitsClose < 26 and tickers[item].currentCandle.openPrice < tickers[item].intervalUnderConsideration):
                tickers[item].withinFlatTopBreakoutPattern = True
                tickers[item].firstCandleOfBase = True
                #[test]
                print("Start of flat-top-breakout pattern for: " + item + ' at ' + time)
                #[test]
            else:
                tickers[item].withinFlatTopBreakoutPattern = False
                tickers[item].firstCandleOfBase = False
                tickers[item].prohibitedIntervals.append(math.floor(tickers[item].currentCandle.high) + 0.25)
        elif (digitsHigh == 51):
            tickers[item].intervalUnderConsideration = math.floor(tickers[item].currentCandle.high) + 0.5
            if (digitsClose < 51 and tickers[item].currentCandle.openPrice < tickers[item].intervalUnderConsideration):
                tickers[item].withinFlatTopBreakoutPattern = True
                tickers[item].firstCandleOfBase = True
                #[test]
                print("Start of flat-top-breakout pattern for: " + item + ' at ' + time)
                #[test]
            else:
                tickers[item].withinFlatTopBreakoutPattern = False
                tickers[item].firstCandleOfBase = False
                tickers[item].prohibitedIntervals.append(math.floor(tickers[item].currentCandle.high) + 0.5)
        elif (digitsHigh == 76):
            tickers[item].intervalUnderConsideration = math.floor(tickers[item].currentCandle.high) + 0.75
            if (digitsClose < 76 and tickers[item].currentCandle.openPrice < tickers[item].intervalUnderConsideration):
                tickers[item].withinFlatTopBreakoutPattern = True
                tickers[item].firstCandleOfBase = True
                #[test]
                print("Start of flat-top-breakout pattern for: " + item + ' at ' + time)
                #[test]
            else:
                tickers[item].withinFlatTopBreakoutPattern = False
                tickers[item].firstCandleOfBase = False
                tickers[item].prohibitedIntervals.append(math.floor(tickers[item].currentCandle.high) + 0.75)
        elif (digitsHigh == 1):
            tickers[item].intervalUnderConsideration = math.floor(tickers[item].currentCandle.high)
            if ((digitsClose == 0 or digitsClose < 100) and tickers[item].currentCandle.openPrice < tickers[item].intervalUnderConsideration):
                tickers[item].withinFlatTopBreakoutPattern = True
                tickers[item].firstCandleOfBase = True
                #[test]
                print("Start of flat-top-breakout pattern for: " + item + ' at ' + time)
                #[test]
            else:
                tickers[item].withinFlatTopBreakoutPattern = False 
                tickers[item].firstCandleOfBase = False
                tickers[item].prohibitedIntervals.append(math.floor(tickers[item].currentCandle.high))
        else:
            if (digitsHigh == 23 or digitsHigh == 24 or digitsHigh == 25):
                tickers[item].intervalUnderConsideration = math.floor(tickers[item].currentCandle.high) + 0.25
            elif (digitsHigh == 48 or digitsHigh == 49 or digitsHigh == 50):
                tickers[item].intervalUnderConsideration = math.floor(tickers[item].currentCandle.high) + 0.5
            elif (digitsHigh == 73 or digitsHigh == 74 or digitsHigh == 75):
                tickers[item].intervalUnderConsideration = math.floor(tickers[item].currentCandle.high) + 0.75
            elif (digitsHigh == 98 or digitsHigh == 99):
                tickers[item].intervalUnderConsideration = math.ceil(tickers[item].currentCandle.high)
            elif (digitsHigh == 0):
                tickers[item].intervalUnderConsideration = tickers[item].currentCandle.high

            if (tickers[item].currentCandle.openPrice <= tickers[item].intervalUnderConsideration):
                tickers[item].withinFlatTopBreakoutPattern = True
                tickers[item].firstCandleOfBase = True
                #[test]
                print("Start of flat-top-breakout pattern for: " + item + ' at ' + time)
                #[test]

    #check for top tail above entry in the middle of a flat-top-breakout pattern, which would invalidate the pattern
    if (tickers[item].withinFlatTopBreakoutPattern and tickers[item].currentCandle.high > tickers[item].intervalUnderConsideration and not tickers[item].firstCandleOfBase
        and tickers[item].currentCandle.closePrice <= tickers[item].intervalUnderConsideration and tickers[item].currentCandle.openPrice < tickers[item].intervalUnderConsideration):
        tickers[item].withinFlatTopBreakoutPattern = False
        tickers[item].closedBelow10EMA = False
        tickers[item].prohibitedIntervals.append(tickers[item].intervalUnderConsideration)
        tickers[item].sizeOfFlatTopBreakoutPattern = 0
        tickers[item].firstCandleOfBase = False

        #[test]
        print("Flat-top-breakout in " + item + " invalidated because of top tail above mark" + ' at ' + time)
        #[test]

    #check for close below prior interval in flat-top-breakout pattern
    if (tickers[item].withinFlatTopBreakoutPattern and (tickers[item].intervalUnderConsideration - tickers[item].currentCandle.closePrice >= 0.25)):
        tickers[item].withinFlatTopBreakoutPattern = False
        tickers[item].closedBelow10EMA = False
        tickers[item].prohibitedIntervals.append(tickers[item].intervalUnderConsideration)
        tickers[item].sizeOfFlatTopBreakoutPattern = 0
        tickers[item].firstCandleOfBase = False

        #[test]
        print("Flat-top-breakout in " + item + " invalidated because of close below prior interval" + ' at ' + time)
        #[test]

    #check for close below 10EMA for flat-top-breakout pattern
    if (tickers[item].currentCandle.closePrice <= round(tickers[item].EMA10, 2) and tickers[item].withinFlatTopBreakoutPattern):
        #invalidates pattern if closed below 10EMA more than once
        if (tickers[item].closedBelow10EMA):
            tickers[item].withinFlatTopBreakoutPattern = False
            tickers[item].closedBelow10EMA = False
            tickers[item].sizeOfFlatTopBreakoutPattern = 0
            tickers[item].prohibitedIntervals.append(tickers[item].intervalUnderConsideration)
            tickers[item].firstCandleOfBase = False

            #[test]
            print("Flat-top-breakout in " + item + " invalidated because of second close below 10EMA" + ' at ' + time)
            #[test]

        else:
            tickers[item].closedBelow10EMA = True

            #[test]
            print("First close below 10EMA in " + item + " at " + time)
            #[test]

    #check for close above interval under consideration when the base is smaller than 3 candles
    if (tickers[item].withinFlatTopBreakoutPattern and tickers[item].sizeOfFlatTopBreakoutPattern < 3 and tickers[item].currentCandle.closePrice > tickers[item].intervalUnderConsideration):
        tickers[item].withinFlatTopBreakoutPattern = False
        tickers[item].closedBelow10EMA = False
        tickers[item].sizeOfFlatTopBreakoutPattern = 0
        tickers[item].prohibitedIntervals.append(tickers[item].intervalUnderConsideration)
        tickers[item].firstCandleOfBase = False

        #[test]
        print("Flat-top-breakout in " + item + " invalidated because of close above mark when base was too small" + ' at ' + time)
        #[test] 

    #adds to the length of the flat-top-breakout pattern if the high price is equal to or less than the interval under consideration
    if (tickers[item].withinFlatTopBreakoutPattern and tickers[item].currentCandle.high <= tickers[item].intervalUnderConsideration):
        tickers[item].sizeOfFlatTopBreakoutPattern += 1

    #resets the firstCandleOfBase variable
    if (tickers[item].withinFlatTopBreakoutPattern):
        tickers[item].firstCandleOfBase = False

    #raises stop loss interval 
    if (tickers[item].currentCandle.closePrice > tickers[item].nextInterval and tickers[item].havePosition and tickers[item].strategy == 'flat top breakout'):
        tickers[item].stopLossInterval = tickers[item].nextInterval
        tickers[item].nextInterval += 0.25

        #[test]
        print("The stop loss interval for " + item + " is " + str(tickers[item].stopLossInterval))
        #[test]

def checkForFlatTopBreakoutStrategy(tickers, item, orderQueue, ORDERS, size, price, time, currentInvested, DTBP, candleTime):
    #checks for 'flat top breakout' strategy
    if (tickers[item].sizeOfFlatTopBreakoutPattern >= 3 and tickers[item].withinFlatTopBreakoutPattern and tickers[item].currentCandle.closePrice > tickers[item].intervalUnderConsideration
        and tickers[item].currentCandle.closePrice < (tickers[item].intervalUnderConsideration + 0.1) and tickers[item].canTrade and not tickers[item].havePosition
        and tickers[item].currentCandle.closePrice >= (0.7 * (tickers[item].currentCandle.high - tickers[item].currentCandle.low) + tickers[item].currentCandle.low
        and tickers[item].currentCandle.openPrice <= tickers[item].intervalUnderConsideration) and tickers[item].currentCandle.openPrice <= tickers[item].intervalUnderConsideration):
        #[test]
        print(time + '\t' + 'flat top breakout in ' + item)
        #[test]

        #checks if DTBP is exceeded
        if (currentInvested + (price * size) < DTBP - 1000):
            #[test]
            #orderQueue.append({item : {'action' : 'BUY', 'symbol' : item, 'size' : size, 'price' : price}})
            #[test]

            #[test]
            #tickers[item].havePosition = True
            #[test]
            
            #update ticker info
            tickers[item].direction = "long"
            tickers[item].strategy = 'flat top breakout'
            tickers[item].withinFlatTopBreakoutPattern = False
            tickers[item].closedBelow10EMA = False
            tickers[item].sizeOfFlatTopBreakoutPattern = 0
            tickers[item].nextInterval = tickers[item].intervalUnderConsideration + 0.25
            tickers[item].stopLossInterval = 0
            #add order to list
            order = Order(item, candleTime, price, 'flat top breakout', size, 'long')
            ORDERS.append(order)

            #[test]
            print('The next interval is: ' + str(tickers[item].nextInterval))
            #[test]
        #use smaller position size if DTBP would otherwise be exceeded
        elif ((DTBP - 1000 - currentInvested) / price >= 300):
            #[test]
            print('Using smaller size')
            #[test]

            smallerSize = DTBP - 1000 - currentInvested / price

            #[test]
            #orderQueue.append({item : {'action' : 'BUY', 'symbol' : item, 'size' : smallerSize, 'price' : price}})
            #[test]
            
            #update ticker info
            tickers[item].direction = "long"
            tickers[item].strategy = 'flat top breakout'
            tickers[item].withinFlatTopBreakoutPattern = False
            tickers[item].closedBelow10EMA = False
            tickers[item].sizeOfFlatTopBreakoutPattern = 0
            tickers[item].nextInterval = tickers[item].intervalUnderConsideration + 0.25
            tickers[item].stopLossInterval = 0
            #add order to list
            order = Order(item, candleTime, price, 'flat top breakout', smallerSize, 'long')
            ORDERS.append(order)

            #[test]
            print('The next interval is: ' + str(tickers[item].nextInterval))
            #[test]
    elif (tickers[item].withinFlatTopBreakoutPattern and tickers[item].currentCandle.high > tickers[item].intervalUnderConsideration):
        #[test]
        print("Flat top breakout in " + item + " no longer considered")
        #[test]
        tickers[item].withinFlatTopBreakoutPattern = False
        tickers[item].closedBelow10EMA = False
        tickers[item].sizeOfFlatTopBreakoutPattern = 0
        tickers[item].nextInterval = 0
        tickers[item].stopLossInterval = 0
