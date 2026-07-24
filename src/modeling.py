"""Train and compare classifiers for Falcon 9 landing success."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.base import BaseEstimator
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from common import ensure_output_dir, load_csv


RANDOM_STATE = 2


@dataclass
class ModelSpec:
    name: str
    estimator: BaseEstimator
    parameters: dict[str, list[Any]]


def load_model_data() -> tuple[pd.DataFrame, pd.Series]:
    features = load_csv("dataset_part_3.csv")
    launch_data = load_csv("dataset_part_2.csv")

    if "Class" not in launch_data.columns:
        raise ValueError("dataset_part_2.csv must contain the Class target column")

    target = launch_data["Class"].astype(int).reset_index(drop=True)
    features = features.reset_index(drop=True)

    if len(features) != len(target):
        raise ValueError(
            "Feature and target row counts do not match: "
            f"{len(features)} features versus {len(target)} targets"
        )

    non_numeric = features.select_dtypes(exclude="number").columns.tolist()
    if non_numeric:
        raise ValueError(f"dataset_part_3.csv contains nonnumeric columns: {non_numeric}")

    return features, target


def model_specs() -> list[ModelSpec]:
    return [
        ModelSpec(
            name="Logistic Regression",
            estimator=Pipeline(
                [
                    ("scale", StandardScaler()),
                    (
                        "model",
                        LogisticRegression(
                            max_iter=5000,
                            random_state=RANDOM_STATE,
                        ),
                    ),
                ]
            ),
            parameters={
                "model__C": [0.01, 0.1, 1.0, 10.0],
                "model__solver": ["liblinear", "lbfgs"],
            },
        ),
        ModelSpec(
            name="Support Vector Machine",
            estimator=Pipeline(
                [
                    ("scale", StandardScaler()),
                    ("model", SVC()),
                ]
            ),
            parameters={
                "model__C": [0.1, 1.0, 10.0],
                "model__kernel": ["linear", "rbf", "sigmoid"],
                "model__gamma": ["scale", "auto"],
            },
        ),
        ModelSpec(
            name="Decision Tree",
            estimator=DecisionTreeClassifier(random_state=RANDOM_STATE),
            parameters={
                "criterion": ["gini", "entropy"],
                "max_depth": [2, 4, 6, 8, None],
                "min_samples_split": [2, 5, 10],
            },
        ),
        ModelSpec(
            name="K-Nearest Neighbors",
            estimator=Pipeline(
                [
                    ("scale", StandardScaler()),
                    ("model", KNeighborsClassifier()),
                ]
            ),
            parameters={
                "model__n_neighbors": list(range(3, 12)),
                "model__weights": ["uniform", "distance"],
                "model__p": [1, 2],
            },
        ),
    ]


def evaluate_models(
    x_train: pd.DataFrame,
    x_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> tuple[pd.DataFrame, str, BaseEstimator, pd.Series]:
    rows: list[dict[str, Any]] = []
    best_name = ""
    best_estimator: BaseEstimator | None = None
    best_predictions: pd.Series | None = None
    best_test_accuracy = -1.0

    for spec in model_specs():
        search = GridSearchCV(
            estimator=spec.estimator,
            param_grid=spec.parameters,
            scoring="accuracy",
            cv=5,
            n_jobs=-1,
        )
        search.fit(x_train, y_train)
        predictions = search.predict(x_test)
        test_accuracy = accuracy_score(y_test, predictions)

        rows.append(
            {
                "model": spec.name,
                "validation_accuracy": search.best_score_,
                "test_accuracy": test_accuracy,
                "best_parameters": json.dumps(search.best_params_, sort_keys=True),
            }
        )

        if test_accuracy > best_test_accuracy:
            best_test_accuracy = test_accuracy
            best_name = spec.name
            best_estimator = search.best_estimator_
            best_predictions = pd.Series(predictions, index=y_test.index)

    if best_estimator is None or best_predictions is None:
        raise RuntimeError("No model was successfully evaluated")

    results = pd.DataFrame(rows).sort_values("test_accuracy", ascending=False)
    return results, best_name, best_estimator, best_predictions


def save_accuracy_chart(results: pd.DataFrame) -> None:
    plot_data = results.melt(
        id_vars="model",
        value_vars=["validation_accuracy", "test_accuracy"],
        var_name="metric",
        value_name="accuracy",
    )
    plot_data["accuracy"] *= 100

    plt.figure(figsize=(10, 5.5))
    sns.barplot(data=plot_data, x="model", y="accuracy", hue="metric")
    plt.ylim(0, 105)
    plt.title("Classification Model Accuracy")
    plt.xlabel("Model")
    plt.ylabel("Accuracy (%)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(ensure_output_dir() / "model_accuracy.png", dpi=180, bbox_inches="tight")
    plt.close()


def save_confusion_matrix(y_test: pd.Series, predictions: pd.Series, model_name: str) -> None:
    matrix = confusion_matrix(y_test, predictions, labels=[0, 1])
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Failure", "Success"],
        yticklabels=["Failure", "Success"],
    )
    plt.title(f"Confusion Matrix: {model_name}")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(ensure_output_dir() / "confusion_matrix.png", dpi=180, bbox_inches="tight")
    plt.close()


def main() -> None:
    features, target = load_model_data()
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=target,
    )

    results, best_name, _, predictions = evaluate_models(
        x_train,
        x_test,
        y_train,
        y_test,
    )

    output_dir = ensure_output_dir()
    results.to_csv(output_dir / "model_results.csv", index=False)
    save_accuracy_chart(results)
    save_confusion_matrix(y_test, predictions, best_name)

    print(results.to_string(index=False))
    print(f"\nBest test model: {best_name}")
    print("\nClassification report:")
    print(classification_report(y_test, predictions, target_names=["Failure", "Success"]))


if __name__ == "__main__":
    main()
