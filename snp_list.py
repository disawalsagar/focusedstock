# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 19:03:56 2021

@author: sdisawal
"""

import pandas as pd
from datetime import datetime
import datapackage
import numpy as np

class Prepare_snp_data:
    def __init__(self):
        data_url = 'https://datahub.io/core/s-and-p-500-companies-financials/datapackage.json'
        package = datapackage.Package(data_url)
        resources = package.resources
        for resource in resources:
            if resource.tabular:
                data = pd.read_csv(resource.descriptor['path'])
        return data
        

def cal_marketcap(market_cap):
    
    if market_cap > 10000000000:
        mc='Large Cap'
    elif 2000000000 < market_cap <= 10000000000:
        mc='Mid Cap'
    elif 2000000000 >= market_cap:
        mc='Small Cap'
    else:
        mc='NA'
    return mc


def get_prepare_index_data():
    get_df = Prepare_snp_data()
    
    