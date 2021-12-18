# Created by: Hassan Ibrahim 2021-12-9
# GitHub:     https://github.com/HIMH1
# Linkedin:   https://www.linkedin.com/in/mrhimh
#-------------------------------------------------
import pandas as pd
import time


CITY_DATA_GENERAL = {'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv', 'dc': 'dc.csv', 'taxus': 'taxus.csv', 'united states': 'united_states.csv'}

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
CITIES = ["chicago", "new york city", "washington"]
MONTHS = ['1', '2', '3', '4', '5', '6' , '7', '8', '9', '10', '11', '12']
DAYS_OF_THE_WEEK = ["saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"]

def validated_input(options):
    """ Get validated input from the user according to limited options.

    INPUT:
    options: list. a list of the valid limited choices that the input must be one of them.

    OUTPUT: user_input: str. the validated user input.
    """
    user_input = ""
    while(user_input not in options):
        user_input = input("\nPlease pick from {}: ".format(options))
        user_input = user_input.lower()
        if(user_input not in options):
            print("Invalid choice!")
    return user_input

def get_filters():
    """Gets the filters that will be applied on the Data from the user.

    INPUT:
    Takes no input, filters is taken from the user as raw input.

    OUTPUT:
    city: str. the name of the city.
    month: int. the number of the month [1 - 12]. ('all' if no month filter wanted).
    day: The name of the day of the week. ('all' if no day filter wanted).
    """
    # Initializing variables
    city = ""
    month = "All"
    day = "All"
    filters = ""

    # Getting city name
    print("\nChose one of the 3 available cities to start exploring.")
    city = validated_input(CITIES)

    # Getting filteration preferences
    print("\nWould you like to filter based on Month only, Day of Week, Both, or No filters at all?")
    filters = validated_input(["month", "day", "both", "no"])

    # Getting month, and day filters
    if filters != "no":
        if filters == "month":
            month = validated_input(MONTHS)
        if filters == "day":
            day = validated_input(DAYS_OF_THE_WEEK)
        if filters == "both":
            month = validated_input(MONTHS)
            day = validated_input(DAYS_OF_THE_WEEK)

    return city.lower(), month, day.lower().title()

def load_data(city, month, day):
    """load the Data from the CSV file and prepair it according to the specified filters.

    INPUT:
    city: str. the name of the city.
    month: int. the number of the month [1 - 12]. ('all' if no month filter wanted).
    day: The name of the day of the week. ('all' if no day filter wanted).

    OUTPUT:
    df: DataFrame. the loaded data according to the applied filters.
    """
    df = pd.read_csv(CITY_DATA[city])
    # droping the enwanted column "Unnamed" that is added
    df.drop('Unnamed: 0', inplace=True, axis=1)

    # convert the Start Time column to datetime
    # Explaination: The "Start Time" series's type gets converted
    #               from "object" to "datetime64[ns]"
    #               from which we can extract specific time units eg: "month"
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract the "month" from the "Start Time" column to create "month" column
    # Explanation: "dt" part is used to deal with "Start Time" series
    #               as a "timedatelike" to be able to extract the month
    df['month'] = df['Start Time'].dt.month
    # As in extracting the month, the same is done for the day_of_week
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # Extracting the hour
    df['hour'] = df['Start Time'].dt.hour
    if month != 'All':
        df = df[df['month'] == int(month)]

    if day != 'All':
        df = df[df['day_of_week'] == day]

    return df

def explore_data(df, indx):
    """Explore the dataset by showing 5 rows of it.

    INPUT:
    df: DataFrame. The DataFrame that will be explored.
    indx: int. the index of the beginning of the 5 rows.

    OUTPUT:
    No output.
    """
    print("\nPrinting rows from {} to {} ...\n".format(indx, indx + 5))
    print(df[indx:indx + 5],"\n\n\n")

def time_stats(df):
    """Do time analysis on a DataFrame.

    INPUT:
    df: DataFrame. the DataFrame that will be analyzed.

    OUTPUT:
    No output, prints the analysis on the screen directly.
    """
    processing_time = time.time()

    popular_hour = df['hour'].mode()[0]
    popular_day_of_week = df['day_of_week'].mode()[0]
    popular_month = df['month'].mode()[0]
    print("-"*30 + " Viewing Time Statistics " + "-"*30)
    print('\n\nThe Most Common Month is: ', popular_month)
    print('\n\nThe Most Common Day of the week is: ', popular_day_of_week)
    print('\n\nThe Most common Hour is: ', popular_hour)
    # Calculating the time taken for the analysis.
    print("\n\nThis took {:.3f} seconds.\n\n".format(time.time() - processing_time))
    print("-"*70)

