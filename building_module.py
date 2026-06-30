# building_module.py

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Room:
    room_id: str
    name: str
    room_type: str
    floor: int
    capacity: int
    area_m2: float


@dataclass
class Connection:
    from_room: str
    to_room: str
    distance_m: float
    bidirectional: bool = True


class Building:
    def __init__(self, building_name: str):
        self.building_name = building_name
        self.rooms: Dict[str, Room] = {}
        self.connections: List[Connection] = []

    def add_room(self, room: Room):
        if room.room_id in self.rooms:
            raise ValueError(f"Room {room.room_id} already exists.")
        self.rooms[room.room_id] = room

    def add_connection(self, connection: Connection):
        if connection.from_room not in self.rooms:
            raise ValueError(f"{connection.from_room} does not exist.")
        if connection.to_room not in self.rooms:
            raise ValueError(f"{connection.to_room} does not exist.")
        self.connections.append(connection)

    def get_room(self, room_id: str) -> Room:
        return self.rooms[room_id]

    def get_rooms_by_type(self, room_type: str) -> List[Room]:
        return [room for room in self.rooms.values() if room.room_type == room_type]

    def get_rooms_by_floor(self, floor: int) -> List[Room]:
        return [room for room in self.rooms.values() if room.floor == floor]

    def get_connection_distance(self, from_room: str, to_room: str) -> float:

        for connection in self.connections:

            if (
                connection.from_room == from_room
                and connection.to_room == to_room
            ):
                return connection.distance_m

            if (
                connection.bidirectional
                and connection.from_room == to_room
                and connection.to_room == from_room
            ):
                return connection.distance_m

        raise ValueError(
            f"No connection found between {from_room} and {to_room}."
        )
        


