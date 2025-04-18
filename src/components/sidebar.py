"""
Sidebar component for the F1 Analytics app.
"""
import streamlit as st
from datetime import datetime
from utils.helpers import cache_api_response


def display_sidebar():
    """
    Display the sidebar with navigation options.
    
    Returns:
        tuple: Selected view and season.
    """
    with st.sidebar:
        st.title("F1 Analytics")
        st.markdown("Explore Formula 1 data and statistics")
        
        # Season selection
        current_year = datetime.now().year
        selected_season = st.selectbox(
            "Select Season",
            range(current_year, 1949, -1),
            index=0
        )
        
        # Navigation
        st.markdown("---")
        st.subheader("Navigation")
        
        view_options = [
            "Driver Standings",
            "Team Standings",
            "Race Calendar",
            "Race Results",
            "Driver Comparison",
            "Team Comparison",
            "Race Comparison",
            "Season Overview",
            "Season Comparison"
        ]
        
        selected_view = st.radio("Select View", view_options)
        
        # About section
        st.markdown("---")
        st.markdown("### About")
        st.markdown("F1 Analytics uses data from the free f1api.dev API.")
        st.markdown("Built with Streamlit and Python.")
        
        # Version
        st.markdown("---")
        st.markdown("v1.0.0")
    
    return selected_view, selected_season
