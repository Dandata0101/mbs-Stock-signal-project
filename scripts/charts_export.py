# Paths and directory
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd
import numpy as np
import openpyxl
import warnings
warnings.filterwarnings('ignore')

from scripts.buysellfx import buysellfx
from scripts.buysellfx import dfstock
from scripts.yahoofinance import tickerSymbol

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~load final dataframe')
print('')
print('~~~~~~~~~~~~~')
print(dfstock.dtypes)
print('~~~~~~~~~~~~~')
current_directory = os.getcwd()


#charting data -----------------------------------------------------------
plt.figure(figsize=(15, 5))
plt.plot(dfstock.index,dfstock['Close'].values,label=tickerSymbol)
plt.plot(dfstock.index,dfstock['pricebuy'].values,color='red',label='Buy signal',marker='^',markersize=12)
plt.plot(dfstock.index,dfstock['pricesell'].values,color='green',label='Sell signal',marker='v',markersize=12)

n = 5  # Adjust n as per your data
plt.xticks(ticks=dfstock.index[::n], labels=dfstock.index[::n])
plt.xticks(rotation=-75)

plt.legend()
plt.xlabel('Date',fontsize=12)
plt.ylabel('price USD ($)',fontsize=12)
plt.grid()

print('')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~export chart image')
plt.savefig(current_directory+'/02-charts/chart.png', bbox_inches='tight')
plt.close()  
