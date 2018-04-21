# HitObject class


class HitObject:
    def __init__(self, start_x, start_y, end_x, end_y, time, object_type):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.time = time
        self.object_type = object_type  # hit_circle, even_repeat_slider, odd_repeat_slider, spinner


# Finds the line number in which the hit objects start.


def find_start(lines):
    line_number = 0
    for x in lines:
        if x == "[HitObjects]":
            return line_number + 1
        line_number += 1


# Converts a line from .osu file into HitObject.


def convert_hit_object(line):
    split_line = line.split(",")
    start_x = int(split_line[0])
    start_y = int(split_line[1])
    end_x = int(split_line[0])
    end_y = int(split_line[1])
    time = int(split_line[2])

    if int(split_line[3]) & 0b1:
        object_type = "hit_circle"
    elif int(split_line[3]) & 0b1000:
        object_type = "spinner"
    elif int(split_line[6]) % 2 == 0:
        object_type = "even_repeat_slider"
    else:
        object_type = "odd_repeat_slider"
        slider_point_list = split_line[5].split("|")
        end_point = slider_point_list[-1].split(":")
        end_x = int(end_point[0])
        end_y = int(end_point[1])

    return HitObject(start_x, start_y, end_x, end_y, time, object_type)


# Finds distance snap by multiplying distance and time of two objects.


def calculate_distance_snap(first_object, second_object):
    first_x = first_object.end_x
    first_y = first_object.end_y
    first_time = first_object.time
    second_x = second_object.start_x
    second_y = second_object.start_y
    second_time = second_object.time
    difference_x = abs(first_x - second_x)
    difference_y = abs(first_y - second_y)
    difference_time = second_time - first_time
    calculation_time = difference_time

    if difference_time < 100:  # 2x bonus for objects unsingletappable (Detected as streams)
        calculation_time = difference_time / 2.0
    elif difference_time < 120:  # For the grey spot around 300bpm which can be either jumps or streams.
        calculation_time = difference_time / (((120 - difference_time) ** 2) / 400.0 + 1)
    calculation_time = 1.0 / calculation_time

    # 1/time has to be used for calculation as smaller time difference means bigger distance snap.
    distance = (difference_x ** 2 + difference_y ** 2) ** 0.5

    return distance * calculation_time


# Calculates weighting of objects.


def calculate_weighting(average_distance, max_distance, distance_snap):
    second_half = max_distance - average_distance  # used to calculate distance snap above the average
    if distance_snap < average_distance:
        raw_weight = (distance_snap / average_distance) / 2.0  # this is the raw weighting, range from 0 to 1
        # if distance snap is under the average, put it somewhere between 0 and 0.5
    else:
        raw_weight = ((distance_snap - average_distance) / second_half) / 2.0 + 0.5
        # if distance snap is above average, put it somewhere between 0.5 and 1

    # spacing below ~0.67 is weighted just as much as spacing above it, so only relatively
    # BIG jumps will make much of a difference
    print (raw_weight * 1.5) ** 1.7
    return (raw_weight * 1.5) ** 1.7


# Calculates nerf/buff based on percentage change from old objects.


def calculate_percentage_change(old_percentage):
    if old_percentage < 0.65:
        # Nerf all maps which reach under 65%.
        # 55% would get around 5% nerf, while 50% would get around 10% nerf.
        return 1 - (((0.65 - old_percentage) ** 1.5) / 0.524)
    else:
        return 1
