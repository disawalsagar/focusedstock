

import requests
import pandas as pd
from functools import reduce

#%%
import sys
sys.path
sys.path.append(r'C:\Users\sdisawal\Desktop\Stocks\Code\secrets_key.py')
import secrets_key as sk 

#%%
api_key = sk.fmp_api_key()
#%%
p_df = pd.read_csv('rbh.csv')
tickers = p_df["Symbol"].to_list()
 
#%%
###################### Data Ingestion ######################
def fin_dfs(tickers, st_type):
    df = pd.DataFrame()
    for ticker in tickers:
        mk_url = "https://financialmodelingprep.com/api/v3/{}/{}?limit=120&apikey={}".format(st_type,ticker,api_key)
        st = requests.get(mk_url)
        st_j = st.json()
        df = df.append(pd.DataFrame(st_j))      
    return df


df_bal = fin_dfs(tickers, "balance-sheet-statement") 
df_inc = fin_dfs(tickers, "income-statement") 
df_qte = fin_dfs(tickers, "quote") 
df_cf = fin_dfs(tickers, "cash-flow-statement") 

##################### Data Preparation #########################
#%%
def lat_dts(df):
    df_1 = df.groupby(by=["symbol"], dropna=True, as_index=False).apply(lambda x: x.sort_values(["date"], ascending = False)).reset_index(drop=True)
    df_srtd = df_1.groupby('symbol').head(1).reset_index(drop=True)
    return df_srtd

#%%
df_inc_1 = df_inc[["symbol","date","ebitda" , "depreciationAndAmortization", "netIncome" ]]
df_inc_intr = lat_dts(df_inc_1)

#%%
df_qte_intr = df_qte[["symbol","marketCap" , "name"]]
#df_qte_intr = lat_dts(df_qt1_1)

#%%
df_cf_1 = df_cf[["symbol","date","netCashProvidedByOperatingActivities", "capitalExpenditure"]]
df_cf_intr = lat_dts(df_cf_1)

#%%
df_bal_1 = df_bal[["symbol","date","totalDebt","totalCurrentAssets", "propertyPlantEquipmentNet", "totalCurrentLiabilities", "longTermDebt", "totalStockholdersEquity","cashAndShortTermInvestments"]].copy()
df_bal_intr = lat_dts(df_bal_1)


######################## Magic Formula Calcluation ############################
#%%

dfs= [df_inc_intr, df_cf_intr,df_bal_intr, df_qte_intr]
df_f = reduce(lambda left,right: pd.merge(left,right,on=['symbol']), dfs)
df_f = df_f.fillna(0)
df_f["EBIT"] = df_f["ebitda"] - df_f["depreciationAndAmortization"]
df_f["EnterpriseValue"] = df_f["marketCap"] + df_f["totalDebt"] - (df_f["totalCurrentAssets"]-df_f["totalCurrentLiabilities"])
df_f["EarningYield"] = df_f["EBIT"]/df_f["EnterpriseValue"]
df_f["FCFYield"] = (df_f["netCashProvidedByOperatingActivities"] - df_f["capitalExpenditure"])/df_f["marketCap"]
df_f["ROC"]  = df_f["EBIT"]/(df_f["propertyPlantEquipmentNet"]+ df_f["totalCurrentAssets"]-df_f["totalCurrentLiabilities"])


#%%
df_f["CombRank"] = df_f["EarningYield"].rank(ascending=False,na_option='bottom')+ df_f["ROC"].rank(ascending=False,na_option='bottom')
df_f["MagicRank"] = df_f["CombRank"].rank(method='first')

df_final = df_f[["name", "symbol", "MagicRank"]].sort_values("MagicRank").reset_index(drop=True)



