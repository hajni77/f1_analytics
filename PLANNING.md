# F1 Analytics - Project Planning

## Project Overview
F1 Analytics is a Streamlit application that fetches Formula 1 data using the free f1api.dev API and visualizes it through interactive charts and dashboards. The application aims to provide insights into F1 races, drivers, teams, and historical statistics.

## Architecture

### Technology Stack
- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **API Integration**: f1api.dev (free API)
- **Configuration**: python-dotenv

### Directory Structure
```
f1-analytics/
├── requirements.txt    # Project dependencies
├── README.md          # Project documentation
├── PLANNING.md        # Project architecture and goals
├── TASK.md            # Task tracking
└── src/               # Source code
    ├── app.py         # Main Streamlit application
    ├── api/           # API integration with f1api.dev
    │   ├── __init__.py
    │   ├── client.py  # F1 API client
    │   └── models.py  # Data models
    ├── components/    # UI components
    │   ├── __init__.py
    │   ├── sidebar.py # Sidebar navigation
    │   └── header.py  # Header components
    ├── utils/         # Utility functions
    │   ├── __init__.py
    │   └── helpers.py # Helper functions
    └── visualizations/ # Data visualization modules
        ├── __init__.py
        ├── drivers.py  # Driver visualizations
        ├── teams.py    # Team visualizations
        ├── races.py    # Race visualizations
        └── seasons.py  # Season visualizations
```

## Code Style and Conventions
- Use Python type hints for all functions and methods
- Follow PEP8 style guidelines
- Format code with black
- Use docstrings for all functions, classes, and modules (Google style)
- Maximum file length: 400 lines
- Organize imports alphabetically

## Data Flow
1. User selects visualization options in the Streamlit UI
2. Application fetches data from f1api.dev API
3. Data is processed and transformed using Pandas
4. Visualizations are generated using Plotly
5. Results are displayed in the Streamlit UI

## Features and Milestones

### Phase 1: Basic Setup and Data Fetching
- Set up project structure
- Implement F1 API client for f1api.dev
- Create basic Streamlit UI
- Implement data fetching and caching

### Phase 2: Core Visualizations
- Driver standings visualization
- Team standings visualization
- Race results visualization
- Season comparison visualization

### Phase 3: Advanced Features
- Historical data analysis
- Prediction models
- Custom data exports
- User preferences and settings

## Testing Strategy
- Unit tests for API client and data processing functions
- Integration tests for visualization components
- End-to-end tests for the complete application flow
