HR Analytics Pipeline with Elasticsearch

Data processing pipeline for HR analytics with Elasticsearch indexing and Kibana visualization.

Business requirements:
- Filter employees by salary range (50 000 – 200 000 RUB)
- Filter employees by height (> 160 cm)
- Index filtered data into Elasticsearch
- Visualize metrics in Kibana dashboard

Architecture
------------
Source data (JSON)
        ↓
Business logic filtering (Python)
        ↓
Elasticsearch indexing
        ↓
Kibana dashboard visualization

Technology stack
----------------
- Python 3.11
- Elasticsearch 8.x client library
- Kibana 8.x for visualization

Project structure
-----------------
config/
    index_mapping.json    Elasticsearch index mapping definition
src/
    loader.py             Main data processing and indexing module
docs/
    dashboard.md          Dashboard specification and metrics
requirements.txt          Python dependencies
.env.example              Environment variables template
.gitignore                Git ignore rules

Setup and execution
-------------------
1. Clone repository (if applicable)
   git clone https://github.com/anastasiia-matveeva/hr-analytics-elastic.git

2. Create virtual environment and install dependencies
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

3. Configure connection parameters
   copy .env.example .env
   # Edit .env with actual Elasticsearch credentials

4. Prepare source data
   # Place source JSON file into data/job.json
   # Note: data/ directory is excluded from Git by .gitignore

5. Execute data loading pipeline
   python -m src.loader

Security notes
--------------
- Connection credentials are passed via environment variables (.env)
- Source data files are excluded from version control (.gitignore)
- No personally identifiable information is stored in the repository
- All data processing complies with internal information security policies

Author
------
Matveeva Anastasiia Ruslanovna
Senior Specialist, Department of Development and New Businesses
JSC NPO CNIITMASH (Rosatom State Corporation)
armatveeva@rosatom.ru

License
-------
MIT License
Copyright (c) 2026 Anastasiia Matveeva
