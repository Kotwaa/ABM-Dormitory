# agents.py

# This module defines 1. Agent class, 2. Agent movement functions, 3. Agent creation functions, and 4. Occupancy calculation functions.
import random

from stochastic_module import wake_up_time
from stochastic_module import walking_speed
from stochastic_module import morning_departure_offset
from stochastic_module import afternoon_departure_offset
from stochastic_module import morning_study_decision
from stochastic_module import bathroom_duration
from stochastic_module import preparation_duration
# ==========================================================
# SECTION 1 - AGENT CLASS
# ==========================================================
class Agent:
    def __init__(self, agent_id, agent_type, current_room):

        # -------------------------
        # BASIC INFORMATION
        # -------------------------
        self.agent_id = agent_id
        self.agent_type = agent_type

        # -------------------------
        # ROOM INFORMATION
        # -------------------------
        self.assigned_room = current_room
        self.current_room = current_room
        self.destination_room = current_room
        self.current_destination = None
        self.path = []

        # -------------------------
        # STATE INFORMATION
        # -------------------------
        self.state = "idle"
        self.current_activity = None
        self.is_travelling = False

        # -------------------------
        # BEHAVIORAL PROFILES
        # -------------------------
        self.wake_up_profile = random.choices(
            ["early", "normal", "late"],
            weights=[10, 80, 10]
        )[0]

        self.bathroom_profile = random.choices(
            ["quick", "normal", "long"],
            weights=[15, 75, 10]
        )[0]

        self.preparation_profile = random.choices(
            ["quick", "normal", "careful"],
            weights=[15, 75, 10]
        )[0]

        self.walking_profile = random.choices(
            ["fast", "normal", "slow"],
            weights=[10, 80, 10]
        )[0]

        self.departure_profile = random.choices(
            ["early", "normal", "late"],
            weights=[10, 88, 2]
        )[0]
        
        self.arrival_profile = random.choices(
            ["early", "normal", "late"],
            weights=[15, 70, 15]
        )[0]

        # -------------------------
        # STOCHASTIC ATTRIBUTES
        # -------------------------
        self.wake_up_offset = wake_up_time(self)
        self.walking_speed = walking_speed(self)
        self.leave_time_offset = morning_departure_offset(self)

        self.afternoon_departure_offset = afternoon_departure_offset()

        self.morning_study = morning_study_decision()

        # -------------------------
        # MOVEMENT TIMING
        # -------------------------
        self.next_move_time = None

        # -------------------------
        # MORNING WAKE-UP
        # -------------------------
        self.wake_up_time = None

        # -------------------------
        # MORNING BATHROOM SEQUENCE
        # -------------------------
        self.bathroom_entry_time = None
        self.bathroom_start_time = None
        self.bathroom_exit_time = None
        self.bathroom_finish_time = None
        self.has_finished_bathroom = False
        self.has_returned_from_bathroom = False
        self.return_dorm_time = None

        # -------------------------
        # MORNING PREPARATION AND DEPARTURE
        # -------------------------
        self.preparation_start_time = None
        self.preparation_duration = None
        self.preparation_finish_time = None
        self.morning_leave_time = None
        self.dining_departure_time = None
        self.leave_dorm_time = None
        self.arrive_outside_time = None
        self.has_completed_morning_routine = False

        # -------------------------
        # AFTERNOON ACTIVITY
        # -------------------------
        self.afternoon_return_time = None
        self.afternoon_activity = None

        # -------------------------
        # DINNER BATHROOM SEQUENCE
        # -------------------------
        self.dinner_bathroom_entry_time = None
        self.dinner_bathroom_exit_time = None
        self.dinner_bathroom_start_time = None
        self.dinner_bathroom_finish_time = None
        self.has_finished_dinner_bathroom = False
        self.dinner_return_dorm_time = None
        self.has_returned_from_dinner_bathroom = False

        # -------------------------
        # DINNER PREPARATION
        # -------------------------
        self.dinner_prep_start_time = None
        self.dinner_prep_duration = None
        self.dinner_prep_finish_time = None

        # -------------------------
        # DINNER DEPARTURE / ARRIVAL
        # -------------------------
        self.leave_for_dinner_time = None
        self.arrive_dinner_time = None
        self.evening_return_time = None

        # -------------------------
        # EVENING / LIGHTS OUT
        # -------------------------
        self.evening_activity = None

    # -------------------------
    # AGENT MOVEMENT FUNCTIONS
    # -------------------------
    def set_destination(self, destination):
        self.destination_room = destination
        self.state = "moving"

    def move_to_destination(self, building=None):
        if self.destination_room is not None:
            if building is not None:
                try:
                    self.current_room = building.rooms[self.destination_room]
                except Exception:
                    pass

            self.destination_room = None
            self.state = "idle"

    def set_state(self, new_state):
        self.state = new_state

