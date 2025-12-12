#!/usr/bin/env python3
"""
Refactored Bikeshare Starter Code

Improvements made:
- Module-level documentation and clearer function docstrings
- Descriptive variable names (e.g., selected_city, data_frame)
- Added reusable helper: get_valid_input()
- Defensive checks for missing columns in datasets
- Clean main loop and separation of concerns for easier testing
"""

from typing import Tuple, List
import time
import pandas as pd

# Map of city name to CSV file name (used by load_data)
CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv"
}

VALID_MONTHS = ["january", "february", "march", "april", "may", "june", "all"]
VALID_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]


def get_valid_input(prompt: str, valid_options: List[str]) -> str:
    """
    Prompt the user until they provide a valid response.

    Args:
        prompt: The prompt message shown to the user.
        valid_options: Lowercase list of valid answers.

    Returns:
        The validated user input (lowercased).
    """
    user_response = input(prompt).strip().lower()
    while user_response not in valid_options:
        print(f"Invalid input. Choose one of: {', '.join(valid_options)}")
        user_response = input(prompt).strip().lower()
    return user_response


def get_filters() -> Tuple[str, str, str]:
    """
    Ask user to specify a city, month, and day to analyze.

    Returns:
        A tuple of (selected_city, selected_month, selected_day).
    """
    print("Hello! Let's explore some US bikeshare data.")

    # City input
    city_prompt = "Enter city (Chicago, New York City, Washington): "
    selected_city = get_valid_input(city_prompt, list(CITY_DATA.keys()))

    # Month input
    month_prompt = "Enter month (January - June) or 'all' to apply no month filter: "
    selected_month = get_valid_input(month_prompt, VALID_MONTHS)

    # Day input
    day_prompt = "Enter day of week (e.g., Monday) or 'all' to apply no day filter: "
    selected_day = get_valid_input(day_prompt, VALID_DAYS)

    print(f"\nFilters: city = {selected_city.title()}, month = {selected_month.title()}, day = {selected_day.title()}\n")
    return selected_city, selected_month, selected_day


