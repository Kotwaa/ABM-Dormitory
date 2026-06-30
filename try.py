# core_abm_module.py
import csv
from building_module import Building
from L_Shaped_Dormitory import create_dormitory
from agent_module import create_students
from schedule_module import get_student_schedule
from movement_module import find_path
from queue_module import apply_queueing
from stochastic_module import wake_up_time
from stochastic_module import bathroom_duration
from stochastic_module import preparation_duration
from stochastic_module import walking_speed
from stochastic_module import morning_study_decision
from stochastic_module import choose_afternoon_activity
from stochastic_module import choose_evening_activity
from stochastic_module import morning_leave_time


# -------------------------
# MOVEMENT HELPER FUNCTIONS
# -------------------------
def can_enter_room(room_id, building, occupancy_counts):
    if room_id == "OUTSIDE":
        return True
    room = building.rooms[room_id]
    current_occupancy = occupancy_counts.get(room_id, 0)
    return current_occupancy < room.capacity


def move_student_one_step(student, building, occupancy_counts):
    path = student.path

    if not path:
        student.state = "arrived"
        return

    if student.current_room.room_id == student.destination_room:
        student.state = "arrived"
        return

    if student.current_room.room_id not in path:
        student.state = "queued"
        return

    current_index = path.index(student.current_room.room_id)

    if current_index >= len(path) - 1:
        student.state = "arrived"
        return

    next_room = path[current_index + 1]

    if can_enter_room(next_room, building, occupancy_counts):
        cur_id = student.current_room.room_id
        occupancy_counts[cur_id] = max(occupancy_counts.get(cur_id, 0) - 1, 0)
        occupancy_counts[next_room] = occupancy_counts.get(next_room, 0) + 1
        student.current_room = building.rooms[next_room]
        student.state = "moving"
    else:
        student.state = "queued"


# -------------------------
# TIME FUNCTIONS
# -------------------------
def time_to_minutes(time_string):
    hour, minute = time_string.split(":")
    return int(hour) * 60 + int(minute)


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


def get_current_schedule_block(schedule, current_time):
    current_minutes = time_to_minutes(current_time)

    for block in schedule:
        start_minutes = time_to_minutes(block.start_time)
        end_minutes = time_to_minutes(block.end_time)
        if start_minutes <= current_minutes < end_minutes:
            return block

    return None


# -------------------------
# OCCUPANCY FUNCTIONS
# -------------------------
def count_room_occupancy(results):
    occupancy_counts = {}
    for result in results:
        room_id = result["current_room"]
        occupancy_counts[room_id] = occupancy_counts.get(room_id, 0) + 1
    return occupancy_counts


def get_all_room_ids():
    building = create_dormitory()
    return list(building.rooms.keys())


# -------------------------
# INITIALIZATION FUNCTIONS
# -------------------------
def initialize_simulation():
    building = create_dormitory()
    dorm_rooms = building.get_rooms_by_type("dormroom")
    students = create_students(
        num_students=132,
        room_list=dorm_rooms,
        students_per_room=12
    )
    schedule = get_student_schedule()
    return building, students, schedule


