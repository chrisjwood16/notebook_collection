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

# ### Notebook to check oral androgen deprivation therapy data
#
# A notebook using [English Prescribing Data](https://www.nhsbsa.nhs.uk/prescription-data/prescribing-data/english-prescribing-data-epd) to compare codelists used by OpenPrescribing measure against study findings.
#
# - [Imports](#IMPORTS)
# - [Standard functions](#FUNCTIONS)
# - [OpenPrescribing BNF codes](#OPBNF)
# - [Item / quantity plots](#CHARTS)
# - [Injections of different durations](#INJDURATION)

# <a id='IMPORTS'></a>
# ### Imports
# Import libraries required for analysis

# +
#import libraries required for analysis
from ebmdatalab import bq
import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

#set to display all rows in data
#pd.set_option('display.max_rows', None)
# -

# <a id='FUNCTIONS'></a>
# ### Standard functions
# Setup standard functions

def plot(df, column_to_plot, chart_title, y_label, y_min='default', y_max='default', lockdownline=False):
    ax = df.groupby(["month"])[column_to_plot].sum().plot(kind='line', title=chart_title)
    plt.xticks(rotation=90);
    plt.ylabel(y_label);
    if (y_min!='default'):
        plt.ylim((y_min, y_max));
    else:
        y_max=df[column_to_plot].max() * 1.05
    if (lockdownline):
        plt.vlines(x=[pd.to_datetime("2020-03-23")], ymin=0, ymax=int(y_max), colors="red", ls="--", label="Start of restrictions");
    plt.grid();


# <a id='OPBNF'></a>
# ### OpenPrescribing BNF codes
# Get [English Prescribing Data](https://www.nhsbsa.nhs.uk/prescription-data/prescribing-data/english-prescribing-data-epd) for monthly items and quantity for BNF codes from codelists:
# - [Oral ADT](https://www.opencodelists.org/codelist/user/agleman/oral-adt-prostate-ca-dmd/1e2a36a0/)
# - [Injectable ADT](https://www.opencodelists.org/codelist/user/agleman/adt-injectable-dmd/20f9318d/)
#

# +
#OpenPrescribing BNF codes
sql = '''
SELECT
     CAST(month AS DATE) AS month,
     SUM (CASE WHEN bnf_code IN ("0803042A0AAAAAA", "0803042A0AAABAB", "0803042A0AAACAC", "0803042A0AAADAD", "0803042A0BBAAAA",
                                 "0803042A0BBABAB", "0803042E0AAAAAA", "0803042E0AAABAB", "0803042E0AAADAD", "0803042E0AAAEAE", 
                                 "0803042E0AAAFAF", "0803042E0AAAHAH", "0803042E0AAAIAI", "0803042E0BBAAAA", "0803042E0BBABAB", 
                                 "0803042H0AAAAAA", "0803042H0BBAAAA", "0803042H0BCAAAA")  THEN items ELSE 0 END) as OralADTitems,
     SUM (CASE WHEN bnf_code IN ("0803042A0AAAAAA", "0803042A0AAABAB", "0803042A0AAACAC", "0803042A0AAADAD", "0803042A0BBAAAA",
                                 "0803042A0BBABAB", "0803042E0AAAAAA", "0803042E0AAABAB", "0803042E0AAADAD", "0803042E0AAAEAE", 
                                 "0803042E0AAAFAF", "0803042E0AAAHAH", "0803042E0AAAIAI", "0803042E0BBAAAA", "0803042E0BBABAB", 
                                 "0803042H0AAAAAA", "0803042H0BBAAAA", "0803042H0BCAAAA")  THEN quantity ELSE 0 END) as OralADTqty,
     SUM (CASE WHEN bnf_code IN ("0803042B0AAAAAA", "0803042B0BBAAAA", "0803042K0AAAAAA", "0803042K0AAABAB", "0803042K0BBAAAA", 
                                 "0803042K0BBABAB", "0803042K0BCAAAA", "0803042N0AAAAAA", "0803042N0AAABAB", "0803042N0AAACAC", 
                                 "0803042N0AAADAD", "0803042N0AAAEAE", "0803042N0AAAFAF", "0803042N0BBAAAA", "0803042N0BBABAB", 
                                 "0803042N0BBACAC", "0803042N0BBADAD", "0803042N0BCAAAA", "0803042N0BCABAE", "0803042N0BDAAAF", 
                                 "0803042P0AAAAAA", "0803042P0AAABAB", "0803042P0BBAAAA", "0803042P0BCAAAB", "0803042R0AAAAAA", 
                                 "0803042R0AAABAB", "0803042R0BBAAAA", "0803042R0BBABAB", "0803042S0AAABAB", "0803042S0BCAAAB", 
                                 "0803042W0AAAAAA", "0803042W0BBAAAA")  THEN items ELSE 0 END) as InjADTitems,
     SUM (CASE WHEN bnf_code IN ("0803042B0AAAAAA", "0803042B0BBAAAA", "0803042K0AAAAAA", "0803042K0AAABAB", "0803042K0BBAAAA", 
                                 "0803042K0BBABAB", "0803042K0BCAAAA", "0803042N0AAAAAA", "0803042N0AAABAB", "0803042N0AAACAC", 
                                 "0803042N0AAADAD", "0803042N0AAAEAE", "0803042N0AAAFAF", "0803042N0BBAAAA", "0803042N0BBABAB", 
                                 "0803042N0BBACAC", "0803042N0BBADAD", "0803042N0BCAAAA", "0803042N0BCABAE", "0803042N0BDAAAF", 
                                 "0803042P0AAAAAA", "0803042P0AAABAB", "0803042P0BBAAAA", "0803042P0BCAAAB", "0803042R0AAAAAA", 
                                 "0803042R0AAABAB", "0803042R0BBAAAA", "0803042R0BBABAB", "0803042S0AAABAB", "0803042S0BCAAAB", 
                                 "0803042W0AAAAAA", "0803042W0BBAAAA")  THEN quantity ELSE 0 END) as InjADTqty,
 FROM hscic.normalised_prescribing
 WHERE month >= '2015-01-01'
 GROUP BY month
 ORDER BY month'''

