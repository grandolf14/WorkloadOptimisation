# Calendar Optimization Tool

This project is a PyQt5-based desktop application designed to manage and optimize project workloads over time. It provides a calendar interface that helps users create, view, and update projects, automatically distributing workloads to optimize time usage.

## Features

- **Graphical Interface**: User-friendly GUI built using PyQt5.
- **Project Management**: Create, edit, and delete projects with start/end dates and workload (in hours).
- **Workload Optimization**: Automatically redistributes workloads to avoid overlapping or excessive workdays.
- **Visualization**:
  - **Today Tab**: Shows what tasks are due today.
  - **Timeline Tab**: Displays workload distribution across sectors.
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
   git clone <your-repo-url>
   cd <your-project-directory>
   ```

3. **Run the Application**:
   ```bash
   python GUI.py
   ```

## Usage

- Navigate through the tabs:
  - **Today**: View current day's workload.
  - **Timeline**: See visual workload spread over time.
  - **Project Manager**: Manage project lifecycle.
- Create a new project by entering:
  - Start Date (`DD.MM.YYYY`)
  - End Date (`DD.MM.YYYY`)
  - Workload in hours
- Edit or delete existing projects as needed.
- Click **Update** to re-optimize all workloads across the timeline.

## Data Structure & Logic

The optimization algorithm splits project durations into **domains**, and organizes them into **sectors** (`bereich`) and **supersectors** (`superbereich`). The system then calculates optimal workload distribution using project-specific constraints and recursively re-balances overlapping segments.

The project data is saved in:
```
data.txt
```
as semi-colon-separated entries with format:
```
start_date,end_date,workload;start_date,end_date,workload;...
```

## Project Structure

- `GUI.py`: Main file containing the PyQt5 GUI logic and data management.
- `Kalender.py`: Contains backend logic for workload optimization and domain management.

## To-Do / Known Issues

- [ ] Add support for saving and loading project domains.
- [ ] Show completed workloads under "Today".
- [ ] Add button to register work time to a project.
- [ ] Improve table and visualization structure.

## Author

Created by [Your Name]. Contributions are welcome!

## License

MIT License (or your preferred license)
