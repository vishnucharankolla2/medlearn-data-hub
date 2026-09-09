import pandas as pd
import os
from datetime import datetime
import glob

def ingest_to_bronze(source_pattern, destination_folder="data/bronze"):
    # Find all raw CSV files matching the pattern
    csv_files = glob.glob(source_pattern)
    
    for file_path in csv_files:
        # Read the raw data
        df = pd.read_csv(file_path)
        
        # Add ingestion timestamp for data lineage
        df['_ingest_timestamp'] = datetime.now().isoformat()
        
        # Create filename with timestamp
        base_name = os.path.basename(file_path).replace("_raw.csv", "")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{base_name}_{timestamp}.parquet"
        
        # Ensure folder exists
        os.makedirs(destination_folder, exist_ok=True)
        
        # Save to bronze (as parquet to save space and preserve data types)
        full_path = os.path.join(destination_folder, new_filename)
        df.to_parquet(full_path, index=False)
        print(f"✅ Ingested {file_path} -> {full_path}")
        print(f"   Records: {len(df)}, Columns: {list(df.columns)}")

if __name__ == "__main__":
    # Move all raw files to bronze
    ingest_to_bronze("data/*_raw.csv")
    
    print("\n🎉 Bronze layer populated successfully. Raw data is now immutable!")
    print("📂 Check the data/bronze/ folder for Parquet files with timestamps.")
