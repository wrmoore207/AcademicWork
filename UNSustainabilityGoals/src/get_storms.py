import os
import requests
import pandas as pd

def get_storms(output_directory):
    # URL of the directory containing the .csv files
    base_url = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Define data types for columns with mixed types
    column_data_types = {
        25: str,
        26: str,
        28: str,
        29: str,
        34: str,
        35: str,
        37: str,
        40: str,
        42: str,
        43: str,
        48: str,
        49: str,
    }

    # Function to download a file and save it to the output_directory
    def download_file(url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(output_directory, filename), 'wb') as file:
                file.write(response.content)

    # Get a list of all .csv files in the directory
    response = requests.get(base_url)
    if response.status_code == 200:
        file_links = [base_url + "/" + line.split('href="')[1].split('"')[0] for line in response.text.split('\n') if ".csv" in line]

        # Download .csv files with 'details' in the title and save them as separate .csv files
        for link in file_links:
            filename = link.split("/")[-1]
            if 'details' in filename:
                download_file(link, filename)
                print(f"Downloaded: {filename}")

    # Merge the downloaded 'details' files into one .csv file titled 'details_combined'
    all_data = []
    for root, dirs, files in os.walk(output_directory):
        for file in files:
            if 'details' in file:
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path, dtype=column_data_types)  # Specify data types
                all_data.append(df)

    if all_data:
        combined_details = pd.concat(all_data, ignore_index=True)
        combined_details.to_csv(os.path.join(output_directory, 'raw_storm_df.csv'), index=False)
        print("All 'details' files merged into 'raw_storm_df.csv' at the specified path.")

        # Delete the individual 'details' files
        for root, dirs, files in os.walk(output_directory):
            for file in files:
                if 'details' in file:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                    print(f"Deleted: {file}")

    else:
        print("No 'details' files found for merging.")

    
get_storms('data')