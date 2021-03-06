import sys
import numpy
import hit_object


# Function to calculate the nerf and return it.


def calculate_nerf(osu_file_path):
    # Opening the osu file and splitting it into lines.
    osu_file = open(osu_file_path, "r")
    osu_lines = [line.rstrip('\n') for line in osu_file]

    # Making a separate list with only the lines for the hit objects.
    hit_object_string_list = osu_lines[hit_object.find_start(osu_lines):]
    hit_object_list = map(lambda _hit_object: hit_object.convert_hit_object(_hit_object), hit_object_string_list)

    # If neither of the two objects are a spinner, calculate their distance snap and add it to a list.
    global time_list
    distance_snap_list = []
    time_list = []
    for x in range(len(hit_object_list) - 1):
        if hit_object_list[x].object_type is not "spinner" and hit_object_list[x + 1].object_type is not "spinner":
            distance_snap_list.append(hit_object.calculate_distance_snap(hit_object_list[x], hit_object_list[x + 1]))
            time_list.append(hit_object_list[x].time)
    distance_snap_average = sum(distance_snap_list) / len(distance_snap_list)
    distance_snap_max = max(distance_snap_list)

    # Weighing distance snap based on the objects' raw distance snap compared to the rest of the map.
    global weighted_distance_snap_list
    weighted_distance_snap_list = map(lambda distance_snap:
                                      hit_object.calculate_weighting(distance_snap_average,
                                                                     distance_snap_max,
                                                                     distance_snap),
                                      distance_snap_list)

    # Calculate the final nerf.
    final_nerf = hit_object.calculate_percentage_change(sum(weighted_distance_snap_list)
                                                        / len(weighted_distance_snap_list))

    return final_nerf
