from typing import Iterable, Optional, Tuple


class Element:
    def __init__(self, id=None, container=None):
        if id is None:
            id = container.next_id()
        self.__id = id
    
    @property
    def id(self):
        return self.__id


class Container:
    def __init__(self, last_id: int = 0) -> None:
        self._next_id = last_id
        self._id_to_element_map = {}
        self._element_to_id_map = {}

    def values(self) -> Iterable[Element]:
        return self._id_to_element_map.values()
    
    def items(self) -> Iterable[Tuple[int, Element]]:
        return self._id_to_element_map.items()

    def __getitem__(self, id: int) -> Element:
        return self._id_to_element_map[id]
    
    def __contains__(self, element):
        return element in self._element_to_id_map

    def next_id(self) -> int:
        self._next_id += 1
        return self._next_id + 1

    def add(self, element: Element) -> int:
        if element.id < self._next_id:
            raise KeyError(f"New element's id cannot be less than {self._next_id}")

        if element.id in self._id_to_element_map and element is not self[element.id]:
            raise ValueError(f"An element with id={element.id} exists and is not {element}")

        self._id_to_element_map[element.id] = element
        self._element_to_id_map[element] = element.id
        if self._next_id <= element.id:
            self._next_id = element.id + 1
        return self._next_id

    def extend(self, *elements: Iterable[Element]) -> int:
        for element in elements:
            self.add(element)
        return self._next_id

    def remove(self, id: Optional[int] = None, element: Optional[Element] = None) -> None:
        if id is None:
            id = element.id
        element = self[id]
        del self._id_to_element_map[id]
        del self._element_to_id_map[element]

    def __str__(self):
        return f"{self.__class__.__name__}({self._id_to_element_map})"
