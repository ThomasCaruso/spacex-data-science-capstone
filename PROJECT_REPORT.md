# SpaceX Falcon 9 Landing Prediction: Project Summary

## Executive summary

This capstone evaluates whether Falcon 9 first stages can be classified as successful or unsuccessful landings from launch and mission characteristics. The analysis combines data collection, cleaning, exploratory visualization, SQL, geospatial analysis, dashboarding, and supervised machine learning.

## Dataset

The cleaned analysis dataset contains 90 Falcon 9 launches:

- 60 successful first-stage landings
- 30 unsuccessful landings
- 66.7% overall landing success rate
- Payload mass ranging from approximately 350 kg to 15,600 kg

## Analytical findings

- Landing performance improved substantially over time as the Falcon 9 program matured.
- Launch site is associated with landing outcomes. In the analyzed sample, KSC LC-39A produced a higher success rate than CCAFS SLC-40.
- Orbit, payload mass, flight number, reuse history, grid fins, landing legs, and booster characteristics provide useful predictive information.
- Mission context matters. A single variable does not fully explain landing success, so the analysis relies on several complementary features and visualizations.

## Machine-learning approach

The project compares four classification methods:

1. Logistic Regression
2. Support Vector Machine
3. Decision Tree
4. K-Nearest Neighbors

Each model is tuned with cross-validation and evaluated on a held-out test sample. The report's strongest cross-validation result came from the Decision Tree model at approximately 86.3%. The final test accuracy was approximately 77.8%, corresponding to 14 correct predictions out of 18 test records.

## Interpretation

The results show that Falcon 9 landing outcomes are predictable to a useful degree, but the dataset is small and historical. The model should be treated as an analytical demonstration rather than a production forecasting system. A stronger production version would use more recent launch records, time-aware validation, probability calibration, and additional weather and mission variables.

## Business relevance

Successful recovery is central to launch-vehicle reuse and cost reduction. A landing prediction model can help analysts compare mission risk, identify the variables most associated with recovery, and understand how operational performance changes over time.