def load_data(selected_city: str, selected_month: str, selected_day: str) -> pd.DataFrame:
    """
    Load city data into a DataFrame and apply month and day filters.

    Args:
        selected_city: city name (key of CITY_DATA)
        selected_month: month name or 'all'
        selected_day: day name or 'all'

    Returns:
        Filtered pandas DataFrame.
    """
    csv_file = CITY_DATA[selected_city]
    try:
        data_frame = pd.read_csv(csv_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file for {selected_city} not found: expected '{csv_file}' in repo root.")

    # Convert Start Time to datetime and create helper columns
    data_frame['Start Time'] = pd.to_datetime(data_frame['Start Time'])
    data_frame['month'] = data_frame['Start Time'].dt.month_name().str.lower()
    data_frame['day_of_week'] = data_frame['Start Time'].dt.day_name().str.lower()
    data_frame['hour'] = data_frame['Start Time'].dt.hour

    # Filter by month
    if selected_month != 'all':
        data_frame = data_frame[data_frame['month'] == selected_month]

    # Filter by day
    if selected_day != 'all':
        data_frame = data_frame[data_frame['day_of_week'] == selected_day]

    return data_frame


def time_stats(data_frame: pd.DataFrame) -> None:
    """Display statistics on the most frequent times of travel."""
    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    if data_frame.empty:
        print("No data for given filters.")
        return

    most_common_month = data_frame['month'].mode()[0].title()
    most_common_day = data_frame['day_of_week'].mode()[0].title()
    most_common_hour = int(data_frame['hour'].mode()[0])

    print(f"Most common month: {most_common_month}")
    print(f"Most common day of week: {most_common_day}")
    print(f"Most common start hour: {most_common_hour}:00")

    print(f"\nThis took {(time.time() - start_time):.4f} seconds.")


def station_stats(data_frame: pd.DataFrame) -> None:
    """Display statistics on the most popular stations and trips."""
    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    if data_frame.empty:
        print("No data for given filters.")
        return

    most_common_start_station = data_frame['Start Station'].mode()[0]
    most_common_end_station = data_frame['End Station'].mode()[0]

    # Create a combined trip column for the most frequent trip
    data_frame['trip_combo'] = data_frame['Start Station'] + " -> " + data_frame['End Station']
    most_common_trip = data_frame['trip_combo'].mode()[0]

    print(f"Most common start station: {most_common_start_station}")
    print(f"Most common end station: {most_common_end_station}")
    print(f"Most common trip (start -> end): {most_common_trip}")

    print(f"\nThis took {(time.time() - start_time):.4f} seconds.")


def trip_duration_stats(data_frame: pd.DataFrame) -> None:
    """Display statistics on the total and average trip duration."""
    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    if data_frame.empty:
        print("No data for given filters.")
        return

    total_duration = data_frame['Trip Duration'].sum()
    mean_duration = data_frame['Trip Duration'].mean()

    print(f"Total travel time (seconds): {int(total_duration)}")
    print(f"Mean travel time (seconds): {mean_duration:.2f}")

    print(f"\nThis took {(time.time() - start_time):.4f} seconds.")


def user_stats(data_frame: pd.DataFrame) -> None:
    """Display statistics on bikeshare users (user types, gender, birth year)."""
    print("\nCalculating User Stats...\n")
    start_time = time.time()

    if data_frame.empty:
        print("No data for given filters.")
        return

    # User types
    if 'User Type' in data_frame.columns:
        user_type_counts = data_frame['User Type'].value_counts()
        print("User Types:")
        print(user_type_counts.to_string())
    else:
        print("User Type data not available for this city.")

    # Gender breakdown (may not exist for all datasets)
    if 'Gender' in data_frame.columns:
        gender_counts = data_frame['Gender'].value_counts()
        print("\nGender counts:")
        print(gender_counts.to_string())
    else:
        print("\nGender data not available for this city.")

    # Birth year statistics (may not exist)
    if 'Birth Year' in data_frame.columns:
        earliest_year = int(data_frame['Birth Year'].min())
        most_recent_year = int(data_frame['Birth Year'].max())
        most_common_year = int(data_frame['Birth Year'].mode()[0])
        print(f"\nEarliest birth year: {earliest_year}")
        print(f"Most recent birth year: {most_recent_year}")
        print(f"Most common birth year: {most_common_year}")
    else:
        print("\nBirth Year data not available for this city.")

    print(f"\nThis took {(time.time() - start_time):.4f} seconds.")


def display_raw_data(data_frame: pd.DataFrame) -> None:
    """
    Offer the user to display raw data 5 rows at a time.
    """
    show_prompt = "Would you like to view 5 rows of raw data? Enter yes or no: "
    start_loc = 0
    while True:
        show_rows = get_valid_input(show_prompt, ['yes', 'no'])
        if show_rows == 'no':
            break
        # print next 5 rows
        print(data_frame.iloc[start_loc:start_loc + 5])
        start_loc += 5
        if start_loc >= len(data_frame):
            print("No more data to display.")
            break


def main() -> None:
    """
    Main program loop: get filters, load data, compute stats, optionally show raw data,
    and allow user to restart or quit.
    """
    while True:
        try:
            selected_city, selected_month, selected_day = get_filters()
            data_frame = load_data(selected_city, selected_month, selected_day)

            time_stats(data_frame)
            station_stats(data_frame)
            trip_duration_stats(data_frame)
            user_stats(data_frame)

            display_raw_data(data_frame)

            restart_prompt = "Would you like to restart? Enter yes or no: "
            restart_answer = get_valid_input(restart_prompt, ['yes', 'no'])
            if restart_answer == 'no':
                print("Exiting program. Thank you!")
                break
        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting.")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please check the CSV files and try again.")
            break


if __name__ == "__main__":
    main()
