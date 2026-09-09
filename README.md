<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=MedLearn%20Data%20Hub&fontSize=60&fontAlignY=35&animation=twinkling&fontColor=fff" width="100%">
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=500&color=00BFFF&center=true&vCenter=true&width=800&lines=End-to-End+Data+Observability;Automated+Quality+Assurance;REST+API+Driven+Ingestion;Real-Time+Healthcare+Analytics" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-green?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.20+-red?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge" />
</p>

---

## 📖 1. The Problem We Solve

In the healthcare industry, data comes from dozens of disconnected sources—EHR systems, lab equipment, patient portals, and manual entry. This data is often **inconsistent, incomplete, or just plain wrong**. 

Common issues include:
- ❌ **Null Patient IDs** making it impossible to link records.
- ❌ **Orphan Visit Records** with no associated patient.
- ❌ **Future Birth Dates** breaking age calculations.
- ❌ **Inconsistent Gender Formats** (`M`, `Male`, `1`, etc.).
- ❌ **Lab Value Outliers** (e.g., Glucose = 9999 mg/dL).

**The Result:** Business users lose trust in the data, leading to bad decisions and wasted time manually cleaning spreadsheets.

---

## 🎯 2. Our Solution: MedLearn Data Hub

**MedLearn Data Hub** is a **Data Observability Platform** that sits between raw data ingestion and business dashboards. It automatically validates incoming data against a configurable set of quality rules, generates real-time health reports, and provides a visual dashboard to monitor data trustworthiness.

**Core Objectives:**
1.  **Immutability:** Never lose raw data. Every upload is timestamped and stored.
2.  **Automation:** Eliminate manual data cleaning with automated, rule-based validation.
3.  **Configurability:** Allow business analysts to define quality rules in YAML—no code changes required.
4.  **Observability:** Provide a live dashboard that shows *how healthy* the data is, not just what the data contains.

---

## 🏗️ 3. System Architecture (How It Works)

The platform follows a **Medallion Architecture** (Bronze → Silver → Gold), a best practice in modern data engineering.

```mermaid
graph LR
    A[📁 CSV Upload] --> B{⚡ FastAPI Gateway};
    B --> C[🛡️ Bronze Layer];
    C --> D[⚙️ YAML Quality Engine];
    D --> E{📊 Quality Report JSON};
    E --> F[📈 Streamlit Dashboard];

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style C fill:#bfb,stroke:#333,stroke-width:2px
    style D fill:#fbf,stroke:#333,stroke-width:2px
    style F fill:#ffb,stroke:#333,stroke-width:2px
