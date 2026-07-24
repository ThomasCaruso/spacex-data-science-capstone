"""Create an interactive Folium map of Falcon 9 launch sites and outcomes."""

from __future__ import annotations

import folium
from folium.plugins import MarkerCluster

from common import ensure_output_dir, load_csv


def outcome_color(value: int) -> str:
    return "green" if int(value) == 1 else "red"


def build_map() -> folium.Map:
    data = load_csv("dataset_part_2.csv")
    required = {"LaunchSite", "Latitude", "Longitude", "Class", "FlightNumber"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"dataset_part_2.csv is missing columns: {sorted(missing)}")

    launch_map = folium.Map(
        location=[data["Latitude"].mean(), data["Longitude"].mean()],
        zoom_start=4,
        tiles="CartoDB positron",
    )

    sites = (
        data.groupby("LaunchSite", as_index=False)
        .agg(
            Latitude=("Latitude", "first"),
            Longitude=("Longitude", "first"),
            Launches=("Class", "size"),
            SuccessRate=("Class", "mean"),
        )
    )

    for _, row in sites.iterrows():
        folium.Marker(
            [row["Latitude"], row["Longitude"]],
            popup=(
                f"<b>{row['LaunchSite']}</b><br>"
                f"Launches: {int(row['Launches'])}<br>"
                f"Success rate: {row['SuccessRate']:.1%}"
            ),
            tooltip=row["LaunchSite"],
            icon=folium.Icon(color="blue", icon="rocket", prefix="fa"),
        ).add_to(launch_map)

    cluster = MarkerCluster(name="Launch records").add_to(launch_map)
    for _, row in data.iterrows():
        success = int(row["Class"])
        folium.CircleMarker(
            [row["Latitude"], row["Longitude"]],
            radius=5,
            color=outcome_color(success),
            fill=True,
            fill_opacity=0.75,
            popup=(
                f"Flight {int(row['FlightNumber'])}<br>"
                f"Site: {row['LaunchSite']}<br>"
                f"Outcome: {'Success' if success else 'Failure'}"
            ),
        ).add_to(cluster)

    folium.LayerControl().add_to(launch_map)
    return launch_map


def main() -> None:
    output_path = ensure_output_dir() / "falcon9_launch_map.html"
    build_map().save(output_path)
    print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
