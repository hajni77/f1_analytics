"""
F1 API Client module for interacting with the f1api.dev API.
"""
import os
from typing import Dict, List, Any, Optional
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class F1ApiClient:
    """
    Client for interacting with the F1 API using f1api.dev.
    
    This client provides methods to fetch various F1 data including 
    drivers, teams, races, and seasons from the free f1api.dev API.
    """
    
    BASE_URL = "https://f1api.dev"

    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the F1 API client.
        
        Args:
            api_key (Optional[str]): Not used for f1api.dev as it's a free API.
       
        """
        
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    
    def get_current_season(self) -> Dict[str, Any]:
        """
        Get data for the current F1 season.
        
        Returns:
            Dict[str, Any]: Current season data.
        """
        response = self.session.get(f"{self.BASE_URL}/api/current/drivers-championship")
        response.raise_for_status()
        return response.json()
    
    def get_driver_standings(self, season: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get driver standings for a specific season.
        
        Args:
            season (Optional[int]): Season year. If not provided, uses current season.
            
        Returns:
            List[Dict[str, Any]]: List of driver standings.
        """



        if season:
            url = f"{self.BASE_URL}/api/{season}/drivers-championship"
        else:
            url = f"{self.BASE_URL}/api/current/drivers-championship"
            
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("drivers_championship", [])
    
    def get_constructor_standings(self, season: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get constructor (team) standings for a specific season.
        
        Args:
            season (Optional[int]): Season year. If not provided, uses current season.
            
        Returns:
            List[Dict[str, Any]]: List of constructor standings.
        """


        if season:
            url = f"{self.BASE_URL}/api/{season}/constructors-championship"
        else:
            url = f"{self.BASE_URL}/api/current/constructors-championship"
            
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("constructors_championship", [])
    
    def get_race_results(self, race_id: str) -> List[Dict[str, Any]]:
        """
        Get results for a specific race.
        
        Args:
            race_id (str): ID of the race in format "year/round" (e.g., "2023/1")
                           or race_id for f1connectapi.
            
        Returns:
            List[Dict[str, Any]]: List of race results.
        """

        year, round_num = race_id.split('/')
        url = f"{self.BASE_URL}/api/{year}/{round_num}"
            
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("race", [])
    
    def get_races(self, season: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all races for a specific season.
        
        Args:
            season (Optional[int]): Season year. If not provided, uses current season.
            
        Returns:
            List[Dict[str, Any]]: List of races.
        """

        if season:
            url = f"{self.BASE_URL}/api/{season}"
        else:
            url = f"{self.BASE_URL}/api/current"
            
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("race", [])
    
    def get_driver_info(self, driver_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific driver.
        
        Args:
            driver_id (str): ID of the driver.
            
        Returns:
            Dict[str, Any]: Driver information.
        """

        response = self.session.get(f"{self.BASE_URL}/api/{driver_id}")
        response.raise_for_status()
        return response.json()
    
    def get_drivers(self) -> List[Dict[str, Any]]:
        """
        Get list of drivers.
        
        Returns:
            List[Dict[str, Any]]: List of drivers.
        """
        response = self.session.get(f"{self.BASE_URL}/api/drivers")
        response.raise_for_status()
        return response.json().get("drivers", [])
    
    def get_team_info(self, team_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific team.
        
        Args:
            team_id (str): ID of the team.
            
        Returns:
            Dict[str, Any]: Team information.
        """

        response = self.session.get(f"{self.BASE_URL}/api/{team_id}")
            
        response.raise_for_status()
        return response.json()
    
    def get_championship_info(self, year: Optional[int] = None) -> Dict[str, Any]:
        """
        Get information about a specific championship.
        
        Args:
            year (Optional[int]): Year of the championship. If not provided, uses current season.
            
        Returns:
            Dict[str, Any]: Championship information.
        """

        if year:
            url = f"{self.BASE_URL}/api/{year}"
        else:
            url = f"{self.BASE_URL}/api/current"
            
        response = self.session.get(url)
        response.raise_for_status()
        return response.json().get("championship", {})
