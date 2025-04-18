"""
Visualizations for F1 team data.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any

from api.client import F1ApiClient
from api.models import Team, TeamStanding
from utils.helpers import convert_to_dataframe, get_color_scale, cache_api_response


def display_team_standings(client: F1ApiClient, season: int) -> None:
    """
    Display team standings visualization.
    
    Args:
        client (F1ApiClient): F1 API client instance.
        season (int): Season year to display.
    """
    st.header(f"Team Standings - {season} Season")
    
    with st.spinner("Loading team standings..."):
        # Fetch data with caching
        standings_data = cache_api_response(client.get_constructor_standings, season)
        
        if not standings_data:
            st.warning(f"No team standings data available for the {season} season.")
            return
        
        # Convert API data to our models
        standings = [TeamStanding.from_api(item) for item in standings_data]
        
        # Convert to DataFrame for visualization
        df = convert_to_dataframe(standings)
        
        # Add team name if available
        df['team_name'] = [s.team.teamName if s.team else s.teamId for s in standings]
        
        # Create bar chart for points
        fig = px.bar(
            df.sort_values('position'),
            x='team_name',
            y='points',
            color='team_name',
            labels={
                'team_name': 'Team',
                'points': 'Points'
            },
            title=f"Team Standings - {season}",
            height=500,
            color_discrete_sequence=get_color_scale(len(df))
        )
        
        # Customize layout
        fig.update_layout(
            xaxis_title="Team",
            yaxis_title="Points",
            legend_title="Team",
            font=dict(size=12),
            xaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display standings table
        st.subheader("Team Standings Table")
        
        # Prepare data for table
        table_data = {
            "Position": [s.position for s in standings],
            "Team": [s.team.teamName if s.team else s.teamId for s in standings],
            "Points": [s.points for s in standings],
            "Wins": [s.wins for s in standings],
            "Country": [s.team.country if s.team else "Unknown" for s in standings]
        }
        
        table_df = pd.DataFrame(table_data)
        st.dataframe(table_df, use_container_width=True)


def display_team_comparison(client: F1ApiClient, season: int) -> None:
    """
    Display team comparison visualization.
    
    Args:
        client (F1ApiClient): F1 API client instance.
        season (int): Season year to display.
    """
    st.header(f"Team Comparison - {season} Season")
    
    with st.spinner("Loading team data..."):
        # Fetch data with caching
        standings_data = cache_api_response(client.get_constructor_standings, season)
        
        if not standings_data:
            st.warning(f"No team data available for the {season} season.")
            return
        
        # Convert API data to our models
        standings = [TeamStanding.from_api(item) for item in standings_data]
        
        # Get list of teams for selection with proper names
        teams = [(i, s.team.teamName if s.team else s.teamId) for i, s in enumerate(standings)]
        
        # Create team selection
        col1, col2 = st.columns(2)
        
        with col1:
            team1_idx = st.selectbox(
                "Select Team 1",
                range(len(teams)),
                format_func=lambda i: teams[i][1]
            )
        
        with col2:
            team2_idx = st.selectbox(
                "Select Team 2",
                range(len(teams)),
                format_func=lambda i: teams[i][1],
                index=1 if len(teams) > 1 else 0
            )
        
        # Display team comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(teams[team1_idx][1])
            st.metric("Position", standings[team1_idx].position)
            st.metric("Points", standings[team1_idx].points)
            st.metric("Wins", standings[team1_idx].wins)
            if standings[team1_idx].team:
                st.text(f"Country: {standings[team1_idx].team.country}")
                st.text(f"Championships: {standings[team1_idx].team.constructorsChampionships}")
        
        with col2:
            st.subheader(teams[team2_idx][1])
            st.metric("Position", standings[team2_idx].position)
            st.metric("Points", standings[team2_idx].points)
            st.metric("Wins", standings[team2_idx].wins)
            if standings[team2_idx].team:
                st.text(f"Country: {standings[team2_idx].team.country}")
                st.text(f"Championships: {standings[team2_idx].team.constructorsChampionships}")
        
        # Create radar chart for comparison
        categories = ['Points', 'Wins', 'Position']
        
        # Normalize position (lower is better, so invert)
        max_position = max(s.position for s in standings)
        position1_normalized = (max_position - standings[team1_idx].position + 1) / max_position
        position2_normalized = (max_position - standings[team2_idx].position + 1) / max_position
        
        # Normalize points
        max_points = max(s.points for s in standings)
        points1_normalized = standings[team1_idx].points / max_points if max_points > 0 else 0
        points2_normalized = standings[team2_idx].points / max_points if max_points > 0 else 0
        
        # Normalize wins
        max_wins = max(s.wins for s in standings)
        wins1_normalized = standings[team1_idx].wins / max_wins if max_wins > 0 else 0
        wins2_normalized = standings[team2_idx].wins / max_wins if max_wins > 0 else 0
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=[points1_normalized, wins1_normalized, position1_normalized],
            theta=categories,
            fill='toself',
            name=teams[team1_idx][1]
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=[points2_normalized, wins2_normalized, position2_normalized],
            theta=categories,
            fill='toself',
            name=teams[team2_idx][1]
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            title="Team Performance Comparison"
        )
        
        st.plotly_chart(fig, use_container_width=True)
