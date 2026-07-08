# core_abm_module.py
import csv
from building_module import Building
from L_Shaped_Dormitory import create_dormitory
from agent_module import create_students
from schedule_module import get_student_schedule
from movement_module import find_path, get_room_at_elapsed_time
from queue_module import apply_queueing
from stochastic_module import afternoon_arrival_offset 
from stochastic_module import evening_arrival_offset
from stochastic_module import wake_up_time
from stochastic_module import bathroom_duration
from stochastic_module import preparation_duration
from stochastic_module import walking_speed
from stochastic_module import morning_study_decision
from stochastic_module import choose_afternoon_activity
from stochastic_module import choose_evening_activity
from stochastic_module import morning_departure_offset

# -------------------------
# MOVEMENT HELPER FUNCTIONS
# -------------------------
def can_enter_room(room_id, building, occupancy_counts):
    room = building.rooms[room_id]

    # OUTSIDE can be unlimited
    if room_id == "OUTSIDE":
        return True

    current_occupancy = occupancy_counts.get(room_id, 0)

    return current_occupancy < room.capacity


def move_student_one_step(student, building, occupancy_counts):
    path = student.path

    # If student has no path or is already at destination
    # compare room_id strings
    if not path or student.current_room.room_id == student.destination_room:
        student.state = "arrived"
        return

    # current_room is a Room object; use its room_id for path indexing
    current_index = path.index(student.current_room.room_id)

    # If already at final room
    if current_index == len(path) - 1:
        student.state = "arrived"
        return

    next_room = path[current_index + 1]

    if can_enter_room(next_room, building, occupancy_counts):
        # update occupancy using room_id keys
        cur_id = student.current_room.room_id
        occupancy_counts[cur_id] = max(occupancy_counts.get(cur_id, 0) - 1, 0)
        occupancy_counts[next_room] = occupancy_counts.get(next_room, 0) + 1

        # move student (store Room object)
        student.current_room = building.rooms[next_room]
        student.state = "moving"

    else:
        student.state = "queued"


# -------------------------
# SCHEDULE FUNCTIONS
# -------------------------
def get_current_schedule_block(schedule, current_time):
    current_minutes = time_to_minutes(current_time)

    for block in schedule:
        start_minutes = time_to_minutes(block.start_time)
        end_minutes = time_to_minutes(block.end_time)

        if start_minutes <= current_minutes < end_minutes:
            return block

    return None


# -------------------------
# TIME FUNCTIONS
# -------------------------
def time_to_minutes(time_string):
    hour, minute = time_string.split(":")
    return int(hour) * 60 + int(minute)


def get_elapsed_minutes(current_time, start_time):
    current_minutes = time_to_minutes(current_time)
    start_minutes = time_to_minutes(start_time)

    return current_minutes - start_minutes


def minutes_to_time(minutes):

    if minutes is None:
        return None

    hour = int(minutes // 60)
    minute = int(minutes % 60)

    return f"{hour:02d}:{minute:02d}"


def generate_time_steps(start_time, end_time, step_minutes):
    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)

    time_steps = []

    for minute in range(start_minutes, end_minutes + 1, step_minutes):
        time_steps.append(minutes_to_time(minute))

    return time_steps


# -------------------------
# OCCUPANCY FUNCTIONS
# -------------------------


def count_room_occupancy(results):
    occupancy_counts = {}

    for result in results:
        room_id = result["current_room"]

        if room_id not in occupancy_counts:
            occupancy_counts[room_id] = 0

        occupancy_counts[room_id] += 1

    return occupancy_counts


def get_all_room_ids():
    building = create_dormitory()
    return list(building.rooms.keys())


