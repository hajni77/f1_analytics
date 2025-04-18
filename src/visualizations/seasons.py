"""
Visualizations for F1 season data.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any

from api.client import F1ApiClient
from api.models import Season, Driver, Team
from utils.helpers import convert_to_dataframe, get_color_scale, cache_api_response


def display_season_overview(client: F1ApiClient, season: int) -> None:
    """
    Display season overview visualization.
    
    Args:
        client (F1ApiClient): F1 API client instance.
        season (int): Season year to display.
    """
    st.header(f"Season Overview - {season}")
    
    with st.spinner("Loading season data..."):
        # Fetch driver standings with caching
        driver_standings_data = cache_api_response(client.get_driver_standings, season)
        
        # Fetch constructor standings with caching
        constructor_standings_data = cache_api_response(client.get_constructor_standings, season)
        
        # Fetch races with caching
        races_data = cache_api_response(client.get_races, season)
        
        # Display season statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Drivers", len(driver_standings_data) if driver_standings_data else "N/A")
        
        with col2:
            st.metric("Teams", len(constructor_standings_data) if constructor_standings_data else "N/A")
        
        with col3:
            st.metric("Races", len(races_data) if races_data else "N/A")
        
        # Display top 3 drivers if data available
        if driver_standings_data:
            st.subheader("Top Drivers")
            
            # Sort by position
            sorted_drivers = sorted(driver_standings_data, key=lambda x: x.get('position', 999))[:3]
            
            driver_cols = st.columns(3)
            for i, driver_data in enumerate(sorted_drivers):
                with driver_cols[i]:
                    driver_name = f"{driver_data.get('Driver', {}).get('name', '')} {driver_data.get('Driver', {}).get('surname', '')}"
                    st.markdown(f"**{i+1}. {driver_name}**")
                    st.markdown(f"Points: {driver_data.get('points', 0)}")
                    st.markdown(f"Wins: {driver_data.get('wins', 0)}")
        
        # Display top 3 teams if data available
        if constructor_standings_data:
            st.subheader("Top Teams")
            
            # Sort by position
            sorted_teams = sorted(constructor_standings_data, key=lambda x: x.get('position', 999))[:3]
            
            team_cols = st.columns(3)
            for i, team_data in enumerate(sorted_teams):
                with team_cols[i]:
                    team_name = team_data.get('teamId', 'Unknown Team')
                    st.markdown(f"**{i+1}. {team_name}**")
                    st.markdown(f"Points: {team_data.get('points', 0)}")
                    st.markdown(f"Wins: {team_data.get('wins', 0)}")


def display_season_comparison(client: F1ApiClient) -> None:
    """
    Display season comparison visualization.
    
    Args:
        client (F1ApiClient): F1 API client instance.
    """
    st.header("Season Comparison")
    
    with st.spinner("Loading seasons..."):
        # Fetch seasons with caching
        seasons_data = cache_api_response(client.get_seasons)
        
        if not seasons_data:
            st.warning("No seasons data available.")
            return
        
        # Convert to list of years
        available_seasons = [s.get('year', 0) for s in seasons_data]
        available_seasons.sort(reverse=True)
        
        # Create season selection
        col1, col2 = st.columns(2)
        
        with col1:
            season1 = st.selectbox(
                "Select Season 1",
                available_seasons,
                index=0 if available_seasons else 0
            )
        
        with col2:
            season2 = st.selectbox(
                "Select Season 2",
                available_seasons,
                index=1 if len(available_seasons) > 1 else 0
            )
        
        # Fetch data for both seasons
        with st.spinner(f"Loading data for {season1} and {season2}..."):
            # Fetch driver standings for both seasons
            driver_standings1 = cache_api_response(client.get_driver_standings, season1)
            driver_standings2 = cache_api_response(client.get_driver_standings, season2)
            
            # Fetch constructor standings for both seasons
            constructor_standings1 = cache_api_response(client.get_constructor_standings, season1)
            constructor_standings2 = cache_api_response(client.get_constructor_standings, season2)
            
            # Fetch races for both seasons
            races1 = cache_api_response(client.get_races, season1)
            races2 = cache_api_response(client.get_races, season2)
            
            # Display season statistics comparison
            st.subheader("Season Statistics Comparison")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"### {season1}")
                st.metric("Drivers", len(driver_standings1) if driver_standings1 else "N/A")
                st.metric("Teams", len(constructor_standings1) if constructor_standings1 else "N/A")
                st.metric("Races", len(races1) if races1 else "N/A")
                
                if driver_standings1:
                    champion_data = sorted(driver_standings1, key=lambda x: x.get('position', 999))[0]
                    champion_name = f"{champion_data.get('Driver', {}).get('name', '')} {champion_data.get('Driver', {}).get('surname', '')}"
                    st.metric("Champion", champion_name)
                    st.metric("Champion Points", champion_data.get('points', 0))
            
            with col2:
                st.markdown(f"### {season2}")
                st.metric("Drivers", len(driver_standings2) if driver_standings2 else "N/A")
                st.metric("Teams", len(constructor_standings2) if constructor_standings2 else "N/A")
                st.metric("Races", len(races2) if races2 else "N/A")
                
                if driver_standings2:
                    champion_data = sorted(driver_standings2, key=lambda x: x.get('position', 999))[0]
                    champion_name = f"{champion_data.get('Driver', {}).get('name', '')} {champion_data.get('Driver', {}).get('surname', '')}"
                    st.metric("Champion", champion_name)
                    st.metric("Champion Points", champion_data.get('points', 0))
            
            # Create a bar chart comparing top 5 drivers from both seasons
            st.subheader("Top Drivers Comparison")
            
            if driver_standings1 and driver_standings2:
                # Prepare data for top 5 drivers from each season
                top_drivers1 = sorted(driver_standings1, key=lambda x: x.get('position', 999))[:5]
                top_drivers2 = sorted(driver_standings2, key=lambda x: x.get('position', 999))[:5]
                
                drivers1_data = {
                    'Season': [str(season1)] * len(top_drivers1),
                    'Driver': [f"{d.get('Driver', {}).get('name', '')} {d.get('Driver', {}).get('surname', '')}" for d in top_drivers1],
                    'Points': [d.get('points', 0) for d in top_drivers1]
                }
                
                drivers2_data = {
                    'Season': [str(season2)] * len(top_drivers2),
                    'Driver': [f"{d.get('Driver', {}).get('name', '')} {d.get('Driver', {}).get('surname', '')}" for d in top_drivers2],
                    'Points': [d.get('points', 0) for d in top_drivers2]
                }
                
                # Combine data
                combined_data = pd.DataFrame({
                    'Season': drivers1_data['Season'] + drivers2_data['Season'],
                    'Driver': drivers1_data['Driver'] + drivers2_data['Driver'],
                    'Points': drivers1_data['Points'] + drivers2_data['Points']
                })
                
                # Create grouped bar chart
                fig = px.bar(
                    combined_data,
                    x='Driver',
                    y='Points',
                    color='Season',
                    barmode='group',
                    title=f"Top Drivers Comparison: {season1} vs {season2}",
                    height=500
                )
                
                fig.update_layout(
                    xaxis_title="Driver",
                    yaxis_title="Points",
                    legend_title="Season",
                    font=dict(size=12)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Insufficient data to compare drivers between seasons.")
            
            # Create a bar chart comparing top 5 teams from both seasons
            st.subheader("Top Teams Comparison")
            
            if constructor_standings1 and constructor_standings2:
                # Prepare data for top 5 teams from each season
                top_teams1 = sorted(constructor_standings1, key=lambda x: x.get('position', 999))[:5]
                top_teams2 = sorted(constructor_standings2, key=lambda x: x.get('position', 999))[:5]
                
                teams1_data = {
                    'Season': [str(season1)] * len(top_teams1),
                    'Team': [t.get('teamId', 'Unknown Team') for t in top_teams1],
                    'Points': [t.get('points', 0) for t in top_teams1]
                }
                
                teams2_data = {
                    'Season': [str(season2)] * len(top_teams2),
                    'Team': [t.get('teamId', 'Unknown Team') for t in top_teams2],
                    'Points': [t.get('points', 0) for t in top_teams2]
                }
                
                # Combine data
                combined_data = pd.DataFrame({
                    'Season': teams1_data['Season'] + teams2_data['Season'],
                    'Team': teams1_data['Team'] + teams2_data['Team'],
                    'Points': teams1_data['Points'] + teams2_data['Points']
                })
                
                # Create grouped bar chart
                fig = px.bar(
                    combined_data,
                    x='Team',
                    y='Points',
                    color='Season',
                    barmode='group',
                    title=f"Top Teams Comparison: {season1} vs {season2}",
                    height=500
                )
                
                fig.update_layout(
                    xaxis_title="Team",
                    yaxis_title="Points",
                    legend_title="Season",
                    font=dict(size=12)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Insufficient data to compare teams between seasons.")