OP_DF = bq.cached_read(sql, csv_path=os.path.join('../..','data','OPADT.csv'))
# -

OP_DF.dtypes

OP_DF['OralADTqty_per_item']=OP_DF['OralADTqty']/OP_DF['OralADTitems']
OP_DF['InjADTqty_per_item']=OP_DF['InjADTqty']/OP_DF['InjADTitems']
OP_DF

# <a id='CHARTS'></a>
# ### Item/quantity plots
#
# Generate plots from data in above
# 1. Injectable ADT items dispensed per month - from English Prescribing Dataset
# 2. Injectable ADT quantity dispensed per month - from English Prescribing Dataset
# 3. Injectable ADT quantity per item dispensed per month - from English Prescribing Dataset
# 4. Oral ADT items dispensed per month - from English Prescribing Dataset
# 5. Oral ADT quantity dispensed per month - from English Prescribing Dataset
# 6. Oral ADT quantity per item dispensed per month - from English Prescribing Dataset

plot(
    df=OP_DF, 
    column_to_plot='InjADTitems', 
    chart_title="Injectable ADT items per month - y-axis starts at 0", 
    y_label='Items', 
    y_min=0, 
    y_max=OP_DF['InjADTitems'].max() * 1.05, 
    lockdownline=True
)

plot(
    df=OP_DF, 
    column_to_plot='InjADTqty', 
    chart_title="Injectable ADT quantity per month - y-axis starts at 0", 
    y_label='Items', 
    y_min=0, 
    y_max=OP_DF['InjADTqty'].max() * 1.05, 
    lockdownline=True
)

plot(
    df=OP_DF, 
    column_to_plot='InjADTqty_per_item', 
    chart_title="Injectable ADT quantity per item month - y-axis starts at 0", 
    y_label='Quantity per item', 
    y_min=0, 
    y_max=OP_DF['InjADTqty_per_item'].max() * 1.05, 
    lockdownline=True
)

plot(
    df=OP_DF, 
    column_to_plot='OralADTitems', 
    chart_title="Oral ADT items per month", 
    y_label='Items', 
    y_min=0, 
    y_max=OP_DF['OralADTitems'].max() * 1.05, 
    lockdownline=True
)

