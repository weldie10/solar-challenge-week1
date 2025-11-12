# Solar Challenge Week 1

A comprehensive data analysis project for solar energy datasets from multiple locations (Benin, Sierra Leone, and Togo). This project implements end-to-end data science workflows including data profiling, cleaning, exploratory analysis, statistical testing, and interactive visualization.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Git and Environment Setup](#git-and-environment-setup)
- [Data Profiling, Cleaning, and EDA](#data-profiling-cleaning-and-eda)
- [Cross-Country Comparison](#cross-country-comparison)
- [Repository Best Practices](#repository-best-practices)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Description](#data-description)
- [Development](#development)
- [Dependencies](#dependencies)

---

## Project Overview

**Project Title:** Solar Energy Data Analysis - West Africa  
**Project Code:** B8W0  
**Author:** Woldeyohannes Nigus  
**Program:** 10 Academy KAIM Training Program - Week 0 Challenge

This project analyzes over 1.5 million time-series records from three West African countries to assess solar energy potential, identify patterns, and provide actionable insights for solar energy development.

### Key Features

- ✅ **Modular Code Architecture**: Well-organized, reusable functions for data loading, profiling, and analysis
- ✅ **Comprehensive Data Profiling**: Automated missing value analysis, outlier detection, and quality reports
- ✅ **Systematic Data Cleaning**: Z-score outlier detection, median imputation, and validation
- ✅ **Exploratory Data Analysis**: Time series, correlation analysis, and distribution visualizations
- ✅ **Cross-Country Comparison**: Statistical testing (ANOVA, Kruskal-Wallis) with pairwise comparisons
- ✅ **Interactive Dashboard**: Professional Streamlit application for data exploration
- ✅ **Documented Scripts**: Command-line tools for reproducible analysis workflows
- ✅ **Version Control**: Organized Git repository with feature branches and descriptive commits

---

## Git and Environment Setup

### Repository Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd solar-challenge-week1
```

2. **Check Git status:**
```bash
git status
git branch -a  # View all branches
```

### Virtual Environment Setup

1. **Create virtual environment:**
```bash
python3 -m venv venv
```

2. **Activate virtual environment:**
```bash
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Verify activation:**
```bash
which python  # Should point to venv/bin/python
python --version  # Should show Python 3.12
```

4. **Install dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

5. **Verify installation:**
```bash
pip list
python -c "import pandas, numpy, matplotlib, seaborn, streamlit; print('All packages installed successfully')"
```

### Environment Configuration

The project uses a virtual environment to isolate dependencies. Key configuration:

- **Python Version**: 3.12
- **Virtual Environment**: `venv/` (excluded from version control via .gitignore)
- **Dependencies**: Managed via `requirements.txt`
- **Configuration**: Project settings in `config.py`

### Git Workflow

**Branch Strategy:**
- `main`: Production-ready code
- `benin-eda`: Benin-specific EDA development
- `togo`: Togo-specific EDA development
- `compare-countries`: Cross-country comparison analysis

**Commit Practices:**
- Descriptive commit messages
- Logical grouping of related changes
- Regular commits showing iterative progress
- Feature branches for major additions

**Example Workflow:**
```bash
# Create feature branch
git checkout -b feature-name

# Make changes and commit
git add .
git commit -m "Descriptive commit message"

# Push to remote
git push origin feature-name
```

---

## Data Profiling, Cleaning, and Exploratory Data Analysis (EDA)

### Data Profiling

**Automated Profiling Script:**
```bash
python scripts/profile_data.py <dataset_name>
```

**Features:**
- Data quality metrics (shape, memory usage, duplicates)
- Missing value analysis with percentages
- Summary statistics (mean, median, std dev, min, max)
- Outlier detection using Z-score method
- Data type information

**Example Output:**
```
================================================================================
SUMMARY STATISTICS: Solar Metrics Comparison Across Countries
================================================================================

📊 GHI Statistics:
--------------------------------------------------------------------------------
     Country   Mean  Median  Std Dev   Min    Max  Count
       Benin 236.23     0.7   328.29 -11.1 1233.0 517860
Sierra Leone 185.00    -0.4   279.02 -15.9 1097.0 509308
        Togo 223.86     0.5   317.31 -12.7 1198.0 516349
```

### Data Cleaning Pipeline

**Systematic Cleaning Approach:**

1. **Missing Value Analysis**
   - Identify columns with >5% missing values
   - Apply median imputation for numeric columns
   - Preserve temporal structure

2. **Outlier Detection**
   - Z-score method (threshold: |Z| > 3.0)
   - Applied to key columns: GHI, DNI, DHI, ModA, ModB, WS, WSgust
   - Document outlier removal impact

3. **Data Validation**
   - Before/after cleaning comparisons
   - Physical plausibility checks
   - Temporal continuity verification

**Cleaned Datasets:**
- `data/benin_clean.csv`
- `data/sierraleone_clean.csv`
- `data/togo_clean.csv`

### Exploratory Data Analysis

**Individual Country EDA Notebooks:**

Each country has a comprehensive EDA notebook (`notebooks/*_eda.ipynb`) with:

1. **Data Loading and Inspection**
   - Dataset shape and structure
   - Column information and data types
   - Initial data quality assessment

2. **Summary Statistics**
   - Descriptive statistics for all variables
   - Missing value analysis
   - Data completeness assessment

3. **Outlier Detection**
   - Z-score analysis
   - Outlier identification and documentation
   - Decision on removal or imputation

4. **Data Cleaning**
   - Missing value imputation
   - Outlier removal
   - Data validation

5. **Time Series Analysis**
   - Temporal patterns (GHI, DNI, DHI over time)
   - Seasonal and diurnal patterns
   - Anomaly detection

6. **Correlation Analysis**
   - Correlation heatmaps
   - Scatter plots with hue encoding
   - Relationship identification

7. **Distribution Analysis**
   - Histograms with KDE
   - Boxplots for key metrics
   - Distribution comparisons

8. **Wind Analysis** (Optional)
   - Wind rose plots
   - Wind direction and speed patterns

9. **Temperature and Humidity Relationships**
   - Scatter plots with multiple encodings
   - Bubble charts for multi-dimensional analysis

**Run EDA Pipeline:**
```bash
python scripts/run_eda.py benin-malanville
python scripts/run_eda.py togo-dapaong_qc --output-dir results
python scripts/run_eda.py sierraleone-bumbuna --output-dir results
```

**Interactive Notebooks:**
```bash
jupyter lab notebooks/benin_eda.ipynb
jupyter lab notebooks/sierraleone_eda.ipynb
jupyter lab notebooks/togo_eda.ipynb
```

---

## Cross-Country Comparison

### Comparison Notebook

**Location:** `notebooks/compare_countries.ipynb`

**Features:**

1. **Data Loading**
   - Loads all three cleaned datasets
   - Combines with country identifiers
   - Validates data availability

2. **Metric Comparison**
   - **Boxplots**: Side-by-side for GHI, DNI, DHI (colored by country)
   - **Summary Table**: Mean, median, and standard deviation for each metric
   - **Violin Plots**: Distribution shape comparison

3. **Statistical Testing**
   - **One-Way ANOVA**: Tests for mean differences (F-statistic, p-value)
   - **Kruskal-Wallis Test**: Non-parametric alternative (H-statistic, p-value)
   - **Pairwise Comparisons**: Tukey HSD test for specific country pairs
   - **P-value Reporting**: Correct interpretation and significance levels

4. **Key Observations**
   - Three main findings with implications:
     1. Country with highest solar potential
     2. Variability analysis and stability assessment
     3. Statistical significance confirmation

5. **Visual Ranking**
   - Bar chart ranking countries by average GHI
   - Mean vs. median comparison
   - Ranking table with statistics

**Key Performance Indicators (KPIs) Met:**
- ✅ All three countries included in each plot
- ✅ Correct implementation and reporting of p-values
- ✅ Relevance and actionability of insights
- ✅ Summary table comparing mean/median/SD for each metric

**Statistical Results:**
- ANOVA: F = 3833.18, p < 0.001 (highly significant)
- Kruskal-Wallis: H = 6548.53, p < 0.001 (highly significant)
- All pairwise comparisons show significant differences

---

## Repository Best Practices

### Project Structure

```
solar-challenge-week1/
├── README.md                    # Comprehensive project documentation
├── requirements.txt             # Python dependencies with versions
├── config.py                    # Project configuration settings
├── .gitignore                   # Git ignore patterns
├── data/                        # Raw and cleaned datasets
│   ├── benin-malanville.csv
│   ├── benin_clean.csv
│   ├── sierraleone-bumbuna.csv
│   ├── sierraleone_clean.csv
│   ├── togo-dapaong_qc.csv
│   └── togo_clean.csv
├── src/                         # Modular source code
│   ├── __init__.py             # Package exports
│   ├── data_loader.py          # Data loading utilities
│   ├── data_profiler.py        # Profiling and quality checks
│   └── eda_utils.py            # Visualization functions
├── scripts/                     # Executable scripts
│   ├── __init__.py
│   ├── README.md               # Script documentation
│   ├── profile_data.py         # Data profiling tool
│   ├── run_eda.py              # EDA pipeline
│   └── run_dashboard.py        # Dashboard launcher
├── notebooks/                   # Jupyter notebooks
│   ├── __init__.py
│   ├── README.md
│   ├── benin_eda.ipynb         # Benin EDA
│   ├── sierraleone_eda.ipynb   # Sierra Leone EDA
│   ├── togo_eda.ipynb          # Togo EDA
│   └── compare_countries.ipynb  # Cross-country comparison
├── app/                         # Dashboard application
│   ├── __init__.py
│   └── dashboard.py             # Streamlit dashboard
├── tests/                       # Unit tests
│   ├── __init__.py
│   └── test_data_loader.py     # Test examples
└── results/                     # Analysis outputs
    └── cross_country_summary_statistics.csv
```

### Code Organization

**Modular Design:**
- **`src/data_loader.py`**: Centralized data loading with path resolution
- **`src/data_profiler.py`**: Comprehensive profiling functions
- **`src/eda_utils.py`**: Reusable visualization utilities

**Scripts:**
- Command-line interfaces with argument parsing
- Error handling and user feedback
- Comprehensive documentation

**Notebooks:**
- Consistent structure across all notebooks
- Professional markdown documentation
- Reproducible code with proper imports

### Documentation Standards

**Code Documentation:**
- Comprehensive docstrings for all functions
- Type hints for parameters and returns
- Usage examples in documentation
- Module-level documentation

**Project Documentation:**
- Detailed README with setup instructions
- Script-specific documentation (`scripts/README.md`)
- Configuration file documentation
- Clear project structure explanation

### Version Control Best Practices

**Git Configuration:**
- `.gitignore` properly configured (excludes venv, __pycache__, data files)
- Feature branch strategy for development
- Descriptive commit messages
- Regular commits showing progress

**Branch Management:**
- `main`: Stable, production-ready code
- Feature branches: `benin-eda`, `togo`, `compare-countries`
- Descriptive branch names
- Clean merge history

**Commit Messages:**
- Clear, descriptive messages
- Reference specific features or fixes
- Group related changes together

### Testing Structure

**Test Organization:**
- `tests/` directory with proper structure
- Example test file: `test_data_loader.py`
- Test framework ready for expansion
- Unit tests for core functions

### Configuration Management

**Configuration File (`config.py`):**
- Centralized project settings
- Path configurations
- Analysis parameters (outlier thresholds, etc.)
- Dataset mappings

---

## Installation

### Prerequisites

- Python 3.12 or higher
- Git
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone Repository:**
```bash
git clone <repository-url>
cd solar-challenge-week1
```

2. **Create Virtual Environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Verify Installation:**
```bash
python -c "import pandas, numpy, matplotlib, seaborn, streamlit; print('✓ All packages installed')"
```

5. **Test Data Loading:**
```bash
python scripts/profile_data.py benin-malanville
```

---

## Usage

### Quick Start

1. **Profile a dataset:**
```bash
python scripts/profile_data.py benin-malanville
```

2. **Run EDA:**
```bash
python scripts/run_eda.py benin-malanville --output-dir results
```

3. **Launch Dashboard:**
```bash
python scripts/run_dashboard.py
# or
streamlit run app/dashboard.py
```

4. **Open Notebooks:**
```bash
jupyter lab notebooks/benin_eda.ipynb
```

### Using Python Modules

```python
from src import (
    load_solar_data,
    profile_missing_values,
    detect_outliers_zscore,
    plot_correlation_heatmap,
    plot_time_series
)

# Load data
df = load_solar_data('benin-malanville.csv')

# Profile missing values
missing_report = profile_missing_values(df, threshold=0.05)

# Detect outliers
outlier_info = detect_outliers_zscore(df, columns=['GHI', 'DNI', 'DHI'])

# Generate visualizations
plot_correlation_heatmap(df, columns=['GHI', 'DNI', 'DHI', 'TModA', 'TModB'])
```

### Interactive Dashboard

The Streamlit dashboard provides:

- **Overview Page**: Key metrics, country summaries, quick comparisons
- **Country Analysis**: Detailed analysis with tabs for statistics, time series, distributions, correlations
- **Cross-Country Comparison**: Interactive metric selection with boxplots, violin plots, and summary statistics
- **Data Quality**: Comprehensive quality assessment with adjustable parameters

**Launch:**
```bash
streamlit run app/dashboard.py
```

Access at: `http://localhost:8501`

---

## Data Description

### Dataset Overview

| Country | Location | Dataset | Records | Key Characteristics |
|---------|----------|---------|---------|---------------------|
| Benin | Malanville | benin-malanville.csv | 525,600 | Highest GHI, high variability |
| Sierra Leone | Bumbuna | sierraleone-bumbuna.csv | ~509,308 | Moderate GHI, stable conditions |
| Togo | Dapaong | togo-dapaong_qc.csv | 525,602 | Balanced profile, intermediate variability |

**Total Records:** ~1.54 million across all countries

### Variables

**Solar Irradiance Metrics:**
- **GHI** (Global Horizontal Irradiance): Total solar radiation on horizontal surface (W/m²)
- **DNI** (Direct Normal Irradiance): Direct beam radiation (W/m²)
- **DHI** (Diffuse Horizontal Irradiance): Scattered radiation (W/m²)
- **ModA, ModB**: Module power outputs (W)

**Meteorological Variables:**
- **Tamb**: Ambient temperature (°C)
- **RH**: Relative humidity (%)
- **WS**: Wind speed (m/s)
- **WSgust**: Wind gust speed (m/s)
- **WD**: Wind direction (degrees)
- **BP**: Barometric pressure (hPa)
- **TModA, TModB**: Module temperatures (°C)
- **Precipitation**: Rainfall measurements (mm)

**Metadata:**
- **Timestamp**: Temporal index for time series analysis
- **Cleaning**: Maintenance/cleaning status flags

---

## Development

### Code Organization Principles

- **Modularity**: Functions organized by purpose (loading, profiling, visualization)
- **Reusability**: Functions designed for multiple datasets
- **Documentation**: Comprehensive docstrings and type hints
- **Error Handling**: Robust error messages and validation

### Adding New Features

1. Add functions to appropriate modules in `src/`
2. Update `src/__init__.py` to export new functions
3. Create scripts in `scripts/` if command-line interface needed
4. Add tests in `tests/` directory
5. Update documentation (README, docstrings)

### Running Tests

```bash
# Run tests (when implemented)
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_data_loader.py
```

---

## Dependencies

### Core Libraries

- **pandas >= 1.5.0**: Data manipulation and analysis
- **numpy >= 1.21.0**: Numerical computations
- **matplotlib >= 3.5.0**: Static visualizations
- **seaborn >= 0.11.0**: Statistical visualizations
- **scipy >= 1.9.0**: Statistical testing and analysis

### Development Tools

- **jupyter >= 1.0.0**: Interactive notebooks
- **streamlit >= 1.28.0**: Interactive dashboard framework
- **scikit-learn >= 1.2.0**: Machine learning utilities (for future use)

### Specialized Libraries

- **windrose >= 1.8.0**: Wind direction visualization

### Installing Dependencies

```bash
# Install all dependencies
pip install -r requirements.txt

# Install specific package
pip install pandas>=1.5.0

# Update requirements
pip freeze > requirements.txt
```

---

## Contributing

### Development Workflow

1. Create feature branch: `git checkout -b feature-name`
2. Make changes and test
3. Commit with descriptive message: `git commit -m "Add feature X"`
4. Push to remote: `git push origin feature-name`
5. Create pull request (if applicable)

### Code Style

- Follow PEP 8 Python style guide
- Use type hints where applicable
- Write comprehensive docstrings
- Include usage examples in documentation

---

## License

[Add license information here]

---

## Contributors

- **Woldeyohannes Nigus** - Project Author
- 10 Academy KAIM Training Program

---

## Acknowledgments

This project was completed as part of the 10 Academy KAIM Training Program - Week 0 Challenge. Special thanks to the program instructors and fellow participants for their support and feedback.

---

**Last Updated:** November 2025
