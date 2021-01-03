# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 19:03:56 2021

@author: sdisawal
"""

import pandas as pd
from datetime import datetime
import datapackage
import numpy as np


def get_snp_list():
    data_url = 'https://datahub.io/core/s-and-p-500-companies-financials/datapackage.json'
    package = datapackage.Package(data_url)
    resources = package.resources
    for resource in resources:
        if resource.tabular:
            data = pd.read_csv(resource.descriptor['path'])
    return data     