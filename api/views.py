from services import unit_of_work
from sqlalchemy import text

def get_aircraft(uow: unit_of_work):
    with uow:
        rows = uow.session.execute(
            text("""
            SELECT * from aircraft
            """)
        ).fetchall()
    return [dict(row._asdict()) for row in rows]

def get_aircraft_by_id(id: str, uow: unit_of_work):
    with uow:
        row = uow.session.execute(
            text(f"""
            SELECT * from aircraft WHERE id = {id}
            """)
        ).fetchone()
    return row._asdict()

def get_flight_plans(uow: unit_of_work):
    with uow:
        rows = uow.session.execute(
            text("""
            SELECT * from flight_plan
            """)
        ).fetchall()
    return [dict(row._asdict()) for row in rows]

def get_flight_plans_by_aircraft_id(aircraft_id: int, uow: unit_of_work):
    with uow:
        rows = uow.session.execute(
            text(f"""
            SELECT * from flight_plan WHERE aircraft_id = {aircraft_id}
            """)
        ).fetchall()
    return [dict(row._asdict()) for row in rows]

def get_flight_plans_by_tail_number(tail_number: str, uow: unit_of_work):
    with uow:
        rows = uow.session.execute(
            text(f"""
            SELECT * from flight_plan
            INNER JOIN aircraft ON aircraft.id = flight_plan.aircraft_id
            WHERE aircraft.tail_number = '{tail_number}'
            """)
        ).fetchall()
    return [dict(row._asdict()) for row in rows]