"""Exploratory analysis for Falcon 9 first-stage landing outcomes."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common import ensure_output_dir, load_csv


sns.set_theme(style="whitegrid")


def save_current_figure(filename: str) -> None:
    output_path = ensure_output_dir() / filename
    plt.tight_layout()
    plt.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close()
    print(f"Saved {output_path}")


def prepare_launch_data() -> pd.DataFrame:
    data = load_csv("dataset_part_2.csv")
    required = {
        "FlightNumber",
        "Date",
        "PayloadMass",
        "Orbit",
        "LaunchSite",
        "Class",
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"dataset_part_2.csv is missing columns: {sorted(missing)}")

    data = data.copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data["Year"] = data["Date"].dt.year
    data["Landing Outcome"] = data["Class"].map({1: "Success", 0: "Failure"})
    return data


def print_summary(data: pd.DataFrame) -> None:
    total = len(data)
    successes = int(data["Class"].sum())
    rate = data["Class"].mean()
    site_rates = data.groupby("LaunchSite")["Class"].mean().sort_values(ascending=False)

    print("Falcon 9 landing analysis")
    print(f"Launches: {total}")
    print(f"Successful landings: {successes}")
    print(f"Overall success rate: {rate:.1%}")
    print("\nSuccess rate by site:")
    print(site_rates.to_string(float_format=lambda value: f"{value:.1%}"))


def plot_site_success(data: pd.DataFrame) -> None:
    summary = (
        data.groupby("LaunchSite", as_index=False)
        .agg(success_rate=("Class", "mean"), launches=("Class", "size"))
    )
    summary["success_rate"] *= 100

    plt.figure(figsize=(9, 5.5))
    axis = sns.barplot(data=summary, x="LaunchSite", y="success_rate")
    for index, row in summary.iterrows():
        axis.text(
            index,
            row["success_rate"] + 2,
            f"{row['success_rate']:.0f}%\nn={int(row['launches'])}",
            ha="center",
            fontsize=9,
        )
    plt.ylim(0, 105)
    plt.title("Falcon 9 Landing Success Rate by Launch Site")
    plt.xlabel("Launch site")
    plt.ylabel("Success rate (%)")
    save_current_figure("site_success_rate.png")


def plot_flight_number(data: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 5.5))
    sns.scatterplot(
        data=data,
        x="FlightNumber",
        y="LaunchSite",
        hue="Landing Outcome",
        style="Landing Outcome",
        s=85,
    )
    plt.title("Landing Outcomes by Flight Number and Launch Site")
    plt.xlabel("Flight number")
    plt.ylabel("Launch site")
    save_current_figure("flight_number_by_site.png")


def plot_payload(data: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 5.5))
    sns.scatterplot(
        data=data,
        x="PayloadMass",
        y="LaunchSite",
        hue="Landing Outcome",
        style="Landing Outcome",
        s=85,
    )
    plt.title("Payload Mass and Landing Outcome by Launch Site")
    plt.xlabel("Payload mass (kg)")
    plt.ylabel("Launch site")
    save_current_figure("payload_by_site.png")


def plot_orbit_success(data: pd.DataFrame) -> None:
    orbit = (
        data.groupby("Orbit", as_index=False)
        .agg(success_rate=("Class", "mean"), launches=("Class", "size"))
        .sort_values("success_rate", ascending=False)
    )
    orbit["success_rate"] *= 100

    plt.figure(figsize=(11, 5.5))
    sns.barplot(data=orbit, x="Orbit", y="success_rate")
    plt.ylim(0, 105)
    plt.title("Landing Success Rate by Orbit")
    plt.xlabel("Orbit")
    plt.ylabel("Success rate (%)")
    plt.xticks(rotation=35, ha="right")
    save_current_figure("orbit_success_rate.png")


def plot_yearly_trend(data: pd.DataFrame) -> None:
    trend = (
        data.dropna(subset=["Year"])
        .groupby("Year", as_index=False)
        .agg(success_rate=("Class", "mean"), launches=("Class", "size"))
    )
    trend["success_rate"] *= 100

    plt.figure(figsize=(9, 5.5))
    sns.lineplot(data=trend, x="Year", y="success_rate", marker="o")
    plt.ylim(0, 105)
    plt.title("Falcon 9 Landing Success Improved Over Time")
    plt.xlabel("Year")
    plt.ylabel("Success rate (%)")
    save_current_figure("yearly_success_trend.png")


def main() -> None:
    data = prepare_launch_data()
    print_summary(data)
    plot_site_success(data)
    plot_flight_number(data)
    plot_payload(data)
    plot_orbit_success(data)
    plot_yearly_trend(data)


if __name__ == "__main__":
    main()
