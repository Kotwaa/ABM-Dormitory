# stochastic_module.py

import random

def morning_study_decision():
    return random.random() < 0.30

def bathroom_duration():
    return round(random.triangular(5, 8, 15), 2)


def walking_speed():
    speed = random.normalvariate(0.6, 0.2)
    return round(max(speed, 0.5), 2)


def wake_up_time():
    """
    Returns wake-up offset in minutes
    relative to the scheduled wake-up time.
    """
    offset = random.normalvariate(-20, 20)

    # limit wake-up variation to ±30 minutes
    offset = max(min(offset, 30), -30)

    return round(offset)


def preparation_duration():
    return round(random.triangular(5, 8, 12), 2)



def morning_departure_offset():
    return round(random.triangular(-10, 0, 20))

def afternoon_departure_offset():
    return round(random.triangular(-5, 0, 15))

def dorm_return_offset():
    return round(random.triangular(-5, 0, 10))


def morning_leave_time(student):
    return (
        student.preparation_finish_time
        + student.leave_time_offset
    )


#AFTERNOON ACTIVITIES
def arrival_offset():
    return random.randint(0, 20)

def choose_afternoon_activity():
    choice = random.random()

    if choice < 0.6:
        return "siesta"

    elif choice < 0.8:
        return "study"

    else:
        return "recreation"


# EVENING ACTIVITIES     
def choose_evening_activity():
    choice = random.random()

    if choice < 0.6:
        return "dorm"

    elif choice < 0.8:
        return "study"

    else:
        return "recreation"         
              
# -------------------------
# TEST SECTION
# -------------------------
if __name__ == "__main__":
    for i in range(10):

        activity = choose_afternoon_activity()

        if activity == "siesta":
            destination_room = "D201"

        elif activity == "study":
            destination_room = "S101"

        elif activity == "recreation":
            destination_room = "R101"

        print(activity, destination_room)
