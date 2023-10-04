from dataclasses import dataclass


@dataclass
class Team:
    team_id: str
    name: str
    short_code: str
    primary_color: str
    secondary_color: str


@dataclass
class MatchConfig:
    home_team: Team
    away_team: Team
    period_count: int
