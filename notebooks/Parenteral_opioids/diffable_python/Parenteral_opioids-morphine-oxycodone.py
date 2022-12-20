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

# ### Notebook to investigate parenteral opioid dispensing trends
# A notebook using [English Prescribing Data](https://www.nhsbsa.nhs.uk/prescription-data/prescribing-data/english-prescribing-data-epd) to investigate trends in parenteral opioid dispensing data.
# - [Imports](#IMPORTS)
# - [Standard functions](#FUNCTIONS)
# - [OpenPrescribing data extract](#OPBNF)
# - [Item plots](#CHARTS)

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
# ### OpenPrescribing data extract
# Get [English Prescribing Data](https://www.nhsbsa.nhs.uk/prescription-data/prescribing-data/english-prescribing-data-epd) from BigQuery for monthly items based on BNF codes in this [morphine codelist](https://www.opencodelists.org/codelist/opensafely/morphine-subcutaneous-dmd/1185fc5b/) and this [oxycodone codelist](https://www.opencodelists.org/codelist/opensafely/oxycodone-subcutaneous-dmd/2a956f90/).

# +
#OpenPrescribing BNF codes
sql = '''
SELECT
     CAST(month AS DATE) AS month,
     SUM (CASE WHEN bnf_code IN ("0407020Q0AAA2A2", "0407020Q0AAA3A3", "0407020Q0AAA4A4", "0407020Q0AAA5A5", "0407020Q0AAA8A8",
                                 "0407020Q0AAAAAA", "0407020Q0AAABAB", "0407020Q0AAACAC", "0407020Q0AAADAD", "0407020Q0AAAEAE", 
                                 "0407020Q0AAAFAF", "0407020Q0AAAMAM", "0407020Q0AABCBC", "0407020Q0AADIDI", "0407020Q0AAFCFC", 
                                 "0407020Q0AAFJFJ", "0407020Q0AAFKFK", "0407020Q0AAFTFT", "0407020Q0AAFVFV", "0407020Q0AAFWFW", 
                                 "0407020Q0AAFZFZ", "0407020Q0AAGAGA", "0407020Q0BEABFJ"
                                 )  THEN items ELSE 0 END) as SCMorphine,
     SUM (CASE WHEN bnf_code IN ("0407020ADAAALAL", "0407020ADAAAMAM", "0407020ADAAANAN", "0407020ADBBAFAL", "0407020ADBBAGAM", 
                                 "0407020ADBBAHAN", "0407020ADBJADAL", "0407020ADBJAEAM", "0407020ADBJAFAN"
                                 )  THEN items ELSE 0 END) as SCOxycodone,
 FROM hscic.normalised_prescribing
 WHERE month >= '2018-01-01'
 GROUP BY month
 ORDER BY month'''

OP_DF = bq.cached_read(sql, csv_path=os.path.join('../..','data','scmorphineoxycodone.csv'))
# -

OP_DF

plot(
    df=OP_DF, 
    column_to_plot='SCMorphine', 
    chart_title="SC morphine items per month", 
    y_label='Items', 
    y_min=0, 
    y_max=OP_DF['SCMorphine'].max() * 1.05, 
)

plot(
    df=OP_DF, 
    column_to_plot='SCOxycodone', 
    chart_title="SC oxycodone items per month", 
    y_label='Items', 
    y_min=0, 
    y_max=OP_DF['ParenteralOxycodone'].max() * 1.05, 
)


