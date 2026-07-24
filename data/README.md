# Data files

This repository includes the datasets required by the runnable analysis:

- `dataset_part_2.csv`: cleaned Falcon 9 launch records, geographic coordinates, mission variables, and the binary landing target
- `spacex_launch_dash.csv`: dashboard-ready launch data

The modeling script creates its encoded feature matrix directly from `dataset_part_2.csv`, so a separate `dataset_part_3.csv` file is not required.

The datasets are derived from the IBM Data Science Capstone labs and SpaceX launch records.
