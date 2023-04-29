from abc import ABC
from dataclasses import dataclass
from typing import Optional

class Command(ABC):
    pass


@dataclass
class AddAircraftCommand(Command):
    name: str
    make: str
    model: str
    tail_number: str


@dataclass
class EditAircraftCommand(Command):
    id: int
    name: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    tail_number: Optional[str] = None


@dataclass
class DeleteAircraftCommand(Command):
    id: int


@dataclass
class GetAircraftByIdCommand(Command):
    id: int

@dataclass
class AddFlightPlanCommand(Command):
    aircraft_id: int
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    notes: Optional[str] = None

@dataclass
class EditFlightPlanCommand(Command):
    id: int
    aircraft_id: Optional[int] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure_time: Optional[str] = None
    arrival_time: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class DeleteFlightPlanCommand(Command):
    id: int

@dataclass
class GetFlightPlanByIdCommand(Command):
    id: int

@dataclass
class GetFlightPlansByAircraftCommand(Command):
    aircraft_id: int