'''
    CSV files column names
'''

#--------------------------------------------------------------------------------------------------
#   Strategy Detail report column names
DATE='Date'
OPEN='Open'
HIGH='High'
LOW = 'Low'
CLOSE = 'Close'
VOLUME = 'Volume'
SPLIT = 'Split'
HICHAN = 'HiChan'
LOCHAN = 'LoChan'
ORDERS = 'Orders'
FILLS = 'Fills'
POSITION = 'Position'
TXN_PL = 'Txn P/L'
CASH = 'Cash'
BV = 'BV'
MV = 'MV'
POSN_PL = 'Posn P/L'

#--------------------------------------------------------------------------------------------------
#   raw PL file names
NORM_PL = 'NormalizedPL'

#--------------------------------------------------------------------------------------------------
#   Detail output file column names
PL='PL'

#--------------------------------------------------------------------------------------------------
#   Detail derived / calculated
CUM_PL=0.0
FILL_ACTION = 'FillAction'
FILL_QTY = 'FillQty'
FILL_PRICE = 'FillPrice'


#--------------------------------------------------------------------------------------------------
#   Summary csv column name constants
PORTFOLIO = 'Portfolio'
EQUITY = 'Equity'
STRATEGY = 'Strategy'
ANALYSIS = 'Strategy'       # alias for STRATEGY
DAYS = 'Days'
TRADE_GAINS = 'TradeGains'
TRADE_LOSSES = 'TradeLosses'
COMMISSIONS = 'Comms'
SKID = 'Skid'
EARNINGS = 'ETD'
EPD = 'EPD'
ROI = 'ROI%'
TXNS = 'Txns'
GTPerTXN = 'GT/Txn'
EPerTXN = 'E/Txn'
GPerTXN = 'G/Txn'
LPerTXN = 'L/Txn'
LONG_GAINS = 'Long Gain'
LONG_LOSSES = 'Long Loss'
SHORT_GAINS = 'Short Gain'
SHORT_LOSSES = 'Short Loss'
MAX_GAIN = 'Max Gain'
MAX_LOSS = 'Max Loss'

#   Summary derived / calculated
ME_RATIO = 'MaxGain/ETD'  # to identify if a single trade is dominating result
R_GT = 'R_GT'
R_MER = 'R_MER'
R_ROI = 'R_ROI'
R_COMP = 'R_COMP'
R_AVG = 'R_AVG'
