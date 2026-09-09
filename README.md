<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=MedLearn%20Data%20Hub&fontSize=60&fontAlignY=35&animation=twinkling&fontColor=fff" width="100%">
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=500&color=00BFFF&center=true&vCenter=true&width=600&lines=End-to-End+Data+Observability;Automated+Quality+Assurance;REST+API+Driven+Ingestion;Real-Time+Healthcare+Analytics" alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-green?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.20+-red?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

---

## 📖 Overview

**MedLearn Data Hub** solves the critical "garbage in, garbage out" problem. It ingests messy CSV data, validates it against configurable rules, and provides real-time data health visibility.

---

## 🏗️ Architecture Flow

```mermaid
graph LR
    A[📁 CSV Upload] --> B{⚡ FastAPI Gateway};
    B --> C[🛡️ Bronze Layer];
    C --> D[⚙️ YAML Quality Engine];
    D --> E{📊 Quality Report};
    E --> F[📈 Streamlit Dashboard];
