from __future__ import annotations
from typing import TYPE_CHECKING, List
from datetime import datetime

from domain import commands, model

if TYPE_CHECKING:
    from . import unit_of_work

def add_aircraft(
    cmd: commands.AddAircraftCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        aircraft = model.Aircraft(
            id=None,
            name=cmd.name,
            make=cmd.make,
            model=cmd.model,
            tail_number=cmd.tail_number,
            created_at=None,
            updated_at=None
        )
        result = uow.aircraft_repo.create(aircraft)
        uow.commit()
        return result.to_dict()


def delete_aircraft(
    cmd: commands.DeleteAircraftCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        result = uow.aircraft_repo.delete(cmd.id)
        return result.to_dict()


def edit_aircraft(
    cmd: commands.EditAircraftCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        aircraft = uow.aircraft_repo.get_by_id(cmd.id)
        if aircraft is None:
            return None
        aircraft.name = cmd.name
        aircraft.make = cmd.make
        aircraft.model = cmd.model
        aircraft.tail_number = cmd.tail_number
        result = uow.aircraft_repo.update(aircraft)
        return result.to_dict()
    
def add_flight_plan(
    cmd: commands.AddFlightPlanCommand, uow: unit_of_work.AbstractUnitOfWork
) -> dict:
    with uow:
        flight_plan = model.FlightPlan(
            id=None,
            aircraft_id=cmd.aircraft_id,
            origin=cmd.origin,
            destination=cmd.destination,
            departure_time=datetime.fromisoformat(cmd.departure_time),
            arrival_time=datetime.fromisoformat(cmd.arrival_time),
            created_at=None,
            updated_at=None,
        )
        result = uow.flight_plan_repo.create(flight_plan)
        uow.commit()
        return result.to_dict()


def delete_flight_plan(
    cmd: commands.DeleteFlightPlanCommand, uow: unit_of_work.AbstractUnitOfWork
) -> dict:
    with uow:
        result = uow.flight_plan_repo.delete(cmd.id)
        return result.to_dict()


def update_flight_plan(
    cmd: commands.EditFlightPlanCommand, uow: unit_of_work.AbstractUnitOfWork
) -> dict:
    with uow:
        flight_plan = uow.flight_plan_repo.get_by_id(cmd.id)
        if flight_plan is None:
            return None
        flight_plan.aircraft_id = cmd.aircraft_id
        flight_plan.origin = cmd.origin
        flight_plan.destination = cmd.destination
        flight_plan.departure_time = datetime.fromisoformat(cmd.departure_time)
        flight_plan.arrival_time = datetime.fromisoformat(cmd.arrival_time)
        result = uow.flight_plan_repo.update(flight_plan)
        return result.to_dict()


def get_flight_plan_by_id(
    cmd: commands.GetFlightPlanByIdCommand, uow: unit_of_work.AbstractUnitOfWork
) -> dict:
    with uow:
        flight_plan = uow.flight_plan_repo.get_by_id(cmd.id)
        if flight_plan is None:
            return None
        return flight_plan.to_dict()


def get_flight_plans_by_aircraft_id(
    cmd: commands.GetFlightPlansByAircraftCommand, uow: unit_of_work.AbstractUnitOfWork
) -> List[dict]:
    with uow:
        flight_plans = uow.flight_plan_repo.get_by_aircraft_id(cmd.aircraft_id)
        return [flight_plan.to_dict() for flight_plan in flight_plans]