from typing import Text
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    DateTime,
    event,
    ForeignKey,
    create_engine,
    inspect
)

from sqlalchemy.orm import registry, relationship
from sqlalchemy.sql import func

from domain.model import Aircraft, FlightPlan
from config import Config

mapper_registry = registry()


if Config.TESTING:
    engine = create_engine("sqlite:///:memory:", echo=True)
else:
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

aircraft = Table(
    "aircraft",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("tail_number", String(255), unique=True),
    Column("make", String(255)),
    Column("model", String(255)),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)

flight_plan = Table(
    "flight_plan",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("aircraft_id", Integer, ForeignKey("aircraft.id"), nullable=False),
    Column("origin", String(255)),
    Column("destination", String(255)),
    Column("departure_time", DateTime(timezone=True)),
    Column("arrival_time", DateTime(timezone=True)),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
)

def start_mappers():
    print("**** starting mappers ****")
    flights_mapper = mapper_registry.map_imperatively(
        Aircraft,
        aircraft,
        properties={
            "flight_plans": relationship(
                "FlightPlan", back_populates="aircraft", cascade="all, delete-orphan"
            )
        },
    )

    flight_plans_mapper = mapper_registry.map_imperatively(
        FlightPlan,
        flight_plan,
        properties={
            "aircraft": relationship("Aircraft", back_populates="flight_plans"),
        },
    )

def create_tables():
    with engine.connect() as conn:
        if not inspect(engine).has_table("aircraft"):
            print('**** creating tables ****')
            mapper_registry.metadata.create_all(engine)
            print('**** tables created ****')

def drop_tables():
    print('**** dropping tables ****')
    mapper_registry.metadata.drop_all(engine)
    print('**** tables dropped ****')

@event.listens_for(Aircraft, "load")
def receive_load(aircraft, _):
    aircraft.events = []

@event.listens_for(FlightPlan, "load")
def receive_load(flight_plan, _):
    flight_plan.events = []