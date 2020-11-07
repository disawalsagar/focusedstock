# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 15:37:18 2020

@author: sdisawal
"""

#%% ###### Do not delete this cell ###
import sys
sys.path.append(r'C:\Users\sdisawal\Desktop\Stocks\Code')
sys.path.append(r'C:\Users\sdisawal\PycharmProjects\LearnApi\alpha_vantage')
#print(sys.path)


#%% Import Statements
import secrets_key as sk
#from alpha_vantage.fundamentaldata  import FundamentalData 
import pandas as pd
import time
from functools import reduce
import numpy as np

#%% Generate api key
api_key = sk.fmp_api_key()

#%%
fd = FundamentalData(key=api_key, output_format='pandas')

#%% 
p_df = pd.read_csv(r'C:\Users\sdisawal\python_projects\focusedstock\rbh.csv')
tickers = p_df["Symbol"].to_list() 
#%%
###################### Data Ingestion ######################
def fin_dfs(tickers, st_type):
    df = pd.DataFrame()
    start_time = time.time()
    api_call_count = 1
    global_count = 0

    for ticker in tickers:
        global_count += 1
        print("Api Count is {}, and global_count {}".format(api_call_count, global_count))
        
        if st_type == "income-statement":
            data, metadata = fd.get_income_statement_annual(symbol=ticker)
            data['Ticker'] = ticker
            df = df.append(data)
            
            
        elif st_type == "balance-sheet-statement":
            data, metadata = fd.get_balance_sheet_annual(symbol=ticker)
            data['Ticker'] = ticker
            df = df.append(data)
            
        
        elif st_type == "cash-flow-statement":
            data, metadata = fd.get_cash_flow_annual(symbol=ticker)
            data['Ticker'] = ticker
            df = df.append(data)
        
        elif st_type == "company-overview":
             data, metadata = fd.get_company_overview(symbol=ticker)
             data['Ticker'] = ticker
             df = df.append(data)
            
        
        api_call_count+=1
        if api_call_count==5:
            api_call_count = 0
            time.sleep(60 - ((time.time() - start_time) % 60.0))
    
    return df

#%%
#df_bal = fin_dfs(tickers, "balance-sheet-statement") 
#df_inc = fin_dfs(tickers, "income-statement") 
#df_qte = fin_dfs(tickers, "company-overview") 
df_cf = fin_dfs(tickers, "cash-flow-statement")  
#%%
df_bal.to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\bal.csv', header=True, index=False)
df_inc.to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\inc.csv', header=True, index=False)
df_cf.to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\cf.csv', header=True, index=False)
df_qte.to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\qte.csv', header=True, index=False)

#%%

def lat_dts(df):
    df_1 = df.groupby(by=["Ticker"], dropna=True, as_index=False).apply(lambda x: x.sort_values(["fiscalDateEnding"], ascending = False)).reset_index(drop=True)
    df_srtd = df_1.groupby('Ticker').head(1).reset_index(drop=True)
    return df_srtd

#%%
df_bal = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\bal.csv')
df_inc = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\inc.csv')
df_cf = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\cf.csv')
df_qte = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\qte.csv')
#%%

df_inc_1 = df_inc[["Ticker","ebit", "netIncome","fiscalDateEnding"]]
df_inc_intr = lat_dts(df_inc_1)
df_qte_intr = df_qte[["MarketCapitalization", "Ticker"]]
df_bal_1 = df_bal[["Ticker","propertyPlantEquipment","totalCurrentAssets","totalCurrentLiabilities", "totalLiabilities","fiscalDateEnding"]]
df_bal_intr = lat_dts(df_bal_1)
df_cf_1 = df_cf[["Ticker","operatingCashflow", "capitalExpenditures","fiscalDateEnding"]]
df_cf_intr = lat_dts(df_cf_1)



######################## Magic Formula Calculation ############################
#%%

dfs = [df_inc_intr, df_cf_intr,df_bal_intr, df_qte_intr]
df_f = reduce(lambda left,right: pd.merge(left,right,on=['Ticker']), dfs)
#In order to first replace with string None in the dataframe, converted "None" to Nan and then used 
#fillna to convert nan with o.
df_f = df_f.replace('None', np.nan).fillna(0)
#print(df_f.head())
#df_C = df_f["ebit"].replace('None', np.nan).fillna(0)
int_cols=["ebit", "netIncome","MarketCapitalization","propertyPlantEquipment","totalCurrentAssets","totalCurrentLiabilities", "totalLiabilities","operatingCashflow", "capitalExpenditures"]
#While reading CSV by default thedefault type for certain column came to Object type which gave error in doing calculations.Also, int too small to handle int value s
df_f[int_cols] = df_f[int_cols].astype(str).astype(np.int64)
#print(df_f.dtypes)
df_f["EnterpriseValue"] = df_f["MarketCapitalization"] + df_f["totalLiabilities"]- (df_f["totalCurrentAssets"]-df_f["totalCurrentLiabilities"])
df_f["EarningYield"] = df_f["ebit"]/df_f["EnterpriseValue"]
df_f["FCFYield"] = (df_f["operatingCashflow"] - df_f["capitalExpenditures"])/df_f["MarketCapitalization"]
df_f["ROC"]  = df_f["ebit"]/(df_f["propertyPlantEquipment"]+ df_f["totalCurrentAssets"]-df_f["totalCurrentLiabilities"])


#%%
df_f["CombRank"] = df_f["EarningYield"].rank(ascending=False,na_option='bottom')+ df_f["ROC"].rank(ascending=False,na_option='bottom')
df_f["MagicRank"] = df_f["CombRank"].rank(method='first')

df_final = df_f[["Ticker", "MagicRank"]].sort_values("MagicRank").reset_index(drop=True)

#%%
df_final.to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\temp.csv', header=True, index=False)

