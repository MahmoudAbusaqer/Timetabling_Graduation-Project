def cost(chromosome):
    """
    Cost function for all hard constraints and soft constraint regarding preferred order. All parameters are empirical.
    :param chromosome: Timetable for which we are calculating the cost function.
    :return: Value of cost
    """
    prof_cost = 0
    classrooms_cost = 0
    # groups_cost = 0
    subjects_cost = 0

    # Traverse all classes for hard constraints
    for single_class in chromosome[0]:
        time = single_class['assigned_time']  # the initial assigned time to the class
        class_length = single_class['Duration']

        # Check hard constraint violation in classes time frame
        for i in range(time, time + int(class_length)):
            # check if in the current class time have more than 1 professor
            if chromosome[1][single_class['Lecturer']][i] > 1:
                prof_cost += 1
            # check if in the current class time have more than 1 classroom
            if chromosome[2][single_class['assigned_classroom']][i] > 1:
                classrooms_cost += 1
            # check if in the current class time have more than 1 group
            # for group in single_class['Group']:
            #     if chromosome[3][group][i] > 1:
            #         groups_cost += 1

    """
        Soft constraint not important yet
    """
    # Traverse all classes for soft constraint regarding preferred order
    # for single_class in chromosome[4]:
    #     for lab in chromosome[4][single_class]['L']:  # L -> Lap
    #         for practice in chromosome[4][single_class]['V']:  # V -> practice
    #             for grupa in lab[1]:
    #                 if grupa in practice[1] and lab[0] < practice[0]: # If lab is before practical
    #                     subjects_cost += 0.0025
    #         for lecture in chromosome[4][single_class]['P']:  # P -> lecture
    #             for grupa in lab[1]:
    #                 if grupa in lecture[1] and lab[0] < lecture[0]:  # If lab is before lecture
    #                     subjects_cost += 0.0025
    #     for practice in chromosome[4][single_class]['V']:
    #         for lecture in chromosome[4][single_class]['P']:
    #             for grupa in practice[1]:
    #                 if grupa in lecture[1] and practice[0] < lecture[0]: # If practical is before lecture
    #                     subjects_cost += 0.0025

    return prof_cost + classrooms_cost + round(subjects_cost, 4)
    # return prof_cost + classrooms_cost + groups_cost + round(subjects_cost, 4)

    """
        Soft constraint not important yet
    """
# def cost2(chromosome):
#     """
#     Cost function for all hard constraints and all soft constraints. All parameters are empirical.
#     :param chromosome: Timetable for which we are calculating the cost function.
#     :return: Value of cost
#     """
#     groups_empty = 0
#     prof_empty = 0
#     load_groups = 0
#     load_prof = 0
#
#     # Call function for calculating cost for hard constratins and soft constraint regarding preferred order
#     original_cost = cost(chromosome)
#
#     # Calculating idleness and load for groups
#     for group in chromosome[3]:
#         for day in range(5):
#             last_seen = 0
#             found = False
#             current_load = 0
#             for hour in range(12):
#                 time = day * 12 + hour
#                 if chromosome[3][group][time] >= 1:
#                     current_load += 1
#                     if not found:
#                         found = True
#                     else:
#                         groups_empty += (time - last_seen - 1) / 500
#                     last_seen = time
#             if current_load > 6:
#                 load_groups += 0.005
#
#     # Calculating idleness and load for professors
#     for prof in chromosome[1]:
#         for day in range(5):
#             last_seen = 0
#             found = False
#             current_load = 0
#             for hour in range(12):
#                 time = day * 12 + hour
#                 if chromosome[1][prof][time] >= 1:
#                     current_load += 1
#                     if not found:
#                         found = True
#                     else:
#                         prof_empty += (time - last_seen - 1) / 2000
#                     last_seen = time
#             if current_load > 6:
#                 load_prof += 0.0025
#
#     return original_cost + round(groups_empty, 3) + round(prof_empty, 5) + round(load_prof, 3) + round(load_groups, 4)