# -------------------------
# MORNING BEHAVIOR
# -------------------------
def update_morning_behavior(student, building, current_time_minutes):
    scheduled_wake_up_time = time_to_minutes("05:00")
    actual_wake_up_time = scheduled_wake_up_time + student.wake_up_offset

    if student.wake_up_time is None:
        student.wake_up_time = actual_wake_up_time

    if current_time_minutes < actual_wake_up_time:
        student.destination_room = student.assigned_room.room_id
        return

    student_floor = student.assigned_room.floor
    bathrooms = building.get_rooms_by_type("bathroom")
    same_floor_bathrooms = [room for room in bathrooms if room.floor == student_floor]

    if not same_floor_bathrooms:
        student.destination_room = student.assigned_room.room_id
        return

    bathroom_id = same_floor_bathrooms[0].room_id

    if not student.has_finished_bathroom:
        student.destination_room = bathroom_id

    if student.current_room.room_id == bathroom_id:
        if student.bathroom_entry_time is None:
            student.bathroom_entry_time = current_time_minutes
            student.bathroom_start_time = current_time_minutes
            student.bathroom_exit_time = current_time_minutes + bathroom_duration()

        if student.bathroom_exit_time is not None and current_time_minutes >= student.bathroom_exit_time:
            student.has_finished_bathroom = True
            student.bathroom_finish_time = current_time_minutes
        return

    if student.has_finished_bathroom and not student.has_returned_from_bathroom:
        student.destination_room = student.assigned_room.room_id

    if student.current_room.room_id == student.assigned_room.room_id and student.return_dorm_time is None:
        student.has_returned_from_bathroom = True
        student.return_dorm_time = current_time_minutes

    if not student.has_returned_from_bathroom:
        return

    if student.preparation_start_time is None:
        student.preparation_start_time = current_time_minutes
        student.preparation_duration = preparation_duration()
        student.preparation_finish_time = student.preparation_start_time + student.preparation_duration

    if current_time_minutes < student.preparation_finish_time:
        student.destination_room = student.assigned_room.room_id
        return

    if student.morning_leave_time is None:
        student.morning_leave_time = student.preparation_finish_time + student.leave_time_offset

    if current_time_minutes < student.morning_leave_time:
        student.destination_room = student.assigned_room.room_id
        return

    student.destination_room = "OUTSIDE"
    if student.leave_dorm_time is None:
        student.leave_dorm_time = current_time_minutes


# -------------------------
# CORE SIMULATION ENGINE
# -------------------------
def run_simulation(current_time, building, students, schedule, step_minutes):
    current_block = get_current_schedule_block(schedule, current_time)
    current_time_minutes = time_to_minutes(current_time)

    print(current_time, current_block.activity if current_block else "NO BLOCK")

    occupancy_counts = {}
    for s in students:
        room_id = s.current_room.room_id
        occupancy_counts[room_id] = occupancy_counts.get(room_id, 0) + 1

    results = []

    for student in students:
        if current_block:
            student.state = current_block.activity

        if not student.has_completed_morning_routine:
            update_morning_behavior(student, building, current_time_minutes)

        if not student.path or student.path[-1] != student.destination_room:
            path = find_path(building, student.current_room.room_id, student.destination_room)
            if path is None:
                path = [student.current_room.room_id]
            student.path = path

        move_student_one_step(student, building, occupancy_counts)

        actual_current_room = student.current_room.room_id

        if (
            actual_current_room == "OUTSIDE"
            and student.arrive_outside_time is None
            and student.leave_dorm_time is not None
            and current_time_minutes >= student.leave_dorm_time
        ):
            student.arrive_outside_time = current_time_minutes

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
# TIME SERIES DRIVER
# -------------------------
def run_occupancy_time_series(start_time, end_time, step_minutes):
    building, students, schedule = initialize_simulation()
    time_steps = generate_time_steps(start_time, end_time, step_minutes)
    all_room_ids = get_all_room_ids()

    occupancy_series = []
    debug_rows = []

    for time in time_steps:
        results = run_simulation(time, building, students, schedule, step_minutes)

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

        print("Student debug output exported.")

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

        print("Student activity timeline exported.")

    return occupancy_series, students


# -------------------------
# TEST SECTION
# -------------------------
if __name__ == "__main__":
    occupancy_series, students = run_occupancy_time_series(
        start_time="05:00",
        end_time="07:30",
        step_minutes=5
    )

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
        total_students = sum(row[room] for room in row if room != "time")
        print("\t".join(str(row[room]) for room in key_rooms) + f"\t{total_students}")

    print("\nSTUDENT TIMELINE TABLE")
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
        if student.leave_dorm_time is not None and student.arrive_outside_time is not None:
            travel_time = student.arrive_outside_time - student.leave_dorm_time

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