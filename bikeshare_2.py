#note: Need bikeshare data sets for chicago, new york city, and washington that are named as 'chicago.csv', 'new_york_city.csv', and 'washington.csv' respectively)

import time
import pandas as pd
import numpy as np

pd.set_option("display.max_columns",200)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
        try:
            city = input("Please enter a city: chicago, new york city, washington: ").lower()
        
        except ValueError:
            print('This is not a valid entry!')
            continue

        if city not in ('chicago', 'new york city', 'washington'):
            print('You entered', city,', which is not one of the choices listed')
            continue
        else:
            break


    # get user input for month (all, january, february, ... , june)

    month_filter_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    while True:
        try:
            month = input("Please enter a month (i.e january, february, march, april, may, june, all): ").lower()
        
        except ValueError:
            print('This is not a valid entry!')
            continue    
    
        if month in month_filter_list:
            break
        else:
            print("That is an invalid entry - try again")
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day_filter_list = ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    while True:
        try:
            day = input("Please enter a day (i.e Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, all): ").lower()
        
        except ValueError:
            print('This is not a valid entry!')
            continue

        if day in day_filter_list:
            break
        else:
            print("That is an invalid entry - try again")
            continue

    print('-'*40) # prints a line of 40 dashes
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
    
    # load data file into a dataframe using the city filter
    df = pd.read_csv(CITY_DATA[city])  

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])  

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df
    


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    df['month'] = pd.to_datetime(df['month'], format='%m').dt.month_name() # changed indexed interger month to month name
    print('Most Frequent Month: ', df['month'].mode()[0])

    # display the most common day of week

    print('Most Frequent Day: ', df['day_of_week'].mode()[0])

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    print('Most Frequent Start Hour (24 hour clock): ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    print('Most Commonly Used Start Station: ', df['Start Station'].mode()[0])

    # display most commonly used end station

    popular_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station: ', popular_end_station)

    # display most frequent combination of start station and end station trip
#introduct new column df[comb station = df start + df end]

    df['Comb Station'] = df['Start Station'] + ' : ' + df['End Station']
    popular_comb_station = df['Comb Station'].mode()[0]
    print('Most Common Trip from Start to End: ', popular_comb_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    
    total_travel_time_minutes = df['Trip Duration'].sum()
    total_travel_time_hours = total_travel_time_minutes / 60
    print('The Total Travel Time for all Trips was: ', total_travel_time_minutes, ' minutes')
    print('The Total Travel Time for all Trips was: ', total_travel_time_hours, ' hours')

    # display mean travel time

    print('The Average Travel Time was: ', np.mean(df['Trip Duration'])) #used numpy vs panda here to have better precision

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    print('Here are the counts for the different user types:\n', df['User Type'].value_counts())
    print() #space between next data showing

    # Display counts of gender
    
    try:
        print('Here are the counts for each gender:\n', df['Gender'].value_counts())
        print() #space between next data showing
    
    except:
        print('Sorry, the gender data is not present for this city')

    # Display earliest, most recent, and most common year of birth
#same as previous - handle it or conditional statement
# oldest - minimum - min (most recent - max, and common mode function)

    try:
        oldest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode())
        print('The earliest birth year is: ', oldest_birth_year)
        print('The most recent birth year is: ', most_recent_birth_year)
        print('The most common birth year is: ', most_common_birth_year)
    
    except:
        print('Sorry, the birth year data is not present for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Asks user if they want to see 5 lines of raw data.
    Then returns 5 lines of raw data if user inputs 'yes'. Iterates until user responds with a 'no'
    """
    position = 0
    data = df
    while True:
        try:
            raw_data = input('Would you like to see 5 lines of raw data? Enter yes/y or no/n: ')
        
        except ValueError:
            print('This is not a valid entry!')
            continue 
        
        if (raw_data.lower() == 'yes') | (raw_data.lower() == 'y'):
            print(data.iloc[position:position+5, :])
            position += 5
        elif (raw_data.lower() == 'no') | (raw_data.lower() == 'n'):
            break
        else:
            print('Invalid entry. Please enter yes or no')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        restart = input('\nWould you like to restart to select different options? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
