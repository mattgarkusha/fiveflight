import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from api.flaskapi import app
from services import message_bus, unit_of_work
from adapters import orm

from config import Config

Config.TESTING = True


@pytest.fixture(scope='session')
def in_memory_db():
    orm.create_tables()

@pytest.fixture(scope='session', autouse=True)
def drop_all_tables_after_tests():
    yield
    orm.drop_tables()

@pytest.fixture
def client(in_memory_db):
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost'
    app.config['SERVER_PORT'] = 5000
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.secret_key = 'mysecret'

    with app.test_client() as client:
        with app.app_context():
            client.application.message_bus = message_bus
            yield client
