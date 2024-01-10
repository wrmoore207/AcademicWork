import pandas as pd

# There are mixed types in some of the columns, this is a list to cast them as strings

# Define data types for columns with mixed types
column_data_types = {
    16: str,
    25: str,
    26: str,
    28: str,
    29: str,
    34: str,
    35: str,
    37: str,
    39: str,
    40: str,
    42: str,
    43: str,
    48: str,
    49: str,
}

def filter_maine_coastal_data(input_df):
    # Drop All Non-Maine Data
    maine_df = input_df[input_df['STATE'].str.contains('MAINE', case=False, na=False)]

    # Keep Only Coastal Records
    values_to_keep = [5, 9, 13, 15, 23, 27, 29, 31]

    # Create a boolean mask to filter the rows
    mask = maine_df['CZ_FIPS'].isin(values_to_keep)

    # Use the mask to filter the DataFrame
    coastal_df = maine_df[mask]

    return coastal_df

def convert_and_merge_date_data(input_df):
    # Make a copy of the input DataFrame
    coastal_df = input_df.copy()

    # Convert columns to string
    coastal_df['BEGIN_YEARMONTH'] = coastal_df['BEGIN_YEARMONTH'].astype(str)
    coastal_df['BEGIN_DAY'] = coastal_df['BEGIN_DAY'].astype(str)

    # Combine and convert to datetime
    coastal_df['BEGIN_DATE'] = pd.to_datetime(
        coastal_df['BEGIN_YEARMONTH'] + coastal_df['BEGIN_DAY'], format='%Y%m%d')

    return coastal_df

def filter_dataframe_by_date_range(df, start_date, end_date, date_column='BEGIN_DATE'):
    """
    Filter a DataFrame based on a date range.

    Parameters:
    - df: The DataFrame to filter.
    - start_date: The start date of the date range (as a string or pandas Timestamp).
    - end_date: The end date of the date range (as a string or pandas Timestamp).
    - date_column: The name of the date column in the DataFrame (default is 'BEGIN_DATE').

    Returns:
    - A filtered DataFrame containing rows within the specified date range.
    """
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    filtered_df = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]
    return filtered_df

def merge_dataframes(df1, df2, date_column):
    """
    Merge two pandas DataFrames based on a common date column after converting
    date columns to a common data type (e.g., datetime).

    Args:
    df1 (pd.DataFrame): The first DataFrame to be merged.
    df2 (pd.DataFrame): The second DataFrame to be merged.
    date_column (str): The name of the date column on which to merge.

    Returns:
    pd.DataFrame: The merged DataFrame.
    """
    # Convert date columns to a common data type (e.g., datetime)
    df1[date_column] = pd.to_datetime(df1[date_column])
    df2[date_column] = pd.to_datetime(df2[date_column])

    # Merge the DataFrames based on the common date column
    merged_df = pd.merge(df1, df2, on=date_column, how='inner')

    return merged_df


# Drop Unused Columns
def drop_extra_columns(data):

    drop_columns = [
    'BEGIN_YEARMONTH',
    'BEGIN_DAY',
    'END_YEARMONTH',
    'END_DAY',
    'EPISODE_ID',
    'YEAR',
    'MONTH_NAME',
    'CZ_TYPE',
    'CZ_NAME',
    'WFO',
    'CZ_TIMEZONE',
    'DAMAGE_CROPS',
    'TOR_F_SCALE',
    'TOR_LENGTH',
    'TOR_WIDTH',
    'TOR_OTHER_WFO',
    'TOR_OTHER_CZ_STATE',
    'TOR_OTHER_CZ_FIPS',
    'TOR_OTHER_CZ_NAME',
    'BEGIN_RANGE',
    'BEGIN_AZIMUTH',
    'END_RANGE',
    'END_AZIMUTH',
    'BEGIN_LAT',
    'BEGIN_LON',
    'END_LAT',
    'END_LON',
    'EPISODE_NARRATIVE',
    'EVENT_NARRATIVE',
    ]
    cleaned_df = data.drop(columns=drop_columns, axis=1)\
    
    return cleaned_df

# Keep Only Wind Events

def keep_wind_only(data):
    # List of event types to keep
    event_types_to_keep = [
    'Thunderstorm Wind',
    # 'High Wind',
    # 'Strong Wind',
    # 'Coastal Flood',
    # 'Storm Surge/Tide',
    # 'Tropical Storm',
    # 'High Surf'
    ]

    # Filter the DataFrame to keep rows with the specified event types
    wind_df = data[data['EVENT_TYPE'].isin(event_types_to_keep)]

    return wind_df

def storms_in_given_month(df, target_month, start_year, end_year):
    # Assuming 'BEGIN_DATE' is in datetime format, if not convert it to datetime using pd.to_datetime
    df['BEGIN_DATE'] = pd.to_datetime(df['BEGIN_DATE'])

    # Create new columns for the month and year
    df['Month'] = df['BEGIN_DATE'].dt.month
    df['Year'] = df['BEGIN_DATE'].dt.year

    # Filter the dataframe for storms in the specified month and years
    selected_storms = df[(df['Month'] == target_month) & (df['Year'] >= start_year) & (df['Year'] <= end_year)]

    # Count the number of storms in the specified month and years
    num_storms = selected_storms.shape[0]

    return num_storms

def average_storms_in_given_month(df, target_month, start_year, end_year):
    # Assuming 'BEGIN_DATE' is in datetime format, if not convert it to datetime using pd.to_datetime
    df['BEGIN_DATE'] = pd.to_datetime(df['BEGIN_DATE'])

    # Create new columns for the month and year
    df['Month'] = df['BEGIN_DATE'].dt.month
    df['Year'] = df['BEGIN_DATE'].dt.year

    # Filter the dataframe for storms in the specified month and years
    selected_storms = df[(df['Month'] == target_month) & (df['Year'] >= start_year) & (df['Year'] <= end_year)]

    # Count the number of storms in the specified month and years
    num_storms = selected_storms.shape[0]

    # Calculate the number of years in the specified time span
    num_years = end_year - start_year + 1

    # Calculate the average number of storms per year
    average_storms = num_storms / num_years

    return average_storms


import pandas as pd
from scipy import stats

def remove_outliers(df, magnitude_column='MAGNITUDE', threshold=3):
    """
    Remove outliers from a DataFrame based on the specified 'MAGNITUDE' column using Z-score.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        magnitude_column (str): The name of the column containing magnitude values. Default is 'MAGNITUDE'.
        threshold (float): Z-score threshold for identifying outliers. Default is 3.
        
    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    df_no_outliers = df.copy()
    
    z_scores = stats.zscore(df_no_outliers[magnitude_column])
    outliers = (abs(z_scores) > threshold)
    df_no_outliers = df_no_outliers[~outliers]
    
    return df_no_outliers