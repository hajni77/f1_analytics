"""
Visualizations for F1 race data.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional

from api.client import F1ApiClient
from api.models import Race, RaceResult, Championship
from utils.helpers import convert_to_dataframe, get_color_scale, format_driver_name, format_time, cache_api_response


def display_race_calendar(client: F1ApiClient, season: int) -> None:
    """
    Display race calendar visualization.
    
    Args:
        client (F1ApiClient): F1 API client instance.
        season (int): Season year to display.
    """
    st.header(f"Race Calendar - {season} Season")
    
    with st.spinner("Loading race calendar..."):
        # Fetch data with caching
        races_data = cache_api_response(client.get_races, season)
        
        if not races_data:
            st.warning(f"No race calendar data available for the {season} season.")
            return
        
        # Get championship info if available
        championship = None
        try:
            championship_data = cache_api_response(client.get_championship_info, season)
            if championship_data and isinstance(championship_data, dict):
                championship = Championship.from_api(championship_data)
                st.subheader(championship.name)
        except Exception as e:
            st.warning(f"Could not load championship data: {str(e)}")
        
        # Convert API data to our models
        api_type = 'f1api'
        races = [Race.from_api(item, api_type=api_type) for item in races_data]

        # Convert to DataFrame for visualization
        df = convert_to_dataframe(races)

        # Sort by round number
        if 'round' in df.columns:
            df = df.sort_values('round')
        
        # Create timeline chart
        try:
            # Create a more detailed timeline for F1 Connect API
            if 'schedule.race.date' in df.columns and 'name' in df.columns:
                # Create a new column for visualization
                df['race_date'] = df['schedule.race.date']
                df['qualy_date'] = df['schedule.qualy.date']
                df['fp1_date'] = df['schedule.fp1.date']
                df['fp2_date'] = df['schedule.fp2.date']
                df['fp3_date'] = df['schedule.fp3.date']
                
                # Create a list of events for each race
                events = []
                for _, row in df.iterrows():
                    race_name = row['name']
                    
                    # Handle different column names for circuit info
                    if 'circuit.name' in df.columns:
                        circuit_name = row['circuit.name']
                    elif 'schedule.circuit.circuitName' in df.columns:
                        circuit_name = row['schedule.circuit.circuitName']
                    else:
                        circuit_name = "Unknown Circuit"
                        
                    if 'circuit.country' in df.columns:
                        country = row['circuit.country']
                    elif 'schedule.circuit.country' in df.columns:
                        country = row['schedule.circuit.country']
                    else:
                        country = "Unknown Country"
                    
                    # Add each session as a separate event if date exists
                    if pd.notna(row['race_date']):
                        events.append({
                            'Race': race_name,
                            'Circuit': circuit_name,
                            'Country': country,
                            'Date': row['race_date'],
                            'Session': 'Race'
                        })
                    
                    if pd.notna(row['qualy_date']):
                        events.append({
                            'Race': race_name,
                            'Circuit': circuit_name,
                            'Country': country,
                            'Date': row['qualy_date'],
                            'Session': 'Qualifying'
                        })
                    
                    if pd.notna(row['fp1_date']):
                        events.append({
                            'Race': race_name,
                            'Circuit': circuit_name,
                            'Country': country,
                            'Date': row['fp1_date'],
                            'Session': 'Practice 1'
                        })
                    
                    if pd.notna(row['fp2_date']):
                        events.append({
                            'Race': race_name,
                            'Circuit': circuit_name,
                            'Country': country,
                            'Date': row['fp2_date'],
                            'Session': 'Practice 2'
                        })
                    
                    if pd.notna(row['fp3_date']):
                        events.append({
                            'Race': race_name,
                            'Circuit': circuit_name,
                            'Country': country,
                            'Date': row['fp3_date'],
                            'Session': 'Practice 3'
                        })
                
                # Create a new DataFrame for the timeline
                events_df = pd.DataFrame(events)
                if not events_df.empty:
                    fig = px.timeline(
                        events_df,
                        x_start='Date',
                        y='Race',
                        color='Session',
                        labels={
                            'Date': 'Date',
                            'Race': 'Grand Prix',
                            'Session': 'Session'
                        },
                        title=f"Race Calendar - {season}",
                        height=600
                    )
                    
                    # Customize layout
                    fig.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Grand Prix",
                        legend_title="Session",
                        font=dict(size=12)
                    )
                    
                    if 'round' in df.columns:
                        fig.update_layout(yaxis={'categoryorder': 'array', 'categoryarray': df.sort_values('round')['name']})
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("No session dates available for visualization")
            else:
                # Fallback to simple visualization
                st.warning("Race data format doesn't contain required fields for detailed visualization")
                
                # Create a simple bar chart of races by round
                if 'round' in df.columns and 'name' in df.columns:
                    simple_fig = px.bar(
                        df.sort_values('round'),
                        x='round',
                        y='name',
                        labels={
                            'round': 'Round',
                            'name': 'Grand Prix'
                        },
                        title=f"Race Calendar - {season}",
                        height=400
                    )
                    st.plotly_chart(simple_fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating visualization: {str(e)}")
            
            # Fallback to simple table display
            st.warning("Displaying data in table format instead")
        

        st.subheader("Circuit Information")
        
        # Create a selection for circuits
        try:
            circuit_options = []
            for i, race in enumerate(races):
                if hasattr(race, 'circuit') and hasattr(race.circuit, 'name'):
                    circuit_name = f"{race.circuit.name}, {race.circuit.country}"
                else:
                    circuit_name = f"Circuit {i+1}"
                circuit_options.append((i, circuit_name))
                
            selected_circuit_idx = st.selectbox(
                "Select Circuit",
                range(len(circuit_options)),
                format_func=lambda i: circuit_options[i][1]
            )
            
            selected_race = races[selected_circuit_idx]
            
            # Create columns for circuit info
            col1, col2 = st.columns(2)
            
            with col1:
                if hasattr(selected_race, 'circuit'):
                    circuit = selected_race.circuit
                    st.markdown(f"**Circuit**: {circuit.name}")
                    st.markdown(f"**Country**: {circuit.country}")
                    if hasattr(circuit, 'city') and circuit.city:
                        st.markdown(f"**City**: {circuit.city}")
                    if hasattr(circuit, 'length') and circuit.length:
                        st.markdown(f"**Length**: {circuit.length}")
                    if hasattr(circuit, 'corners') and circuit.corners:
                        st.markdown(f"**Corners**: {circuit.corners}")
            
            with col2:
                if hasattr(selected_race, 'circuit'):
                    circuit = selected_race.circuit
                    if hasattr(circuit, 'first_year') and circuit.first_year:
                        st.markdown(f"**First F1 Race**: {circuit.first_year}")
                    if hasattr(circuit, 'lap_record') and circuit.lap_record:
                        st.markdown(f"**Lap Record**: {circuit.lap_record}")
                        if hasattr(circuit, 'fastest_lap_driver_id') and circuit.fastest_lap_driver_id and hasattr(circuit, 'fastest_lap_year') and circuit.fastest_lap_year:
                            st.markdown(f"**Record Set By**: {circuit.fastest_lap_driver_id} ({circuit.fastest_lap_year})")
                    if hasattr(circuit, 'url') and circuit.url:
                        st.markdown(f"[More Information]({circuit.url})")
        except Exception as e:
            st.warning(f"Could not display circuit information: {str(e)}")
        
        # Display race calendar table
        st.subheader("Race Calendar Table")
        
        # Prepare a clean dataframe for display
        try:
            display_df = df.copy()
            
            # Select relevant columns
            if 'name' in display_df.columns and 'round' in display_df.columns:
                display_cols = ['round', 'name']
                
                if 'circuit.name' in display_df.columns:
                    display_cols.append('circuit.name')
                    
                if 'circuit.country' in display_df.columns:
                    display_cols.append('circuit.country')
                    
                # Add race date if available
                if 'schedule.race.date' in display_df.columns:
                    display_cols.append('schedule.race.date')
                    
                # Filter to only include columns that exist
                existing_cols = [col for col in display_cols if col in display_df.columns]
                display_df = display_df[existing_cols]
                
                # Rename columns for better display
                column_mapping = {
                    'round': 'Round',
                    'name': 'Grand Prix',
                    'circuit.name': 'Circuit',
                    'circuit.country': 'Country',
                    'schedule.race.date': 'Race Date'
                }
                
                # Only rename columns that exist
                rename_mapping = {k: v for k, v in column_mapping.items() if k in display_df.columns}
                display_df = display_df.rename(columns=rename_mapping)
            
            # Display the dataframe
            st.dataframe(display_df, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying race calendar table: {str(e)}")
            # Display the original dataframe as fallback
            st.dataframe(df, use_container_width=True)


def display_race_results(client: F1ApiClient, season: int) -> None:
    """
    Display race results visualization.
    
    Args:
        client (F1ApiClient): F1 API client instance.
        season (int): Season year to display.
    """
    st.header(f"Race Results - {season} Season")
    
    with st.spinner("Loading races..."):
        # Fetch races with caching
        races_data = cache_api_response(client.get_races, season)
        
        if not races_data:
            st.warning(f"No race data available for the {season} season.")
            return
        
        # Convert API data to our models
        api_type = 'f1api'
        races = [Race.from_api(item, api_type=api_type) for item in races_data]
        
        # Sort races by round if available
        if hasattr(races[0], 'round'):
            races.sort(key=lambda r: r.round)
        
        # Create race selection
        race_options = []
        for i, r in enumerate(races):
            race_name = r.name if hasattr(r, 'name') and r.name else f"Race {i+1}"
            race_id = f"{season}/{i+1}"
            race_options.append((race_id, f"Round {i+1}: {race_name}"))
        
        selected_race_idx = st.selectbox(
            "Select Race",
            range(len(race_options)),
            format_func=lambda i: race_options[i][1]
        )
        
        selected_race_id = race_options[selected_race_idx][0]
        selected_race = races[selected_race_idx]
        
        # Fetch race results
        with st.spinner(f"Loading results for {race_options[selected_race_idx][1]}..."):
            results_data = cache_api_response(client.get_race_results, selected_race_id)
            
            if not results_data:
                st.warning(f"No results available for {selected_race.name}.")
                return
            
            # Convert API data to our models
            results = [RaceResult.from_api(item) for item in results_data]
            
            # Convert to DataFrame for visualization
            df = convert_to_dataframe(results)
            
            # Sort by position
            if 'position' in df.columns:
                df = df.sort_values('position')
            
            # Create bar chart for positions
            if 'position' in df.columns and 'driver.name' in df.columns and 'driver.surname' in df.columns:
                # Create a column with full driver name
                df['driver_full_name'] = df.apply(lambda row: f"{row['driver.name']} {row['driver.surname']}", axis=1)
                
                fig = px.bar(
                    df,
                    x='position',
                    y='driver_full_name',
                    color='team.teamName' if 'team.teamName' in df.columns else None,
                    labels={
                        'position': 'Position',
                        'driver_full_name': 'Driver',
                        'team.teamName': 'Team'
                    },
                    title=f"Race Results - {selected_race.name}",
                    orientation='h',
                    height=600
                )
                
                # Customize layout
                fig.update_layout(
                    xaxis_title="Position",
                    yaxis_title="Driver",
                    legend_title="Team",
                    font=dict(size=12),
                    yaxis={'categoryorder': 'array', 'categoryarray': df.sort_values('position')['driver_full_name']}
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Display results table
            st.subheader("Race Results Table")
            
            # Display the dataframe directly
            st.dataframe(df, use_container_width=True)


def display_race_comparison(client: F1ApiClient, season: int) -> None:
    """
    Display race comparison visualization.
    
    Args:
        client (F1ApiClient): F1 API client instance.
        season (int): Season year to display.
    """
    st.header(f"Race Comparison - {season} Season")
    
    with st.spinner("Loading races..."):
        # Fetch races with caching
        races_data = cache_api_response(client.get_races, season)
        
        if not races_data:
            st.warning(f"No race data available for the {season} season.")
            return
        
        # Convert API data to our models
        api_type = 'f1api'
        races = [Race.from_api(item, api_type=api_type) for item in races_data]
        
        # Sort races by round if available
        if hasattr(races[0], 'round'):
            races.sort(key=lambda r: r.round)
        
        # Get list of drivers
        drivers_data = cache_api_response(client.get_drivers)
        
        if drivers_data:
            # Create driver selection
            driver_options = [(driver.get('driverId', ''), f"{driver.get('name', '')} {driver.get('surname', '')}") 
                             for driver in drivers_data]
            
            selected_driver_idx = st.selectbox(
                "Select Driver to Track Across Races",
                range(len(driver_options)),
                format_func=lambda i: driver_options[i][1]
            )
            
            selected_driver_id = driver_options[selected_driver_idx][0]
            selected_driver_name = driver_options[selected_driver_idx][1]
            
            # Create a message to inform the user
            st.info("This feature requires collecting race results for each race, which may take some time. The API might not support this functionality directly.")
            
            # Display a placeholder for future implementation
            st.subheader(f"{selected_driver_name}'s Performance Across Races")
            
            # Create a sample visualization with mock data
            race_names = [r.name if hasattr(r, 'name') and r.name else f"Race {i+1}" for i, r in enumerate(races)]
            mock_positions = [i % 10 + 1 for i in range(len(races))]
            mock_points = [(10 - (i % 10)) * 2 for i in range(len(races))]
            
            mock_df = pd.DataFrame({
                'Race': race_names,
                'Position': mock_positions,
                'Points': mock_points
            })
            
            # Position chart
            fig1 = px.line(
                mock_df,
                x='Race',
                y='Position',
                markers=True,
                title=f"{selected_driver_name}'s Positions (Mock Data)",
                height=400
            )
            
            fig1.update_layout(
                xaxis_title="Race",
                yaxis_title="Position",
                yaxis={'autorange': 'reversed'}
            )
            
            st.plotly_chart(fig1, use_container_width=True)
            
            # Points chart
            fig2 = px.line(
                mock_df,
                x='Race',
                y='Points',
                markers=True,
                title=f"{selected_driver_name}'s Points (Mock Data)",
                height=400
            )
            
            fig2.update_layout(
                xaxis_title="Race",
                yaxis_title="Points"
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            
            st.warning("Note: This is mock data for demonstration purposes. The actual data would require fetching results for each race individually.")
        else:
            st.warning("Could not load driver data for comparison.")
