import Tkinter
import weighted_objects
import tkFileDialog
import time
import ttk
import numpy
import sys

while True:
    # Ask user for file dialog.
    Tkinter.Tk().withdraw()
    osu_file_path = tkFileDialog.askopenfilename(title="Select an osu file", filetypes=(("osu files", "*.osu"),))

    # Calculate final nerf.
    final_nerf = weighted_objects.calculate_nerf(osu_file_path)

    distance_snap_list = weighted_objects.weighted_distance_snap_list
    time_list = weighted_objects.time_list

    # Separate list into multiple lists when breaks exist.
    time_break_separated_list = [[]]
    list_number = 0
    for i in range(len(time_list) - 1):
        if time_list[i + 1] - time_list[i] > 3000:
            # Create new list.
            list_number += 1
            time_break_separated_list.append([])
        time_break_separated_list[list_number].append(time_list[i])

    # Coordinates to be later used in the canvas.
    canvas_distance_snap_list = []
    canvas_time_list = []

    # Calculating coordinates.
    for i in time_list:
        canvas_time_list.append(350 * (i - time_list[0]) / (time_list[-1] - time_list[0]))
    for i in distance_snap_list:
        canvas_distance_snap_list.append(150 - i * 75)

    # Creating the GUI.
    root = Tkinter.Tk()
    root.resizable(width=False, height=False)
    root.geometry("400x500")
    root.title("Weighted Objects")

    # Stuff for the timer.
    ms = time_list[0]
    note_number = 0

    # Function to be used to initialize the timer.

    def first_load():
        # Variable relative_time is the time when the user has clicked the button to start timer.
        global relative_time
        relative_time = int(round(time.time() * 1000)) - time_list[0]
        tick()

    # Function to be used to run the timer.

    def tick():
        # Variable ms is the time that constantly goes up during the timer.
        global ms
        time_label.after(30, tick)
        ms = int(round(time.time() * 1000)) - relative_time
        time_label["text"] = "Timer: {}ms".format(ms)

        update_labels()
        draw_timer_line()


    # Function to be used to update the labels that need constant updates.

    def update_labels():
        global note_number
        # Updates note number depending on where the timer is at.
        for i in range(len(time_list)):
            if ms < time_list[i]:
                note_number = i - 1
                break

        distance_snap_label["text"] = "Weighted: {:.2f}x".format(distance_snap_list[note_number])
        progress_bar["value"] = distance_snap_list[note_number]
        cumulative_label["text"] = "Cumulative Value: {}".format(numpy.cumsum(distance_snap_list)[note_number])


    # Function to be used to draw the green line that indicates where the timer is at.

    def draw_timer_line():
        if ms < time_list[-1]:
            draw_x = 350 * (ms - time_list[0]) / (time_list[-1] - time_list[0])
            difficulty_graph.coords(timer_line, draw_x, 0, draw_x, 150)


    # Function used to kill the GUI.

    def stop():
        root.quit()
        root.destroy()


    # Function used to kill the program entirely.

    def kill():
        sys.exit()

    Tkinter.Label(root, fg="black",
                  text="Old Amount of Objects: {}".format(len(distance_snap_list))).pack()

    Tkinter.Label(root, fg="black",
                  text="New Calculated Weighted Objects: {:.2f}".format(sum(distance_snap_list))).pack()

    Tkinter.Label(root, fg="black",
                  text="Raw Percentage Change: {:.2f}%".format(100 * sum(distance_snap_list)
                                                               / len(distance_snap_list))).pack()

    Tkinter.Label(root, fg="black",
                  text="Calculated Nerf/Buff: {:.2f}%".format(100 * final_nerf)).pack()

    Tkinter.Label(root, fg="blue", text="Graph of Distance Snap/Cumulative Sum of Distance Snap against Time").pack()

    difficulty_graph = Tkinter.Canvas(root, width=350, height=150)
    difficulty_graph.pack()

    Tkinter.Label(root, fg="black", text="Red/Blue: Distance Snap").pack()

    Tkinter.Label(root, fg="black", text="Yellow: Cumulative Sum of Distance Snap").pack()

    # Draw grid lines and fill background
    difficulty_graph.create_rectangle(0, 0, 350, 150, fill="#dddddd")
    difficulty_graph.create_line(0, 30, 350, 30, fill="#cccccc")
    difficulty_graph.create_line(0, 60, 350, 60, fill="#cccccc")
    difficulty_graph.create_line(0, 90, 350, 90, fill="#cccccc")
    difficulty_graph.create_line(0, 120, 350, 120, fill="#cccccc")
    difficulty_graph.create_line(70, 0, 70, 150, fill="#cccccc")
    difficulty_graph.create_line(140, 0, 140, 150, fill="#cccccc")
    difficulty_graph.create_line(210, 0, 210, 150, fill="#cccccc")
    difficulty_graph.create_line(280, 0, 280, 150, fill="#cccccc")

    # Draw blue line graph, distance snap.
    for i in range(len(distance_snap_list) - 1):
        # Don't continue the graph if there is a break.
        if time_list[i + 1] - time_list[i] < 3000:
            difficulty_graph.create_line(canvas_time_list[i], canvas_distance_snap_list[i],
                                         canvas_time_list[i + 1], canvas_distance_snap_list[i + 1],
                                         fill="#9999ff")

    # Draw red line graph, the average thing (what do you call this?).
    for n in range(len(time_break_separated_list)):
        for x in range(len(time_break_separated_list[n]) - 20):
            if n == 0:
                i = x
            else:
                i = x + numpy.cumsum(map(len, time_break_separated_list))[n - 1]

            # Don't continue graph if there's a break.
            if time_list[i + 11] - time_list[i + 10] < 3000:
                difficulty_graph.create_line(canvas_time_list[i + 10], 
                                             sum(canvas_distance_snap_list[i:i + 20]) / 20.0,
                                             canvas_time_list[i + 11],
                                             sum(canvas_distance_snap_list[i + 1:i + 21]) / 20.0,
                                             fill="#990000")
    
    # Draw yellow line graph, cumulative distance snap sum. 
    for i in range(len(distance_snap_list) - 1):
        difficulty_graph.create_line(canvas_time_list[i],
                                     150 - (149 * numpy.cumsum(distance_snap_list)[i] / sum(distance_snap_list)),
                                     canvas_time_list[i + 1],
                                     150 - (149 * numpy.cumsum(distance_snap_list)[i + 1] / sum(distance_snap_list)),
                                     fill="#ffff00")

    timer_line = difficulty_graph.create_line(0, 0, 0, 150, fill="#77ff77")

    time_label = Tkinter.Label(root, fg="black")
    time_label.pack()

    distance_snap_label = Tkinter.Label(root, fg="black")
    distance_snap_label.pack()

    cumulative_label = Tkinter.Label(root, fg="black")
    cumulative_label.pack()

    progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack()
    progress_bar["maximum"] = 2

    Tkinter.Button(root, fg="blue", text="Start Realtime!", command=first_load).pack()

    Tkinter.Button(root, fg="red", text="Choose another map", command=stop).pack()

    # If window is closed, stop the program.
    root.protocol("WM_DELETE_WINDOW", kill)

    root.mainloop()
