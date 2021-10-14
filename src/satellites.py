import pandas as pd
import numpy as np
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import seaborn as sns

from web_scraper import get_file_from_ucs_page

def clean_sat_df(df_orig):
    """Clean the dataframe: 
    - Remove null, unnamed columns
    - Create new fields from existing columns

    We know from earlier exploration of the dataset that all unnamed columns have no useful information.
    Only a few unnamed cols have any data at all, and only for <10 rows as of 2021 May.
    None of these columns are worth keeping, so they will be dropped.
    """
    valid_cols = [col for col in df_orig.columns if "unnamed:" not in col.lower()]
    df = df_orig[valid_cols].copy()
    
    return df

def get_satellites_df(fname):
    """Read in the csv file saved from the UCS website."""
    orig_sat_df = pd.read_excel(fname)
    sat_df = clean_sat_df(orig_sat_df)

    return sat_df

def main():
    filename = get_file_from_ucs_page()
    df = get_satellites_df(filename)
    print(df.head())

if __name__ == '__main__':
    main()
