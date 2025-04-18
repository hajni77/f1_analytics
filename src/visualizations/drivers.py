"""
Visualizations for F1 driver data.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any

from api.client import F1ApiClient
from api.models import Driver, DriverStanding
from utils.helpers import convert_to_dataframe, get_color_scale, cache_api_response


def display_driver_standings(client: F1ApiClient, season: int) -> None:
    """
    Display driver standings visualization.
    
    Args:
        client (F1ApiClient): F1 API client instance.
        season (int): Season year to display.
    """
    st.header(f"Driver Standings - {season} Season")
    
    with st.spinner("Loading driver standings..."):
        # Fetch data with caching
        standings_data = cache_api_response(client.get_driver_standings, season)
     
        if not standings_data:
            st.warning(f"No driver standings data available for the {season} season.")
            return
        
        # Convert API data to our models
        standings = [DriverStanding.from_api(item) for item in standings_data]
        
        # Convert to DataFrame for visualization
        df = convert_to_dataframe(standings)
        
        # Add team information if available
        df['team_name'] = [s.team.teamName if s.team else s.teamId for s in standings]
        df['driver_name'] = [f"{s.driver.name} {s.driver.surname}" if s.driver else s.driverId for s in standings]
        
        # Create bar chart for points
        fig = px.bar(
            df.sort_values('position'),
            x='driver_name',
            y='points',
            color='team_name',
            labels={
                'driver_name': 'Driver',
                'points': 'Points',
                'team_name': 'Team'
            },
            title=f"Driver Standings - {season}",
            height=500,
            color_discrete_sequence=get_color_scale(len(df['team_name'].unique()))
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title="Driver",
            yaxis_title="Points",
            legend_title="Team",
            font=dict(size=12),
            xaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display standings table
        st.subheader("Driver Standings Table")
        
        # Prepare data for table
        table_data = {
            "Position": [s.position for s in standings],
            "Driver": [f"{s.driver.name} {s.driver.surname}" if s.driver else s.driverId for s in standings],
            "Team": [s.team.teamName if s.team else s.teamId for s in standings],
            "Points": [s.points for s in standings],
            "Wins": [s.wins for s in standings]
        }
        
        table_df = pd.DataFrame(table_data)
        st.dataframe(table_df, use_container_width=True)


def display_driver_comparison(client: F1ApiClient, season: int) -> None:
    """
    Display driver comparison visualization.
    
    Args:
        client (F1ApiClient): F1 API client instance.
        season (int): Season year to display.
    """
    st.header(f"Driver Comparison - {season} Season")
    
    with st.spinner("Loading driver data..."):
        # Fetch data with caching
        standings_data = cache_api_response(client.get_driver_standings, season)
        
        if not standings_data:
            st.warning(f"No driver data available for the {season} season.")
            return
        
        # Convert API data to our models
        standings = [DriverStanding.from_api(item) for item in standings_data]
        
        # Get list of drivers for selection with proper names
        drivers = [(i, f"{s.driver.name} {s.driver.surname}" if s.driver else s.driverId) for i, s in enumerate(standings)]
        
        # Create driver selection
        col1, col2 = st.columns(2)
        
        with col1:
            driver1_idx = st.selectbox(
                "Select Driver 1",
                range(len(drivers)),
                format_func=lambda i: drivers[i][1]
            )
        
        with col2:
            driver2_idx = st.selectbox(
                "Select Driver 2",
                range(len(drivers)),
                format_func=lambda i: drivers[i][1],
                index=1 if len(drivers) > 1 else 0
            )
        
        # Display driver comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(drivers[driver1_idx][1])
            st.metric("Position", standings[driver1_idx].position)
            st.metric("Points", standings[driver1_idx].points)
            st.metric("Wins", standings[driver1_idx].wins)
            if standings[driver1_idx].team:
                st.text(f"Team: {standings[driver1_idx].team.teamName}")
            if standings[driver1_idx].driver:
                st.text(f"Nationality: {standings[driver1_idx].driver.nationality}")
        
        with col2:
            st.subheader(drivers[driver2_idx][1])
            st.metric("Position", standings[driver2_idx].position)
            st.metric("Points", standings[driver2_idx].points)
            st.metric("Wins", standings[driver2_idx].wins)
            if standings[driver2_idx].team:
                st.text(f"Team: {standings[driver2_idx].team.teamName}")
            if standings[driver2_idx].driver:
                st.text(f"Nationality: {standings[driver2_idx].driver.nationality}")
        
        # Create radar chart for comparison
        categories = ['Points', 'Wins', 'Position']
        
        # Normalize position (lower is better, so invert)
        max_position = max(s.position for s in standings)
        position1_normalized = (max_position - standings[driver1_idx].position + 1) / max_position
        position2_normalized = (max_position - standings[driver2_idx].position + 1) / max_position
        
        # Normalize points
        max_points = max(s.points for s in standings)
        points1_normalized = standings[driver1_idx].points / max_points if max_points > 0 else 0
        points2_normalized = standings[driver2_idx].points / max_points if max_points > 0 else 0
        
        # Normalize wins
        max_wins = max(s.wins for s in standings)
        wins1_normalized = standings[driver1_idx].wins / max_wins if max_wins > 0 else 0
        wins2_normalized = standings[driver2_idx].wins / max_wins if max_wins > 0 else 0
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=[points1_normalized, wins1_normalized, position1_normalized],
            theta=categories,
            fill='toself',
            name=drivers[driver1_idx][1]
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=[points2_normalized, wins2_normalized, position2_normalized],
            theta=categories,
            fill='toself',
            name=drivers[driver2_idx][1]
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            title="Driver Performance Comparison"
        )
        
        st.plotly_chart(fig, use_container_width=True)
