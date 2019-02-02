import data

class Order():
    def __init__(self, symbol, entryTime, entryPrice, strategy, size, direction):
        self.symbol = symbol
        self.entryTime = entryTime
        self.entryPrice = entryPrice
        self.strategy = strategy
        self.size = size
        self.direction = direction
        self.exitPrice = 0
        self.exitTime = '00:00'

    def exit(self, exitTime, exitPrice):
        self.exitTime = exitTime
        self.exitPrice = exitPrice


class Candle():
        def calculateDirection(self):
            if (self.closePrice > self.openPrice):
                self.direction = 'up'
            elif (self.closePrice < self.openPrice):
                self.direction = 'down'
            else:
                self.direction = 'none'

        def __init__(self, symbol): 
            self.symbol = symbol
            self.time = '00:00' 
            self.closePrice = 0
            self.openPrice = 0
            self.high = 0
            self.low = 0
            self.volume = 0
            self.EMA5 = 0
            self.EMA10 = 0
            self.EMA20 = 0
            self.direction = ''



class Ticker():
    def __init__(self, symbol):
        self.EMA5 = 0
        self.EMA10 = 0
        self.EMA20 = 0
        self.symbol = symbol
        self.calculateEMA()
        self.currentCandle = Candle(symbol)
        self.priceHistory = []
        self.lastInteraction = '00:00'
        self.canTrade = False
        self.canUseEMAStrategy = False
        self.tradedEMAStrategy = False
        self.havePosition = False
        self.useEMA10AsStop = False
        self.useEMA5AsStop = False
        self.profitTarget = 10000
        self.trend = "none" #needed for reversal, high tight flag, and flat top breakout strategies
        self.strategy = "none" 
        self.previousTotalVolume = 0 #used to calculate volume of candle
        self.direction = "none" #long or short
        self.numberOfConsecutiveBars = 0
        self.numberOfBarsBelowEMAs = 0
        self.percentageOfDownBarsInDowntrend = 0
        self.breakoutBarLow = 0
        self.breakoutBarHigh = 0
        self.numberOfDownBarsAfterBreakout = 0
        self.canPrintInteractionStatus = True
        self.canRun00SecondCode = True
        self.positionSize = 0
        self.interactedWithEMA = False
        self.minutesSinceLastInteraction = 0
        self.isInSidewaysTrend = False
        self.averageRange = 0
        self.triggeredHardStop = False

        #data related to flat top breakout pattern
        self.highOfDay = 0
        self.prohibitedIntervals = []
        self.withinFlatTopBreakoutPattern = False
        self.closedBelow10EMA = False
        self.sizeOfFlatTopBreakoutPattern = 0
        self.intervalUnderConsideration = 0
        self.firstCandleOfBase = False
        self.stopLossInterval = 0
        self.nextInterval = 0

        #data related to morning breakout
        self.morningHigh = 0
        self.EMA50 = 0
        self.useEMA50AsStop = False

        #data related to initial EMA calculation
        self.initialEMA5 = 0
        self.initialEMA10 = 0
        self.initialEMA20 = 0

        #data related to reversals
        self.lowOfDay = 1000

    def isInSteepUptrend(self, downbars):
        if (len(self.priceHistory) < 7):
            return False
        if (downbars == 1):
            if (not(self.priceHistory[-3].openPrice >= self.priceHistory[-3].closePrice 
                    and self.priceHistory[-3].openPrice >= self.EMA5 - 0.02 and self.priceHistory[-3].closePrice >= self.EMA5
                    and self.priceHistory[-3].openPrice >= self.EMA10 and self.priceHistory[-3].closePrice >= self.EMA10
                    and self.priceHistory[-3].openPrice >= self.EMA20 and self.priceHistory[-3].closePrice >= self.EMA20
                    and (self.priceHistory[-3].high - self.priceHistory[-3].closePrice) <= 0.4 * (self.priceHistory[-3].high - self.priceHistory[-3].low))):

                    return False 
        
        elif (downbars == 2):
            if (not(self.priceHistory[-7].openPrice >= self.priceHistory[-7].closePrice 
                    and self.priceHistory[-7].openPrice >= self.EMA5 - 0.02 and self.priceHistory[-7].closePrice >= self.EMA5
                    and self.priceHistory[-7].openPrice >= self.EMA10 and self.priceHistory[-7].closePrice >= self.EMA10
                    and self.priceHistory[-7].openPrice >= self.EMA20 and self.priceHistory[-7].closePrice >= self.EMA20
                    and (self.priceHistory[-7].high - self.priceHistory[-7].closePrice) <= 0.4 * (self.priceHistory[-7].high - self.priceHistory[-7].low))):

                    return False

        if (not(self.priceHistory[-4].openPrice >= self.priceHistory[-4].closePrice 
                and self.priceHistory[-4].openPrice >= self.EMA5 - 0.02 and self.priceHistory[-4].closePrice >= self.EMA5
                and self.priceHistory[-4].openPrice >= self.EMA10 and self.priceHistory[-4].closePrice >= self.EMA10
                and self.priceHistory[-4].openPrice >= self.EMA20 and self.priceHistory[-4].closePrice >= self.EMA20
                and (self.priceHistory[-4].high - self.priceHistory[-4].closePrice) <= 0.4 * (self.priceHistory[-4].high - self.priceHistory[-4].low))):

                return False

        if (not(self.priceHistory[-5].openPrice >= self.priceHistory[-5].closePrice 
                and self.priceHistory[-5].openPrice >= self.EMA5 - 0.02 and self.priceHistory[-5].closePrice >= self.EMA5
                and self.priceHistory[-5].openPrice >= self.EMA10 and self.priceHistory[-5].closePrice >= self.EMA10
                and self.priceHistory[-5].openPrice >= self.EMA20 and self.priceHistory[-5].closePrice >= self.EMA20
                and (self.priceHistory[-5].high - self.priceHistory[-5].closePrice) <= 0.4 * (self.priceHistory[-5].high - self.priceHistory[-5].low))):

                return False

        if (not(self.priceHistory[-6].openPrice >= self.priceHistory[-6].closePrice 
                and self.priceHistory[-6].openPrice >= self.EMA5 - 0.02 and self.priceHistory[-6].closePrice >= self.EMA5
                and self.priceHistory[-6].openPrice >= self.EMA10 and self.priceHistory[-6].closePrice >= self.EMA10
                and self.priceHistory[-6].openPrice >= self.EMA20 and self.priceHistory[-6].closePrice >= self.EMA20
                and (self.priceHistory[-6].high - self.priceHistory[-6].closePrice) <= 0.4 * (self.priceHistory[-6].high - self.priceHistory[-6].low))):

                return False

        return True

    def calculateAverageRange(self):
        if (len(self.priceHistory) < 9):
            self.averageRange = 0
        else:
            sumOfRange = 0
            for i in range(1, 10):
                sumOfRange += (self.priceHistory[i * -1].high - self.priceHistory[i * -1].low)
            self.averageRange = sumOfRange / 9

    def calculateEMA(self, price=0):
        if (price == 0):
            #calculate current EMAs based on previous day's last 1-minute candle's EMAs
            self.EMA5 = data.EMA[self.symbol]['EMA5']
            self.EMA10 = data.EMA[self.symbol]['EMA10']
            self.EMA20 = data.EMA[self.symbol]['EMA20']
        else:
            #calculate EMA5
            multiplier = 2 / (5 + 1)
            EMA_5 = ((price - self.EMA5) * multiplier) + self.EMA5
            self.EMA5 = EMA_5#round(EMA_5, 2)

            #calculate EMA10
            multiplier = 2 / (10 + 1)
            EMA_10 = ((price - self.EMA10) * multiplier) + self.EMA10
            self.EMA10 = EMA_10#round(EMA_10, 2)

            #calculate EMA20
            multiplier = 2 / (20 + 1)
            EMA_20 = ((price - self.EMA20) * multiplier) + self.EMA20
            self.EMA20 = EMA_20#round(EMA_20, 2)

    def calculateEMA50(self, listOfClosingPrices):
        multiplier = 2 / (50 + 1)
        initialEMA = 0
        EMA_50 = 0
        for i in range(1, 51):
            if (i == 1):
                initialEMA = listOfClosingPrices[i]
                EMA_50 = initialEMA
            else:
                EMA_50 = (multiplier * listOfClosingPrices[i]) + ((1 - multiplier) * initialEMA)
                initialEMA = EMA_50
        
        self.EMA50 = EMA_50
    

    def determineTrend(self):
        if (len(self.priceHistory) < 8):
            self.trend = 'none'
        else:
            firstBarLow = self.priceHistory[-8].low - 0.03
            firstBarHigh = self.priceHistory[-8].high + 0.03
            eighthBarClose = self.priceHistory[-1].closePrice
            lowestClosingPrice = self.priceHistory[-8].closePrice
            #prevent the reversal trade if the reversal bar range is too large
            eighthBarRange = self.priceHistory[-1].high - self.priceHistory[-1].low
            numberOfDownBars = 0
            numberOfUpBars = 0

            for i in range(1, 9):
                if (self.priceHistory[i * -1].closePrice >= self.priceHistory[i * -1].openPrice):
                    numberOfUpBars += 1
                elif (self.priceHistory[i * -1].closePrice < self.priceHistory[i * -1].openPrice):
                    numberOfDownBars += 1

                if (self.priceHistory[i * -1].closePrice < lowestClosingPrice):
                    lowestClosingPrice = self.priceHistory[i * -1].closePrice

            if (numberOfUpBars > 4 and (eighthBarClose > firstBarHigh)):
                self.trend = 'uptrend'
            elif (numberOfDownBars > 5 and (eighthBarClose < firstBarLow) and (eighthBarClose == lowestClosingPrice)):
                self.trend = 'downtrend'
            else:
                self.trend = 'sideways'

    def determineNumberOfConsecutiveBars(self):
        self.numberOfConsecutiveBars = 0
        if (len(self.priceHistory) != 0):
            currentBarDirection = self.priceHistory[-1].calculateDirection()
            for i in range(len(self.priceHistory) - 1):
                self.priceHistory[(i + 1) * -1].calculateDirection()
                if (self.priceHistory[(i + 1) * -1].direction == currentBarDirection or self.priceHistory[(i + 1) * -1].direction == 'none'):
                    self.numberOfConsecutiveBars += 1
                else:
                    break

    def determineNumberOfBarsBelowEMAs(self):
        self.numberOfBarsBelowEMAs = 0
        if (len(self.priceHistory) != 0):
            for i in range(len(self.priceHistory) - 1):
                if (self.priceHistory[(i + 1) * -1].closePrice <= self.priceHistory[(i + 1) * -1].EMA10 and self.priceHistory[(i + 1) * -1].closePrice <= self.priceHistory[i * -1].EMA20):
                    self.numberOfBarsBelowEMAs += 1
                else:
                    break

    def calculatePercentageOfDownBarsInDowntrend(self):
        numberOfDownBars = 0
        for i in range(1, self.numberOfBarsBelowEMAs + 1):
            if (self.priceHistory[i * -1].closePrice <= self.priceHistory[i * -1].openPrice):
                numberOfDownBars += 1
        self.percentageOfDownBarsInDowntrend = (numberOfDownBars / self.numberOfBarsBelowEMAs) * 100

    def detectSidewaysTrend(self):
        if (len(self.priceHistory) < 6):
            self.isInSidewaysTrend = True
        else:
            sixthBarHigh = self.priceHistory[-6].high + 0.02
            sixthBarLow = self.priceHistory[-6].low - 0.02
            self.isInSidewaysTrend = True

            for i in range(1, 7):
                if (self.priceHistory[i * -1].closePrice > sixthBarHigh or self.priceHistory[i * -1].closePrice < sixthBarLow):
                    self.isInSidewaysTrend = False