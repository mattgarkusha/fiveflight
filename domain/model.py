from datetime import datetime
from dataclasses import dataclass

@dataclass(unsafe_hash=True)
class Aircraft:
    id: int
    name: str
    make: str
    model: str
    tail_number: str
    # flight_plans: List[FlightPlan]
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        id: int,
        name: str,
        make: str,
        model: str,
        tail_number: str,
        # flight_plans: List[FlightPlan],
        created_at: datetime,
        updated_at: datetime
    ) -> None:
        self.id = id
        self.name = name
        self.make = make
        self.model = model
        self.tail_number = tail_number
        # self.flight_plans = flight_plans
        self.created_at = created_at
        self.updated_at = updated_at
        self.events = []

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'model': self.model,
            'make': self.make,
            'tail_number': self.tail_number,
            # 'flight_plans': [fp.to_dict() for fp in self.flight_plans],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

@dataclass(unsafe_hash=True)
class FlightPlan:
    id: int
    aircraft_id: int
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    created_at: datetime
    updated_at: datetime

    def __init__(
        self,
        id: int,
        aircraft_id: int,
        origin: str,
        destination: str,
        departure_time: datetime,
        arrival_time: datetime,
        created_at: datetime,
        updated_at: datetime,
    ) -> None:
        self.id = id
        self.aircraft_id = aircraft_id
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.created_at = created_at
        self.updated_at = updated_at
        self.events = []

    def to_dict(self):
        return {
            'id': self.id,
            'aircraft_id': self.aircraft_id,
            'origin': self.origin,
            'destination': self.destination,
            'departure_time': self.departure_time.isoformat(),
            'arrival_time': self.arrival_time.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }