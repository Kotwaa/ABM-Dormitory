# schedule_module.py


class ScheduleBlock:
    def __init__(self, start_time, end_time, activity, destination_room):
        self.start_time = start_time
        self.end_time = end_time
        self.activity = activity
        self.destination_room = destination_room


def time_to_minutes(time_string):
    hour, minute = time_string.split(":")
    return int(hour) * 60 + int(minute)


def get_student_schedule():
    return [
        ScheduleBlock("00:00", "05:00", "sleep", "DORM_ROOM"),
        ScheduleBlock("05:00", "06:00", "wake_up", "DORM_ROOM"),
        ScheduleBlock("05:00", "07:00", "bath", "Bathroom"),
        ScheduleBlock("07:00", "08:00", "breakfast", "OUTSIDE"),
        ScheduleBlock("08:00", "12:00", "class", "OUTSIDE"),
        ScheduleBlock("12:00", "13:00", "lunch", "OUTSIDE"),
        ScheduleBlock("13:00", "15:00", "class", "OUTSIDE"),
        ScheduleBlock("15:00", "16:00", "afternoon_free_time", "Dorm"),
        ScheduleBlock("16:00", "17:00", "dinner_prep", "Bathroom"),
        ScheduleBlock("17:00", "18:00", "dinner", "OUTSIDE"),
        ScheduleBlock("18:00", "20:00", "study", "OUTSIDE"),
        ScheduleBlock("20:00", "21:00", "evening_free_time", "Dorm"),
        ScheduleBlock("21:00", "24:00", "sleep", "DORM_ROOM"),
    ]


def get_current_activity(schedule, current_time):
    current_minutes = time_to_minutes(current_time)

    for block in schedule:
        start_minutes = time_to_minutes(block.start_time)
        end_minutes = time_to_minutes(block.end_time)

        if start_minutes <= current_minutes < end_minutes:
            return block

    return None


# -------------------------
# TEST SECTION
# -------------------------
if __name__ == "__main__":

    student_schedule = get_student_schedule()

    print("\nSTUDENT SCHEDULE")
    print("-" * 75)
    print(f"{'START':<10}" f"{'END':<10}" f"{'ACTIVITY':<25}" f"{'DESTINATION'}")
    print("-" * 75)

    for block in student_schedule:
        print(
            f"{block.start_time:<10}"
            f"{block.end_time:<10}"
            f"{block.activity:<25}"
            f"{block.destination_room}"
        )

    print("-" * 75)

    test_time = "05:30"
    current_block = get_current_activity(student_schedule, test_time)

    print(f"\nTIME: {test_time}")

    if current_block:
        print(f"CURRENT ACTIVITY: {current_block.activity}")
        print(f"DESTINATION: {current_block.destination_room}")
    else:
        print("No scheduled activity.")

    print("BEFORE MOVEMENT")
