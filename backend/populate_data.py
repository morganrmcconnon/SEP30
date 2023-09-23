if __name__ == '__main__':    
    from datetime import datetime, timedelta
    # Wrap inside if __name__ == '__main__' to avoid circular import
    from analysis_pipeline import analyze_data_by

    # Get the current time, but fix the year to 2022 because the Twitter Stream collection only contains tweets up to 2022
    starting_time = datetime(2022, 8, 31, 23, 59, 0)
    # Calculate the previous [period] minutes from the starting_time and download the tweets at that time
    time_period = 10100
    for _ in range(time_period):
        analyze_data_by(starting_time.year, starting_time.month, starting_time.day, starting_time.hour, starting_time.minute)
        starting_time -= timedelta(minutes=1)

