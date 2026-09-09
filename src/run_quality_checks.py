import pandas as pd
import yaml
import json
import os
import glob
from datetime import datetime
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.bool_, np.int64, np.float64)):
            return obj.item()
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

def load_latest_bronze_file(dataset_name):
    pattern = f"data/bronze/{dataset_name}_*.parquet"
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"No Bronze file found for {dataset_name}")
    latest = max(files, key=os.path.getmtime)
    print(f"📂 Loading: {os.path.basename(latest)}")
    return pd.read_parquet(latest)

def load_rules():
    with open("configs/quality_rules.yaml", 'r') as file:
        return yaml.safe_load(file)

def check_not_null(df, column):
    null_count = df[column].isnull().sum()
    return {
        "passed": bool(null_count == 0),
        "null_count": int(null_count),
        "total_rows": len(df),
        "failure_percentage": round((null_count / len(df)) * 100, 2)
    }

def check_date_not_future(df, column):
    try:
        df[column] = pd.to_datetime(df[column])
        future_count = (df[column] > pd.Timestamp.now()).sum()
        return {
            "passed": bool(future_count == 0),
            "future_count": int(future_count),
            "total_rows": len(df),
            "failure_percentage": round((future_count / len(df)) * 100, 2)
        }
    except:
        return {"passed": False, "error": "Could not parse dates", "total_rows": len(df)}

def check_accepted_values(df, column, accepted_values):
    invalid_count = (~df[column].isin(accepted_values)).sum()
    return {
        "passed": bool(invalid_count == 0),
        "invalid_count": int(invalid_count),
        "total_rows": len(df),
        "failure_percentage": round((invalid_count / len(df)) * 100, 2)
    }

def check_foreign_key_exists(df, column, reference_table, reference_column):
    try:
        ref_df = load_latest_bronze_file(reference_table)
        valid_keys = set(ref_df[reference_column].dropna().unique())
        df_keys = set(df[column].dropna().unique())
        missing_keys = df_keys - valid_keys
        orphan_count = df[~df[column].isin(valid_keys)].shape[0]
        return {
            "passed": bool(orphan_count == 0),
            "orphan_count": int(orphan_count),
            "total_rows": len(df),
            "missing_keys": list(missing_keys)[:10],
            "failure_percentage": round((orphan_count / len(df)) * 100, 2)
        }
    except Exception as e:
        return {"passed": False, "error": str(e), "total_rows": len(df)}

def check_date_less_than(df, column, compare_column):
    try:
        df[column] = pd.to_datetime(df[column])
        df[compare_column] = pd.to_datetime(df[compare_column])
        invalid_count = (df[column] >= df[compare_column]).sum()
        return {
            "passed": bool(invalid_count == 0),
            "invalid_count": int(invalid_count),
            "total_rows": len(df),
            "failure_percentage": round((invalid_count / len(df)) * 100, 2)
        }
    except:
        return {"passed": False, "error": "Could not parse dates", "total_rows": len(df)}

def check_between(df, column, min_val, max_val):
    invalid_count = ((df[column] < min_val) | (df[column] > max_val)).sum()
    return {
        "passed": bool(invalid_count == 0),
        "invalid_count": int(invalid_count),
        "total_rows": len(df),
        "failure_percentage": round((invalid_count / len(df)) * 100, 2)
    }

def check_not_empty(df, column):
    empty_count = (df[column].astype(str).str.strip() == '').sum()
    return {
        "passed": bool(empty_count == 0),
        "empty_count": int(empty_count),
        "total_rows": len(df),
        "failure_percentage": round((empty_count / len(df)) * 100, 2)
    }

def run_quality_checks():
    rules = load_rules()
    results = {
        "run_timestamp": datetime.now().isoformat(),
        "dataset_checks": {}
    }
    error_count = 0
    warning_count = 0

    for dataset_name, dataset_rules in rules['rules'].items():
        print(f"\n🔍 Checking {dataset_name.upper()} dataset...")
        try:
            df = load_latest_bronze_file(dataset_name)
            dataset_results = []
            for rule in dataset_rules:
                rule_type = rule['check']
                column = rule['column']
                severity = rule['severity']
                print(f"  - {rule['rule_name']} ({severity})...", end=" ")
                
                if rule_type == 'not_null':
                    result = check_not_null(df, column)
                elif rule_type == 'date_not_future':
                    result = check_date_not_future(df, column)
                elif rule_type == 'accepted_values':
                    result = check_accepted_values(df, column, rule['accepted'])
                elif rule_type == 'foreign_key_exists':
                    result = check_foreign_key_exists(df, column, rule['reference_table'], rule['reference_column'])
                elif rule_type == 'date_less_than':
                    result = check_date_less_than(df, column, rule['compare_column'])
                elif rule_type == 'between':
                    result = check_between(df, column, rule['min'], rule['max'])
                elif rule_type == 'not_empty':
                    result = check_not_empty(df, column)
                else:
                    result = {"passed": False, "error": f"Unknown check type: {rule_type}"}
                
                result['rule_name'] = rule['rule_name']
                result['severity'] = severity
                result['column'] = column
                result['description'] = rule.get('description', '')
                
                if not result.get('passed', False):
                    if severity == 'ERROR':
                        error_count += 1
                        print("❌ FAILED (ERROR)")
                    else:
                        warning_count += 1
                        print("⚠️  FAILED (WARNING)")
                    if 'failure_percentage' in result:
                        print(f"     → {result['failure_percentage']}% of records failed")
                else:
                    print("✅ PASSED")
                
                dataset_results.append(result)
            results['dataset_checks'][dataset_name] = dataset_results
        except Exception as e:
            print(f"❌ Error loading {dataset_name}: {e}")
            results['dataset_checks'][dataset_name] = [{"error": str(e), "passed": False}]
    
    results['summary'] = {
        "total_error_failures": error_count,
        "total_warning_failures": warning_count,
        "overall_status": "❌ FAILED" if error_count > 0 else "⚠️  WARNINGS" if warning_count > 0 else "✅ PASSED"
    }
    return results

if __name__ == "__main__":
    print("🚀 Running Quality Checks on Bronze Layer...\n")
    print("=" * 60)
    results = run_quality_checks()
    print("\n" + "=" * 60)
    print(f"\n📊 SUMMARY: {results['summary']['overall_status']}")
    print(f"   ERROR failures: {results['summary']['total_error_failures']}")
    print(f"   WARNING failures: {results['summary']['total_warning_failures']}")
    os.makedirs("logs", exist_ok=True)
    report_file = f"logs/quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w') as f:
        json.dump(results, f, indent=2, cls=NumpyEncoder)
    print(f"\n📄 Full report saved to: {report_file}")
    print("\n✨ Quality check complete!")
