# test_building_module.py

from building_module import Building, Room, Connection


def create_dormitory():
    building = Building("L-Shaped Dormitory")
    # OUTSIDE
    building.add_room(
        Room(
            room_id="OUTSIDE",
            name="outside_building",
            room_type="outside",
            floor=0,
            capacity=9999,
            area_m2=0.0,
        )
    )

    # DEFGROUNDFLOOR
    building.add_room(
        Room(
            room_id="D101",
            name="student_room_101",
            room_type="dormroom",
            floor=1,
            capacity=12,
            area_m2=48.0,
        )
    )

    building.add_room(
        Room(
            room_id="D102",
            name="student_room_102",
            room_type="dormroom",
            floor=1,
            capacity=12,
            area_m2=61.0,
        )
    )

    building.add_room(
        Room(
            room_id="R101",
            name="recreation_room_101",
            room_type="recroom",
            floor=1,
            capacity=45,
            area_m2=96.0,
        )
    )

    building.add_room(
        Room(
            room_id="S101",
            name="study_room_101",
            room_type="studyroom",
            floor=1,
            capacity=30,
            area_m2=114.0,
        )
    )

    building.add_room(
        Room(
            room_id="B101",
            name="bathroom 101",
            room_type="bathroom",
            floor=1,
            capacity=30,
            area_m2=84.0,
        )
    )

    # GFCORRIDOR
    building.add_room(
        Room(
            room_id="C101_A",
            name="corridor_101",
            room_type="corridor",
            floor=1,
            capacity=5,
            area_m2=5.0,
        )
    )
    
    building.add_room(
        Room(
            room_id="C101",
            name="corridor_101",
            room_type="corridor",
            floor=1,
            capacity=10,
            area_m2=21.0,
        )
    )

    building.add_room(
        Room(
            room_id="C102",
            name="corridor_102",
            room_type="corridor",
            floor=1,
            capacity=10,
            area_m2=16.0,
        )
    )

    building.add_room(
        Room(
            room_id="C103",
            name="corridor_103",
            room_type="corridor",
            floor=1,
            capacity=10,
            area_m2=16.0,
        )
    )

    building.add_room(
        Room(
            room_id="C104",
            name="corridor_104",
            room_type="corridor",
            floor=1,
            capacity=10,
            area_m2=16.0,
        )
    )

    building.add_room(
        Room(
            room_id="C105",
            name="corridor_105",
            room_type="corridor",
            floor=1,
            capacity=30,
            area_m2=38.0,
        )
    )

    building.add_room(
        Room(
            room_id="C106",
            name="corridor_106",
            room_type="corridor",
            floor=1,
            capacity=10,
            area_m2=32.0,
        )
    )

    # GFSTAIRS
    building.add_room(
        Room(
            room_id="ST101",
            name="stair_101",
            room_type="stair",
            floor=1,
            capacity=20,
            area_m2=10.0,
        )
    )
    
    building.add_room(
        Room(
            room_id="ST102",
            name="stair_101",
            room_type="stair",
            floor=1,
            capacity=20,
            area_m2=10.0,
        )
    )

    # DEFFIRSTFLOOR
    building.add_room(
        Room(
            room_id="D201",
            name="student_room_201",
            room_type="dormroom",
            floor=2,
            capacity=12,
            area_m2=61.0,
        )
    )

    building.add_room(
        Room(
            room_id="D202",
            name="student_room_202",
            room_type="dormroom",
            floor=2,
            capacity=12,
            area_m2=61.0,
        )
    )

    building.add_room(
        Room(
            room_id="D203",
            name="student_room_203",
            room_type="dormroom",
            floor=2,
            capacity=12,
            area_m2=61.0,
        )
    )

    building.add_room(
        Room(
            room_id="D204",
            name="student_room_204",
            room_type="dormroom",
            floor=2,
            capacity=12,
            area_m2=61.0,
        )
    )

    building.add_room(
        Room(
            room_id="D205",
            name="student_room_205",
            room_type="dormroom",
            floor=2,
            capacity=12,
            area_m2=61.0,
        )
    )

    building.add_room(
        Room(
            room_id="S201",
            name="study_room_201",
            room_type="studyroom",
            floor=2,
            capacity=30,
            area_m2=114.0,
        )
    )

    building.add_room(
        Room(
            room_id="B201",
            name="bathroom 201",
            room_type="bathroom",
            floor=2,
            capacity=30,
            area_m2=84.0,
        )
    )

    # FFCORRIDOR
    building.add_room(
        Room(
            room_id="C201",
            name="corridor_201",
            room_type="corridor",
            floor=2,
            capacity=10,
            area_m2=21.0,
        )
    )

    building.add_room(
        Room(
            room_id="C202",
            name="corridor_202",
            room_type="corridor",
            floor=2,
            capacity=10,
            area_m2=16.0,
        )
    )

    building.add_room(
        Room(
            room_id="C203",
            name="corridor_203",
            room_type="corridor",
            floor=2,
            capacity=10,
            area_m2=16.0,
        )
    )

    building.add_room(
        Room(
            room_id="C204",
            name="corridor_204",
            room_type="corridor",
            floor=2,
            capacity=10,
            area_m2=16.0,
        )
    )

    building.add_room(
        Room(
            room_id="C205",
            name="corridor_205",
            room_type="corridor",
            floor=2,
            capacity=30,
            area_m2=38.0,
        )
    )

    building.add_room(
        Room(
            room_id="C206",
            name="corridor_206",
            room_type="corridor",
            floor=2,
            capacity=10,
            area_m2=32.0,
        )
    )

    # FFSTAIRS
    building.add_room(
        Room(
            room_id="ST201",
            name="stair_201",
            room_type="stair",
            floor=2,
            capacity=20,
            area_m2=10.0,
        )
    )
    
    building.add_room(
        Room(
            room_id="ST202",
            name="stair_201",
            room_type="stair",
            floor=2,
            capacity=20,
            area_m2=10.0,
        )
    )

    # DEFSECONDFLOOR
    building.add_room(
        Room(
            room_id="D301",
            name="student_room_301",
            room_type="dormroom",
            floor=3,
            capacity=12,
            area_m2=61.0,
        )
    )

    building.add_room(
        Room(
            room_id="D302",
            name="student_room_302",
            room_type="dormroom",
            floor=3,
            capacity=12,
            area_m2=61.0,
        )
    )

    building.add_room(
        Room(
            room_id="D303",
            name="student_room_303",
            room_type="dormroom",
            floor=3,
            capacity=12,
            area_m2=61.0,
        )
    )

    building.add_room(
        Room(
            room_id="D304",
            name="student_room_304",
            room_type="dormroom",
            floor=3,
            capacity=12,
            area_m2=61.0,
        )
    )

    building.add_room(
        Room(
            room_id="D305",
            name="student_room_305",
            room_type="dormroom",
            floor=3,
            capacity=12,
            area_m2=61.0,
        )
    )

    building.add_room(
        Room(
            room_id="S301",
            name="study_room_301",
            room_type="studyroom",
            floor=3,
            capacity=30,
            area_m2=114.0,
        )
    )

    building.add_room(
        Room(
            room_id="B301",
            name="bathroom 301",
            room_type="bathroom",
            floor=3,
            capacity=30,
            area_m2=84.0,
        )
    )

    # SFCORRIDOR
    building.add_room(
        Room(
            room_id="C301",
            name="corridor_301",
            room_type="corridor",
            floor=3,
            capacity=10,
            area_m2=21.0,
        )
    )

    building.add_room(
        Room(
            room_id="C302",
            name="corridor_302",
            room_type="corridor",
            floor=3,
            capacity=10,
            area_m2=16.0,
        )
    )

    building.add_room(
        Room(
            room_id="C303",
            name="corridor_303",
            room_type="corridor",
            floor=3,
            capacity=10,
            area_m2=16.0,
        )
    )

    building.add_room(
        Room(
            room_id="C304",
            name="corridor_304",
            room_type="corridor",
            floor=3,
            capacity=10,
            area_m2=16.0,
        )
    )

    building.add_room(
        Room(
            room_id="C305",
            name="corridor_305",
            room_type="corridor",
            floor=3,
            capacity=30,
            area_m2=38.0,
        )
    )

    building.add_room(
        Room(
            room_id="C306",
            name="corridor_306",
            room_type="corridor",
            floor=3,
            capacity=10,
            area_m2=32.0,
        )
    )

    # SFSTAIRS
    building.add_room(
        Room(
            room_id="ST301",
            name="stair_301",
            room_type="stair",
            floor=3,
            capacity=20,
            area_m2=10.0,
        )
    )
    
    building.add_room(
        Room(
            room_id="ST302",
            name="stair_301",
            room_type="stair",
            floor=3,
            capacity=20,
            area_m2=10.0,
        )
    )

    # CONNECTION(using student speed of 1.4m/s and 84m/m)

    # FIRSTFLOOR
    # Rooms & corridor
    # R&CGF
    building.add_connection(
        Connection(from_room="D101", to_room="C101", distance_m=1, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="D102", to_room="C106", distance_m=1, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="R101", to_room="C103", distance_m=1, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="S101", to_room="C106", distance_m=2, bidirectional=True)
    )

    # R&CFF
    building.add_connection(
        Connection(from_room="D201", to_room="C201", distance_m=1, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="D202", to_room="C202", distance_m=1, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="D203", to_room="C203", distance_m=1, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="D204", to_room="C204", distance_m=1, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="D205", to_room="C206", distance_m=1, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="S201", to_room="C206", distance_m=2, bidirectional=True)
    )

    # R&CSF
    building.add_connection(
        Connection(from_room="D301", to_room="C301", distance_m=1, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="D302", to_room="C302", distance_m=1, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="D303", to_room="C303", distance_m=1, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="D304", to_room="C304", distance_m=1, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="D305", to_room="C306", distance_m=1, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="S301", to_room="C306", distance_m=2, bidirectional=True)
    )

    # Corridor 4 & bathroom
    building.add_connection(
        Connection(from_room="C105", to_room="B101", distance_m=2, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C205", to_room="B201", distance_m=2, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C305", to_room="B301", distance_m=2, bidirectional=True)
    )

    # Corridor 5 & Stairs
    building.add_connection(
        Connection(from_room="C101_A", to_room="ST102", distance_m=1.5, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C201", to_room="ST202", distance_m=8.5, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C301", to_room="ST302", distance_m=8.5, bidirectional=True)
    )
    
    building.add_connection(
        Connection(from_room="C105", to_room="ST101", distance_m=2, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C205", to_room="ST201", distance_m=2, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C305", to_room="ST301", distance_m=2, bidirectional=True)
    )

    # Inter Corridors
    # GFIC
    building.add_connection(
        Connection(from_room="C101_A", to_room="C101", distance_m=7.5, bidirectional=True)
    )
    
    building.add_connection(
        Connection(from_room="C101", to_room="C102", distance_m=8, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C102", to_room="C103", distance_m=8, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C103", to_room="C104", distance_m=8, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C104", to_room="C105", distance_m=2, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C105", to_room="C106", distance_m=15, bidirectional=True)
    )

    # FFIC
    building.add_connection(
        Connection(from_room="C201", to_room="C202", distance_m=8, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C202", to_room="C203", distance_m=8, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C203", to_room="C204", distance_m=8, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C204", to_room="C205", distance_m=2, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C205", to_room="C206", distance_m=15, bidirectional=True)
    )

    # SFIC
    building.add_connection(
        Connection(from_room="C301", to_room="C302", distance_m=8, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C302", to_room="C303", distance_m=8, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C303", to_room="C304", distance_m=8, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C304", to_room="C305", distance_m=2, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="C305", to_room="C306", distance_m=15, bidirectional=True)
    )

  
      # Stairs & Stairs
    building.add_connection(
        Connection(from_room="ST301", to_room="ST201", distance_m=2, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="ST201", to_room="ST101", distance_m=2, bidirectional=True)
    )

    # Corridors and outside
    building.add_connection(
        Connection(from_room="C105", to_room="OUTSIDE", distance_m=5, bidirectional=True,
        )
    )
    
    building.add_connection(
        Connection(from_room="C101_A", to_room="OUTSIDE", distance_m=1, bidirectional=True,
        )
    )
    
    # Stairs & Stairs
    building.add_connection(
        Connection(from_room="ST302", to_room="ST202", distance_m=2, bidirectional=True)
    )

    building.add_connection(
        Connection(from_room="ST202", to_room="ST102", distance_m=2, bidirectional=True)
    )
    
    return building


# For any connections not explicitly defined, we can assume a default distance (e.g., 8 meters)
def get_connection_distance(building, room_a, room_b):

    for connection in building.connections:

        if (
            connection.from_room == room_a
            and connection.to_room == room_b
        ):
            return connection.distance_m

        if (
            connection.bidirectional
            and connection.from_room == room_b
            and connection.to_room == room_a
        ):
            return connection.distance_m

    return 8  # Default distance if no specific connection is defined


def get_path_distance(building, path):
    total_distance = 0

    for i in range(len(path) - 1):
        room_a = path[i]
        room_b = path[i + 1]

        total_distance += get_connection_distance(
    building,
    room_a,
    room_b
)


# ==========================================================
# SECTION - TESTING
# ==========================================================

if __name__ == "__main__":
    building = create_dormitory()


