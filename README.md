---
title: Project Samarth - Agricultural Data Q&A
emoji: 🌾
colorFrom: purple
colorTo: blue
sdk: streamlit
sdk_version: "1.33.0"
app_file: app.py
pinned: false
license: mit
---

# Project Samarth 🌾

AI-powered Q&A over live Indian agriculture and climate data with beautiful, modern UI and fully cited answers.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.33+-FF4B4B.svg)](https://streamlit.io)
[![data.gov.in](https://img.shields.io/badge/data-data.gov.in-00a65a.svg)](https://data.gov.in)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)

## ✨ What is Samarth?

Project Samarth fetches live datasets from data.gov.in (crop production, rainfall, and prices), normalizes them into clean schemas, and answers natural language questions with cross-domain reasoning. Every answer comes with sources, filters, and confidence.

### Highlights
- 🤖 Natural language understanding via Gemini
- 🌧️ + 🌾 Cross-domain reasoning (rainfall × production)
- 📑 Source citations and filters for transparency
- ⚡ Smart caching to respect API limits
- 🧭 Entity normalization (states, districts, crops)
- 🎨 Modern Streamlit UI with animated gradients and glassmorphism

## 🚀 Quickstart (Windows PowerShell)

```powershell
# 1) Clone and enter the project
git clone https://github.com/your-username/project-samarth.git
cd project-samarth

# 2) Create and activate a virtual environment
py -3.11 -m venv .venv
. .venv\Scripts\Activate.ps1

# 3) Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4) Configure API keys
Copy-Item .env.example .env  # or create a new .env file
# Edit .env and set:
# DATA_GOV_IN_API_KEY=your_data_gov_in_key
# GEMINI_API_KEY=your_gemini_key

# 5) Run the app
streamlit run app.py
```

Optional (macOS/Linux):
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env  # or create .env
streamlit run app.py
```

## ⚙️ Configuration

Create a `.env` in the project root with:

```
DATA_GOV_IN_API_KEY=your_data_gov_in_key
GEMINI_API_KEY=your_gemini_key
```

## 🧠 Supported Questions

- “Which state had more rice production in 2015 — Karnataka or Tamil Nadu?”
- “Compare rainfall in Karnataka vs Tamil Nadu for the last 5 years.”
- “Which district in Karnataka has the highest maize production?”
- “Is there a correlation between rainfall and rice yield in Andhra Pradesh?”

## 🧩 Architecture (High level)

```
┌─────────────────┐
│  User Question  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Query Planner (Gemini)         │ Intent, entities, validation
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Query Executor                 │ Live fetch, normalize, analyze
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│  Answer + Data + Citations      │ Confidence + sources
└─────────────────────────────────┘
```

## 📦 Project Structure

```
project-samarth/
├── app.py
├── requirements.txt
├── config/
│   └── data_sources.json
└── src/
    ├── __init__.py
    ├── answer_generator.py
    ├── cache.py
    ├── data_connector.py
    ├── data_quality.py
    ├── mappings.py
    ├── normalizers.py
    ├── query_executor.py
    ├── query_planner.py
    └── schema_mapper.py
```

## 🐍 Minimal Python Usage

```python
import os
from dotenv import load_dotenv
from src import DataGovInConnector, QueryExecutor, QueryPlanner

load_dotenv()

connector = DataGovInConnector(api_key=os.getenv("DATA_GOV_IN_API_KEY"))
planner = QueryPlanner(api_key=os.getenv("GEMINI_API_KEY"))
executor = QueryExecutor(connector)

question = "Which state had more rice production in 2015 - Karnataka or Tamil Nadu?"
plan = planner.parse_question(question)
result = executor.execute(plan)

print(result.answer)
print(result.metadata)
```

## 🗃️ Data Sources

- Crop Production: 1997–present (district/state level)
- Rainfall (IMD): 1901–2017 (sub-division level; aggregated to state)
- Commodity Prices (Agmarknet): 2016–present (daily)

## 🛠️ Troubleshooting

- “Import 'streamlit' could not be resolved” → Install dependencies: `pip install -r requirements.txt`
- Empty answers → Ensure years exist in datasets (rainfall ends at 2017) and that state/crop names match mappings.
- API throttling → The app caches results (24h TTL). Re-run later or adjust in `src/cache.py`.

## 📜 License

MIT License — see LICENSE (or repo metadata) for details.

## 🙌 Acknowledgments

- Data: data.gov.in (Government of India)
- Weather: India Meteorological Department (IMD)
- AI: Google Gemini

—

Built with ❤️ for open data and farmers. Last updated: October 2025.
