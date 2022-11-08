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
import numpy as np

# +
#Read csv file containing ONS defined coastal towns - https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1005216/cmo-annual_report-2021-health-in-coastal-communities-accessible.pdf - appendix 2 - p233
df_ONS_coastal = pd.read_csv('ONS_coastal_BUA_BUASU_(2021).csv')

#Read csv file containing ONS MSOA lookup file - https://geoportal.statistics.gov.uk/datasets/lower-layer-super-output-area-2011-to-built-up-area-sub-division-to-built-up-area-to-local-authority-district-to-region-december-2011-lookup-in-england-and-wales/explore
df_LSOA_to_BUA_BUASD = pd.read_csv('LSOA_(2011)_to_BUASD_to_BUA_to_LAD_to_Region_(December_2011)_Lookup_in_England_and_Wales.csv', usecols=['LSOA11CD','BUASD11CD','BUA11CD'])

#Read csv file containing ONS LSOA to IMD lookup file - https://geoportal.statistics.gov.uk/datasets/index-of-multiple-deprivation-december-2019-lookup-in-england/explore
df_LSOA_to_IMD = pd.read_csv('Index_of_Multiple_Deprivation_(December_2019)_Lookup_in_England.csv', usecols=['LSOA11CD','IMD19'])

# +
df_BUASD = pd.merge(df_LSOA_to_BUA_BUASD, df_ONS_coastal, how='inner', left_on = 'BUASD11CD', right_on = 'Area_Code')
df_BUA = pd.merge(df_LSOA_to_BUA_BUASD, df_ONS_coastal, how='inner', left_on = 'BUA11CD', right_on = 'Area_Code')
df_coastal_lookup = pd.concat([df_BUASD, df_BUA])

df_coastal_lookup = pd.merge(df_coastal_lookup, df_LSOA_to_IMD, how='inner', left_on = 'LSOA11CD', right_on = 'LSOA11CD')

# +
conditions = [
    (df_coastal_lookup['IMD19'] >= 0) & (df_coastal_lookup['IMD19'] < 32844*1/5),
    (df_coastal_lookup['IMD19'] >= 32844*1/5) & (df_coastal_lookup['IMD19'] < 32844*2/5),
    (df_coastal_lookup['IMD19'] >= 32844*2/5) & (df_coastal_lookup['IMD19'] < 32844*3/5),
    (df_coastal_lookup['IMD19'] >= 32844*3/5) & (df_coastal_lookup['IMD19'] < 32844*4/5),
    (df_coastal_lookup['IMD19'] >= 32844*4/5) & (df_coastal_lookup['IMD19'] < 32844),
    ]

# create a list of the values we want to assign for each condition
values = [1, 2, 3, 4, 5]

# create a new column and use np.select to assign values to it using our lists as arguments
df_coastal_lookup['IMDQ'] = np.select(conditions, values)

# +
df_coastal_lookup.head()
areas=df_coastal_lookup['Area_Name'].unique()

area_column=[]
minimd_column=[]
maximd_column=[]
meanimd_column=[]
medianimd_column=[]

for area in areas:
    mask = df_coastal_lookup[df_coastal_lookup['Area_Name'] == area]
    area_column.append(area)
    minimd_column.append(mask['IMDQ'].min())
    maximd_column.append(mask['IMDQ'].max())
    meanimd_column.append(mask['IMDQ'].mean())
    medianimd_column.append(mask['IMDQ'].median())


d = {'Area_Name': area_column,'IMDmin':minimd_column, 'IMDmax': maximd_column, 'IMDmean': meanimd_column, 'IMDmedian': medianimd_column}
df_min_max_imd = pd.DataFrame(d)

# +
df_min_max_imd.to_csv('Coastal_min_max_IMD_output.csv', index=False)  

df_min_max_imd

# +
df_coastal_lookup.to_csv('Coastal_IMD_output.csv', index=False)  

df_coastal_lookup
# -


