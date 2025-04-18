"""
Helper functions for the F1 Analytics application.
"""
import os
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import streamlit as st
from datetime import datetime
from api.models import Driver, Team, Race, DriverStanding, TeamStanding, RaceResult


def format_time(time_str: Optional[str]) -> str:
    """
    Format a lap time string for display.
    
    Args:
        time_str (Optional[str]): Lap time string in format "MM:SS.mmm".
        
    Returns:
        str: Formatted time string or empty string if None.
    """
    if not time_str:
        return ""
    
    try:
        parts = time_str.split(":")
        if len(parts) == 2:
            minutes, seconds = parts
            return f"{int(minutes)}m {float(seconds):.3f}s"
        return time_str
    except Exception:
        return time_str


def convert_to_dataframe(data_list: List[Any]) -> pd.DataFrame:
    """
    Convert a list of dataclass instances to a pandas DataFrame.
    
    Args:
        data_list (List[Any]): List of dataclass instances.
        
    Returns:
        pd.DataFrame: DataFrame representation of the data.
    """
    if not data_list:
        return pd.DataFrame()
    
    # Convert dataclass instances to dictionaries
    data_dicts = []
    for item in data_list:
        # if the item is a dictionary, add it directly
        if isinstance(item, dict):
            data_dicts.append(item)
        else:
            data_dicts.append(vars(item))

    if not data_dicts:
        return pd.DataFrame()
    print(data_dicts)
    # Process nested objects recursively
    flattened_dicts = []
    for data_dict in data_dicts:
        flattened_dict = {}
        _flatten_dict(data_dict, flattened_dict)
        flattened_dicts.append(flattened_dict)
    
    # Create DataFrame from flattened dictionaries
    return pd.DataFrame(flattened_dicts)

def _flatten_dict(nested_dict: Dict[str, Any], flattened_dict: Dict[str, Any], prefix: str = '') -> None:
    """
    Recursively flatten a nested dictionary.
    
    Args:
        nested_dict (Dict[str, Any]): The nested dictionary to flatten.
        flattened_dict (Dict[str, Any]): The output flattened dictionary.
        prefix (str, optional): Prefix for keys in the flattened dictionary.
    """
    for key, value in nested_dict.items():
        # Create the new key with prefix
        new_key = f"{prefix}.{key}" if prefix else key
        
        # Handle different types of values
        if hasattr(value, '__dataclass_fields__'):
            # If value is a dataclass, flatten its fields
            _flatten_dict(vars(value), flattened_dict, new_key)
        elif isinstance(value, dict):
            # If value is a dictionary, flatten it recursively
            _flatten_dict(value, flattened_dict, new_key)
        elif isinstance(value, list) and value and hasattr(value[0], '__dataclass_fields__'):
            # If value is a list of dataclasses, flatten each item
            for i, item in enumerate(value):
                _flatten_dict(vars(item), flattened_dict, f"{new_key}[{i}]")
        else:
            # For primitive types or other objects, store directly
            flattened_dict[new_key] = value


def get_color_scale(n: int) -> List[str]:
    """
    Generate a list of n distinct colors for visualizations.
    
    Args:
        n (int): Number of colors needed.
        
    Returns:
        List[str]: List of hex color codes.
    """
    # Predefined colors for F1 teams (2023 season)
    team_colors = {
        "mercedes": "#00D2BE",
        "red_bull": "#0600EF",
        "ferrari": "#DC0000",
        "mclaren": "#FF8700",
        "alpine": "#0090FF",
        "aston_martin": "#006F62",
        "williams": "#005AFF",
        "rb": "#900000",
        "haas": "#FFFFFF",
        "sauber": "#0090FF"
    }
    
    # Default color palette if we need more colors
    default_colors = [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
        "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
        "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5"
    ]
    
    if n <= len(default_colors):
        return default_colors[:n]
    
    # If we need more colors than available, repeat with different opacity
    colors = default_colors.copy()
    while len(colors) < n:
        colors.extend(default_colors[:n-len(colors)])
    
    return colors[:n]


@st.cache_data(ttl=3600)  # Cache for 1 hour
def cache_api_response(_func, *args, **kwargs) -> Any:
    """
    Cache API responses to reduce API calls and improve performance.
    
    Args:
        func: Function to call.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.
        
    Returns:
        Any: Result of the function call.
    """
    return _func(*args, **kwargs)


def create_season_selector(min_year: int = 2000, max_year: int = None) -> int:
    """
    Create a season selector widget in the Streamlit sidebar.
    
    Args:
        min_year (int): Minimum year to include in the selector.
        max_year (int): Maximum year to include in the selector.
        
    Returns:
        int: Selected season year.
    """
    if max_year is None:
        max_year = datetime.now().year
    
    years = list(range(max_year, min_year - 1, -1))
    selected_year = st.sidebar.selectbox("Select Season", years, index=0)
    
    return selected_year


def format_driver_name(driver: Driver) -> str:
    """
    Format a driver's name for display.
    
    Args:
        driver (Driver): Driver instance.
        
    Returns:
        str: Formatted driver name.
    """
    return f"{driver.name[0]}. {driver.surname}"
