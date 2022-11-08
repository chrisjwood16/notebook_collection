# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Coastal Towns lookup

A notebook to explore the use of using MSOA codes to identify 

# ### Imports

import os
import pandas as pd

# ### Read CSV from ONS

df_MSOA_to_BUA_BUASD = pd.read_csv('MSOA_(2011)_to_BUASD_to_BUA_to_LAD_to_Region_(December_2011)_Lookup_in_England_and_Wales.csv', usecols=['MSOA11CD','BUASD11CD','BUA11CD'])
df_MSOA_to_BUA_BUASD

df_ONS_coastal = pd.read_csv('ONS_coastal_BUA_BUASU.csv')
df_ONS_coastal

df_BUASD = pd.merge(df_MSOA_to_BUA_BUASD, df_ONS_coastal, how='inner', left_on = 'BUASD11CD', right_on = 'Town Code')
df_BUASD

df_BUA = pd.merge(df_MSOA_to_BUA_BUASD, df_ONS_coastal, how='inner', left_on = 'BUA11CD', right_on = 'Town Code')
df_BUA

df_coastal_lookup = pd.concat([df_BUASD, df_BUA])
df_coastal_lookup

dftest = pd.read_csv('codetest.csv')
dftest

df_test = pd.merge(dftest, df_coastal_lookup, how='left', left_on = 'Code', right_on = 'MSOA11CD')
df_test


