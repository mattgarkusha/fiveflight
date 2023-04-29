from adapters.repository import AircraftRepository, FlightPlanRepository
from abc import ABC, abstractmethod
from typing import  List
from domain.events import Event

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config


class AbstractUnitOfWork(ABC):
    aircraft_repo: AircraftRepository
    flight_plan_repo: FlightPlanRepository
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    def collect_new_events(self):
        for aircraft in self.aircraft_repo.seen:
            while aircraft.events:
                yield aircraft.events.pop(0)
        
        for flight_plans in self.flight_plan_repo.seen:
            while flight_plans.events:
                yield flight_plans.events.pop(0)

    @abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

    

    def collect_new_events(self):
        for aircraft in self.aircraft_repo.seen:
            while aircraft.events:
                yield aircraft.events.pop(0)

        for flight_plans in self.flight_plan_repo.seen:
            while flight_plans.events:
                yield flight_plans.events.pop(0)



DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        Config.SQLALCHEMY_DATABASE_URI,
        isolation_level="READ UNCOMMITTED",
    )
)

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.aircraft_repo = AircraftRepository(self.session)
        self.flight_plan_repo = FlightPlanRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def collect_new_events(self) -> List[Event]:
        return [] 