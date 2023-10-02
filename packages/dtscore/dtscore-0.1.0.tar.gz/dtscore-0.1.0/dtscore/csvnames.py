"""
    CSV files column names
"""

#--------------------------------------------------------------------------------------------------
#   Detail csv column names
CSV_DATE="Date"
CSV_OPEN='Open'
CSV_HIGH='High'
CSV_LOW = 'Low'
CSV_CLOSE = 'Close'
CSV_VOLUME = 'Volume'
CSV_SPLIT = 'Split'
CSV_HICHAN = 'HiChan'
CSV_LOCHAN = 'LoChan'
CSV_ORDERS = 'Orders'
CSV_FILLS = 'Fills'
CSV_POSITION = 'Position'
CSV_TXN_PL = 'Txn P/L'
CSV_CASH = 'Cash'
CSV_BV = 'BV'
CSV_MV = 'MV'
CSV_POSN_PL = 'Posn P/L'

#--------------------------------------------------------------------------------------------------
#   raw PL file names
CSV_NORM_PL = 'NormalizedPL'

#--------------------------------------------------------------------------------------------------
#   Detail output file column names
CSV_PL="PL"

#--------------------------------------------------------------------------------------------------
#   Detail derived / calculated
CSV_CUM_PL=0.0
CSV_FILL_ACTION = 'FillAction'
CSV_FILL_QTY = 'FillQty'
CSV_FILL_PRICE = 'FillPrice'


#--------------------------------------------------------------------------------------------------
#   Summary csv column name constants
CSV_EQUITY = "Equity"
CSV_ANALYSIS = "Strategy"
CSV_STRATEGY = "Strategy"       # alias for CSV_ANALYSIS
CSV_DAYS = "Days"
CSV_TRADE_GAINS = "TradeGains"
CSV_TRADE_LOSSES = "TradeLosses"
CSV_COMMISSIONS = "Comms"
CSV_SKID = "Skid"
CSV_EARNINGS = "ETD"
CSV_EPD = "EPD"
CSV_ROI = "ROI%"
CSV_TXNS = "Txns"
CSV_GTPerTXN = "GT/Txn"
CSV_EPerTXN = "E/Txn"
CSV_GPerTXN = "G/Txn"
CSV_LPerTXN = "L/Txn"
CSV_LONG_GAINS = "Long Gain"
CSV_LONG_LOSSES = "Long Loss"
CSV_SHORT_GAINS = "Short Gain"
CSV_SHORT_LOSSES = "Short Loss"
CSV_MAX_GAIN = "Max Gain"
CSV_MAX_LOSS = "Max Loss"

#   Summary derived / calculated
CSV_MAXGAIN_EARNINGS_RATIO = "MaxGain/ETD"  # to identify if a single trade is dominating result
CSV_R_GT = 'R_GT'
CSV_R_MER = 'R_MER'
CSV_R_ROI = 'R_ROI'
CSV_R_COMP = 'R_COMP'
CSV_R_AVG = 'R_AVG'
