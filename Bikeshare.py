import time
import pandas as pd
import numpy as np


print('=' * 60)
print("US bikeshare Data".center(60, '-'))
print('=' * 60)



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
    print('Hello! Let\'s explore some US bikeshare data!')
    # Below will get user input for city (chicago, new york city, washington).


    while True:
        cities = ['chicago', 'new york city', 'washington'] # Used this variable to limit invalid inputs
        city = input("Please pick a city [Chicago, New York City, Washington]: ").lower()
        if city not in cities:
            print("Invalid input!")
        else:
            print(f"You have selected {city.title()}")
            break

    # Below will get user input for month (all, january, february, ... , june)

    while True:
        months = ['all','january', 'february', 'march', 'april', 'may', 'june'] # Used this variable to limit invalid inputs
        month = input("Please pick a month [January to June] or type All for all available months: ").lower()
        if month not in months:
            print("Invalid input!")
        else:
            print(f"You have selected {month.title()}")
            break

    # Below will get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        days_of_week = ['all','saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday'] # Used this variable to limit invalid inputs
        day = input("Please pick a day of the week or type All for all days: ").lower()
        if day not in days_of_week:
            print("Invalid input!")
        else:
            print(f"You have selected {day.title()}")
            break

    print('-'*40)
    return city, month, day

def view_raw_data(df):
    """
    Prompt the user if they want to see some lines of raw data.
    This is a revised code instead of the original 5 lines option..
    The below code will allow user selecting their desirable number of lines to display, with other option to skip for final results.
    Also calculated the total rows in the raw data to inform users the maximum lines in the raw data.
    """
    rows_in_data = (df['Start Time'].count()) # The total rows in the raw data to inform user of the maximum limit, will be used later.
    user_input= input("Would you like to see some lines of the filtered data? [Y/N]: ").lower() # Giving the user option to proceed or to cancel
    required_answers=["y", "n"] # Used this variable to limit invalid inputs
    while True:
        while user_input not in required_answers:
            print("Invalid input!")
            user_input = input("Would you like to see some lines of the filtered data? [Y/N]: ").lower()
        if user_input == 'y':
            number_of_lines = input(f"Please enter a number of data lines to display [Max. lines available {rows_in_data:,}] or type '0' to get the final results: ")
            if number_of_lines == '0':
                break
            else:
                try: # Used a try statement here for error handling purpose.
                    print(df.head(int(number_of_lines))) # Converted the user input from str to int to avoid ValueError.
                except: # Used the except clause to handle the expected error.
                    print("That is not a valid number")
        else:
            break


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
    # This will load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # This to convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # This to extract month , day of week, and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() # used a newer version here
    df['hour'] = df['Start Time'].dt.hour

    # filtering by month if applicable
    if month != 'all':
        # using the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filtering by month to create the new dataframe
        df = df[df['month'] == month]

    # filtering by day of week if applicable
    if day != 'all':
        # filtering by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print(f'Most Frequent month: {popular_month}')

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print(f'Most Frequent day: {popular_day}')

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print(f'Most Frequent Start Hour: {popular_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f'Most commonly used start station: {popular_start_station}')

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f'Most commonly used end station: {popular_end_station}')

    # display most frequent combination of start station and end station trip
    freq_start_end = (df['Start Station'] + ' | ' + df['End Station']).mode()[0]
    print(f'Most commonly used start station and end station: {freq_start_end}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time is : {tot_travel_time/3600:,} hours")

    # display mean travel time
    avrg_travel_time = df['Trip Duration'].mean()
    print(f"Average Travel Time is : {avrg_travel_time/60:,} minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts()
        print(gender_types)
        #Eearliest, most recent, most common year of birth (only available for NYC and Chicago)
        earliest_yob = int(df['Birth Year'].min())
        recent_yob = int(df['Birth Year'].max())
        common_yob = int(df['Birth Year'].mode()[0])
        print(f"Out of all users, the oldest user was born in the year {earliest_yob}, and the youngest user born in the year {recent_yob}, while most frequest users born in {common_yob}")
    else:
        print("Users gender information is not available for this city.")
    # Display earliest, most recent, and most common year of birth

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        view_raw_data(df) # Included the function here
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()

