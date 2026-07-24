# SpaceX Falcon 9 Landing Prediction

End-to-end data science capstone analyzing Falcon 9 launches and predicting whether the first stage lands successfully.

## Project objective

SpaceX can reduce launch costs by reusing the Falcon 9 first stage. This project studies the factors associated with successful landings and builds classification models that estimate landing outcomes from launch characteristics.

## Workflow

1. Collect and clean launch records
2. Explore launch-site, payload, orbit, and time-based patterns
3. Query launch data with SQL
4. Analyze launch sites geographically
5. Build an interactive Plotly Dash dashboard
6. Train and compare classification models
7. Summarize business findings and model limitations

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── data/
│   └── README.md
├── sql/
│   └── launch_analysis.sql
└── src/
    ├── exploratory_analysis.py
    ├── modeling.py
    └── dashboard.py
```

## Main findings

- Landing success improved over time as the Falcon 9 program matured.
- Launch site, orbit, payload mass, booster version, and flight number all provide useful predictive information.
- Success rates differ across launch sites and mission profiles.
- Model comparison is necessary because a strong training score does not guarantee reliable performance on unseen launches.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Place the course CSV files in the project root or in a `data/` directory, then run:

```bash
python src/exploratory_analysis.py
python src/modeling.py
python src/dashboard.py
```

The dashboard opens at `http://127.0.0.1:8050/`.

## Tools

Python, pandas, NumPy, Matplotlib, Seaborn, Plotly, Dash, scikit-learn, SQL, and Folium.

## Author

Thomas Caruso
