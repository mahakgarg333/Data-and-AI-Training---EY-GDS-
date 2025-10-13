import pandas as pd
from datetime import datetime

def extract(file_path):
    """Extract data from CSV file."""
    return pd.read_csv(file_path)


def transform(df):
    """Add RestockNeeded and TotalValue columns."""
    # Add RestockNeeded column
    df["RestockNeeded"] = df.apply(
        lambda row: "Yes" if row["Quantity"] < row["ReorderLevel"] else "No",
        axis=1
    )

    # Add TotalValue column
    df["TotalValue"] = df["Quantity"] * df["PricePerUnit"]

    return df


def load(df, output_path):
    """Load the transformed data into a new CSV file."""
    df.to_csv(output_path, index=False)


def main():
    # Step 1: Extract
    df = extract("inventory.csv")

    # Step 2: Transform
    transformed_df = transform(df)

    # Step 3: Load
    load(transformed_df, "restock_report.csv")

    # Step 4: Print completion message with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Inventory pipeline completed at {timestamp}")


if __name__ == "__main__":
    main()
