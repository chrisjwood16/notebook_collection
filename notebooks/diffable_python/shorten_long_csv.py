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

# # Notebook to investigate linking MSOA to ONS Coastal Towns data

# ### Imports

import os
import pandas as pd

# ### Read CSV from ONS

df = pd.read_csv('gridall.csv', nrows=999999)
df


