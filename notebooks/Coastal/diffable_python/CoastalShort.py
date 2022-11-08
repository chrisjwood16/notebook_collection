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

import pandas as pd

# +
#Read csv file containing ONS defined coastal towns - https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1005216/cmo-annual_report-2021-health-in-coastal-communities-accessible.pdf - appendix 2 - p233
df_ONS_coastal = pd.read_csv('ONS_coastal_BUA_BUASU_(2021).csv')

#Read csv file containing ONS MSOA lookup file - https://geoportal.statistics.gov.uk/maps/middle-layer-super-output-area-2011-to-built-up-area-sub-division-to-built-up-area-to-local-authority-district-to-region-december-2011-lookup-in-england-and-wales
df_MSOA_to_BUA_BUASD = pd.read_csv('MSOA_(2011)_to_BUASD_to_BUA_to_LAD_to_Region_(December_2011)_Lookup_in_England_and_Wales.csv', usecols=['MSOA11CD','BUASD11CD','BUA11CD'])



df_BUASD = pd.merge(df_MSOA_to_BUA_BUASD, df_ONS_coastal, how='inner', left_on = 'BUASD11CD', right_on = 'Town Code')
df_BUA = pd.merge(df_MSOA_to_BUA_BUASD, df_ONS_coastal, how='inner', left_on = 'BUA11CD', right_on = 'Town Code')
df_coastal_lookup = pd.concat([df_BUASD, df_BUA])
