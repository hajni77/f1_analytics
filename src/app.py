"""
F1 Analytics - Main Streamlit Application

This is the main entry point for the F1 Analytics application.
It integrates all components and visualizations to create a
comprehensive F1 data visualization dashboard.
"""
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import components
from components.sidebar import display_sidebar
from components.header import display_header

# Import API client
from api.client import F1ApiClient

# Import visualizations
from visualizations.drivers import display_driver_standings, display_driver_comparison
from visualizations.teams import display_team_standings, display_team_comparison
from visualizations.races import display_race_calendar, display_race_results, display_race_comparison
from visualizations.seasons import display_season_overview, display_season_comparison


def main():
    """
    Main application entry point.
    """
    # Set page configuration
    st.set_page_config(
        page_title="F1 Analytics",
        page_icon="🏎️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Create sidebar navigation
    selected_page, selected_season = display_sidebar()
    
    # Initialize API client (no API key needed for f1api.dev)
    client = F1ApiClient()
    
    try:
        # Create page header
        display_header()
        
        # Display selected page
        if selected_page == "Driver Standings":
            display_driver_standings(client, selected_season)
        
        elif selected_page == "Team Standings":
            display_team_standings(client, selected_season)
        
        elif selected_page == "Race Calendar":
            display_race_calendar(client, selected_season)
        
        elif selected_page == "Race Results":
            display_race_results(client, selected_season)
        
        elif selected_page == "Driver Comparison":
            display_driver_comparison(client, selected_season)
        
        elif selected_page == "Team Comparison":
            display_team_comparison(client, selected_season)
        
        elif selected_page == "Race Comparison":
            display_race_comparison(client, selected_season)
        
        elif selected_page == "Season Overview":
            display_season_overview(client, selected_season)
        
        elif selected_page == "Season Comparison":
            display_season_comparison(client)
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please try again later or check the console for more details.")


if __name__ == "__main__":
    main()
