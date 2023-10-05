from abc import ABC, abstractmethod
from queue import Queue
from typing import List, Dict
import logging


class Event:
    def __init__(self, event_type: str, occurred_on, attributes: Dict):
        self.event_type = event_type
        self.occurred_on = occurred_on
        self.attributes = attributes


class EventStore(ABC):
    @abstractmethod
    def get_events(self, timestamp) -> List[Event]:
        pass


class QueueEventStore(EventStore):
    def __init__(self, match_event_queue: Queue):
        self._match_event_queue = match_event_queue
        self._events = []  # type: List[Event]

    def _update_events(self):
        while not self._match_event_queue.empty():
            event = self._match_event_queue.get()
            logging.debug("Received event: {}".format(event))
            event_type = event["eventType"]
            event_attributes = event["eventAttributes"]
            occurred_on = event["occurredOn"]

            if event_type == "SportingEventCreated":
                self._events = []

            if event_type == "ObservationRemoved":
                event_to_remove_id = event_attributes["id"]
                indexes_to_remove = []
                for i, event_ in enumerate(self._events):
                    event_attributes_ = event_.attributes
                    if event_attributes_.get("id") == event_to_remove_id:
                        indexes_to_remove.append(i)
                        break

                for i in reversed(indexes_to_remove):
                    # print("removing", event_to_remove_id)
                    # print(self._events[i])
                    del self._events[i]
            else:
                self._events.append(
                    Event(
                        event_type=event_type,
                        attributes=event_attributes,
                        occurred_on=occurred_on,  # datetime.fromtimestamp(float(event_attributes['time']), timezone.utc) if 'time' in event_attributes else occurred_on
                    )
                )

    def get_events(self, timestamp=None) -> List[Event]:
        self._update_events()

        def _filter(event: Event):
            if event.event_type == "SportingEventCreated":
                return True
            return event.occurred_on <= timestamp

        if timestamp:
            return list(filter(_filter, self._events))
        else:
            return self._events


class StaticEventStore(EventStore):
    def __init__(self, events: List[Dict]):
        self._events = [
            Event(
                event_type=event["eventType"],
                attributes=event["eventAttributes"],
                occurred_on=event["occurredOn"],
            )
            for event in events
        ]

    def get_events(self, timestamp) -> List[Event]:
        def _filter(event: Event):
            if event.event_type == "SportingEventCreated":
                return True
            return event.occurred_on <= timestamp

        return list(filter(_filter, self._events))
