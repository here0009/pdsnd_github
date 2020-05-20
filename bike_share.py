import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}


def seconds_to_hours(seconds):
    mins, seconds = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return int(hours), int(mins), seconds

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Enter the name of the city , Chicago, New York city and Washington are now avilable\n')
        if city in CITY_DATA:
            break
        else:
            print('Data are not avilable for {}.'.format(city))

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        month_filter_flag = input("Would you like to filter data by month? Please Enter 'Yes' or 'No.\n").lower()
        if month_filter_flag == 'yes':
            while True:
                month = input("Enter the month you'd like to check, the data of January, February, March, April, May and June are avilable.\n").lower()
                if month in months:
                    # use the index of the months list to get the corresponding int
                    month = months.index(month) + 1
                    break
                else:
                    print('Not a valid month')
            break
        elif month_filter_flag == 'no':
            month = 'all'
            break
        else:
            print("Please enter 'Yes' or 'No'.")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_filter_flag = input("Would you like to filter data by day? Enter 'Yes' or 'No' please.\n").lower()
        if day_filter_flag == 'yes':
            while True:
                day = input("Which day you'd like to check? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday.\n").lower()
                if day in days:
                    day = day.title()
                    break
                else:
                    print('Not a valid day')
            break
        elif day_filter_flag == 'no':
            day = 'all'
            break
        else:
            print("Please enter 'Yes' or 'No'.")

        day = input('Enter the day of week : ')
        if day == 'all' or day.lower() in days:
            break
        else:
            print('Not a valid day.')

    print('-' * 40)
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
    df = pd.read_csv(CITY_DATA[city])
    rows = df.shape[0]
    for i in range(0, rows, 5):
        check_raw_data = input("Would you check the raw data? Enter 'Yes' or 'No' please.\n").lower()
        if check_raw_data != 'yes':
            break
        print("The data for line {} to line {}:".format(i, i+5))
        print(df.iloc[i: i + 5, :])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    time_stats(df)
    if month != 'all':
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day]
    return df


def time_stats(df):
    """Displays statistics on the times of travel, no filter."""

    print('\nCalculating The time of trips by month, day of week, hour...\n')
    start_time = time.time()

    # TO DO: display total trips for each month
    print('\nTotal trips for each month :\n', )
    print(df['month'].value_counts())
    # TO DO: display total trips for day of week
    print('\nTotal trips for each day of week :\n', )
    print(df['day_of_week'].value_counts())
    # TO DO: display the counts of start hour for the trips
    print('\nCounts of start hour for all the trips :\n', )
    print(df['hour'].value_counts())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    df['Start and End Station'] = df['Start Station'] + ' - ' + df['End Station']
    # TO DO: display most commonly used start station
    print('The most commonly used start station is :', df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('The most common used end station is :', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print('The most common combination of start station and end station trip is :', df['Start and End Station'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    h, m, s = seconds_to_hours(df['Trip Duration'].sum(skipna=True))
    print('\nThe total travel time is {:d} hours, {:d} mins {:.2f} seconds\n'.format(h, m, s))

    # TO DO: display mean travel time
    h, m, s = seconds_to_hours(df['Trip Duration'].mean(skipna=True))
    print('\nThe mean travel time is {:d} hours, {:d} mins {:.2f} seconds\n'.format(h, m, s))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if 'User Type' in df:
        print('Counts of user types:')
        print(df['User Type'].value_counts())
    else:
        print('User type information is not avilable.\n')
    # TO DO: Display counts of gender
    if 'Gender' in df:
        print('Counts of user gender:')
        print(df['Gender'].value_counts())
    else:
        print('Gender information is not avilable.\n')
    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print('The earliest year of birth is:', int(df['Birth Year'].min()))
        print('The most recent year of birth is:', int(df['Birth Year'].max()))
        print('The most common year of birth is:', int(df['Birth Year'].mode()[0]))
    else:
        print('Birth Year information is not avilable')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
