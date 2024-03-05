#testing area for functions

import os
from scripts.yahoofinance import create_dataframe
from scripts.ml_buysellfx import predict_trading_signals
from scripts.profit_calc import calculate_profit
from scripts.ml_chart_export import plot_stock_signals,interactive_plot_stock_signals,first_buy_record,Last_record
from scripts.excel_export import export_df_to_excel_with_chart
from EmailBody.emailbody import generate_email_body
from scripts.sendemail import send_email

stock='TEAM'
email=["dan@y-data.co"]

df,company_details=create_dataframe(tickerSymbol=stock)
company_name = company_details['CompanyName'].iloc[0]

print('CompanyName:',company_name)

test_df, accuracy, precision, recall, f1, feature_importances,importance_df,metrics_df=predict_trading_signals(df)
profit=calculate_profit(test_df)

chart = plot_stock_signals(df=profit, tickerSymbol=stock)
firstbuy=first_buy_record(df=profit)
Last_transaction=Last_record(df=profit)
export = export_df_to_excel_with_chart(df=profit, tickerSymbol=stock)

Body=generate_email_body(tickerSymbol=company_name)
send=send_email(email_body=Body,recipient_emails=email)


