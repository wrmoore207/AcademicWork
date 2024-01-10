from os.path import isfile
import sys
from storm_helpers import *

def preprocess_storms():
    
    datafile = "data/raw_storm_df.csv"

    if not isfile(datafile):
        print("Raw Storms Data not found. Please run 'make get_storms' first.")
        sys.exit(1)
    
    df = pd.read_csv(datafile, dtype=column_data_types)

    # Keep only coastal maine records
    df = filter_maine_coastal_data(df)

    # Convert and merge date columns into one column "BEGIN_DATE"
    df = convert_and_merge_date_data(df)

    # Drop Extra Columns
    df = drop_extra_columns(df)

    # Keep only wind related events
    df = keep_wind_only(df)
    
    # Remove outliers
    df = remove_outliers(df, 'MAGNITUDE', 3)

    # Drop duplicates 
    df['BEGIN_DATE'] = pd.to_datetime(df['BEGIN_DATE'])
    df = df.drop_duplicates(subset=['BEGIN_DATE'])

    # Concatenate the folder path and file name
    folder_path = 'data'
    file_name = 'cleaned_storms.csv'
    file_path = f"{folder_path}/{file_name}"

    # Save the DataFrame to CSV
    df.to_csv(file_path, index=False)

    print("saved successfully as 'cleaned_storms.csv'")

    return df