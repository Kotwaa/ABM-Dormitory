# stochastic_module.py

import random

def morning_study_decision():
    return random.random() < 0.30

def bathroom_duration(student):

    if student.bathroom_profile == "quick":
        return round(random.triangular(3, 8, 5))

    elif student.bathroom_profile == "long":
        return round(random.triangular(12, 25, 18))

    else:  # normal
        return round(random.triangular(5, 15, 8))


def walking_speed(student):

    if student.walking_profile == "fast":
        speed = random.normalvariate(0.85, 0.05)

    elif student.walking_profile == "slow":
        speed = random.normalvariate(0.45, 0.05)

    else:  # normal
        speed = random.normalvariate(0.70, 0.08)

    return round(max(speed, 0.5), 2)


def wake_up_time(student):

    if student.wake_up_profile == "early":
        offset = random.normalvariate(-5, 4)

    elif student.wake_up_profile == "late":
        offset = random.normalvariate(20, 5)

    else:  # normal
        offset = random.normalvariate(10, 8)

    offset = max(min(offset, 30), -10)

    return round(offset)


def preparation_duration(student):

    if student.preparation_profile == "quick":
        return round(random.triangular(3, 8, 5))

    elif student.preparation_profile == "careful":
        return round(random.triangular(12, 25, 18))

    else:  # normal
        return round(random.triangular(5, 15, 8))


def morning_departure_offset(student):

    if student.departure_profile == "late":
        return round(random.triangular(30, 60, 45))

    elif student.departure_profile == "early":
        return round(random.triangular(-10, 5, 0))

    else:
        return round(random.triangular(0, 20, 8))


#AFTERNOON ACTIVITIES
def arrival_offset(student):

    if student.arrival_profile == "early":
        return random.randint(0, 5)

    elif student.arrival_profile == "normal":
        return random.randint(5, 15)

    else:  # late
        return random.randint(15, 20)

def choose_afternoon_activity():
    choice = random.random()

    if choice < 0.6:
        return "siesta"

    elif choice < 0.8:
        return "study"

    else:
        return "recreation"

def afternoon_departure_offset():
    return round(random.triangular(-10, 15, 5))


# EVENING ACTIVITIES     
def dorm_return_offset():
    return round(random.triangular(-10, 15, 5))

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
