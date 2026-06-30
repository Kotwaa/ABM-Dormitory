# movement_module.py
import random
from L_Shaped_Dormitory import create_dormitory
from stochastic_module import walking_speed




def move_agent(agent, destination_room):
    """
    Moves an agent from the current room to the destination room.
    For now, movement is instant.
    """

    if agent.current_room != destination_room:
        agent.current_room = destination_room
        agent.state = "moving"
    else:
        agent.state = "idle"


def update_agent_location(agent, schedule_block):
    """
    Updates the agent location based on the current schedule block.
    """

    destination = schedule_block.destination_room
    move_agent(agent, destination)


# movement_module.py

from collections import deque


def get_neighbors(building, room_id):
    neighbors = []

    for connection in building.connections:
        if connection.from_room == room_id:
            neighbors.append(connection.to_room)

        if connection.bidirectional and connection.to_room == room_id:
            neighbors.append(connection.from_room)

    return neighbors


def find_path(building, start_room, destination_room):
    queue = deque()
    queue.append([start_room])

    visited = set()

    while queue:
        path = queue.popleft()
        current_room = path[-1]

        if current_room == destination_room:
            return path

        if current_room not in visited:
            visited.add(current_room)

            for neighbor in get_neighbors(building, current_room):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None


# -------------------------
# TRAVEL TIME FUNCTIONS
# -------------------------


def get_connection_time(building, from_room, to_room):
    for connection in building.connections:
        if connection.from_room == from_room and connection.to_room == to_room:
            return connection.travel_time_min

        if (
            connection.bidirectional
            and connection.from_room == to_room
            and connection.to_room == from_room
        ):
            return connection.travel_time_min

    return None


def calculate_path_travel_time(building, path):
    total_time = 0

    for i in range(len(path) - 1):
        travel_time = get_connection_time(building, path[i], path[i + 1])

        # If travel_time is missing for a leg, skip it (safe fallback).
        if travel_time is not None:
            total_time += travel_time
        else:
            # missing connection -> treat as 0 for safety
            continue

    return round(total_time, 2)


def get_room_at_elapsed_time(building, path, elapsed_time_min):
    time_so_far = 0

    if elapsed_time_min <= 0:
        return path[0]

    for i in range(len(path) - 1):
        from_room = path[i]
        to_room = path[i + 1]

        travel_time = get_connection_time(building, from_room, to_room)

        # if travel_time missing, treat as 0 to avoid crashes
        if travel_time is None:
            travel_time = 0

        time_so_far += travel_time

        if elapsed_time_min <= time_so_far:
            return to_room

    return path[-1]

# -------------------------
# TRAVEL TIME FUNCTIONS
# -------------------------
#One connection calculation
def get_connection_distance(building, room_a, room_b):
    for connection in building.connections:
        if (
            connection.from_room == room_a
            and connection.to_room == room_b
        ) or (
            connection.from_room == room_b
            and connection.to_room == room_a
        ):
            return connection.distance_m

    return None

#Total Path distance calculation
def get_path_distance(building, path):
    total_distance = 0

    for i in range(len(path) - 1):
        room_a = path[i]
        room_b = path[i + 1]

        distance = get_connection_distance(
            building,
            room_a,
            room_b
        )

        if distance is None:
            print(
                "WARNING: Missing distance between",
                room_a,
                "and",
                room_b
            )
            distance = 0

        total_distance += distance

    return total_distance




#Walking Speed Calculation
def walking_speed():
    speed = random.normalvariate(0.6, 0.2)

    return round(max(speed, 0.5), 2)



#Calculate TRavel Time as distance / speed
def calculate_travel_time(path_distance_m, speed_mps):
    travel_time_seconds = path_distance_m / speed_mps
    travel_time_minutes = travel_time_seconds / 60

    return travel_time_minutes

#Calculate segment travel times for a path
def get_segment_travel_times(building, path, speed_mps):
    segment_times = []

    for i in range(len(path) - 1):
        from_room = path[i]
        to_room = path[i + 1]

        distance = get_connection_distance(
            building,
            from_room,
            to_room
        )
        if distance is None:
            print(
                "WARNING: Missing distance for segment:",
                f"{from_room} -> {to_room}",
                "| path =",
                " -> ".join(path)
            )
            distance = 0
            
        travel_time = calculate_travel_time(
            distance,
            speed_mps
        )

        segment_times.append(
            {
                "from_room": from_room,
                "to_room": to_room,
                "distance_m": distance,
                "travel_time_min": travel_time,
            }
        )

    return segment_times


#Total_Path travel time calculation
def get_total_path_travel_time(building, path, speed_mps):

    segment_times = get_segment_travel_times(
        building,
        path,
        speed_mps
    )

    total_time = 0

    for segment in segment_times:
        total_time += segment["travel_time_min"]

    return total_time


# -------------------------
# TEST SECTION
# -------------------------

if __name__ == "__main__":

    building = create_dormitory()

    path = [
        "D101",
        "C101",
        "C102",
        "C103",
        "C104",
        "C105",
        "B101"
    ]

    speed = walking_speed()

    print("Speed:", speed)

    print(
        "Total Travel Time:",
        get_total_path_travel_time(
            building,
            path,
            speed
        )
    )