import argparse
from datetime import datetime, timedelta

def parse_args():
    parser = argparse.ArgumentParser(description="Calculate a new date based on a starting date and a time delta.")
    
    # Define command-line arguments
    parser.add_argument('-y', "--year", type=int, default=2022, help="Starting year")
    parser.add_argument('-m', "--month", type=int, default=10, help="Starting month")
    parser.add_argument('-d', "--day", type=int, default=8, help="Starting day")
    parser.add_argument('-H', "--hour", type=int, default=12, help="Starting hour")
    parser.add_argument('-M', "--minute", type=int, default=0, help="Starting minute")

    parser.add_argument('-dd', "--delta_day", type=int, default=1, help="Time delta in days")
    parser.add_argument('-dH', "--delta_hour", type=int, default=0, help="Time delta in hours")
    parser.add_argument('-dM', "--delta_minute", type=int, default=0, help="Time delta in minutes")

    return parser.parse_args()

def main():
    args = parse_args()

    # Create a datetime object for the starting date
    start_date = datetime(args.year, args.month, args.day, args.hour, args.minute)

    # Create a timedelta based on the input values
    time_delta = timedelta(
        days=args.delta_day,
        hours=args.delta_hour,
        minutes=args.delta_minute,
    )

    from analysis_pipeline import analyze_data_by
    while True:
        analyze_data_by(start_date.year, start_date.month, start_date.day, start_date.hour, start_date.minute)
        start_date -= time_delta

if __name__ == "__main__":
    main()