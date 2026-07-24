# Data files

The project expects the following course datasets:

- `dataset_part_2.csv`: cleaned Falcon 9 launch records and the binary landing target
- `dataset_part_3.csv`: encoded feature matrix used for classification
- `spacex_launch_dash.csv`: dashboard-ready launch data
- `spacex_launch_geo.csv`: launch records with site latitude and longitude

Place the files either in this `data/` directory or in the repository root. The Python scripts check both locations.

The datasets are derived from the IBM Data Science Capstone labs and SpaceX launch records. They are intentionally not duplicated inside the source code.
