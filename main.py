import pandas as pd

def Wrangling(df):
    data = df[["server_id", "Timestamp", "service_id", "service_description", "CPU_percent"]]

    data["Timestamp"] = pd.to_datetime(data["Timestamp"])    

    
    # Convert to datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], dayfirst=True)

    # Check timestamp interval 
    # Sort by time
    df = df.sort_values("Timestamp")
    
    # Compute differences
    df["delta"] = df["Timestamp"].diff()
    
    # Convert to minutes
    df["delta_minutes"] = df["delta"].dt.total_seconds() / 60
    
    print(df["delta_minutes"].value_counts().head(10))

    # Count how many services per timestamp
    service_counts = (
        df.groupby("Timestamp")["service_id"]
          .nunique()
          .reset_index(name="unique_services")
    )


    # Show a few examples
    data["parallel_flag"] = (service_counts["unique_services"] > 1).astype(int)
    data = data.merge(service_counts, on="Timestamp", how="left")

    
    data["hour"] = data["Timestamp"].dt.hour
    data["day"] = data["Timestamp"].dt.day
    data["day_of_week"] = data["Timestamp"].dt.dayofweek 
    data["month"] = data["Timestamp"].dt.month
    data["is_weekend"] = data["day_of_week"].isin([5, 6]).astype(int)
    # Add working hour flag (1 = working hours, 0 = non-working hours)
    data["is_working_hour"] = data["hour"].between(8, 17).astype(int)

        # --- Add seasons (Northern Hemisphere convention) ---
    def get_season(month):
        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"
    
    data["season"] = data["month"].apply(get_season)
    
        

    print(data["service_description"].unique())
    print(data["server_id"].unique())
    print("-------------------- data length ----------------")
    print("length general data:\n", len(data))
    print("length of server_id:\n", len(data["server_id"].unique()))
    print("length of service_id:\n", len(data["service_id"].unique()))
    print("--------------------- Different Group By ------------- ")
    print("service_description group by Cpu percent")
    grouped = data.groupby("service_description")["CPU_percent"].mean().reset_index()
    print("Average CPU usage per service:\n", grouped)
    print("-------------- Check Missing Values for each column --------------")
    for col in data.columns:
        missing_count = data[col].isnull().sum()
        print(f"{col}: {missing_count} missing values")
     
    data = data[["server_id", "Timestamp", "service_id", "service_description", "CPU_percent", "hour", "day_of_week", "is_weekend", "is_working_hour", "season", "parallel_flag", "unique_services"]].copy()
    data.to_csv("data/end_data.csv", index=False)

df = pd.read_csv("data/raw_data.csv")

Wrangling(df)

