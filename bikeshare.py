import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York or Washington?")
        if city.lower() in ['chicago', 'new york', 'washington']:
            city = city.lower()
            break
        else:
            print("Invalid input. Please enter either Chicago, New York or Washington.")

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("What month would you like to filter by (all, january, february,... , june)?")
        if month.lower() in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            month = month.lower()
            break
        elif month.lower() in ['jan', 'feb', 'mar', 'apr', 'jun']:
            month = month.lower()
            month_dict = {'jan': 'january', 'feb': 'february', 'mar': 'march', 'apr': 'april', 'jun': 'june'}
            month = month_dict[month]
            break
        else:
            print("Invalid input. Please enter all, january, feburary, march, april, may, or june")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("What day of the week would you like to filter by (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)?")
        if day.title() in ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            day = day.title()
            break
        elif day.title() in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
            day = day.title()
            day_abbrev1 = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}
            day = day_abbrev1[day]
            break
        elif day.title() in ['M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su']:
            day = day.title()
            day_abbrev2 = {'M': 'Monday', 'Tu': 'Tuesday', 'W': 'Wednesday', 'Th': 'Thursday', 'F': 'Friday', 'Sa': 'Saturday', 'Su': 'Sunday'}
            day = day_abbrev2[day]
            break        
        else:
            print("Invalid input. Please enter All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday")


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # check that a month filter hasn't been applied 
    if 'month' in df:
        # find the most common month (from January to June)
        popular_month = df['month'].mode()[0]
        # find the count of the most common month
        count_popular_month = (df['month'] == popular_month).sum()
        # display the most common month
        print('Most Common Month: {}, Count: {}'.format(popular_month, count_popular_month))

    # check that a day filter hasn't been applied 
    if len(df['day_of_week'].unique()) > 1:   
        # find the most common day of week (from Monday to Sunday)
        popular_day = df['day_of_week'].mode()[0]
        # find the count of the most common day of week
        count_popular_day = (df['day_of_week'] == popular_day).sum()
        # display the most common day of week
        print('Most Common Day of the Week: {}, Count: {}'.format(popular_day, count_popular_day))

    # find the most common hour (from a0 to 23)
    popular_hour = df['hour'].mode()[0]
    # find the count of the most common start hour
    count_popular_hour = (df['hour'] == popular_hour).sum()
    # display the most common start hour
    print('Most Common Start Hour: {}, Count: {}'.format(popular_hour, count_popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    # find the count of the most commonly used start station
    count_start_popular_station = (df['Start Station'] == popular_start_station).sum()
    print('Most Commonly Used Start Station: {}, Count: {}'.format(popular_start_station, count_start_popular_station))


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    # find the count of the most commonly used end station
    count_popular_end_station = (df['End Station'] == popular_end_station).sum()
    print('Most Commonly Used End Station: {}, Count: {}'.format(popular_end_station, count_popular_end_station))


    # display most frequent combination of start station and end station trip
    df['Combo Stations'] = df['Start Station'] + ' to ' + df['End Station']
    popular_combo_stations =  df['Combo Stations'].mode()[0]
    # find the count of the most frequent combination of start station and end station trip
    count_popular_combo_stations = (df['Combo Stations'] == popular_combo_stations).sum()
    print('Most Frequent Combination of Start Station and End Station Trip: {}, Count: {}'.format(popular_combo_stations, count_popular_combo_stations))
    df = df.drop('Combo Stations', axis=1, inplace=True)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate total travel time
    total_travel_time = df['Trip Duration'].sum()
    # convert to and display days, hours, mins, and secs
    total_days, total_seconds = divmod(total_travel_time, 86400)
    total_hours, total_seconds = divmod(total_seconds, 3600)
    total_minutes, total_seconds = divmod(total_seconds, 60)
    print('Total Travel Time: {} days, {} hours, {} minutes, and {} seconds'. format(int(total_days), int(total_hours), int(total_minutes), int(total_seconds)))

    # calculate mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    # convert to and displaymins, and secs
    mean_minutes, mean_seconds = divmod(mean_travel_time, 60)
    print('Mean Travel Time: {} minutes and {} seconds'.format(int(mean_minutes), int(mean_seconds)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nWhat is the breakdown of users?\n')
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    print('\nWhat is the breakdown of gender?\n')
    try:
        gender = df['Gender'].value_counts()
    except KeyError:
        print("No gender data to share")
    else:
        print(gender)

    # Display earliest, most recent, and most common year of birth
    print('\nWhat is the oldest, youngest, and most popular year of birth, respectively\n')
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        count_earliest_birth_year = (df['Birth Year'] == earliest_birth_year).sum()
        most_recent_birth_year = int(df['Birth Year'].max())
        count_most_recent_birth_year = (df['Birth Year'] == most_recent_birth_year).sum()
        popular_birth_year = int(df['Birth Year'].mode())
        count_popular_birth_year = (df['Birth Year'] == popular_birth_year).sum()
    except KeyError:
        print("No birth year data to share")
    else:
        print('Earliest Year of Birth: {}, Count: {}'.format(earliest_birth_year, count_earliest_birth_year))
        print('Most Recent Year of Birth: {}, Count: {}'.format(most_recent_birth_year, count_most_recent_birth_year))
        print('Most Common Year of Birth: {}, Count: {}'.format(popular_birth_year, count_popular_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw individual trip data."""
    start_row = 0
    while True:
        show_raw_data = input('\nWould you like to see individual trip data? Type \'yes\' or \'no\'.\n')
        if show_raw_data.lower() in ['yes', 'y']:
            if start_row >= len(df):
                print("There is no more individual data to display")
                break
            print(df.iloc[start_row:start_row+5])
            start_row += 5
        elif show_raw_data.lower() in ['no', 'n']:
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() in ['yes', 'y']:
                break
            elif restart.lower() in ['no', 'n']:
                return



if __name__ == "__main__":
	main()
