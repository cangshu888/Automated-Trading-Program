Links to TD Ameritrade Account and places daytrades based on hard-coded strategies with a pre-defined list of daytrading candidates.

To use the program:
  1) Create a brokerage account with TD Ameritrade
  2) Create a developer account with TD Ameritrade
  3) Enter client ID in redirect.py and Trader.py
  4) Generate key.pm and certificate.pm files for SSL, add the files to the repo, and enter the file names in redirect.py
  5) Generate refresh token on the TD Ameritrade developer website and enter the refresh token in Trader.py
  6) Enter account number in Trader.py
  
  To do daily:
    1) Enter the EMAs in EMA.json from the current trading day before the next trading day
    2) Run the program before the market opens
        To run the program, type the command 'python Trader.py'
        
        
