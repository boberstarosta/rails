import unittest
from unittest.mock import Mock
from rail.events import Event


class EventTest(unittest.TestCase):
    def test_sanity(self):
        event = Event()
        mock_function = Mock()
        args = ("A", "B")
        kwargs = {"C": 1, "D": 2}
        event.fire(*args, **kwargs)
        mock_function.assert_not_called()
        event.append(mock_function)
        event.fire(*args, **kwargs)
        mock_function.assert_called_once_with(*args, **kwargs)
