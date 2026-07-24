# SpaceX Falcon 9 Landing Prediction

End-to-end data science capstone analyzing Falcon 9 launches and predicting whether the first stage lands successfully.

## Project objective

SpaceX lowers launch costs by recovering and reusing Falcon 9 first stages. This project studies the variables associated with successful landings and compares classification models that estimate landing outcomes from launch characteristics.

## Project workflow

1. Clean and prepare Falcon 9 launch records
2. Explore launch-site, payload, orbit, and time-based patterns
3. Query launch data with SQL
4. Analyze launch sites geographically with Folium
5. Build an interactive Plotly Dash dashboard
6. Tune and compare classification models
7. Summarize findings, limitations, and business relevance

## Dataset snapshot

- 90 Falcon 9 launches
- 60 successful landings
- 30 unsuccessful landings
- 66.7% overall landing success rate
- Payload range of approximately 350 kg to 15,600 kg

## Repository structure

```text
.
├── README.md
├── PROJECT_REPORT.md
├── requirements.txt
├── data/
│   ├── README.md
│   ├── dataset_part_2.csv
│   └── spacex_launch_dash.csv
├── sql/
│   └── launch_analysis.sql
└── src/
    ├── common.py
    ├── exploratory_analysis.py
    ├── launch_map.py
    ├── dashboard.py
    └── modeling.py
```

## Main findings

- Landing success improved substantially as the Falcon 9 program matured.
- Launch site, orbit, payload mass, flight number, reuse history, and booster characteristics provide useful predictive information.
- KSC LC-39A showed a higher landing-success rate than CCAFS SLC-40 in the analyzed sample.
- The Decision Tree produced the strongest cross-validation result in the final report at approximately 86.3%.
- Final held-out test accuracy was approximately 77.8%, or 14 correct predictions out of 18 test records.

See [`PROJECT_REPORT.md`](PROJECT_REPORT.md) for the written summary.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Generate exploratory charts:

```bash
python src/exploratory_analysis.py
```

Create the interactive launch map:

```bash
python src/launch_map.py
```

Train and compare the models:

```bash
python src/modeling.py
```

Run the dashboard:

```bash
python src/dashboard.py
```

The dashboard normally opens at `http://127.0.0.1:8050/`. Generated charts, maps, and model outputs are written to the local `outputs/` directory.

## Tools

Python, pandas, NumPy, Matplotlib, Seaborn, Plotly, Dash, scikit-learn, SQL, and Folium.

## Limitations

The dataset is relatively small and historical. Results should be treated as a capstone analysis rather than a production launch-risk system. A production model would benefit from newer launches, time-aware validation, probability calibration, weather data, and richer mission characteristics.

## Author

Thomas Caruso
