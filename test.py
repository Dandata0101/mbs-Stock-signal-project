# Import functions from your custom modules.
from scripts.yahoofinance import create_dataframe
from scripts.buysellfx import buysellfx
from scripts.charts_export import plot_stock_signals,new_plot_stock_signals
from scripts.excel_export import export_df_to_excel_with_chart
from EmailBody.emailbody import generate_email_body
from scripts.sendemail import send_email

stock='AMZN'
email=["dan@y-data.co"]

data=create_dataframe(stock)
print(data.dtypes)

fx=buysellfx(data)
print(data.dtypes)

newchart=new_plot_stock_signals(df=fx,tickerSymbol=stock)
chart=plot_stock_signals(df=fx,tickerSymbol=stock)
export=export_df_to_excel_with_chart(df=fx,tickerSymbol=stock)


#Body=generate_email_body(tickerSymbol=stock)
#send=send_email(email_body=Body,recipient_emails=email)


