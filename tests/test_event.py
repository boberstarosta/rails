import unittest
from unittest.mock import Mock, call
from rail.event import Event


class EventTest(unittest.TestCase):
    def test_event(self):
        event = Event()
        callback = Mock()
        event.append(callback)
        callback.assert_not_called()
        event.fire("A", "B", c="C")
        callback.assert_called_once_with("A", "B", c="C")
