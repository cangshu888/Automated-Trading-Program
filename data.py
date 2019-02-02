import json

AVAILABLE_TICKERS = ['MU', 'AMAT', 'X', 'GM', 'M', 'C', 'INTC', 'V', 'TWTR', 'MSFT', 'CSCO', 'NBL', 'AXP', 'CSX', 'IBM', 'VZ', 'LLY', 'PM', 'MO', 'AMD', 'XEL', 'PHM', 'COG', 'CMS', 'TECK', 'XOM', 'CVX', 'CL', 'BMY', 'COP', 'DHI', 'XRX', 'AAL', 'PFE', 'BSX', 'DVN', 'WMT', 'NKE', 'TGT', 'GPS', 'HPQ', 'MOS', 'QCOM', 'TSM', 'MYL', 'SBUX', 'EBAY', 'EXC', 'ATVI', 'LB', 'LEN', 'TJX', 'CAG', 'GIS', 'KHC', 'KR', 'MDLZ', 'WBA', 'ENB', 'NOV', 'OXY', 'WLL', 'AFL', 'ALLY', 'COF', 'PGR', 'PRU', 'STI', 'WFC', 'ABT', 'BHC', 'BAX', 'CAH', 'CVS', 'GILD', 'MRK', 'DAL']
EMA_STRATEGY_TICKERS = ['MU', 'AMAT', 'M', 'C', 'INTC', 'BOX', 'V']
REVERSAL_STRATEGY_TICKERS = ['MU', 'AMAT', 'M', 'C', 'INTC', 'V']
HIGH_TIGHT_FLAG_STRATEGY_TICKERS = ['MU', 'AMAT', 'M', 'C', 'INTC', 'V']
FLAT_TOP_BREAKOUT_TICKERS = ['MU', 'AMAT', 'X', 'GM', 'M', 'C', 'INTC', 'V', 'TWTR', 'MSFT', 'CSCO', 'NBL', 'AXP', 'CSX', 'IBM', 'VZ', 'LLY', 'PM', 'MO', 'AMD', 'XEL', 'PHM', 'COG', 'CMS', 'TECK', 'XOM', 'CVX', 'CL', 'BMY', 'COP', 'DHI', 'XRX', 'AAL', 'PFE', 'BSX', 'DVN', 'WMT', 'NKE', 'TGT', 'GPS', 'HPQ', 'MOS', 'QCOM', 'HRB', 'MYL', 'SBUX', 'EBAY', 'EXC', 'ATVI', 'LB', 'LEN', 'TJX', 'CAG', 'GIS', 'KHC', 'KR', 'MDLZ', 'WBA', 'ENB', 'NOV', 'OXY', 'WLL', 'AFL', 'ALLY', 'COF', 'PGR', 'PRU', 'STI', 'WFC', 'ABT', 'BHC', 'BAX', 'CAH', 'CVS', 'GILD', 'MRK', 'DAL']
MORNING_BREAKOUT_TICKERS = ['WMT', 'PZZA', 'UAL', 'HAS', 'HCA', 'LW', 'NSC', 'GRUB', 'BEAT', 'ALV', 'LRCX', 'TEAM', 'HRS', 'ZTS', 'DVA', 'HLF', 'KORS', 'AYX', 'ROKU', 'YELP', 'TPR', 'AAP', 'EL', 'ALXN', 'WB', 'WUBA', 'LOW', 'WSM', 'SNPS', 'ADSK', 'SPLK', 'VEEV', 'TIF', 'LULU', 'WTW', 'ATVI']
#AVAILABLE_TICKERS = list(set(FLAT_TOP_BREAKOUT_TICKERS + MORNING_BREAKOUT_TICKERS))

HARD_TO_BORROW = ['V', 'LLY', 'PM']
VERY_SMALL_POSITION = ['MSFT', 'IBM', 'LLY', 'CL', 'TGT', 'COF']
SMALL_POSITION = ['MU', 'AMAT', 'V', 'WMT', 'NKE', 'WBA', 'PGR', 'PRU']
LARGE_POSITION = ['X', 'GM', 'M', 'C', 'INTC', 'TWTR', 'CSCO', 'NBL', 'AXP', 'CSX', 'VZ', 'PM', 'MO', 'AMD', 'XEL', 'PHM', 'COG', 'CMS', 'TECK', 'XOM', 'CVX', 'BMY', 'COP', 'DHI', 'XRX', 'AAL', 'PFE', 'BSX', 'DVN', 'GPS', 'HPQ', 'MOS', 'QCOM', 'TSM', 'MYL', 'SBUX', 'EBAY', 'EXC', 'ATVI', 'LB', 'LEN', 'TJX', 'CAG', 'GIS', 'KHC', 'KR', 'MDLZ', 'ENB', 'NOV', 'OXY', 'WLL', 'AFL', 'ALLY', 'STI', 'WFC', 'ABT', 'BHC', 'BAX', 'CAH', 'CVS', 'GILD', 'MRK', 'DAL']

VERY_SMALL_POSITION_SIZE = 300
SMALL_POSITION_SIZE = 500
LARGE_POSITION_SIZE = 700

SMALL_POSITION_PT = 0.3
LARGE_POSITION_PT = 0.2

canPlaceOrders = False
tradeEMAStrategy = False
tradeReversalStrategy = False
tradeHighTightFlagStrategy = False
tradeFlatTopBreakoutStrategy = True
tradeMorningBreakoutStrategy = False
trade3BarReversalStrategy = True
trade25CentReversalStrategy = True
tradeOversoldReversalStrategy = True

EMA = json.load(open('EMA.json', 'r'))

useEMAstop = False