import json


def load_data(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)
    return data


def cost(chromosome):
    """
    Cost function for all hard constraints and soft constraint regarding preferred order. All parameters are empirical.
    :param chromosome: Timetable for which we are calculating the cost function.
    :return: Value of cost
    """
    prof_cost = 0
    classrooms_cost = 0
    groups_cost = 0
    subjects_cost = 0

    # Traverse all classes for hard constraints
    for single_class in chromosome[0]:
        # print(single_class)
        if single_class['Type'] == "V":
            length = 4
        elif (single_class['Type']) == "P" and (single_class['Duration']) == "3" and (
                single_class['assigned_time'][0]) <= 15:
            length = 2
        elif (single_class['Type']) == "P" and (single_class['Duration']) == "3" and (
                single_class['assigned_time'][0]) > 15:
            length = 3
        elif (single_class['Type']) == "P" and ((single_class['Duration']) == "2" or (single_class['Duration']) == "1"):
            length = 2

        time = single_class['assigned_time']  # the initial assigned time to the class
        # print(single_class)
        for t in time:
            for i in range(t, (t + length)):
                for Lecturer in single_class['Lecturer']:
                    if chromosome[1][Lecturer][i] > 1:
                        prof_cost += 1
                if chromosome[2][single_class['assigned_classroom']][i] > 1:
                    classrooms_cost += 1
                if single_class['Type'] == "V":
                    for single_group in single_class['for']:
                        if chromosome[4][f"{single_group} {single_class['Group']}"][i] > 1:
                            groups_cost += 1
                elif single_class['Type'] == "P":
                    for single_group in single_class['For_Group']:
                        if chromosome[4][single_group][i] > 1:
                            groups_cost += 1

    # print(prof_cost)
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
    # print(prof_cost)
    return prof_cost,  classrooms_cost, groups_cost

    # return prof_cost + classrooms_cost + groups_cost + round(subjects_cost, 4)
    # if __name__ == "__main__":
    #     data = dt.load_data(input_file)
    #     #neighbour = mutationModifed.neighbour
    #     chromosome = dt.generate_chromosome(data)
    #     #new_chromosome = neighbour(deepcopy(chromosome))
    #     ft = cost(chromosome)
    #     print(ft)
    #     #ftn = cost(new_chromosome)
    # print(ftn)

    """
        Soft constraint not important yet
    """


def cost2(chromosome):
    """
    Cost function for all hard constraints and all soft constraints. All parameters are empirical.
    :param chromosome: Timetable for which we are calculating the cost function.
    :return: Value of cost
    """
    groups_empty = 0
    prof_empty = 0
    load_groups = 0
    load_prof = 0

    # Call function for calculating cost for hard constratins and soft constraint regarding preferred order
    original_cost = cost(chromosome)

    # Calculating idleness and load for groups
    for group in chromosome[4]:
        for day in range(5):
            last_seen = 0
            found = False
            current_load = 0
            for hour in range(16):
                time = day * 16 + hour
                if chromosome[4][group][time] >= 1:
                    current_load += 1
                    if not found:
                        found = True
                    else:
                        groups_empty += (time - last_seen - 1) / 500
                    last_seen = time
            if current_load > 6:
                load_groups += 0.005

    # Calculating idleness and load for professors
    for prof in chromosome[1]:
        for day in range(5):
            last_seen = 0
            found = False
            current_load = 0
            for hour in range(16):
                time = day * 16 + hour
                if chromosome[1][prof][time] >= 1:
                    current_load += 1
                    if not found:
                        found = True
                    else:
                        prof_empty += (time - last_seen - 1) / 2000
                    last_seen = time
            if current_load > 6:
                load_prof += 0.0025

    return original_cost, round(groups_empty, 3), round(prof_empty, 3), round(load_prof, 3), round(load_groups, 3)

if __name__ == "__main__":
    # chromosome_file = 'classes/chromosome new input data.json'
    chromosome_file = 'classes/chromosome new input data 31.json'
    chromosome = load_data(chromosome_file)

    print("Calculating the fitness value of the hard constraints...")
    result = cost(chromosome)
    print("Lecturer Fitness: " + str(result[0]))
    print("Classroom Fitness: " + str(result[1]))
    print("Departments Groups Fitness: " + str(result[2]))

    print("Calculating the fitness value of the soft constraints...")
    result = cost2(chromosome)
    print("Departments Groups empty Fitness: " + str(result[1]))
    print("Lecturer empty Fitness: " + str(result[2]))
    print("Lecturer Load Fitness: " + str(result[3]))
    print("Departments Groups Load Fitness: " + str(result[4]))