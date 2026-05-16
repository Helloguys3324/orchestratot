"""
Data Analyst Skill — Analyze data with pandas.
"""


def analyze_csv(filepath: str) -> str:
    """Analyze a CSV file and return summary statistics."""
    try:
        import pandas as pd
        df = pd.read_csv(filepath)
        info = f"Shape: {df.shape}\n"
        info += f"Columns: {list(df.columns)}\n"
        info += f"\nFirst 5 rows:\n{df.head().to_string()}\n"
        info += f"\nStatistics:\n{df.describe().to_string()}"
        return info
    except ImportError:
        return "pandas is not installed"
    except Exception as e:
        return f"Error: {str(e)}"
