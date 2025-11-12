"""
Solar Energy Data Dashboard

A comprehensive Streamlit dashboard for visualizing and analyzing solar energy data
from Benin, Sierra Leone, and Togo.

Usage:
    streamlit run app/dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys
from datetime import datetime

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from data_loader import load_solar_data, get_dataset_info
from data_profiler import (
    profile_missing_values,
    generate_summary_statistics,
    detect_outliers_zscore,
    get_data_quality_report
)
from eda_utils import (
    plot_correlation_heatmap,
    plot_time_series,
    plot_distributions
)

# Page configuration
st.set_page_config(
    page_title="Solar Energy Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'datasets' not in st.session_state:
    st.session_state.datasets = {}

@st.cache_data
def load_all_datasets():
    """Load all cleaned datasets"""
    data_dir = project_root / "data"
    datasets = {}
    
    country_files = {
        'Benin': 'benin_clean.csv',
        'Sierra Leone': 'sierraleone_clean.csv',
        'Togo': 'togo_clean.csv'
    }
    
    for country, filename in country_files.items():
        filepath = data_dir / filename
        if filepath.exists():
            try:
                df = pd.read_csv(filepath)
                df['Country'] = country
                if 'Timestamp' in df.columns:
                    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
                datasets[country] = df
            except Exception as e:
                st.error(f"Error loading {country}: {e}")
    
    return datasets

def main():
    """Main dashboard application"""
    
    # Header
    st.markdown('<h1 class="main-header">☀️ Solar Energy Data Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Overview", "Country Analysis", "Cross-Country Comparison", "Data Quality", "About"]
    )
    
    # Load data
    with st.spinner("Loading datasets..."):
        datasets = load_all_datasets()
        st.session_state.datasets = datasets
        st.session_state.data_loaded = True
    
    if not datasets:
        st.error("⚠️ No datasets found. Please ensure cleaned CSV files exist in the data/ directory.")
        return
    
    # Route to appropriate page
    if page == "Overview":
        show_overview(datasets)
    elif page == "Country Analysis":
        show_country_analysis(datasets)
    elif page == "Cross-Country Comparison":
        show_cross_country_comparison(datasets)
    elif page == "Data Quality":
        show_data_quality(datasets)
    elif page == "About":
        show_about()

def show_overview(datasets):
    """Overview page with key metrics"""
    st.header("📊 Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_records = sum(len(df) for df in datasets.values())
    total_countries = len(datasets)
    
    with col1:
        st.metric("Total Countries", total_countries)
    with col2:
        st.metric("Total Records", f"{total_records:,}")
    with col3:
        avg_ghi = np.mean([df['GHI'].mean() for df in datasets.values() if 'GHI' in df.columns])
        st.metric("Average GHI", f"{avg_ghi:.1f} W/m²")
    with col4:
        total_size = sum(df.memory_usage(deep=True).sum() / 1024**2 for df in datasets.values())
        st.metric("Total Data Size", f"{total_size:.1f} MB")
    
    st.markdown("---")
    
    # Country summary table
    st.subheader("Country Summary")
    summary_data = []
    
    for country, df in datasets.items():
        if 'GHI' in df.columns:
            summary_data.append({
                'Country': country,
                'Records': len(df),
                'Mean GHI (W/m²)': df['GHI'].mean(),
                'Median GHI (W/m²)': df['GHI'].median(),
                'Std Dev GHI': df['GHI'].std(),
                'Date Range': f"{df['Timestamp'].min().date() if 'Timestamp' in df.columns else 'N/A'} to {df['Timestamp'].max().date() if 'Timestamp' in df.columns else 'N/A'}"
            })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    # Quick visualization
    st.subheader("Quick Comparison: Average GHI by Country")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    countries = list(datasets.keys())
    avg_ghi_values = [df['GHI'].mean() for df in datasets.values() if 'GHI' in df.columns]
    
    colors = {'Benin': '#2E86AB', 'Sierra Leone': '#A23B72', 'Togo': '#F18F01'}
    bar_colors = [colors.get(country, '#808080') for country in countries]
    
    bars = ax.bar(countries, avg_ghi_values, color=bar_colors, alpha=0.8, edgecolor='black')
    ax.set_ylabel('Average GHI (W/m²)', fontsize=12)
    ax.set_xlabel('Country', fontsize=12)
    ax.set_title('Average Global Horizontal Irradiance by Country', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, value in zip(bars, avg_ghi_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

def show_country_analysis(datasets):
    """Country-specific analysis page"""
    st.header("🌍 Country Analysis")
    
    # Country selector
    selected_country = st.selectbox(
        "Select Country",
        options=list(datasets.keys()),
        index=0
    )
    
    df = datasets[selected_country]
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["Summary Statistics", "Time Series", "Distributions", "Correlations"])
    
    with tab1:
        st.subheader(f"Summary Statistics - {selected_country}")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        key_metrics = ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS']
        available_metrics = [col for col in key_metrics if col in numeric_cols]
        
        if available_metrics:
            summary_stats = df[available_metrics].describe()
            st.dataframe(summary_stats, use_container_width=True)
        else:
            st.warning("No numeric metrics available for summary statistics.")
    
    with tab2:
        st.subheader(f"Time Series Analysis - {selected_country}")
        
        if 'Timestamp' in df.columns:
            metric_options = ['GHI', 'DNI', 'DHI', 'Tamb', 'WS']
            available_metrics = [m for m in metric_options if m in df.columns]
            
            selected_metrics = st.multiselect(
                "Select metrics to plot",
                options=available_metrics,
                default=['GHI', 'DNI', 'DHI'] if all(m in df.columns for m in ['GHI', 'DNI', 'DHI']) else available_metrics[:3]
            )
            
            if selected_metrics:
                # Sample data if too large for performance
                sample_size = st.slider("Sample size (for performance)", 1000, len(df), min(10000, len(df)), 1000)
                df_sample = df.sample(min(sample_size, len(df))) if len(df) > sample_size else df
                
                fig, ax = plt.subplots(figsize=(14, 6))
                for metric in selected_metrics:
                    ax.plot(df_sample['Timestamp'], df_sample[metric], label=metric, alpha=0.7)
                
                ax.set_xlabel("Time", fontsize=12)
                ax.set_ylabel("Value", fontsize=12)
                ax.set_title(f"Time Series: {selected_country}", fontsize=14, fontweight='bold')
                ax.legend(loc="upper right")
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            else:
                st.info("Please select at least one metric to visualize.")
        else:
            st.warning("Timestamp column not available for time series analysis.")
    
    with tab3:
        st.subheader(f"Distribution Analysis - {selected_country}")
        
        metric_options = ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS']
        available_metrics = [m for m in metric_options if m in df.columns]
        
        selected_metrics = st.multiselect(
            "Select metrics for distribution",
            options=available_metrics,
            default=['GHI', 'WS'] if all(m in df.columns for m in ['GHI', 'WS']) else available_metrics[:2]
        )
        
        if selected_metrics:
            n_cols = len(selected_metrics)
            n_rows = (n_cols + 2) // 3
            
            fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5*n_rows))
            axes = axes.flatten() if n_rows > 1 else [axes] if n_cols == 1 else axes
            
            for idx, metric in enumerate(selected_metrics):
                sns.histplot(df[metric], bins=30, kde=True, ax=axes[idx])
                axes[idx].set_title(f"{metric} Distribution", fontweight='bold')
                axes[idx].grid(True, alpha=0.3)
            
            # Hide unused subplots
            for idx in range(len(selected_metrics), len(axes)):
                axes[idx].set_visible(False)
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        else:
            st.info("Please select at least one metric to visualize.")
    
    with tab4:
        st.subheader(f"Correlation Analysis - {selected_country}")
        
        corr_metrics = ['GHI', 'DNI', 'DHI', 'TModA', 'TModB', 'Tamb', 'RH', 'WS']
        available_corr = [m for m in corr_metrics if m in df.columns]
        
        if len(available_corr) >= 2:
            selected_corr = st.multiselect(
                "Select metrics for correlation",
                options=available_corr,
                default=available_corr[:5] if len(available_corr) >= 5 else available_corr
            )
            
            if len(selected_corr) >= 2:
                fig, ax = plt.subplots(figsize=(10, 8))
                corr_matrix = df[selected_corr].corr()
                sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0,
                           square=True, fmt='.2f', cbar_kws={"shrink": 0.8}, ax=ax)
                ax.set_title(f"Correlation Heatmap - {selected_country}", fontsize=14, fontweight='bold')
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()
            else:
                st.warning("Please select at least 2 metrics for correlation analysis.")
        else:
            st.warning("Insufficient metrics available for correlation analysis.")

def show_cross_country_comparison(datasets):
    """Cross-country comparison page"""
    st.header("🔍 Cross-Country Comparison")
    
    # Combine all datasets
    df_combined = pd.concat(datasets.values(), ignore_index=True)
    
    # Metric selector
    metric_options = ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS']
    available_metrics = [m for m in metric_options if m in df_combined.columns]
    
    selected_metric = st.selectbox(
        "Select Metric for Comparison",
        options=available_metrics,
        index=0
    )
    
    # Comparison type
    comparison_type = st.radio(
        "Comparison Type",
        ["Box Plot", "Violin Plot", "Summary Statistics"],
        horizontal=True
    )
    
    if comparison_type == "Box Plot":
        fig, ax = plt.subplots(figsize=(10, 6))
        
        data_for_plot = []
        labels = []
        colors_dict = {'Benin': '#2E86AB', 'Sierra Leone': '#A23B72', 'Togo': '#F18F01'}
        plot_colors = []
        
        for country in sorted(df_combined['Country'].unique()):
            country_data = df_combined[df_combined['Country'] == country][selected_metric].dropna()
            if len(country_data) > 0:
                data_for_plot.append(country_data)
                labels.append(country)
                plot_colors.append(colors_dict.get(country, '#808080'))
        
        bp = ax.boxplot(data_for_plot, labels=labels, patch_artist=True, showmeans=True)
        
        for patch, color in zip(bp['boxes'], plot_colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_title(f'{selected_metric} Comparison Across Countries', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{selected_metric} (W/m²)', fontsize=12)
        ax.set_xlabel('Country', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    elif comparison_type == "Violin Plot":
        fig, ax = plt.subplots(figsize=(10, 6))
        
        data_list = []
        labels_list = []
        colors_dict = {'Benin': '#2E86AB', 'Sierra Leone': '#A23B72', 'Togo': '#F18F01'}
        
        for country in sorted(df_combined['Country'].unique()):
            country_data = df_combined[df_combined['Country'] == country][selected_metric].dropna()
            if len(country_data) > 0:
                data_list.append(country_data.values)
                labels_list.append(country)
        
        parts = ax.violinplot(data_list, positions=range(len(labels_list)), 
                             showmeans=True, showmedians=True)
        
        for pc, country in zip(parts['bodies'], labels_list):
            pc.set_facecolor(colors_dict.get(country, '#808080'))
            pc.set_alpha(0.7)
        
        ax.set_xticks(range(len(labels_list)))
        ax.set_xticklabels(labels_list)
        ax.set_title(f'{selected_metric} Distribution Comparison', fontsize=14, fontweight='bold')
        ax.set_ylabel(f'{selected_metric} (W/m²)', fontsize=12)
        ax.set_xlabel('Country', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
    
    else:  # Summary Statistics
        st.subheader(f"Summary Statistics: {selected_metric}")
        
        summary_data = []
        for country in sorted(df_combined['Country'].unique()):
            country_data = df_combined[df_combined['Country'] == country][selected_metric].dropna()
            if len(country_data) > 0:
                summary_data.append({
                    'Country': country,
                    'Mean': country_data.mean(),
                    'Median': country_data.median(),
                    'Std Dev': country_data.std(),
                    'Min': country_data.min(),
                    'Max': country_data.max(),
                    'Count': len(country_data)
                })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
        # Ranking chart
        st.subheader("Country Ranking")
        summary_df_sorted = summary_df.sort_values('Mean', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors_dict = {'Benin': '#2E86AB', 'Sierra Leone': '#A23B72', 'Togo': '#F18F01'}
        bar_colors = [colors_dict.get(country, '#808080') for country in summary_df_sorted['Country']]
        
        bars = ax.bar(summary_df_sorted['Country'], summary_df_sorted['Mean'], 
                     color=bar_colors, alpha=0.8, edgecolor='black')
        ax.set_ylabel(f'Mean {selected_metric} (W/m²)', fontsize=12)
        ax.set_xlabel('Country', fontsize=12)
        ax.set_title(f'Countries Ranked by Mean {selected_metric}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        
        for bar, value in zip(bars, summary_df_sorted['Mean']):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

def show_data_quality(datasets):
    """Data quality assessment page"""
    st.header("🔍 Data Quality Assessment")
    
    selected_country = st.selectbox(
        "Select Country",
        options=list(datasets.keys()),
        index=0
    )
    
    df = datasets[selected_country]
    
    # Quality metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", len(df))
    with col2:
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        st.metric("Missing Data", f"{missing_pct:.2f}%")
    with col3:
        duplicate_count = df.duplicated().sum()
        st.metric("Duplicate Rows", duplicate_count)
    with col4:
        memory_mb = df.memory_usage(deep=True).sum() / 1024**2
        st.metric("Memory Usage", f"{memory_mb:.2f} MB")
    
    st.markdown("---")
    
    # Missing values analysis
    st.subheader("Missing Values Analysis")
    missing_df = profile_missing_values(df, threshold=0.05)
    
    if len(missing_df) > 0:
        st.dataframe(missing_df, use_container_width=True, hide_index=True)
        
        # Visualize missing values
        if missing_df['Missing_Count'].sum() > 0:
            fig, ax = plt.subplots(figsize=(12, 6))
            missing_df_sorted = missing_df.sort_values('Missing_Percentage', ascending=False).head(10)
            ax.barh(missing_df_sorted['Column'], missing_df_sorted['Missing_Percentage'])
            ax.set_xlabel('Missing Percentage (%)', fontsize=12)
            ax.set_ylabel('Column', fontsize=12)
            ax.set_title('Top 10 Columns with Missing Values', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3, axis='x')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
    else:
        st.success("✅ No missing values detected!")
    
    # Outlier detection
    st.subheader("Outlier Detection (Z-Score Method)")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    key_cols = [col for col in ['GHI', 'DNI', 'DHI', 'ModA', 'ModB', 'WS'] if col in numeric_cols]
    
    if key_cols:
        threshold = st.slider("Z-Score Threshold", 2.0, 5.0, 3.0, 0.5)
        outlier_info = detect_outliers_zscore(df, key_cols, threshold=threshold)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Outliers Detected", outlier_info['outlier_count'])
        with col2:
            outlier_pct = (outlier_info['outlier_count'] / len(df)) * 100
            st.metric("Outlier Percentage", f"{outlier_pct:.2f}%")
    else:
        st.warning("No numeric columns available for outlier detection.")

def show_about():
    """About page"""
    st.header("📖 About")
    
    st.markdown("""
    ### Solar Energy Data Dashboard
    
    This interactive dashboard provides comprehensive analysis and visualization tools for solar energy datasets
    from three West African countries: **Benin**, **Sierra Leone**, and **Togo**.
    
    #### Features
    
    - **Overview**: Key metrics and country summaries
    - **Country Analysis**: Detailed analysis for individual countries including:
      - Summary statistics
      - Time series visualizations
      - Distribution analysis
      - Correlation heatmaps
    - **Cross-Country Comparison**: Compare metrics across all countries with:
      - Box plots
      - Violin plots
      - Summary statistics and rankings
    - **Data Quality**: Assess data quality including:
      - Missing value analysis
      - Outlier detection
      - Data completeness metrics
    
    #### Data Sources
    
    The datasets contain solar energy measurements including:
    - **GHI**: Global Horizontal Irradiance (W/m²)
    - **DNI**: Direct Normal Irradiance (W/m²)
    - **DHI**: Diffuse Horizontal Irradiance (W/m²)
    - **Tamb**: Ambient temperature (°C)
    - **RH**: Relative humidity (%)
    - **WS**: Wind speed (m/s)
    - **WD**: Wind direction (degrees)
    
    #### Technical Details
    
    - Built with **Streamlit**
    - Uses modular code from `src/` directory
    - Supports interactive filtering and exploration
    - Professional, responsive UI design
    
    #### Version
    
    Dashboard Version: 1.0.0
    """)
    
    st.markdown("---")
    st.markdown(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()

