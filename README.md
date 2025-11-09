# Solar Challenge Week 1

A comprehensive data analysis project for solar energy datasets from multiple locations (Benin, Sierra Leone, and Togo).

## Project Structure

```
solar-challenge-week1/
├── data/                    # Raw and cleaned datasets
│   ├── benin-malanville.csv
│   ├── sierraleone-bumbuna.csv
│   ├── togo-dapaong_qc.csv
│   └── *_clean.csv          # Cleaned datasets
├── src/                     # Modular source code
│   ├── data_loader.py       # Data loading utilities
│   ├── data_profiler.py     # Data profiling and quality checks
│   └── eda_utils.py         # EDA visualization functions
├── scripts/                 # Executable scripts
│   ├── profile_data.py      # Data profiling script
│   └── run_eda.py           # EDA execution script
├── notebooks/               # Jupyter notebooks for interactive analysis
│   ├── benin_eda.ipynb
│   ├── sierraleone_eda.ipynb
│   └── togo_eda.ipynb
├── app/                     # Application code (for future use)
├── tests/                   # Unit tests
└── requirements.txt         # Python dependencies
```

## Features

- **Modular Code Architecture**: Well-organized, reusable functions for data loading, profiling, and analysis
- **Comprehensive Data Profiling**: Automated missing value analysis, outlier detection, and quality reports
- **EDA Tools**: Visualization functions for correlation analysis, time series, and distributions
- **Documented Scripts**: Command-line tools for reproducible analysis workflows
- **Interactive Notebooks**: Jupyter notebooks for exploratory analysis

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd solar-challenge-week1
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Data Profiling

Profile a dataset to get comprehensive statistics and quality metrics:

```bash
python scripts/profile_data.py benin-malanville
python scripts/profile_data.py togo-dapaong_qc
python scripts/profile_data.py sierraleone-bumbuna
```

### Exploratory Data Analysis

Run complete EDA pipeline with visualizations:

```bash
python scripts/run_eda.py benin-malanville
python scripts/run_eda.py togo-dapaong_qc --output-dir results
python scripts/run_eda.py sierraleone-bumbuna --output-dir results
```

### Using the Modules

Import and use the modules in your Python code:

```python
from src import load_solar_data, profile_missing_values, plot_correlation_heatmap

# Load data
df = load_solar_data('benin-malanville.csv')

# Profile missing values
missing_report = profile_missing_values(df)

# Generate visualizations
plot_correlation_heatmap(df, columns=['GHI', 'DNI', 'DHI', 'TModA', 'TModB'])
```

### Jupyter Notebooks

For interactive analysis, use the Jupyter notebooks:

```bash
jupyter lab notebooks/benin_eda.ipynb
```

## Data Description

The datasets contain solar energy measurements with the following key variables:

- **GHI**: Global Horizontal Irradiance (W/m²)
- **DNI**: Direct Normal Irradiance (W/m²)
- **DHI**: Diffuse Horizontal Irradiance (W/m²)
- **ModA, ModB**: Module power outputs
- **Tamb**: Ambient temperature (°C)
- **RH**: Relative humidity (%)
- **WS**: Wind speed (m/s)
- **WD**: Wind direction (degrees)
- **Cleaning**: Cleaning status indicator
- **Timestamp**: Time series index

## Development

### Code Organization

- **src/**: Core functionality modules with comprehensive docstrings
- **scripts/**: Executable scripts with command-line interfaces
- **notebooks/**: Interactive analysis notebooks
- **tests/**: Unit tests (to be implemented)

### Adding New Features

1. Add new functions to appropriate modules in `src/`
2. Update `src/__init__.py` to export new functions
3. Create scripts in `scripts/` if needed
4. Update this README with usage examples

## Dependencies

- pandas >= 1.5.0
- numpy >= 1.21.0
- matplotlib >= 3.5.0
- seaborn >= 0.11.0
- scipy >= 1.9.0
- scikit-learn >= 1.2.0
- jupyter >= 1.0.0
- windrose >= 1.8.0

## Version Control

This project uses Git for version control. Regular commits track iterative progress:
- Feature additions
- Bug fixes
- Documentation updates
- Code refactoring

## License

[Add license information here]

## Contributors

[Add contributor information here]
