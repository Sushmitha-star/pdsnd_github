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

    print(f"\nFilters chosen → City: {selected_city.title()}, Month: {selected_month.title()}, Day: {selected_day.title()}\n")
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
        raise FileNotFoundError(f"CSV file not found for {selected_city}. Expected file: '{csv_file}'")

    # Convert Start Time to datetime and create helper columns
    data_frame["Start Time"] = pd.to_datetime(data_frame["Start Time"])
    data_frame["month"] = data_frame["Start Time"].dt.month_name().str.lower()
    data_frame["day_of_week"] = data_frame["Start Time"].dt.day_name().str.lower()
    data_frame["hour"] = data_frame["Start Time"].dt.hour

    # Apply filters
    if selected_month != "all":
        data_frame = data_frame[data_frame["month"] == selected_month]

    if selected_day != "all":
        data_frame = data_frame[data_frame["day_of_week"] == selected_day]

    return data_frame


def time_stats(data_frame: pd.DataFrame) -> None:
    """Display statistics on the most frequent times of travel."""
    print("\nCalculating Most Frequent Travel Times...\n")
    start_time = time.time()

    if data_frame.empty:
        print("No data available for selected filters.")
        return

    print(f"Most common month: {data_frame['month'].mode()[0].title()}")
    print(f"Most common day: {data_frame['day_of_week'].mode()[0].title()}")
    print(f"Most common hour: {int(data_frame['hour'].mode()[0])}:00")

    print(f"\nCompleted in {(time.time() - start_time):.4f} seconds.")


def station_stats(data_frame: pd.DataFrame) -> None:
    """Display statistics on the most popular stations and trip."""
    print("\nCalculating Station Statistics...\n")
    start_time = time.time()

    if data_frame.empty:
        print("No data available for selected filters.")
        return

    print(f"Most common start station: {data_frame['Start Station'].mode()[0]}")
    print(f"Most common end station: {data_frame['End Station'].mode()[0]}")

    data_frame["trip_combo"] = data_frame["Start Station"] + " → " + data_frame["End Station"]
    print(f"Most frequent trip: {data_frame['trip_combo'].mode()[0]}")

    print(f"\nCompleted in {(time.time() - start_time):.4f} seconds.")


def trip_duration_stats(data_frame: pd.DataFrame) -> None:
    """Display statistics on total and average trip duration."""
    print("\nCalculating Trip Duration Stats...\n")
    start_time = time.time()

    if data_frame.empty:
        print("No data available for selected filters.")
        return

    print(f"Total travel time: {int(data_frame['Trip Duration'].sum())} seconds")
    print(f"Average travel time: {data_frame['Trip Duration'].mean():.2f} seconds")

    print(f"\nCompleted in {(time.time() - start_time):.4f} seconds.")


def user_stats(data_frame: pd.DataFrame) -> None:
    """Display statistics on bikeshare users."""
    print("\nCalculating User Stats...\n")
    start_time = time.time()

    if data_frame.empty:
        print("No data available for selected filters.")
        return

    # User Types
    if "User Type" in data_frame:
        print("User Types:")
        print(data_frame["User Type"].value_counts().to_string())
    else:
        print("User Type data not available.")

    # Gender
    if "Gender" in data_frame:
        print("\nGender Breakdown:")
        print(data_frame["Gender"].value_counts().to_string())
    else:
        print("\nGender data not available.")

    # Birth Year
    if "Birth Year" in data_frame:
        print(f"\nEarliest birth year: {int(data_frame['Birth Year'].min())}")
        print(f"Most recent birth year: {int(data_frame['Birth Year'].max())}")
        print(f"Most common birth year: {int(data_frame['Birth Year'].mode()[0])}")
    else:
        print("\nBirth Year data not available.")

    print(f"\nCompleted in {(time.time() - start_time):.4f} seconds.")


def display_raw_data(data_frame: pd.DataFrame) -> None:
    """Prompt user to display raw data 5 rows at a time."""
    start_loc = 0

    while True:
        view_data = get_valid_input("Would you like to view 5 rows of raw data? (yes/no): ", ["yes", "no"])

        if view_data == "no":
            break

        print(data_frame.iloc[start_loc:start_loc + 5])
        start_loc += 5

        if start_loc >= len(data_frame):
            print("No more data to display.")
            break


def main() -> None:
    """Main loop to run bikeshare program."""
    while True:
        selected_city, selected_month, selected_day = get_filters()
        data_frame = load_data(selected_city, selected_month, selected_day)

        time_stats(data_frame)
        station_stats(data_frame)
        trip_duration_stats(data_frame)
        user_stats(data_frame)
        display_raw_data(data_frame)

        restart = get_valid_input("Would you like to restart? (yes/no): ", ["yes", "no"])
        if restart == "no":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()

# commit marker 1765526493
