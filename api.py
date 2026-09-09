from fastapi import FastAPI, File, UploadFile, HTTPException
import subprocess
import os
import shutil
from datetime import datetime
import glob

app = FastAPI(title="MedLearn Ingest API", description="Auto-ingest healthcare data")

os.makedirs("data", exist_ok=True)
os.makedirs("data/bronze", exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "MedLearn Data Hub API is running! Use POST /ingest to upload CSV files."}

@app.post("/ingest")
async def ingest_data(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = f"data/{safe_filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    print(f"✅ File received: {file_path}")
    
    print("🔄 Running Bronze Ingestion...")
    ingest_result = subprocess.run(
        ["python3", "src/ingest_bronze.py"],
        capture_output=True,
        text=True
    )
    
    print("🔄 Running Quality Checks...")
    quality_result = subprocess.run(
        ["python3", "src/run_quality_checks.py"],
        capture_output=True,
        text=True
    )
    
    report_files = glob.glob("logs/quality_report_*.json")
    latest_report = max(report_files, key=os.path.getmtime) if report_files else None
    
    return {
        "status": "success",
        "message": f"File {safe_filename} processed successfully!",
        "bronze_log": ingest_result.stdout,
        "quality_log": quality_result.stdout,
        "latest_quality_report": latest_report
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
