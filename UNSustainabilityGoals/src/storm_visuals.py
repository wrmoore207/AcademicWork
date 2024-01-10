import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import calendar
from os.path import isfile
from storm_helpers import *
from helpers import save_or_display_graph
from preprocess_storms import *

datafile = "data/cleaned_storms.csv"

# preprocess raw data if necessary
if not isfile(datafile):
    print("Clean Storms Data not found. Attempting to preprocess raw data...")
    df = preprocess_storms()
else:
    df = pd.read_csv(datafile)

def plot_storms_per_year(df):
    '''
    plot the number of weather events per year
    '''
    df['year'] = pd.to_datetime(df['BEGIN_DATE']).dt.year
    storm_counts_per_year = df['year'].value_counts().sort_index()

    # Plotting the data
    plt.figure(figsize=(10, 6))
    storm_counts_per_year.plot(kind='line', marker='o', color='green', linestyle='-', linewidth=2)
    plt.title('Number of Storms Per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Storms')
    plt.grid(True)
    save_or_display_graph(plt, 'Storms per Year')
    plt.show()
plot_storms_per_year(df)

def plot_average_storms_per_month_over_time(df):
    '''
    plot the average number of storms per month over time
    '''
    # Assuming 'BEGIN_DATE' is in datetime format, if not convert it to datetime using pd.to_datetime
    df['BEGIN_DATE'] = pd.to_datetime(df['BEGIN_DATE'])

    # Create new columns for the month and year
    df['Month'] = df['BEGIN_DATE'].dt.month
    df['Year'] = df['BEGIN_DATE'].dt.year

    # Group by Year and Month, and count the occurrences
    monthly_storm_counts = df.groupby(['Year', 'Month']).size().reset_index(name='StormCount')

    # Calculate the average number of storms per month
    average_storms_per_month = monthly_storm_counts.groupby('Month')['StormCount'].mean()

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(average_storms_per_month.index, average_storms_per_month, marker='o')
    plt.title('Average Monthly Storms Per Year')
    plt.xlabel('Month')
    plt.ylabel('Average Number of Storms')
    plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.grid(True)
    save_or_display_graph(plt, "avg_monthly_storms")

plot_average_storms_per_month_over_time(df)

def train_and_plot_linear_regression(df):
    # Convert year to datetime and get number of storms per year
    df['year'] = pd.to_datetime(df['BEGIN_DATE']).dt.year
    storm_counts_per_year = df['year'].value_counts().sort_index()

    X = storm_counts_per_year.index.values.reshape(-1, 1)  # Years
    y = storm_counts_per_year.values  # Number of storms per year

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Plot the regression line
    plt.figure(figsize=(10, 6))
    plt.plot(X, y, marker='o', linestyle='', label='Actual Data')
    plt.plot(X_test, y_pred, color='red', linewidth=2, label='Prediction')
    plt.title('Storms Per Year Prediction')
    plt.xlabel('Year')
    plt.ylabel('Number of Storms')
    plt.legend()
    plt.grid(True)
    save_or_display_graph(plt, 'Linear Regression - Storms per Year')
    plt.show()

train_and_plot_linear_regression(df)


def plot_average_storms_in_range(df, start_month, end_month):
    '''
    plots the average number of storms in a given range over time
    ie: the average number of storms between june and september per year
    '''
    # Assuming 'BEGIN_DATE' is in datetime format, if not convert it to datetime using pd.to_datetime
    df['BEGIN_DATE'] = pd.to_datetime(df['BEGIN_DATE'])

    # Create new columns for the month and year
    df['Month'] = df['BEGIN_DATE'].dt.month
    df['Year'] = df['BEGIN_DATE'].dt.year

    # Filter the dataframe for storms between the specified months
    selected_storms = df[(df['Month'] >= start_month) & (df['Month'] <= end_month)]

    # Group by Year and count the occurrences
    yearly_storm_counts = selected_storms.groupby('Year').size().reset_index(name='StormCount')

    # Convert numerical month representation to month names
    month_names = [calendar.month_name[m] for m in range(start_month, end_month + 1)]

    # Plotting as a scatter plot
    plt.figure(figsize=(12, 6))
    plt.scatter(yearly_storm_counts['Year'], yearly_storm_counts['StormCount'], color='blue')
    plt.title(f'Number of Storms Between {month_names[0]} and {month_names[-1]} Over Time')
    plt.xlabel('Year')
    plt.ylabel('Number of Storms')
    plt.grid(axis='both')
    file_title = f'avg_storms_{month_names[0]}_{month_names[-1]}_per_year.png'
    save_or_display_graph(plt, file_title)

plot_average_storms_in_range(df, start_month=6, end_month=9)

def plot_average_storms_in_month(df, target_month, start_year, end_year):
    '''
    A visual to illustrate the change in the average number of storms in a given month in a given time span
    '''
    # Create a list to store average number of storms for each year
    avg_storms_per_year = []

    # Loop through each year and calculate the average number of storms in the specified month
    for year in range(start_year, end_year + 1):
        avg_storms = average_storms_in_given_month(df, target_month=target_month, start_year=year, end_year=year)
        avg_storms_per_year.append(avg_storms)

    # Convert numerical month representation to month names
    month_name = calendar.month_name[target_month]

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(range(start_year, end_year + 1), avg_storms_per_year, marker='o', linestyle='-', color='blue')
    plt.title(f'Average Number of Storms in {month_name} {start_year} to {end_year}')
    plt.xlabel('Year')
    plt.ylabel('Average Number of Storms')
    plt.grid(True)

    # Save the file with the title of the image
    file_title = f'avg_storms_{month_name}_{start_year}_{end_year}.png'
    save_or_display_graph(plt, file_title)

start_year = 1996
end_year = 2023
target_month = 7
plot_average_storms_in_month(df, 7, 1996, 2023)

def plot_wind_events_magnitude(df):
    # Convert 'BEGIN_DATE' to datetime
    df['BEGIN_DATE'] = pd.to_datetime(df['BEGIN_DATE'])

    # Extract year from 'BEGIN_DATE' and create a new column 'YEAR'
    df['YEAR'] = df['BEGIN_DATE'].dt.year

    # Filter rows to keep only 'Thunderstorm Wind' and 'High Wind' events
    selected_event_types = ['Thunderstorm Wind', 'High Wind']
    df = df[df['EVENT_TYPE'].isin(selected_event_types)]

    # Filter rows with 'MAGNITUDE' != 0
    df = df[df['MAGNITUDE'] != 0]

    # Plotting with seaborn for better aesthetics (optional)
    sns.set(style="whitegrid")

    # Create a scatter plot
    plt.figure(figsize=(12, 6))

    # Using scatter plot
    sns.scatterplot(x='BEGIN_DATE', y='MAGNITUDE', hue='EVENT_TYPE', data=df, palette='viridis')

    # Improve the readability of the plot
    plt.title('Maximum Storm Gusts Over Time')
    plt.xlabel('Event Date')
    plt.ylabel('Magnitude')
    plt.legend(title='Event Type')
    save_or_display_graph(plt, 'storm_gusts_over_time')

plot_wind_events_magnitude(df)
