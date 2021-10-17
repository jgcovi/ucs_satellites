import pandas as pd
import numpy as np
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import seaborn as sns

from web_scraper import get_ucs_sat_file

def clean_sat_df(df_orig):
    """Clean the dataframe: 
    - Remove null, unnamed columns
    - Fill nulls in valid, object dtype columns for ease of groupings
    - Create new fields from existing columns

    We know from earlier exploration of the dataset that all unnamed columns have little useful 
    information. Only a few unnamed cols have any data at all (<10 rows as of 2021 May). 
    None of these columns are worth keeping, so they will be dropped.
    """
    valid_cols = [col for col in df_orig.columns if "unnamed:" not in col.lower()]
    df = df_orig[valid_cols].copy()

    # Fills nulls - currently no need to fill numerics.
    # num_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    # df[df.select_dtypes(num_types).columns] = df.select_dtypes(num_types).fillna(0)
    df[df.select_dtypes('object').columns] = df.select_dtypes('object').fillna('Unknown')

    # Calculate estimated end of lifetime
    df['Expected End Date'] = (
        df['Date of Launch'] + pd.to_timedelta(df['Expected Lifetime (yrs.)'] * 365, unit='day')
    )
    return df

def get_satellites_df(fname):
    """Read in the csv file saved from the UCS website."""
    orig_sat_df = pd.read_excel(fname)
    sat_df = clean_sat_df(orig_sat_df)

    return sat_df

def get_daily_launches(df):
    """Get a new dataframe of Date of Launch and Count of Satellites."""
    daily_launched_count = df.groupby('Date of Launch')['NORAD Number'].count().reset_index()
    daily_launched_count = daily_launched_count.rename(columns={'NORAD Number': 'n_satellites'})
    daily_launched_count = daily_launched_count.sort_values('Date of Launch')  # ensure sorted dates
    # create quantitative, incremental field for date from qualitative
    daily_launched_count['Launched Day'] = np.arange(daily_launched_count['Date of Launch'].nunique)
    return daily_launched_count

def plot_launches_over_time(daily_count_df):
    """Plot a count of satellites (by NORAD Number) launched over the timespan covered in the dataset."""
    fig, ax = plt.subplots()
    fig.set_size_inches(15, 5)
    ax.xaxis.set_major_formatter(DateFormatter('%B %Y'))

    sns.lineplot(
        x=daily_count_df['Date of Launch'], y=daily_count_df['n_satellites'], 
        linewidth=3,  color='green'
    ).set(title='Number of Satellites Launched by Date')
    plt.show()
    
def agg_metrics(df):
    """Aggregate metrics from the cleaned dataframe.
    
    How many satellites have been launched by:
    - country (of owner or operator)
    - entity (users - civil, govt, commercial)
    - purpose
    
    Who are the top owners and operators contributing to satellite launches?
    How many satellites are in GEO, MEO, LEO, and Elliptic orbit?
    """
    # store the results of a groupby operation
    # Key = grouped column, Value = Series
    count_dic = {
        'Country of Operator/Owner': None,
        'Users': None,
        'Purpose': None,
        'Operator/Owner': None,
        'Class of Orbit': None,
    }

    def count_group(col_grp, count='NORAD Number'):
        """Count the number of records in the 'count' columns for each group in column 'col_grp'.
        Generally, this should be a count of the Satellite Catalogue number (NORAD Number).

        Should be updated to be used in accord with an if-then statement,
        if any changes to agg method are needed. 
        """
        return df.groupby(col_grp)[count].count()
    
    for k in count_dic:
        count_dic[k] = count_group(k)

    return count_dic

def main(n=5):
    filename = get_ucs_sat_file()
    df = get_satellites_df(filename)
    print('Earliest satellite launch date recorded: {}'.format(
        df['Date of Launch'].min().strftime('%d %B %Y')
        )
    )
    print('Most recent satellite launch date recorded: {}\n'.format(
        df['Date of Launch'].max().strftime('%d %B %Y')
        )
    )
    # daily_count_df = get_daily_launches(df)
    # plot_launches_over_time(daily_count_df)

    print("Top {} count of launched satellites by:\n".format(n))
    counts = agg_metrics(df)
    for k, v in counts.items():
        print(v.nlargest(n).to_string())
        print()


if __name__ == '__main__':
    main()
