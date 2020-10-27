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
from alpha_vantage.fundamentaldata  import FundamentalData 
import pandas as pd
import time

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

    for ticker in tickers:

        if st_type == "income-statement":
            data, metadata = fd.get_income_statement_annual(symbol=ticker)
            df['Ticker'] = ticker
            df = df.append(data)
            
            
        elif st_type == "balance-sheet-statement":
            data, metadata = fd.get_balance_sheet_annual(symbol=ticker)
            df['Ticker'] = ticker
            df = df.append(data)
            
        
        elif st_type == "cash-flow-statement":
            data, metadata = fd.get_cash_flow_annual(symbol=ticker)
            data['Ticker'] = ticker
            df = df.append(data)
        
        elif st_type == "quote":
            data, metadata = fd.get_company_overview(symbol=ticker)
            data['Ticker'] = ticker
            df = df.append(data)
        
        api_call_count+=1
        if api_call_count==5:
            api_call_count = 1
            time.sleep(60 - ((time.time() - start_time) % 60.0))
    
    return df


#df_bal = fin_dfs(tickers, "balance-sheet-statement") 
#df_inc = fin_dfs(tickers, "income-statement") 
df_qte = fin_dfs(tickers, "quote") 
#df_cf = fin_dfs(tickers, "cash-flow-statement")  
#%%
df_qte.to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\qte.csv', header=True, index=False)
df_bal.to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\bal.csv')
df_inc.to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\inc.csv')
df_cf.to_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\cf.csv')

#%%
df_bal = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\bal.csv')
df_inc = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\inc.csv')
df_cf = pd.read_csv(r'C:\Users\sdisawal\Desktop\Stocks\Code\csv\cf.csv')

#%%
def lat_dts(df):
    df_1 = df.groupby(by=["Ticker"], dropna=True, as_index=False).apply(lambda x: x.sort_values(["fiscalDateEnding"], ascending = False)).reset_index(drop=True)
    df_srtd = df_1.groupby("Ticker").head(1).reset_index(drop=True)
    return df_srtd

#%%
df_inc_1 = df_inc[["Ticker","fiscalDateEnding","ebit" , "netIncome"]]
df_inc_intr = lat_dts(df_inc_1)

#%%
df_qte_1 = df_qte[["Ticker","MarketCapitalization" , "Name"]]
df_qte_intr = lat_dts(df_qte_1)

#%%
df_cf_1 = df_cf[["Ticker","fiscalDateEnding","operatingCashflow", "capitalExpenditures"]]
df_cf_intr = lat_dts(df_cf_1)

#%%
df_bal_1 = df_bal[["Ticker","fiscalDateEnding","totalLiabilities","totalCurrentAssets",  "totalAssets" ,"propertyPlantEquipment", "totalCurrentLiabilities", "longTermDebt", "totalShareholderEquity","cash"]].copy()
df_bal_intr = lat_dts(df_bal_1)


######################## Magic Formula Calculation ############################
#%%

dfs= [df_inc_intr, df_cf_intr,df_bal_intr, df_qte_intr]
df_f = reduce(lambda left,right: pd.merge(left,right,on=['symbol']), dfs)
df_f = df_f.fillna(0)
df_f["EBIT"] = df_f["ebitda"] - df_f["depreciationAndAmortization"]
df_f["EnterpriseValue"] = df_f["marketCap"] + df_f["totalDebt"] - (df_f["totalCurrentAssets"]-df_f["totalCurrentLiabilities"])
df_f["EarningYield"] = df_f["EBIT"]/df_f["EnterpriseValue"]
df_f["FCFYield"] = (df_f["netCashProvidedByOperatingActivities"] - df_f["capitalExpenditure"])/df_f["marketCap"]
df_f["ROC"]  = df_f["EBIT"]/(df_f["propertyPlantEquipmentNet"]+ df_f["totalCurrentAssets"]-df_f["totalCurrentLiabilities"])