# ==========================================================
# SECTION 3 - AGENT CREATION
# ==========================================================
def create_students(num_students, room_list, students_per_room):
    students = []

    for i in range(num_students):
        assigned_room = room_list[(i // students_per_room) % len(room_list)]

        student = Agent(
            agent_id=f"S{i+1:03d}", agent_type="student", current_room=assigned_room
        )

        students.append(student)

    return students


# ==========================================================
# SECTION 4 - OCCUPANCY CALCULATIONS  FUNCTIONS
# ==========================================================
def count_room_occupancy(students):
    room_occupancy = {}

    for student in students:
        # normalize to room_id string for counting
        room = student.current_room
        room_id = room.room_id if hasattr(room, "room_id") else room

        if room_id not in room_occupancy:
            room_occupancy[room_id] = 0

        room_occupancy[room_id] += 1

    return room_occupancy


# ==========================================================
# SECTION 7 - TESTING
# ==========================================================
if __name__ == "__main__":

    from schedule_module import get_student_schedule, get_current_activity

    # ==========================================================
    # SECTION 5 - DAILY SCHEDULE FUNCTION
    # ==========================================================
    def assign_student_state_by_time(student, current_time):
        if current_time < 6:
            student.set_state("sleeping")

        elif current_time < 7:
            student.set_state("getting_ready")

        elif current_time < 8:
            student.set_state("breakfast")

        elif current_time < 16:
            student.set_state("outside")

        elif current_time < 22:
            student.set_state("in_dorm")

        else:
            student.set_state("sleeping")

    # ==========================================================
    # SECTION 6 - LOCATION UPDATE BY STATE
    # ==========================================================
    def update_location_by_state(student):
        if student.state == "sleeping":
            student.current_room = student.home_room

        elif student.state == "getting_ready":
            student.current_room = student.home_room

        elif student.state == "breakfast":
            student.current_room = "DINING"

        elif student.state == "outside":
            student.current_room = "OUTSIDE"

        elif student.state == "in_dorm":
            student.current_room = student.home_room

    # ==========================================================
    # SECTION 7 - SCHEDULE-BASED LOCATION UPDATE
    # ==========================================================

    def update_agent_schedule(agent, current_time):
        if agent.agent_type == "student":
            schedule = get_student_schedule()
            current_block = get_current_activity(schedule, current_time)

            if current_block:
                agent.current_activity = current_block.activity
                agent.destination_room = current_block.destination_room
            else:
                agent.current_activity = "unscheduled"
                agent.destination_room = agent.current_room

    # Basic test to create agents and print their attributes
    # room_list = ["D101", "D102", "D201", "D202", "D203", "D204", "D205", "D301", "D302", "D303", "D304", "D305"]

    room_list = ["D101", "D102"]

    # students = create_students(144, room_list, 12)
    students = create_students(10, room_list, 5)

    current_time = "08:30"

    for student in students:
        update_agent_schedule(student, current_time)

    print("\nAGENTS WITH SCHEDULE")
    print("-" * 85)
    print(
        f"{'ID':<10}"
        f"{'TYPE':<12}"
        f"{'CURRENT ROOM':<15}"
        f"{'ACTIVITY':<20}"
        f"{'DESTINATION'}"
    )
    print("-" * 85)

    for student in students:
        print(
            f"{student.agent_id:<10}"
            f"{student.agent_type:<12}"
            f"{student.current_room:<15}"
            f"{student.current_activity:<20}"
            f"{student.destination_room}"
        )


from L_Shaped_Dormitory import create_dormitory

if __name__ == "__main__":

    building = create_dormitory()

    dorm_rooms = building.get_rooms_by_type("dormroom")

    students = create_students(
        num_students=10, room_list=dorm_rooms, students_per_room=12
    )

    print(f"{'ID':<8} {'WAKE-UP OFFSET'}")
    print("-" * 30)

    for student in students:
        print(f"{student.agent_id:<8} " f"{student.wake_up_offset}")