def run_occupancy_time_series(start_time, end_time, simulation_step=1, reporting_step=5):

    building, students, schedule = initialize_simulation()

    time_steps = generate_time_steps(
        start_time,
        end_time,
        simulation_step
    )

    all_room_ids = get_all_room_ids()
    occupancy_series = []
    debug_rows = []

    for time in time_steps:

        results = run_simulation(
            time,
            building,
            students,
            schedule,
            simulation_step
        )

        current_minutes = time_to_minutes(time)

        if current_minutes % reporting_step == 0:

            occupancy_counts = count_room_occupancy(results)

            row = {"time": time}

            for room_id in all_room_ids:
                row[room_id] = occupancy_counts.get(room_id, 0)

            occupancy_series.append(row)

    return occupancy_series, students
        
        # -------------------------
        # STUDENTS NOT OUT BY 8:00
        # -------------------------
    """
    if time == "08:00":
        print("\nNOT OUTSIDE AT 08:00")

        for student in students:
            if student.current_room.room_id != "OUTSIDE":
                print(
                    student.agent_id,
                    student.current_room.room_id,
                    "leave:",
                    minutes_to_time(student.leave_dorm_time),
                    "outside:",
                    minutes_to_time(student.arrive_outside_time),
                    "path:",
                    " -> ".join(student.path)
                )
                """
        # collect per-student debug info from results
    for res in results:
        debug_rows.append(
            {
                "time": time,
                "student_id": res.get("id"),
                "activity": res.get("activity"),
                "current_room": res.get("current_room"),
                "destination": res.get("destination"),
                "bath_done": res.get("bath_done"),
                "returned_to_dorm": res.get("returned_to_dorm"),
                "prep_start": minutes_to_time(res.get("prep_start")),
                "prep_finish": minutes_to_time(res.get("prep_finish")),
                "bathroom_start_time": res.get("bathroom_start_time"),
                "bathroom_finish_time": res.get("bathroom_finish_time"),
                "return_dorm_time": res.get("return_dorm_time"),
                "leave_dorm_time": res.get("leave_dorm_time"),
                "arrive_outside_time": res.get("arrive_outside_time"),
            }
        )

    occupancy_counts = count_room_occupancy(results)

    row = {"time": time}

    for room_id in all_room_ids:
        row[room_id] = occupancy_counts.get(room_id, 0)

    occupancy_series.append(row)

    EXPORT_DEBUG_CSV = False

    # write debug CSV after the simulation loop
    csv_filename = "student_debug_output.csv"
    fieldnames = [
        "time",
        "student_id",
        "activity",
        "current_room",
        "destination",
        "bath_done",
        "returned_to_dorm",
        "bathroom_start_time",
        "bathroom_finish_time",
        "return_dorm_time",
        "prep_start",
        "prep_finish",
        "leave_dorm_time",
        "arrive_outside_time",
    ]

    if EXPORT_DEBUG_CSV:

        with open(csv_filename, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for r in debug_rows:
                writer.writerow(r)

       # print("Student debug output exported.")

    timeline_filename = "student_activity_timeline.csv"

    timeline_fieldnames = [
        "student_id",
        "wake_up_time",
        "bathroom_start_time",
        "bathroom_finish_time",
        "return_dorm_time",
        "prep_start",
        "prep_finish",
        "leave_dorm_time",
        "arrive_outside_time",
    ]

    if EXPORT_DEBUG_CSV:

        with open(timeline_filename, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=timeline_fieldnames)
            writer.writeheader()

            for student in students:
                writer.writerow(
                    {
                        "student_id": student.agent_id,
                        "wake_up_time": student.wake_up_time,
                        "bathroom_start_time": student.bathroom_start_time,
                        "bathroom_finish_time": student.bathroom_finish_time,
                        "return_dorm_time": student.return_dorm_time,
                        "prep_start": minutes_to_time(student.preparation_start_time),
                        "prep_finish": minutes_to_time(student.preparation_finish_time),
                        "leave_dorm_time": student.leave_dorm_time,
                        "arrive_outside_time": student.arrive_outside_time,
                    }
                )

        #print("Student activity timeline exported.")

    return occupancy_series, students


# -------------------------
# INITIALIZATION FUNCTIONS
# -------------------------


def initialize_simulation():
    building = create_dormitory()
    dorm_rooms = building.get_rooms_by_type("dormroom")

    students = create_students(
        num_students=132, room_list=dorm_rooms, students_per_room=12
    )

    schedule = get_student_schedule()

    return building, students, schedule

# -------------------------
# BEHAVIOR FUNCTIONS
# -------------------------
#MORNING BEHAVIOR
def update_morning_behavior(student, building, current_time_minutes):
    
    # 1. Calculate actual wake-up time
    scheduled_wake_up_time = time_to_minutes("05:00")
    actual_wake_up_time = (scheduled_wake_up_time + student.wake_up_offset)
    
    # 2. Record wake-up time once
    if (
        student.wake_up_time is None
        and current_time_minutes >= actual_wake_up_time
    ):
        student.wake_up_time = current_time_minutes
        
    # 3. Before wake-up, keep student in assigned dorm room
    if current_time_minutes < actual_wake_up_time:
      student.destination_room = student.assigned_room.room_id
      return  
  
    # 4. Find the bathroom on the student's floor
    student_floor = student.assigned_room.floor

    bathrooms = building.get_rooms_by_type("bathroom")

    same_floor_bathrooms = [
        room for room in bathrooms
        if room.floor == student_floor
    ]

    bathroom_id = same_floor_bathrooms[0].room_id
    
    # 5. If bathroom is not finished, send student to bathroom
    if not student.has_finished_bathroom:
        student.destination_room = bathroom_id

        # 6. If student is physically inside bathroom, start bathroom timer
        if student.current_room.room_id == bathroom_id:

            if student.bathroom_entry_time is None:
                student.bathroom_entry_time = current_time_minutes
                student.bathroom_start_time = current_time_minutes

                duration = bathroom_duration(student)

                student.bathroom_exit_time = (
                    current_time_minutes
                    + duration
                )

        # 7. If bathroom time is complete, mark bathroom as finished
        if (
            student.bathroom_exit_time is not None
            and current_time_minutes >= student.bathroom_exit_time
        ):
            student.has_finished_bathroom = True
            student.bathroom_finish_time = current_time_minutes

        return

    # 8. If bathroom is finished but student has not returned to dorm, send student back to assigned dorm
    if (
        student.has_finished_bathroom
        and not student.has_returned_from_bathroom
    ):
        student.destination_room = student.assigned_room.room_id
        
    
    # 9. If student is physically back in dorm, record return time
    if (
        student.current_room.room_id == student.assigned_room.room_id
        and student.return_dorm_time is None
    ):
        student.has_returned_from_bathroom = True
        student.return_dorm_time = current_time_minutes
    if not student.has_returned_from_bathroom:
        return
        
    # 10. If student has returned to dorm, start preparation once
    if student.preparation_start_time is None:
        student.preparation_start_time = current_time_minutes
        student.preparation_duration = preparation_duration(student)
        student.preparation_finish_time = (
            student.preparation_start_time
            + student.preparation_duration
        )
        
    # 11. If preparation is not finished, keep student in assigned dorm
    if current_time_minutes < student.preparation_finish_time:
        student.destination_room = student.assigned_room.room_id
        """
        print(
            student.agent_id,
            student.current_room.room_id,
            student.destination_room,
            student.has_finished_bathroom,
            student.has_returned_from_bathroom,
        )
        """
        return
    
    # 11. If preparation is not finished, keep student in assigned dorm
    if current_time_minutes < student.preparation_finish_time:
        student.destination_room = student.assigned_room.room_id
        return

    # 12. Calculate actual morning leave time once
    if student.morning_leave_time is None:
        student.morning_leave_time = (
            student.preparation_finish_time
            + student.leave_time_offset
        )

    # 13. If it is not leave time yet, keep student in dorm
    if current_time_minutes < student.morning_leave_time:
        student.destination_room = student.assigned_room.room_id
        return

    # 14. If leave time has arrived, send student OUTSIDE
    student.destination_room = "OUTSIDE"

    if student.leave_dorm_time is None:
        student.leave_dorm_time = current_time_minutes
    
    pass

#AFTERNOON BEHAVIOUR 
def handle_class_behavior(student, current_time_minutes):
    student.destination_room = "OUTSIDE"

    if student.leave_dorm_time is None:
        student.leave_dorm_time = current_time_minutes


def handle_lunch_behavior(student):
    student.destination_room = "OUTSIDE"


#SIESTA BEHAVIOR
def handle_afternoon_behavior(student, current_time_minutes):

    if student.afternoon_return_time is None:
        student.afternoon_return_time = (
            time_to_minutes("15:00")
            + afternoon_arrival_offset(student)
        )

    if current_time_minutes < student.afternoon_return_time:
        student.destination_room = "OUTSIDE"
        return

    if student.afternoon_activity is None:
        student.afternoon_activity = choose_afternoon_activity()

    if student.afternoon_activity == "siesta":
        student.destination_room = student.assigned_room.room_id

    elif student.afternoon_activity == "study":
        student.destination_room = "S101"

    elif student.afternoon_activity == "recreation":
        student.destination_room = "R101"


#DINNER & PREP BEHAVIOUR
def handle_dinner_prep_behavior(
    student,
    building,
    current_time,
    current_time_minutes
):

    student_floor = student.assigned_room.floor
    bathrooms = building.get_rooms_by_type("bathroom")

    same_floor_bathrooms = [
        room for room in bathrooms
        if room.floor == student_floor
    ]

    bathroom_id = same_floor_bathrooms[0].room_id

    if not student.has_finished_dinner_bathroom:

        student.destination_room = bathroom_id

        if student.current_room.room_id == bathroom_id:

            if student.dinner_bathroom_start_time is None:
                student.dinner_bathroom_start_time = current_time

            if student.dinner_bathroom_entry_time is None:
                student.dinner_bathroom_entry_time = current_time_minutes

                duration = bathroom_duration(student)

                student.dinner_bathroom_exit_time = (
                    current_time_minutes + duration
                )

            if current_time_minutes >= student.dinner_bathroom_exit_time:
                student.has_finished_dinner_bathroom = True
                student.dinner_bathroom_finish_time = current_time

    elif not student.has_returned_from_dinner_bathroom:

        student.destination_room = student.assigned_room.room_id

        if student.current_room.room_id == student.assigned_room.room_id:
            student.has_returned_from_dinner_bathroom = True
            student.dinner_return_dorm_time = current_time

    else:

        student.destination_room = student.assigned_room.room_id

        if student.dinner_prep_start_time is None:

            student.dinner_prep_start_time = current_time_minutes
            student.dinner_prep_duration = preparation_duration(student)

            student.dinner_prep_finish_time = (
                student.dinner_prep_start_time
                + student.dinner_prep_duration
            )

        if (
            student.dinner_prep_finish_time is not None
            and current_time_minutes >= student.dinner_prep_finish_time
        ):

            student.destination_room = "OUTSIDE"

            if student.leave_for_dinner_time is None:
                student.leave_for_dinner_time = current_time


#DINNER EBHAVIOUR
def handle_dinner_behavior(student, current_time):

    student.destination_room = "OUTSIDE"

    if student.leave_for_dinner_time is None:
        student.leave_for_dinner_time = current_time

#LIGHTS OUT BEHAVIOR       
def handle_evening_behavior(student, current_time_minutes):

    if student.evening_return_time is None:
        student.evening_return_time = (
            time_to_minutes("18:00")
            + evening_arrival_offset(student)
        )

    if current_time_minutes < student.evening_return_time:
        student.destination_room = "OUTSIDE"
        return

    if student.evening_activity is None:
        student.evening_activity = choose_evening_activity()

    if student.evening_activity == "dorm":
        student.destination_room = student.assigned_room.room_id

    elif student.evening_activity == "study":
        student.destination_room = "S101"

    elif student.evening_activity == "recreation":
        student.destination_room = "R101"
        
#ALL OTHER BEHAVIOR        
def handle_default_behavior(student, current_block):

    if current_block.destination_room in ["Dorm", "DORM_ROOM"]:

        student.destination_room = student.assigned_room.room_id

    elif current_block.destination_room == "Bathroom":

        # Do not use generic Bathroom as a movement destination.
        # Stay where you are unless morning/dinner bathroom logic assigns B101/B201/B301.
        student.destination_room = student.current_room.room_id

    else:

        student.destination_room = current_block.destination_room  

# -------------------------
# CORE SIMULATION ENGINE
# -------------------------
def run_simulation(current_time, building, students, schedule, step_minutes):
    current_block = get_current_schedule_block(schedule, current_time)
    current_time_minutes = time_to_minutes(current_time)

    #print(current_time, current_block.activity if current_block else "NO BLOCK")

    results = []

    for student in students:

        if current_block:

            # --------------------------------------------------
            # STEP 1: Read the current scheduled activity
            # --------------------------------------------------
            student.state = current_block.activity

            # --------------------------------------------------
            # STEP 2: Student is already travelling
            # --------------------------------------------------
            if student.is_travelling:
                pass
            
            elif (
                student.has_completed_morning_routine
                and current_block.activity in ["wake_up", "bath", "breakfast"]
            ):
                student.destination_room = "OUTSIDE"
                
            elif (
                student.current_room.room_id == "OUTSIDE"
                and current_block.activity in ["wake_up", "bath", "breakfast"]
            ):
                student.destination_room = "OUTSIDE"
                student.has_completed_morning_routine = True

                if student.arrive_outside_time is None:
                    student.arrive_outside_time = current_time_minutes
            # --------------------------------------------------
            # STEP 3: Morning behavior logic
            # --------------------------------------------------
            elif (
                not student.has_completed_morning_routine
                and current_block.activity in ["wake_up", "bath", "breakfast"]
            ):

                update_morning_behavior(
                    student,
                    building,
                    current_time_minutes
                )

            # --------------------------------------------------
            # STEP 4: Class
            # --------------------------------------------------
            elif current_block.activity == "class":

                handle_class_behavior(
                    student,
                    current_time_minutes
                )

            # --------------------------------------------------
            # STEP 5: Lunch
            # --------------------------------------------------
            elif current_block.activity == "lunch":

                handle_lunch_behavior(student)

            # --------------------------------------------------
            # STEP 6: Afternoon free time
            # --------------------------------------------------
            elif current_block.activity == "afternoon_free_time":

                handle_afternoon_behavior(student, current_time_minutes)

            # --------------------------------------------------
            # STEP 7: Dinner preparation
            # --------------------------------------------------
            elif current_block.activity == "dinner_prep":

                handle_dinner_prep_behavior(
                    student,
                    building,
                    current_time,
                    current_time_minutes
                )

            # --------------------------------------------------
            # STEP 8: Dinner
            # --------------------------------------------------
            elif current_block.activity == "dinner":

                handle_dinner_behavior(
                    student,
                    current_time_minutes
                )

            # --------------------------------------------------
            # STEP 9: Evening free time
            # --------------------------------------------------
            elif current_block.activity == "evening_free_time":

                handle_evening_behavior(student, current_time_minutes)

            # --------------------------------------------------
            # STEP 10: Default scheduled behavior
            # --------------------------------------------------
            else:

                handle_default_behavior(
                    student,
                    current_block
                )
                
                
            # --------------------------------------------------
            # STEP 6: Assign a new path only if destination changes
            # --------------------------------------------------
            if student.destination_room != student.current_destination:

                student.current_destination = student.destination_room

                path = find_path(
                    building,
                    student.current_room.room_id,
                    student.destination_room
                )

                if path is None:
                    print(
                        "NO PATH:",
                        student.agent_id,
                        student.current_room.room_id,
                        "->",
                        student.destination_room
                    )
                    student.path = [student.current_room.room_id]
                    student.is_travelling = False

                else:
                    student.path = path
                    student.is_travelling = (
                        student.current_room.room_id != student.destination_room
                    )
                
                

            # --------------------------------------------------
            # STEP 7: Move to the next room when travel time has elapsed
            # --------------------------------------------------
            # Current room occupancy
            occupancy_counts = {}

            for s in students:
                room_id = s.current_room.room_id
                occupancy_counts[room_id] = (
                    occupancy_counts.get(room_id, 0) + 1
                )

            if student.path is not None and student.current_room.room_id in student.path:

                current_index = student.path.index(student.current_room.room_id)

                if current_index < len(student.path) - 1:

                    current_room_id = student.current_room.room_id
                    next_room_id = student.path[current_index + 1]

                    if student.next_move_time is None:
                        student.next_move_time = current_time_minutes

                    if current_time_minutes >= student.next_move_time:

                        leaving_bathroom = (
                            building.rooms[current_room_id].room_type == "bathroom"
                        )

                        if leaving_bathroom or can_enter_room(next_room_id, building, occupancy_counts):

                            occupancy_counts[current_room_id] = max(
                                occupancy_counts.get(current_room_id, 0) - 1,
                                0
                            )

                            occupancy_counts[next_room_id] = (
                                occupancy_counts.get(next_room_id, 0) + 1
                            )

                            student.current_room = building.rooms[next_room_id]

                            distance_m = building.get_connection_distance(
                                current_room_id,
                                next_room_id
                            )

                            travel_minutes = (
                                distance_m /
                                student.walking_speed /
                                60
                            )

                            student.next_move_time = (
                                current_time_minutes +
                                travel_minutes
                            )

                            student.state = "moving"

                        else:
                            student.state = "queued"

            # Stop travelling once destination is reached
            if student.current_room.room_id == student.destination_room:
                student.is_travelling = False
                    

            # --------------------------------------------------
            # DEBUG: Trace one student
            # --------------------------------------------------
            """
            if student.agent_id == "S031":

                print(
                    current_time,
                    "| room:",
                    student.current_room.room_id,
                    "| destination:",
                    student.destination_room,
                    "| next_move_time:",
                    round(student.next_move_time, 2) if student.next_move_time is not None else None,
                    "| path:",
                    " -> ".join(student.path) if student.path else None
                )
                """
            # --------------------------------------------------
            # STEP 8: Record current room after movement
            # --------------------------------------------------
            actual_current_room = student.current_room.room_id

            if (
                actual_current_room == "OUTSIDE"
                and student.arrive_outside_time is None
                and student.leave_dorm_time is not None
                and current_time_minutes >= student.leave_dorm_time
            ):
                student.arrive_outside_time = current_time_minutes
                student.has_completed_morning_routine = True

            # --------------------------------------------------
            # STEP 9: Optional debug checks
            # --------------------------------------------------

            # --------------------------------------------------
            # STEP 10: Store simulation result for this student
            # --------------------------------------------------
            results.append(
                {
                    "id": student.agent_id,
                    "type": student.agent_type,
                    "activity": student.state,
                    "destination": student.destination_room,
                    "current_room": actual_current_room,
                    "path": student.path,
                    "bath_done": student.has_finished_bathroom,
                    "returned_to_dorm": student.has_returned_from_bathroom,
                    "prep_start": student.preparation_start_time,
                    "prep_finish": student.preparation_finish_time,
                    "wake_up_time": student.wake_up_time,
                    "bathroom_start_time": student.bathroom_start_time,
                    "bathroom_finish_time": student.bathroom_finish_time,
                    "return_dorm_time": student.return_dorm_time,
                    "leave_dorm_time": student.leave_dorm_time,
                    "arrive_outside_time": student.arrive_outside_time,
                }
            )

    # --------------------------------------------------
    # STEP 11: Apply queueing after all student movements
    # --------------------------------------------------
    results = apply_queueing(results, building)

    return results


# -------------------------
# OUTPUT FUNCTIONS
# -------------------------
def print_simulation_results(current_time, results):
    print(f"\nTIME: {current_time}")
    print("-" * 110)
    print(
        f"{'ID':<8} {'TYPE':<12} {'ACTIVITY':<15} "
        f"{'DESTINATION':<15} {'CURRENT ROOM':<15} {'PATH'}"
    )
    print("-" * 110)

    for result in results:
        print(
            f"{result['id']:<8} "
            f"{result['type']:<12} "
            f"{result['activity']:<15} "
            f"{result['destination']:<15} "
            f"{result['current_room']:<15} "
            f"{' -> '.join(result['path'])}"
        )


# -------------------------
# EXPORT FUNCTIONS
# -------------------------
def export_occupancy_to_csv(occupancy_series, filename):
    if not occupancy_series:
        return

    fieldnames = occupancy_series[0].keys()

    with open(filename, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for row in occupancy_series:
            writer.writerow(row)

    print(f"\nOccupancy schedule exported to {filename}")


# -------------------------
# TEST SECTION
# -------------------------
if __name__ == "__main__":

    occupancy_series, students = run_occupancy_time_series(
    start_time="04:00",
    end_time="23:00",
    simulation_step=1,
    reporting_step=30
)

    # -------------------------
    # OCCUPANCY TABLE
    # -------------------------
    key_rooms = [
        "time",
        "D101",
        "D102",
        "D201",
        "D202",
        "D203",
        "S101",
        "R101",
        "B101",
        "B201",
        "C105",
        "C205",
        "ST101",
        "ST102",
        "ST201",
        "ST202",
        "ST301",
        "ST302",
        "OUTSIDE",
    ]

    print("\t".join(key_rooms + ["TOTAL"]))

    for row in occupancy_series:

        total_students = sum(
            row[room]
            for room in row
            if room != "time"
        )

        print(
            "\t".join(str(row[room]) for room in key_rooms)
            + f"\t{total_students}"
        )

    # -------------------------
    # STUDENT TIMELINE TABLE
    # -------------------------
    print(
        f"{'ID':<8}"
        f"{'WAKE':<8}"
        f"{'BATH_START':<12}"
        f"{'BATH_END':<10}"
        f"{'PREP_START':<12}"
        f"{'PREP_END':<10}"
        f"{'LEAVE':<8}"
        f"{'OUTSIDE':<8}"
        f"{'TRAVEL':<8}"
    )

    for student in students:

        travel_time = None

        if (
            student.leave_dorm_time is not None
            and student.arrive_outside_time is not None
        ):
            travel_time = (
                student.arrive_outside_time
                - student.leave_dorm_time
            )

        print(
            f"{student.agent_id:<8}"
            f"{str(minutes_to_time(student.wake_up_time)):<8}"
            f"{str(minutes_to_time(student.bathroom_start_time)):<12}"
            f"{str(minutes_to_time(student.bathroom_finish_time)):<10}"
            f"{str(minutes_to_time(student.preparation_start_time)):<12}"
            f"{str(minutes_to_time(student.preparation_finish_time)):<10}"
            f"{str(minutes_to_time(student.leave_dorm_time)):<8}"
            f"{str(minutes_to_time(student.arrive_outside_time)):<8}"
            f"{str(travel_time):<8}"
        )

    # -------------------------
    # TOP 10 LONGEST BATHROOM WAITS
    # -------------------------
    print("\nTOP 10 LONGEST BATHROOM WAITS")

    waits = []

    for student in students:

        if (
            student.wake_up_time is not None
            and student.bathroom_start_time is not None
        ):

            wait_time = (
                student.bathroom_start_time
                - student.wake_up_time
            )

            waits.append(
                (student.agent_id, wait_time)
            )

    waits.sort(
        key=lambda x: x[1],
        reverse=True
    )

    for student_id, wait in waits[:10]:
        print(student_id, round(wait, 1))

    # -------------------------
    # TOP 10 LONGEST PREP WAITS
    # -------------------------
    print("\nTOP 10 LONGEST PREP WAITS")

    prep_waits = []

    for student in students:

        if (
            student.bathroom_finish_time is not None
            and student.preparation_start_time is not None
        ):

            wait = (
                student.preparation_start_time
                - student.bathroom_finish_time
            )

            prep_waits.append(
                (student.agent_id, wait)
            )

    prep_waits.sort(
        key=lambda x: x[1],
        reverse=True
    )

    for student_id, wait in prep_waits[:10]:
        print(student_id, round(wait, 1))

    # -------------------------
    # TOP 10 LONGEST TRAVEL TIMES
    # -------------------------
    print("\nTOP 10 LONGEST TRAVEL TIMES")

    travel_waits = []

    for student in students:

        if (
            student.leave_dorm_time is not None
            and student.arrive_outside_time is not None
        ):

            wait = (
                student.arrive_outside_time
                - student.leave_dorm_time
            )

            travel_waits.append(
                (student.agent_id, wait)
            )

    travel_waits.sort(
        key=lambda x: x[1],
        reverse=True
    )

    for student_id, wait in travel_waits[:10]:
        print(student_id, round(wait, 1))
        
 