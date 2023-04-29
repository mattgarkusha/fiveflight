from domain.model import Aircraft, FlightPlan
from typing import List, Set
from abc import ABC, abstractmethod
from datetime import datetime

class AbstractRepository(ABC):
    def __init__(self):
        self.seen = set()
    
    @abstractmethod
    def get_all(self, sort_field=None, sort_descending=False):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id):
        raise NotImplementedError

    @abstractmethod
    def create(self, aircraft: Aircraft):
        raise NotImplementedError

    @abstractmethod
    def update(self, aircraft: Aircraft):
        raise NotImplementedError

    @abstractmethod
    def delete(self, aircraft: Aircraft):
        raise NotImplementedError

class AircraftRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session
    
    def get_all(self) -> List[Aircraft]:
        query = self.session.query(Aircraft)
        aircrafts = query.all()
        for aircraft in aircrafts:
            self.seen.add(aircraft)
        return aircrafts

    def get_by_id(self, id) -> Aircraft:
        aircraft = self.session.get(Aircraft, id)
        if aircraft:
            self.seen.add(aircraft)
        return aircraft

    def create(self, aircraft: Aircraft) -> Aircraft:
        now = datetime.now()
        aircraft.created_at = now
        aircraft.updated_at = now
        self.session.add(aircraft)
        self.session.commit()
        if aircraft:
            self.seen.add(aircraft)
        return aircraft

    def update(self, aircraft: Aircraft) -> Aircraft:
        now = datetime.now()
        aircraft.updated_at = now
        self.session.commit()
        if aircraft:
            self.seen.add(aircraft)
        return aircraft

    def delete(self, id) -> Aircraft:
        aircraft = self.get_by_id(id)
        self.session.delete(aircraft)
        self.session.commit()
        if aircraft:
            self.seen.add(aircraft)
        return aircraft


class FlightPlanRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session
    
    def get_all(self) -> List[FlightPlan]:
        query = self.session.query(FlightPlan)
        flight_plans = query.all()
        for flight_plan in flight_plans:
            self.seen.add(flight_plan)
        return flight_plans

    def get_by_id(self, id) -> FlightPlan:
        flight_plan = self.session.get(FlightPlan, id)
        if flight_plan:
            self.seen.add(flight_plan)
        return flight_plan
    
    def get_by_aircraft_tail_number(self, tail_number: str) -> List[FlightPlan]:
        query = self.session.query(FlightPlan).join(Aircraft).filter(Aircraft.tail_number == tail_number)
        flight_plans = query.all()
        for flight_plan in flight_plans:
            self.seen.add(flight_plan)
        return flight_plans
    
    def get_by_aircraft_id(self, id) -> List[FlightPlan]:
        query = self.session.query(FlightPlan).join(Aircraft).filter(Aircraft.id == id)
        flight_plans = query.all()
        for flight_plan in flight_plans:
            self.seen.add(flight_plan)
        return flight_plans

    def create(self, flight_plan: FlightPlan) -> FlightPlan:
        now = datetime.now()
        flight_plan.created_at = now
        flight_plan.updated_at = now
        self.session.add(flight_plan)
        self.session.commit()
        if flight_plan:
            self.seen.add(flight_plan)
        return flight_plan

    def update(self, flight_plan: FlightPlan) -> FlightPlan:
        now = datetime.now()
        flight_plan.updated_at = now
        self.session.commit()
        if flight_plan:
            self.seen.add(flight_plan)
        return flight_plan

    def delete(self, id) -> FlightPlan:
        flight_plan = self.get_by_id(id)
        self.session.delete(flight_plan)
        self.session.commit()
        if flight_plan:
            self.seen.add(flight_plan)
        return flight_plan