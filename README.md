
# ADCP Excel Parser

This repository contains a Python script to extract and transform ADCP (Acoustic Doppler Current Profiler) data from Excel files into structured CSV files.

## Features

- Reads multiple Excel files from a directory
- Parses datetime, geographic location, and station metadata
- Extracts velocity and direction measurements from multiple depth levels (average, surface, and bottom)
- Saves output as separate CSV files based on depth level

## File Naming

- `output_air.csv` – contains measurements from average depth
- `output_surface.csv` – contains measurements from surface (2m depth)
- `output_bottom.csv` – contains measurements from bottom (4–8m depth)

## Requirements

- Python 3.x
- pandas
- openpyxl (for reading Excel files)

## Usage

1. Place your Excel files in a folder.
2. Update the `folder_path` variable to match your file location.
3. Run the script using Python.
4. Output CSV files will be generated for each depth level.

---

This script was originally developed to process ADCP data collected in Cirebon, Indonesia.
