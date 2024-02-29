#testing area for functions

import os
from scripts.yahoofinance import create_dataframe
from scripts.buysellfx import buysellfx
from scripts.ml_buysellfx import predict_trading_signals
from scripts.ml_chart_export import plot_stock_signals,interactive_plot_stock_signals,Last_record

from scripts.profit_calc import calculate_profit
from scripts.excel_export import export_df_to_excel_with_chart
from EmailBody.emailbody import generate_email_body
from scripts.sendemail import send_email


stock='AMZN'
email=["dan@y-data.co"]

data=create_dataframe(stock)

fx=buysellfx(data)    

chart=plot_stock_signals(df=fx,tickerSymbol=stock)
export=export_df_to_excel_with_chart(df=fx,tickerSymbol=stock)


#Body=generate_email_body(tickerSymbol=stock)
#send=send_email(email_body=Body,recipient_emails=email)

last=Last_record(fx)

