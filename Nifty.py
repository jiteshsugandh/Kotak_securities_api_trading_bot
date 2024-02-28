from nsetools import Nse
import LatestData as LD
import Login as L
import pandas as pd

nse = Nse()

#fetching fno data
fDataFrame = pd.read_csv(LD.fnourl,sep='|')
df = fDataFrame

NIFTY_LTP =  nse.get_index_quote('NIFTY 50')['lastPrice']
#print(NIFTY_LTP)

# Rounding last traded price for ATM strike to a multiple of 50 and 100
ATM_STRIKE = (50 * round(NIFTY_LTP/50))
#print(ATM_STRIKE)

# #Short Strangle for NIFTY50
CE_Strike = ATM_STRIKE + 100
PE_Strike = ATM_STRIKE - 100

#fetching instrument token
Option_Call = df[((df.segment == 'FO') & (df.instrumentType == 'OI') & (df.instrumentName == 'NIFTY') & (df.strike == CE_Strike) & (df.optionType == 'CE'))]
Option_Put = df[((df.segment == 'FO') & (df.instrumentType == 'OI') & (df.instrumentName == 'NIFTY') & (df.strike == PE_Strike) & (df.optionType == 'PE'))]

Token_number_CE = Option_Call['instrumentToken'].iloc[0]
Token_number_PE = Option_Put['instrumentToken'].iloc[0]

CE_Trade_details = Option_Call[['instrumentName','expiry','strike','optionType']].iloc[0]
PE_Trade_details = Option_Put[['instrumentName','expiry','strike','optionType']].iloc[0]
print(CE_Trade_details)
print(PE_Trade_details)

CE_QUOTE = L.client.quote(instrument_token = str(Token_number_CE)).get('success')[0].get('ltp')
PE_QUOTE = L.client.quote(instrument_token = str(Token_number_PE)).get('success')[0].get('ltp')

print(CE_QUOTE)
print(PE_QUOTE)

#NIFTY, NIFTY_LTP,ATM_STRIKE,EXPIRY

#short selling
def Strangle_Order():
    
    # Place an order NIFTY ATM CALL
    L.client.place_order(order_type = "N", instrument_token = Token_number_CE, transaction_type = "SELL",\
                       quantity = 1, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                            validity = "GFD", variety = "REGULAR", tag = "string")
     
     # Place an order NIFTY ATM PUT
    L.client.place_order(order_type = "N", instrument_token = Token_number_PE, transaction_type = "SELL",\
                       quantity = 1, price = 0, disclosed_quantity = 0, trigger_price = 0,\
                            validity = "GFD", variety = "REGULAR", tag = "string")



    lastPrice_CE = float(L.client.quote(instrument_token = Token_number_CE).get('success')[0].get('ltp'))
    lastPrice_PE = float(L.client.quote(instrument_token = Token_number_PE).get('success')[0].get('ltp'))

    StopLoss_CE = (lastPrice_CE * 1.3)
    SL_CE = (0.1 * round(StopLoss_CE / 0.1))

    StopLoss_PE = (lastPrice_PE * 1.3)
    SL_PE = (0.1 * round(StopLoss_PE / 0.1))
    
     # Place an SL order NIFTY ATM CALL
    L.client.place_order(order_type = "N", instrument_token = Token_number_CE, transaction_type = "BUY",\
                       quantity = 1, price = 0, disclosed_quantity = 0, trigger_price = SL_CE,\
                            validity = "GFD", variety = "REGULAR", tag = "string")

   
    # Place an SL order NIFTY ATM PUT
    L.client.place_order(order_type = "N", instrument_token = Token_number_PE, transaction_type = "BUY",\
                       quantity = 1, price = 0, disclosed_quantity = 0, trigger_price = SL_PE,\
                            validity = "GFD", variety = "REGULAR", tag = "string")