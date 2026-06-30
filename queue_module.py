# queue_module.py

from stochastic_module import bathroom_duration


QUEUE_LOCATIONS = {"B101": "C105", "B201": "C205", "B301": "C305"}


def apply_queueing(results, building):
    adjusted_results = []
    room_occupants = {}

    for result in results:
        room_id = result["current_room"]

        if room_id not in room_occupants:
            room_occupants[room_id] = []

        room_occupants[room_id].append(result)

    for room_id, occupants in room_occupants.items():
        room = building.get_room(room_id)
        capacity = room.capacity

        if len(occupants) <= capacity:
            adjusted_results.extend(occupants)
        else:
            admitted = occupants[:capacity]
            overflow = occupants[capacity:]

            adjusted_results.extend(admitted)

            queue_room = QUEUE_LOCATIONS.get(room_id)

            for student_result in overflow:
                if queue_room:
                    student_result["current_room"] = queue_room
                    student_result["state"] = "waiting"
                    student_result["queue_for"] = room_id

                adjusted_results.append(student_result)

    return adjusted_results


def sort_queue_fifo(queue_list):
    return sorted(queue_list, key=lambda student: student["arrival_time"])


def time_to_minutes_decimal(time_string):
    hour, minute = time_string.split(":")
    return int(hour) * 60 + int(minute)


def minutes_decimal_to_time(minutes_decimal):
    hour = int(minutes_decimal // 60)
    minute = int(minutes_decimal % 60)
    second = int(round((minutes_decimal - int(minutes_decimal)) * 60))

    return f"{hour:02d}:{minute:02d}:{second:02d}"


def simulate_fifo_bathroom(bathroom_id, arriving_students, capacity, arrival_time):
    current_time = time_to_minutes_decimal(arrival_time)

    bathroom = []
    queue = []
    event_log = []

    admitted_students = arriving_students[:capacity]
    queued_students = arriving_students[capacity:]

    for student in admitted_students:
        duration = bathroom_duration()
        exit_time = current_time + duration

        bathroom.append({"id": student["id"], "exit_time": exit_time})

        event_log.append(f"{arrival_time}: {student['id']} enters {bathroom_id}")

    for student in queued_students:
        queue.append(student)

        event_log.append(f"{arrival_time}: {student['id']} waits for {bathroom_id}")

    while bathroom:
        bathroom.sort(key=lambda x: x["exit_time"])

        leaving_student = bathroom.pop(0)
        current_time = leaving_student["exit_time"]

        event_log.append(
            f"{minutes_decimal_to_time(current_time)}: "
            f"{leaving_student['id']} leaves {bathroom_id}"
        )

        if queue:
            next_student = queue.pop(0)

            duration = bathroom_duration()
            exit_time = current_time + duration

            bathroom.append({"id": next_student["id"], "exit_time": exit_time})

            event_log.append(
                f"{minutes_decimal_to_time(current_time)}: "
                f"{next_student['id']} enters {bathroom_id}"
            )

    return event_log


# -------------------------
# TEST SECTION
# -------------------------

if __name__ == "__main__":
    arriving_students = []

    for i in range(24):
        arriving_students.append({"id": f"S{i+1:03d}"})

    event_log = simulate_fifo_bathroom(
        bathroom_id="B101",
        arriving_students=arriving_students,
        capacity=20,
        arrival_time="06:00",
    )

    print("\nFIFO BATHROOM EVENT LOG")
    print("-" * 50)

    for event in event_log:
        print(event)
