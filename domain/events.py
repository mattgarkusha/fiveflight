from abc import ABC
from dataclasses import dataclass
from typing import List

from domain.model import Aircraft, FlightPlan


class Event(ABC):
    pass

@dataclass
class AircraftAdded(Event):
    id: int
    make: str
    model: str
    tail_number: str
    created_at: str
    updated_at: str


@dataclass
class AircraftEdited(Event):
    id: int
    make: str
    model: str
    tail_number: str
    updated_at: str


@dataclass
class sListed(Event):
    aircraft: List[Aircraft]

@dataclass
class AircraftDeleted(Event):
    aircraft: Aircraft

@dataclass
class AircraftGottenByID(Event):
    aircraft: Aircraft

@dataclass
class FlightPlanAdded(Event):
    id: int
    departure: str
    destination: str
    distance: float
    estimated_time_enroute: float
    aircraft: Aircraft
    created_at: str
    updated_at: str

@dataclass
class FlightPlanEdited(Event):
    id: int
    departure: str
    destination: str
    distance: float
    estimated_time_enroute: float
    aircraft: Aircraft
    updated_at: str

@dataclass
class FlightPlanDeleted(Event):
    flight_plan: FlightPlan

@dataclass
class FlightPlansListed(Event):
    flight_plans: List[FlightPlan]

@dataclass
class FlightPlansByAircraftListed(Event):
    aircraft: Aircraft
    flight_plans: List[FlightPlan]