from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable, Dict, List, Type, Union

from domain import commands, events
from services import handlers

if TYPE_CHECKING:
    from . import unit_of_work

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: Dict[Type[events.Event], List[Callable]],
        command_handlers: Dict[Type[commands.Command], Callable],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers

    def handle(self, message: Message):
        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                self.handle_event(message)
            elif isinstance(message, commands.Command):
                self.handle_command(message)
            else:
                raise Exception(f"{message} was not an Event or Command")
        return self.uow.collect_new_events()

    def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception("Exception handling event %s", event)
                continue

    def handle_command(self, command: commands.Command):
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            handler(command)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception("Exception handling command %s", command)
            raise


EVENT_HANDLERS = {
    events.AircraftAdded: [handlers.add_aircraft],
    events.AircraftDeleted: [handlers.delete_aircraft],
    events.AircraftEdited: [handlers.edit_aircraft],
    events.FlightPlanAdded: [handlers.add_flight_plan],
    events.FlightPlanEdited: [handlers.update_flight_plan],
    events.FlightPlanDeleted: [handlers.delete_flight_plan],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.AddAircraftCommand: handlers.add_aircraft,
    commands.DeleteAircraftCommand: handlers.delete_aircraft,
    commands.EditAircraftCommand: handlers.edit_aircraft,
    commands.AddFlightPlanCommand: handlers.add_flight_plan,
    commands.EditFlightPlanCommand: handlers.update_flight_plan,
    commands.DeleteFlightPlanCommand: handlers.delete_flight_plan,
}  # type: Dict[Type[commands.Command], Callable]