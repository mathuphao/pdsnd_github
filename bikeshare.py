import time
import datetime
import pandas as pd

pd.set_option('display.max_columns', None)

CITY_CSV = {'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv'}

CITIES = list(CITY_CSV.keys())
MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'saturday', 'sunday']


def get_valid_input(valid_inputs):
    """
    Function that asks the user for input and checks that it exists in valid_inputs, if not
    ask again if it is, then return the valid input value.

    If the user input is 'all', then return a list of all the values in valid_inputs except 'all'

    Parameters
    valid_inputs (list): list of inputs that are valid

    Returns
    user_input (list): a list of user entered valid inputs
    """

    valid_input = False
    while not valid_input:
        user_input = input('Please select one of: %s \n' %
                           (', '.join(valid_inputs))).lower()
        valid_input = user_input in valid_inputs
        if not valid_input:
            print('%s is not a valid input' % user_input)
    if user_input == 'all':
        user_input = [v for v in valid_inputs if v != 'all']
    else:
        user_input = [user_input]
    return user_input


def verify_selection():
    """
    Function that asks the user to verify selection

    Parameters
    None

    Returns
    selected items
    """
    sure = False
    while not sure:
        cities = get_valid_input(CITIES)
        months = get_valid_input(MONTHS)
        days = get_valid_input(DAYS)
        sure_input = input("""
Do you want to use the following input?
%s
User Input:
city: %s
month(s): %s
day(s): %s

Y/N?
""" % ('-'*60,
        ', '.join(cities),
        ', '.join(months),
        ', '.join(days))).lower()

        if sure_input == 'y':
            sure = True

    print("""

Selected Input
%s
User Input:
city: %s
month(s): %s
day(s): %s
""" % ('-'*60,
        ', '.join(cities),
        ', '.join(months),
        ', '.join(days)))
    return(cities, months, days)


selection = verify_selection()
cities = selection[0]
months = selection[1]
days = selection[2]


def load_data(cities, months, days):
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
    df = pd.read_csv(CITY_CSV[cities[0]])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if months != 'all':
        month = months[0]
        # use the index of the months list to get the corresponding int
        all_months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = all_months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if days != 'all':
        day = days[0]
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    start_time = time.time()
    popular_month = df['month'].mode()[0]
    print('The most popular rental month for {} is {} \n'.format(cities[0].title(), popular_month))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most common rental day for {} is {}'.format(cities[0].title(), popular_day))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most common rental start hour for {} is {}'.format(cities[0].title(), popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station in {} is {}'.format(cities[0].title(), popular_start_station))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station in {} is {}'.format(cities[0].title(), popular_end_station))

    # display most frequent combination of start station and end station trip
    df['Start End Station'] = df['Start Station'] + ' to ' + df['End Station']
    popular_combination = df['Start End Station'].value_counts().index.values[0]
    print('The most common pickup and dropoff station in {} is {}'.format(cities[0].title(), popular_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    total_travel_time = str(datetime.timedelta(seconds=total_travel_time))
    print('Total travel time for selected duration is {}'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    mean_travel_time = str(datetime.timedelta(seconds=mean_travel_time))
    print('Mean travel time for selected duration is {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print('This is count of User types \n{}'.format(user_type_count.to_string()))

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('This is count of Gender types \n{}'.format(gender_count.to_string()))
    except KeyError:
        print('We dont have gender stats for selected city')

    # Display earliest, most recent, and most common year of birth
    try:
        most_recent_birth_year = int(df['Birth Year'].max())
        print('Earliest birth year is {}'.format(most_recent_birth_year))

        most_common_birth_year = int(df['Birth Year'].mode())
        print('Most common birth year is {}'.format(most_common_birth_year))

        earliest_birth_year = int(df['Birth Year'].min())
        print('Earliest birth year is {}'.format(earliest_birth_year))

    except KeyError:
        print('We dont have birth year stats for selected city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    n = 0
    display_data = input('\nWould you like to see raw data? Enter yes or no.\n')
    while display_data.lower() == 'yes':
        raw_df = df.iloc[n: n+5]
        print(raw_df)
        n += 5
        display_data = input('\nDo you want to see more 5 lines of raw data? Enter yes or no.\n').lower()


def main():
    while True:
        df = load_data(cities, months, days)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
