# F1 Analytics

A Streamlit application that visualizes Formula 1 data using the free f1api.dev API.

## Features

- Real-time F1 data visualization
- Historical race statistics
- Driver and team performance comparisons
- Interactive charts and graphs
- No API key required

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   streamlit run src/app.py
   ```

## Project Structure

```
f1-analytics/
├── requirements.txt    # Project dependencies
├── README.md          # Project documentation
├── PLANNING.md        # Project architecture and goals
├── TASK.md            # Task tracking
└── src/               # Source code
    ├── app.py         # Main Streamlit application
    ├── api/           # API integration with f1api.dev
    ├── components/    # UI components
    ├── utils/         # Utility functions
    └── visualizations/ # Data visualization modules
```

## API

This application uses the free [f1api.dev](https://f1api.dev/docs) API, which provides comprehensive Formula 1 data without requiring an API key.

## License

MIT
