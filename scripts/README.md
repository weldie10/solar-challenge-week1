# Scripts Directory

This directory contains executable scripts for data analysis workflows.

## Available Scripts

### `profile_data.py`

Comprehensive data profiling script that generates reports on:
- Data quality metrics
- Missing value analysis
- Summary statistics
- Outlier detection
- Data type information

**Usage:**
```bash
python scripts/profile_data.py <dataset_name>
```

**Examples:**
```bash
python scripts/profile_data.py benin-malanville
python scripts/profile_data.py togo-dapaong_qc
python scripts/profile_data.py sierraleone-bumbuna
```

### `run_eda.py`

Complete EDA pipeline script that:
- Loads and cleans data
- Generates correlation heatmaps
- Creates time series visualizations
- Plots distributions
- Saves cleaned datasets

**Usage:**
```bash
python scripts/run_eda.py <dataset_name> [--output-dir OUTPUT_DIR] [--skip-cleaning]
```

**Examples:**
```bash
python scripts/run_eda.py benin-malanville
python scripts/run_eda.py togo-dapaong_qc --output-dir results
python scripts/run_eda.py sierraleone-bumbuna --output-dir results --skip-cleaning
```

## Making Scripts Executable

On Unix-like systems, you can make scripts executable:

```bash
chmod +x scripts/profile_data.py
chmod +x scripts/run_eda.py
```

Then run directly:
```bash
./scripts/profile_data.py benin-malanville
```

