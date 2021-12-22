import time
from datetime import datetime
import calendar
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('*' * 40)
    print('US BikeShare Data Analysis ::: Udacity Nanodegree From "EG-FWD"')
    print('Presented By: AHMED ELKHAYYAT')
    print('E-MAIL: onlink4it@gmail.com')
    print('*' * 40)
    print('Hello! Let\'s explore some US bikeshare data!')

    # set default values for city, month
    city, month, day = '', '', ''

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while city == '':
        print('Which city do you want to filter with?\nOptions')

        cities = {
            1: 'chicago',
            2: 'new_york_city',
            3: 'washington',
        }

        # Printing Cities
        for index, city_name in cities.items():
            print('\t {}- {}'.format(index, city_name.title()))
        try:
            city_id = int(input('Selected option number: '))
            if city_id not in range(1, 4):
                print('*' * 40)
                print('Please select valid option from 1 to 3')
                print('*' * 40)
            city = cities[city_id]
        except ValueError as e:
            print('*' * 40)
            print('Please select valid option from 1 to 3')
            print('*' * 40)

    # get user input for month (all, january, february, ... , june)
    while month == '':
        print('Which month do you filter with?\nOptions:\n\t 0 - All Months')

        # Printing Months
        for _month in range(1, 13):
            print('\t ' + str(_month) + ' - ' + calendar.month_name[_month])

        try:
            month = int(input('Selected option number: '))
            if month not in range(13):
                print('*' * 40)
                print('Error: Please select valid option from 1 to 12')
                print('*' * 40)
        except ValueError as e:
            print('*' * 40)
            print(e)
            print(month)
            print('Error: Please select valid option from 1 to 12')
            print('*' * 40)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day == '':
        print('Which day do you filter with?\nOptions:\n\t 0 - All Days')

        # Printing Months
        for _day in range(1, 8):
            print('\t ' + str(_day) + ' - ' + calendar.day_name[_day - 1])
        print('Please select valid option from 1 to 7 - 0 For All')

        try:
            day = int(input('Selected option number: '))
            if day not in range(8):
                print('*' * 40)
                print('Error: Please select valid option from 0 to 7')
                print('*' * 40)
        except ValueError as e:
            print('*' * 40)
            print(e)
            print('Error: Please select valid option from 0 to 7')
            print('*' * 40)

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - name of the month to filter by, or "0" to apply no month filter
        (int) day - name of the day of week to filter by, or "0" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Applying City Filtering
    df = pd.read_csv(city + '.csv')
    print('-' * 40)
    print('Data Loaded Successfully')

    # Manipulating Start Time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Start Hour'] = df['Start Time'].dt.hour
    df['Day Of Week'] = df['Start Time'].dt.weekday
    df['Month'] = df['Start Time'].dt.month

    # Applying Month Filtering
    if not month == 0:
        df = df[df['Start Time'].dt.month == month]

    # Applying Day Filtering
    if not day == 0:
        df = df[df['Day Of Week'] == day - 1]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df_by_month = df.groupby(['Month']).count()
    df_by_month['Count By Month'] = df_by_month['Start Time']
    most_common_month = df_by_month[df_by_month['Count By Month'] == df_by_month['Count By Month'].max()].index.values[
        0]
    print('\nMost common month:', calendar.month_name[most_common_month])

    # display the most common day of week
    df_by_weekday = df.groupby(['Day Of Week']).count()
    df_by_weekday['Count By Weekday'] = df_by_weekday['Start Time']
    popular_day = df_by_weekday[df_by_weekday['Count By Weekday'] == df_by_weekday['Count By Weekday'].max()
                                ].index.values[0]
    print('Most Popular Day Of Week:', calendar.day_name[popular_day])

    # display the most common start hour
    df_by_hour = df.groupby(['Start Hour']).count()
    df_by_hour['Count By Hour'] = df_by_hour['Start Time']
    popular_hour = df_by_hour[df_by_hour['Count By Hour'] == df_by_hour['Count By Hour'].max()].index.values[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    trips_by_start_stations = df.groupby(['Start Station']).count()
    trips_by_start_stations['Start Location Count'] = trips_by_start_stations['Start Time']
    most_common_start_stations = trips_by_start_stations[
        trips_by_start_stations['Start Location Count'] == trips_by_start_stations[
            'Start Location Count'].max()].index.values[0]
    print('\nMost Common Start Stations:', most_common_start_stations)

    # display most commonly used end station
    trips_by_end_stations = df.groupby(['End Station']).count()
    trips_by_end_stations['End Location Count'] = trips_by_end_stations['Start Time']
    most_common_end_stations = trips_by_end_stations[
        trips_by_end_stations['End Location Count'] == trips_by_end_stations['End Location Count'].max()].index.values[
        0]
    print('Most Common End Stations:', most_common_end_stations)

    # display most frequent combination of start station and end station trip
    trips_by_both_stations = df.groupby(['Start Station', 'End Station']).count()
    trips_by_both_stations['Both Location Count'] = trips_by_both_stations['Start Time']
    most_common_both_stations = trips_by_both_stations[
        trips_by_both_stations['Both Location Count'] == trips_by_both_stations['Both Location Count'].max()].index.values[0]
    print('Most Common Combination Of Stations:', most_common_both_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    trip_column = df['Trip Duration']

    # display total travel time
    total_travel_time = trip_column.sum()
    print('\nTotal Travel Time:', total_travel_time)

    # display mean travel time
    mean_travel_time = trip_column.mean()
    print('Mean Travel Time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type']).count()
    # Adding new column for count
    user_types['Count By User Types'] = user_types['Start Time']
    user_types = user_types['Count By User Types']
    print('\nCount Of Each User Type:', user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender = df.groupby('Gender').count()
        gender['Count By Gender'] = gender['Start Time']
        gender = gender['Count By Gender']
        print('\nCount Of Each Gender:', gender)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        # earliest
        earliest = df['Birth Year'].min()
        print('\nEarliest Year Of Birth:', str(int(earliest)))

        # most recent
        most_recent = df['Birth Year'].max()
        print('Most Recent Year Of Birth: ', str(int(most_recent)))

        # most common
        # grouping data frame by birth year count
        df_by_year = df.groupby(['Birth Year']).count()
        # create column for country by year of birth
        df_by_year['Count By Year Of Birth'] = df_by_year['Start Time']
        # return the index of max for column count by birth of year
        most_common = df_by_year[df_by_year['Count By Year Of Birth'] == df_by_year['Count By Year Of Birth'].max()].index.values[0]
        print('Most Common Year Of Birth:', str(int(most_common)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df['Start Time'].count() == 0:
            print('*' * 40)
            print('No Data at this time frame, Please try another filter')
            print('*' * 40)
            continue
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