def stations_stats(df):
    """Do station analysis on a DataFrame.

    INPUT:
    df: DataFrame. the DataFrame that will be analyzed.

    OUTPUT:
    No output, prints the analysis on the screen directly.
    """
    processing_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    popular_end_station = df['End Station'].mode()[0]
    df['trip'] = df['Start Station'] + " - " + df['End Station']
    popular_trip = df['trip'].mode()[0]
    print("-"*30 + " Viewing Stations Statistics " + "-"*30)
    print('\n\nThe Most Common Start Station is: ', popular_start_station)
    print('\n\nThe Most common End Station is: ', popular_end_station)
    print('\n\nThe Most common Trip is: (from) ' + str(popular_trip.replace("-", "(to)")))
    # Calculating the time taken for the analysis.
    print("\n\nThis took {:.3f} seconds.\n\n".format(time.time() - processing_time))
    print("-"*70)

def trip_duration_stats(df):
    """Do Trips Duration analysis on a DataFrame.

    INPUT:
    df: DataFrame. the DataFrame that will be analyzed.

    OUTPUT:
    No output, prints the analysis on the screen directly.
    """
    processing_time = time.time()

    total_duration = df['Trip Duration'].sum()
    number_of_durations = df['Trip Duration'].notnull().sum()
    average_duration = total_duration / number_of_durations
    print("-"*30 + " Viewing Trips Durations Statistics " + "-"*30)
    print("\n\nThe total Duration of all trips is: {:.2f} Hours.".format(total_duration / 3600))
    print("\n\nThe average Durration of all trips is: {:.2f} Minutes.".format(average_duration / 60))

    # Calculating the time taken for the analysis.
    print("\n\nThis took {:.3f} seconds.\n\n".format(time.time() - processing_time))
    print("-"*70)

def user_stats(df):
    """Do User info analysis on a DataFrame.

    INPUT:
    df: DataFrame. the DataFrame that will be analyzed.

    OUTPUT:
    No output, prints the analysis on the screen directly.
    """
    processing_time = time.time()

    user_types = df['User Type'].value_counts()
    print("-"*30 + " Viewing User Types Statistics " + "-"*30)
    print("\nUser types and thier counts are: \n\n{}\n".format(str(user_types)))
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts()
        print("\nGender types and thier counts are: \n\n{}\n".format(str(gender_types)))
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print('\nThe Earliest year of birth is: {:.0f}.'.format(earliest_birth_year))
        print('\nThe Most Recent year of birth is: {:.0f}.'.format(recent_birth_year))
        print('\nThe Most common year of birth is: {:.0f}.'.format(common_birth_year))

        # Calculating the time taken for the analysis.
        print("\n\nThis took {:.3f} seconds.\n\n".format(time.time() - processing_time))
        print("-"*70)

def main():
    restart = ""
    while(True):
        print("\nYou have started a script for exploring bikeshare data in the US.\n")
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('\nWould you like to explore "{}" dataset first? (yes / no): '.format(city))
        do_explore = validated_input(["yes", "no"])
        indx = 0
        while (do_explore == 'yes'):
            explore_data(df, indx)
            print('\nWould you like to continue exploring "{}" dataset? (yes / no): '.format(city))
            do_explore = validated_input(["yes", "no"])
            indx += 5

        print("\n\nLet's get to the statistics...")
        stats = ""
        while(stats != "no"):
            print("What type of analysis do you want to see?")
            print("\n\nTime statistics: 1\n\nStations statistics: 2\n\nTrips Durations statistics: 3\n\nUser info statistics: 4\n")
            stats = validated_input(["1", "2", "3", "4"])
            if(stats == "1"):
                time_stats(df)
            elif(stats == "2"):
                stations_stats(df)
            elif(stats == "3"):
                trip_duration_stats(df)
            elif(stats == "4"):
                user_stats(df)
            print("\n\nWould you like to see another type of statistics?")
            stats = validated_input(["yes", "no"])

        print("\n\n\nWould you like to restart?")
        restart = validated_input(["yes", "no"])
        if(restart == "no"):
            break

if __name__ == "__main__":
    main()
