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

# # SNOMED refset extraction
# A notebook to extract medication code lists from SNOMED ref sets

#import libraries required for analysis
import os
import pandas as pd

df = pd.read_csv(os.path.join('..','data/TRUD','der2_Refset_SimpleUKDGFull_GB1000001_20220706.txt'), sep='\t')
df

ampdf = pd.read_xml(os.path.join('..','data/TRUD','f_amp2_3010922.xml'), xpath="/ACTUAL_MEDICINAL_PRODUCTS/AMPS")
ampdf

df_refset_to_get = pd.read_csv(os.path.join('..','data','refset_to_get.csv'), sep='\t')
df_refset_to_get = df_refset_to_get[['Cluster name', 'SNOMED CT']]
refset_to_get_dict=dict(zip(df_refset_to_get['SNOMED CT'], df_refset_to_get['Cluster name']))
refset_to_get_dict

for key in refset_to_get_dict:
    refsetinput=key
    refsetnameinput=refset_to_get_dict[key]
    #refsetnameinput=input("Enter refset name:")
    #refsetinput=int(input("Enter refset ID:"))
    refsetcomponents=df.loc[(df['active'] == 1) & (df['refsetId'] == refsetinput)]
    refsetcomponents=refsetcomponents['referencedComponentId']
    refsetcomponents.to_csv(os.path.join('..','data/refsets',refsetnameinput+'.csv'), index=False)


