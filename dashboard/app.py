import streamlit as st
import pandas as pd
import json
import glob
import os
from datetime import datetime

st.set_page_config(page_title="MedLearn Quality Dashboard", layout="wide")

st.title("🏥 MedLearn Data Hub - Quality Dashboard")
st.markdown("---")

# Find the latest quality report
report_files = glob.glob("logs/quality_report_*.json")
if not report_files:
    st.error("No quality reports found. Run the quality checks first!")
    st.stop()

latest_report = max(report_files, key=os.path.getmtime)
st.caption(f"📄 Loaded report: {os.path.basename(latest_report)}")

# Load the report
with open(latest_report, 'r') as f:
    data = json.load(f)

# --- Summary Metrics ---
summary = data.get('summary', {})
col1, col2, col3, col4 = st.columns(4)

status_color = "🟢" if "PASSED" in summary.get('overall_status', '') else "🟡" if "WARNING" in summary.get('overall_status', '') else "🔴"
col1.metric("Overall Status", f"{status_color} {summary.get('overall_status', 'N/A')}")
col2.metric("❌ ERROR Failures", summary.get('total_error_failures', 0))
col3.metric("⚠️ WARNING Failures", summary.get('total_warning_failures', 0))
col4.metric("Run Timestamp", data.get('run_timestamp', 'N/A')[:16])

st.markdown("---")

# --- Prepare Data for Visualization ---
rows = []
for dataset, checks in data.get('dataset_checks', {}).items():
    for check in checks:
        passed = check.get('passed')
        if isinstance(passed, bool):
            status = "✅ PASSED" if passed else ("❌ FAILED" if check.get('severity') == 'ERROR' else "⚠️ FAILED")
        else:
            status = "❓ UNKNOWN"
        
        failure_pct = check.get('failure_percentage')
        if failure_pct is None:
            failure_pct = 0
        
        rows.append({
            "Dataset": dataset.upper(),
            "Rule": check.get('rule_name', 'Unknown'),
            "Severity": check.get('severity', 'N/A'),
            "Status": status,
            "Failure %": failure_pct,
            "Description": check.get('description', '')
        })

df = pd.DataFrame(rows)

# --- Charts ---
st.subheader("📊 Failure Percentage by Rule")
if not df.empty:
    failed_df = df[df['Status'] != '✅ PASSED']
    if not failed_df.empty:
        chart_data = failed_df.set_index('Rule')[['Failure %']]
        st.bar_chart(chart_data, color="#ff4b4b")
    else:
        st.success("🎉 All quality checks passed! No failures to show.")
    
    st.markdown("---")
    
    # --- Full Results Table ---
    st.subheader("📋 Detailed Quality Results")
    st.dataframe(df, use_container_width=True)
    
    # --- Show Failed Records Details ---
    st.subheader("🔍 Failed Rule Details")
    failed_items = df[df['Status'] != '✅ PASSED']
    if not failed_items.empty:
        for _, row in failed_items.iterrows():
            severity_emoji = "🔴" if row['Severity'] == 'ERROR' else "🟡"
            with st.expander(f"{severity_emoji} {row['Dataset']} - {row['Rule']} ({row['Severity']})"):
                st.write(f"**Failure Rate:** {row['Failure %']}%")
                st.write(f"**Description:** {row['Description']}")
    else:
        st.success("No failed rules to display.")
else:
    st.warning("No quality check data found in the report.")

st.markdown("---")
st.caption(f"⚡ MedLearn Data Hub | Powered by Streamlit | Report generated at {data.get('run_timestamp', '')}")
