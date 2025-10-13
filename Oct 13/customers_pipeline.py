import pandas as pd
from datetime import datetime


def extract(file_path):
    """Extract data from CSV file."""
    return pd.read_csv(file_path)


def transform(df):
    """Add AgeGroup and filter customers."""

    # Add AgeGroup column based on age
    def get_age_group(age):
        if age < 30:
            return "Young"
        elif 30 <= age < 50:
            return "Adult"
        else:
            return "Senior"

    df["AgeGroup"] = df["Age"].apply(get_age_group)

    # Filter out customers younger than 20
    df = df[df["Age"] >= 20]
    return df


def load(df, output_path):
    """Save transformed data to new CSV file."""
    df.to_csv(output_path, index=False)


def main():
    start_time = datetime.now()

    # Step 1: Extract
    df = extract("customers.csv")

    # Step 2: Transform
    transformed_df = transform(df)

    # Step 3: Load
    load(transformed_df, "filtered_customers.csv")

    # Step 4: Print execution time
    print(f"Pipeline executed successfully at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
