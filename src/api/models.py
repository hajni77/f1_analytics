"""
Data models for F1 API responses.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Team:
    """
    Represents a Formula 1 team (constructor).
    """
    teamId: str
    teamName: str
    country: str
    firstAppareance: int
    constructorsChampionships: int
    driversChampionships: int
    url: Optional[str] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'Team':
        """
        Create a Team instance from API data.
        
        Args:
            data (Dict[str, Any]): API response data for a team.
            
        Returns:
            Team: A Team instance.
        """
        return cls(
            teamId=data.get('teamId', ''),
            teamName=data.get('teamName', ''),
            country=data.get('country', ''),
            firstAppareance=data.get('firstAppareance', 0),
            constructorsChampionships=data.get('constructorsChampionships', 0),
            driversChampionships=data.get('driversChampionships', 0),
            url=data.get('url')
        )

@dataclass
class Driver:
    """
    Represents a Formula 1 driver.
    """
    shortName: str
    number: str
    name: str
    surname: str
    nationality: str
    team: Optional[Team] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'Driver':
        """
        Create a Driver instance from API data.
        
        Args:
            data (Dict[str, Any]): API response data for a driver.
            
        Returns:
            Driver: A Driver instance.
        """
        # Create Team instance if team data is available
        team = None
        if 'team' in data and data['team']:
            team = Team.from_api(data['team'])
        
        return cls(
            shortName=data.get('shortName', ''),
            name=data.get('name', ''),
            surname=data.get('surname', ''),
            nationality=data.get('nationality', ''),
            number=data.get('number', ''),
            team=team
        )

@dataclass
class Circuit:
    """
    Represents a Formula 1 circuit.
    """
    circuit_id: str
    name: str
    country: str
    city: Optional[str] = None
    length: Optional[str] = None
    lap_record: Optional[str] = None
    first_year: Optional[int] = None
    corners: Optional[int] = None
    fastest_lap_driver_id: Optional[str] = None
    fastest_lap_team_id: Optional[str] = None
    fastest_lap_year: Optional[int] = None
    url: Optional[str] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'Circuit':
        """
        Create a Circuit instance from API data.
        
        Args:
            data (Dict[str, Any]): API response data for a circuit.
            
        Returns:
            Circuit: A Circuit instance.
        """
        # Handle different API formats
        if isinstance(data.get('country'), dict):
            country = data.get('country', {}).get('name', '')
        else:
            country = data.get('country', '')
            
        return cls(
            circuit_id=data.get('circuitId', ''),
            name=data.get('circuitName', '') or data.get('name', ''),
            country=country,
            city=data.get('city', None),
            length=data.get('circuitLength', None),
            lap_record=data.get('lapRecord', None),
            first_year=data.get('firstParticipationYear', None),
            corners=data.get('corners', None),
            fastest_lap_driver_id=data.get('fastestLapDriverId', None),
            fastest_lap_team_id=data.get('fastestLapTeamId', None),
            fastest_lap_year=data.get('fastestLapYear', None),
            url=data.get('url', None)
        )

@dataclass
class SessionSchedule:
    """
    Represents the schedule for a race weekend session.
    """
    date: Optional[datetime] = None
    time: Optional[str] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'SessionSchedule':
        """
        Create a SessionSchedule instance from API data.
        
        Args:
            data (Dict[str, Any]): API response data for a session schedule.
            
        Returns:
            SessionSchedule: A SessionSchedule instance.
        """
        date_str = data.get('date', '')
        date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else None
        
        return cls(
            date=date,
            time=data.get('time', None)
        )

@dataclass
class RaceSchedule:
    """
    Represents the complete schedule for a race weekend.
    """
    race: SessionSchedule
    qualy: SessionSchedule
    fp1: SessionSchedule
    fp2: SessionSchedule
    fp3: SessionSchedule
    sprint_qualy: Optional[SessionSchedule] = None
    sprint_race: Optional[SessionSchedule] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'RaceSchedule':
        """
        Create a RaceSchedule instance from API data.
        
        Args:
            data (Dict[str, Any]): API response data for a race schedule.
            
        Returns:
            RaceSchedule: A RaceSchedule instance.
        """
        return cls(
            race=SessionSchedule.from_api(data.get('race', {})),
            qualy=SessionSchedule.from_api(data.get('qualy', {})),
            fp1=SessionSchedule.from_api(data.get('fp1', {})),
            fp2=SessionSchedule.from_api(data.get('fp2', {})),
            fp3=SessionSchedule.from_api(data.get('fp3', {})),
            sprint_qualy=SessionSchedule.from_api(data.get('sprintQualy', {})),
            sprint_race=SessionSchedule.from_api(data.get('sprintRace', {}))
        )

@dataclass
class FastLap:
    """
    Represents the fastest lap information for a race.
    """
    time: Optional[str] = None
    driver_id: Optional[str] = None
    team_id: Optional[str] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'FastLap':
        """
        Create a FastLap instance from API data.
        
        Args:
            data (Dict[str, Any]): API response data for a fast lap.
            
        Returns:
            FastLap: A FastLap instance.
        """
        return cls(
            time=data.get('fast_lap', None),
            driver_id=data.get('fast_lap_driver_id', None),
            team_id=data.get('fast_lap_team_id', None)
        )

@dataclass
class Championship:
    """
    Represents a Formula 1 championship season.
    """
    championship_id: str
    name: str
    year: int
    url: Optional[str] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'Championship':
        """
        Create a Championship instance from API data.
        
        Args:
            data (Dict[str, Any]): API response data for a championship.
            
        Returns:
            Championship: A Championship instance.
        """
        return cls(
            championship_id=data.get('championshipId', ''),
            name=data.get('championshipName', ''),
            year=data.get('year', 0),
            url=data.get('url', None)
        )

@dataclass
class Race:
    """
    Represents a Formula 1 race.
    """
    id: str
    name: str
    round: int
    season: int
    circuit: Circuit
    championship_id: Optional[str] = None
    schedule: Optional[RaceSchedule] = None
    laps: Optional[int] = None
    url: Optional[str] = None
    fast_lap: Optional[FastLap] = None
    winner_driver_id: Optional[str] = None
    winner_team_id: Optional[str] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'Race':
        """
        Create a Race instance from API data.
        
        Args:
            data (Dict[str, Any]): API response data for a race.
            api_type (str): The type of API the data is from ('f1api' or 'f1connect').
            
        Returns:
            Race: A Race instance.
        """
        # Handle f1connectapi.vercel.app format
        circuit = Circuit.from_api(data.get('circuit', {}))
            
        race_date = None
        schedule = None
        if 'schedule' in data:
            schedule = RaceSchedule.from_api(data.get('schedule', {}))
        race_date = schedule.race.date
            
        fast_lap = None
        if 'fast_lap' in data:
            fast_lap = FastLap.from_api(data.get('fast_lap', {}))
            
        return cls(
            id=data.get('raceId', ''),
                name=data.get('raceName', '') or f"Round {data.get('round', 0)}",
                round=data.get('round', 0),
                season=data.get('season', 0),
                circuit=circuit,
                championship_id=data.get('championshipId', None),
                schedule=schedule,
                laps=data.get('laps', None),
                url=data.get('url', None),
                fast_lap=fast_lap,
                winner_driver_id=data.get('winner', None),
                winner_team_id=data.get('teamWinner', None)
            )


@dataclass
class DriverStanding:
    """
    Represents a driver's standing in the championship.
    """
    classificationId: int
    driverId: str
    teamId: str
    position: int
    points: float
    wins: int
    driver: Optional[Driver] = None
    team: Optional[Team] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'DriverStanding':
        """
        Create a DriverStanding instance from API data.
        
        Args:
            data (Dict[str, Any]): API response data for a driver standing.
            
        Returns:
            DriverStanding: A DriverStanding instance.
        """
        # Create Driver instance if driver data is available
        driver = None
        if 'Driver' in data and data['Driver']:
            driver = Driver.from_api(data['Driver'])
        
        # Create Team instance if team data is available
        team = None
        if 'Constructor' in data and data['Constructor']:
            team = Team.from_api(data['Constructor'])
        
        return cls(
            position=data.get('position', 0),
            points=data.get('points', 0.0),
            wins=data.get('wins', 0),
            driverId=data.get('driverId', ''),
            teamId=data.get('teamId', ''),
            classificationId=data.get('classificationId', 0),
            driver=driver,
            team=team
        )


@dataclass
class TeamStanding:
    """
    Represents a team's standing in the championship.
    """
    classificationId: int
    teamId: str
    position: int
    points: float
    wins: int
    team: Optional[Team] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'TeamStanding':
        """
        Create a TeamStanding instance from API data.
        
        Args:
            data (Dict[str, Any]): API response data for a team standing.
            
        Returns:
            TeamStanding: A TeamStanding instance.
        """
        # Create Team instance if team data is available
        team = None
        if 'Constructor' in data and data['Constructor']:
            team = Team.from_api(data['Constructor'])
        
        return cls(
            position=data.get('position', 0),
            points=data.get('points', 0.0),
            wins=data.get('wins', 0),
            teamId=data.get('teamId', ''),
            classificationId=data.get('classificationId', 0),
            team=team
        )


@dataclass
class RaceResult:
    """
    Represents a driver's result in a race.
    """
    position: int
    points: float
    status: str
    driver: Optional[Driver] = None
    team: Optional[Team] = None
    lap_time: Optional[str] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'RaceResult':
        """
        Create a RaceResult instance from API data.
        
        Args:
            data (Dict[str, Any]): API response data for a race result.
            
        Returns:
            RaceResult: A RaceResult instance.
        """
        # Create Driver instance if driver data is available
        driver = None
        if 'Driver' in data and data['Driver']:
            driver = Driver.from_api(data['Driver'])
        
        # Create Team instance if team data is available
        team = None
        if 'Constructor' in data and data['Constructor']:
            team = Team.from_api(data['Constructor'])
        
        return cls(
            position=data.get('position', 0),
            points=data.get('points', 0.0),
            status=data.get('status', ''),
            lap_time=data.get('lapTime'),
            driver=driver,
            team=team
        )

@dataclass
class Season:
    """
    Represents a Formula 1 season.
    """
    year: int
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'Season':
        """
        Create a Season instance from API data.
        
        Args:
            data (Dict[str, Any]): API response data for a season.
            
        Returns:
            Season: A Season instance.
        """
        return cls(
            year=data.get('year', 0)
        )