plot(
    df=OP_DF, 
    column_to_plot='OralADTqty', 
    chart_title="Oral ADT quantity per month", 
    y_label='Items', 
    y_min=0, 
    y_max=OP_DF['OralADTqty'].max() * 1.05, 
    lockdownline=True
)

plot(
    df=OP_DF, 
    column_to_plot='OralADTqty_per_item', 
    chart_title="Oral ADT quantity per item per month", 
    y_label='Quantity per item', 
    y_min=0, 
    y_max=OP_DF['OralADTqty_per_item'].max() * 1.05, 
    lockdownline=True
)

# <a id='INJDURATION'></a>
# ### 1 month / 3 month / 6 month injections
#
# Generate plots from data in above
# 1. Oral ADT items dispensed per month - from English Prescribing Dataset
# 2. Oral ADT quantity dispensed per month - from English Prescribing Dataset
# 3. Injectable ADT items dispensed per month - from English Prescribing Dataset
# 4. Injectable ADT quantity dispensed per month - from English Prescribing Dataset

# +
#OpenPrescribing BNF codes
sql = '''
SELECT
     CAST(month AS DATE) AS month,
     SUM (CASE WHEN bnf_code IN ("0803042K0AAAAAA", "0803042K0BBAAAA", "0803042K0BCAAAA", "0803042N0AAAAAA", "0803042N0AAACAC", 
                                 "0803042N0BBAAAA", "0803042N0BBACAC", "0803042N0BCAAAA", "0803042P0AAAAAA", "0803042P0AAABAB", 
                                 "0803042P0BBAAAA", "0803042P0BCAAAB")  THEN items ELSE 0 END) as monthly,
     SUM (CASE WHEN bnf_code IN ("0803042K0AAABAB", "0803042K0BBABAB", "0803042N0AAABAB", "0803042N0AAADAD", "0803042N0AAAEAE", 
                                 "0803042N0AAAFAF", "0803042N0BBABAB", "0803042N0BBADAD", "0803042N0BCABAE", "0803042N0BDAAAF", 
                                 "0803042P0AAACAC", "0803042P0BBABAC", "0803042S0AAACAC", "0803042W0BBAAAA", "0803042W0AAAAAA")  THEN items ELSE 0 END) as three_monthly,
     SUM (CASE WHEN bnf_code IN ("0803042S0AAABAB", "0803042S0BCAAAB")  THEN items ELSE 0 END) as six_monthly,
 FROM hscic.normalised_prescribing
 WHERE month >= '2015-01-01'
 GROUP BY month
 ORDER BY month'''

OP_duration = bq.cached_read(sql, csv_path=os.path.join('../..','data','OPinjduration.csv'))
OP_duration
# -

plot(
    df=OP_duration, 
    column_to_plot='monthly', 
    chart_title="Monthly injectable ADT items per month", 
    y_label='Items', 
    y_min=0, 
    y_max=OP_duration['monthly'].max() * 1.05, 
    lockdownline=True
)

plot(
    df=OP_duration, 
    column_to_plot='three_monthly', 
    chart_title="3 Monthly injectable ADT items per month", 
    y_label='Items', 
    y_min=0, 
    y_max=OP_duration['three_monthly'].max() * 1.05, 
    lockdownline=True
)

plot(
    df=OP_duration, 
    column_to_plot='six_monthly', 
    chart_title="6 Monthly injectable ADT items per month", 
    y_label='Items', 
    y_min=0, 
    y_max=OP_duration['six_monthly'].max() * 1.05, 
    lockdownline=True
)

OP_duration['sixm_normalised']=OP_duration['six_monthly']*6
OP_duration['threem_normalised']=OP_duration['three_monthly']*3
OP_duration['normalised']=OP_duration['monthly']+OP_duration['three_monthly']+OP_duration['six_monthly']

plot(
    df=OP_duration, 
    column_to_plot='normalised', 
    chart_title="Normalised to Monthly injectable ADT items per month", 
    y_label='Normalised items', 
    y_min=0, 
    y_max=OP_duration['normalised'].max() * 1.05, 
    lockdownline=True
)




