"""
Header component for the F1 Analytics app.
"""
import streamlit as st


def display_header():
    """
    Display the application header.
    """
    st.title("🏎️ Formula 1 Analytics")
    st.markdown(
        """
        Explore Formula 1 statistics and data visualizations.
        Data provided by the free f1api.dev API.
        """
    )
    st.markdown("---")
