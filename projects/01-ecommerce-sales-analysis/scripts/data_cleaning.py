"""
Data Cleaning Functions
Reusable Python functions for common data cleaning tasks
"""

import pandas as pd
import numpy as np


def load_data(filepath):
    """
    Load CSV file into a DataFrame
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV file
        
    Returns:
    --------
    pd.DataFrame
        Loaded data
    """
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Successfully loaded {len(df)} rows and {len(df.columns)} columns")
        return df
    except FileNotFoundError:
        print(f"❌ Error: File not found at {filepath}")
        return None


def check_missing_values(df):
    """
    Identify and display missing values
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
        
    Returns:
    --------
    pd.DataFrame
        Summary of missing values
    """
    missing_summary = pd.DataFrame({
        'Column': df.columns,
        'Missing Count': df.isnull().sum().values,
        'Missing %': (df.isnull().sum().values / len(df) * 100).round(2)
    })
    
    return missing_summary[missing_summary['Missing Count'] > 0]


def remove_duplicates(df):
    """
    Remove duplicate rows from DataFrame
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with duplicates removed
    """
    duplicates_before = len(df)
    df_clean = df.drop_duplicates()
    duplicates_removed = duplicates_before - len(df_clean)
    
    print(f"🔍 Found and removed {duplicates_removed} duplicate rows")
    return df_clean


def convert_date_columns(df, date_columns):
    """
    Convert specified columns to datetime
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    date_columns : list
        List of column names to convert
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with converted date columns
    """
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
            print(f"✅ Converted '{col}' to datetime")
    
    return df


def fill_missing_values(df, strategy='mean', columns=None):
    """
    Fill missing values using specified strategy
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    strategy : str
        'mean' - fill with mean value
        'median' - fill with median value
        'forward_fill' - forward fill
        'backward_fill' - backward fill
    columns : list
        Specific columns to fill (if None, all numeric columns)
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with filled missing values
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns
    
    for col in columns:
        if df[col].isnull().sum() > 0:
            if strategy == 'mean':
                df[col].fillna(df[col].mean(), inplace=True)
            elif strategy == 'median':
                df[col].fillna(df[col].median(), inplace=True)
            elif strategy == 'forward_fill':
                df[col].fillna(method='ffill', inplace=True)
            elif strategy == 'backward_fill':
                df[col].fillna(method='bfill', inplace=True)
    
    return df


def get_data_summary(df):
    """
    Get comprehensive data summary
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
        
    Returns:
    --------
    dict
        Summary statistics
    """
    summary = {
        'Total Rows': len(df),
        'Total Columns': len(df.columns),
        'Total Missing Values': df.isnull().sum().sum(),
        'Duplicate Rows': df.duplicated().sum(),
        'Memory Usage (MB)': df.memory_usage(deep=True).sum() / 1024**2
    }
    
    return summary


# Example usage:
if __name__ == "__main__":
    # Load data
    df = load_data('data/sales_data.csv')
    
    if df is not None:
        # Check missing values
        print("\nMissing Values Summary:")
        print(check_missing_values(df))
        
        # Remove duplicates
        df = remove_duplicates(df)
        
        # Convert date column
        df = convert_date_columns(df, ['date'])
        
        # Get summary
        print("\nData Summary:")
        summary = get_data_summary(df)
        for key, value in summary.items():
            print(f"{key}: {value}")
