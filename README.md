# Calendar Optimization Tool

This project is a PyQt5-based desktop application designed to manage and optimize project workloads over time. It provides a timeline interface that helps users create, view and update projects, automatically distributing workloads to optimize time usage.

## Features

- **Graphical Interface**: Easy data management with GUI, built using PyQt5.
- **Project Management**: Create, edit, and delete projects with start/end dates and workload (in hours).
- **Workload Optimization**: Automatically redistributes workloads to avoid overlapping or excessive workdays.
- **Visualization**:
  - **Today Tab**: Shows what timeslots for each project are due today.
  - **Timeline Tab**: Displays workload distribution across timeframes.
  - **Project Manager Tab**: Full list of projects with controls for editing and deletion.
- **Persistent Storage**: Saves data to a `data.txt` file for reloading project states.

## Installation

1. **Install Requirements**:
   Make sure Python 3 and PyQt5 are installed.

   ```bash
   pip install PyQt5
   ```

2. **Download/Clone the Repository**:
   ```bash
   git clone https://github.com/grandolf14/WorkloadOptimisation
   ```

3. **Run the Application**:
   ```bash
   python GUI.py
   ```

## Usage

- Navigate through the tabs:
  - **Today**: View current day's projectspecific workloads.
  - **Timeline**: See visual workload spread over time.
  - **Project Manager**: Manage project data.
- Create a new project by entering:
  - Start Date (`DD.MM.YYYY`)
  - End Date (`DD.MM.YYYY`)
  - Workload in hours
- Edit or delete existing projects as needed.
- Click **Update** to recalculate the workload distribution.

## Data Structure & Logic

The optimization algorithm splits the overall timeframe into **domains** with equal project contribution, organizes them into **sectors** (`bereich`) and **parentsectors** (`superbereich`). The system then calculates optimal workload distribution by recursively re-balancing overlapping segments.

The project data is saved in:
```
data.txt
```

## Project Structure

- `GUI.py`: Main file containing the PyQt5 GUI logic and data management.
- `Kalender.py`: Contains backend logic for workload optimization and domain management.


## Author

Created by Fiete Jantsch.

## License

Apache License
