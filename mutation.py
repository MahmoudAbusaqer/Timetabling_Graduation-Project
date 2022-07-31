import random
import json
import cost_functions
from copy import deepcopy
from first_solution import write_data2

cost_function = cost_functions.cost
cost_function2 = cost_functions.cost2
max_generations = 10000
num_runs = 1


def neighbour(chromosome):
    """
    Returns a mutated chromosome. The mutation is done by searching for all classes that violate some hard constraint
    (with any resource) and randomly choosing one of them. Then, transfer that class in an unoccupied time frame, in
    one of the allowed classrooms for that class. If there exists no such combination of time frame and classroom,
    transfer the class into a random time frame in one of the allowed classrooms.
    :param chromosome: Current timetable
    :return: Mutated timetable
    """
    candidates = []
    for k in range(len(chromosome[0])):  # Search for all classes violating hard constraints
        for j in range(len(chromosome[2][chromosome[0][k]['assigned_classroom']])):
            if chromosome[2][chromosome[0][k]['assigned_classroom']][j] >= 2:
                candidates.append(k)

        for L in chromosome[0][k]['Lecturer']:
            for z in range(len(chromosome[1][L])):
                if chromosome[1][L][z] >= 2:
                    candidates.append(k)

        if chromosome[0][k]['Type'] == "V":
            for group in chromosome[0][k]['for']:
                for j in range(len(chromosome[3][group])):
                    if chromosome[4][f"{group} {chromosome[0][k]['Group']}"][j] >= 2:
                        candidates.append(k)
        elif chromosome[0][k]['Type'] == "P":
            for group in chromosome[0][k]['For_Group']:
                for j in range(len(chromosome[4][group])):
                    if chromosome[4][group][j] >= 2:
                        candidates.append(k)

    if not candidates:
        i = random.randrange(len(chromosome[0]))
    else:
        i = random.choice(candidates)
    # give the length time to the subjects accordaing to its duration and type
    if chromosome[0][i]['Type'] == "V":
        length = 4
    elif (chromosome[0][i]['Type']) == "P" and (chromosome[0][i]['Duration']) == "3" and (
    chromosome[0][i]['assigned_time'][0]) <= 15:
        length = 2
    elif (chromosome[0][i]['Type']) == "P" and (chromosome[0][i]['Duration']) == "3" and (
    chromosome[0][i]['assigned_time'][0]) > 15:
        length = 3
    elif (chromosome[0][i]['Type']) == "P" and (
            (chromosome[0][i]['Duration']) == "2" or (chromosome[0][i]['Duration']) == "1"):
        length = 2
    # Remove that class from its time frame and classroom 

    for t in chromosome[0][i]['assigned_time']:
        for j in range(t, (t + length)):
            # access the number of items in this object in the chromosome and decrease it by one to free up the place
            for Lecturer in chromosome[0][i]['Lecturer']:
                if chromosome[1][Lecturer][j] != 0:
                    chromosome[1][Lecturer][j] -= 1
            if chromosome[2][chromosome[0][i]['assigned_classroom']][j] != 0:
                chromosome[2][chromosome[0][i]['assigned_classroom']][j] -= 1
            # i added an if below to prevent him from accessing the 0 item and decrease it
            if chromosome[0][i]['Type'] == "V":
                for group in chromosome[0][i]['for']:
                    if chromosome[4][f"{group} {chromosome[0][i]['Group']}"][j] != 0:
                        chromosome[4][f"{group} {chromosome[0][i]['Group']}"][j] -= 1
            elif chromosome[0][i]['Type'] == "P":
                for group in chromosome[0][i]['For_Group']:
                    if chromosome[4][group][j] != 0:
                        chromosome[4][group][j] -= 1

    for t in range(len(chromosome[0][i]['assigned_time'])):
        chromosome[5][chromosome[0][i]['Subject']][chromosome[0][i]['Type']].remove(
            ([chromosome[0][i]['assigned_time'][t], chromosome[0][i]['for'], chromosome[0][i]['Group']]))
    # Find a free time and place
    # print(chromosome[0][i]['Type'])
    found = False
    pairs = []
    # iterate over the 80 objects (gene) and get the allowed class from the generated timetable
    # and check if it can be held in this classroom if not continue to the next iteration in the loop
    for classroom in chromosome[2]:
        c = 0  # the free length time for the class
        # If class can't be held in this classroom
        if classroom not in chromosome[0][i]['Classroom']:
            continue
        for k in range(len(chromosome[2][classroom])):
            # check if the classroom is not taken at this time and the start and end time within the day
            # every day consist of 16 gens
            if chromosome[2][classroom][k] == 0 and k % 16 + length <= 16:
                c += 1
                # If we found x consecutive hours where x is length of our class
                # if we found the length of k is free to reserve the time and classroom
                if c == length and (chromosome[0][i]['Type']) == "V" or (
                        (chromosome[0][i]['Type']) == "P" and (chromosome[0][i]['Duration']) == "1"):
                    time = k + 1 - c
                    times = []
                    times.append(time)
                    pairs.append((times, classroom))
                    found = True
                    c = 0
                elif c == length and length == 2 and (chromosome[0][i]['Type']) == "P" and (
                chromosome[0][i]['Duration']) == "3" and k < 15:
                    time1 = k + 1 - c
                    time2 = (k + 1 - c) + 32
                    time3 = (k + 1 - c) + 64
                    times = []
                    times.append(time1)
                    times.append(time2)
                    times.append(time3)
                    pairs.append((times, classroom))
                    found = True
                    c = 0
                elif c == length and length == 3 and (chromosome[0][i]['Type']) == "P" and (
                        chromosome[0][i]['Duration']) == "3" and 17 < k < 32:
                    time1 = k + 1 - c
                    time2 = (k + 1 - c) + 32
                    if time1 == 16 or 19 or 25 or 28:
                        times = []
                        times.append(time1)
                        times.append(time2)
                        pairs.append((times, classroom))
                        found = True
                    c = 0
                elif c == length and length == 2 and (chromosome[0][i]['Type']) == "P" and (
                chromosome[0][i]['Duration']) == "2" and k < 15:
                    time1 = k + 1 - c
                    time2 = (k + 1 - c) + 64
                    times = []
                    times.append(time1)
                    times.append(time2)
                    pairs.append((times, classroom))
                    found = True
                    c = 0
            else:
                c = 0
    # Find a random time
    if not found:
        classroom = random.choice(chromosome[0][i]['Classroom'])
        day = random.randrange(0, 5)
        period = random.randrange(0, 17 - length)
        if day == 0 or day == 2 or day == 4:
            # reserve 1 time for the lab classes
            if chromosome[0][i]['Duration'] == "2" and chromosome[0][i]['Type'] == 'V':
                times = []
                time = 16 * day + period
                times.append(time)
                chromosome[0][i]['assigned_classroom'] = classroom
                chromosome[0][i]['assigned_time'] = times
            # reserve 3 times for the lecture classes with a Length of 3 hours
            elif chromosome[0][i]['Duration'] == "3" and chromosome[0][i]['Type'] == 'P':
                times = []
                time = 16 * 0 + period
                time2 = 16 * 2 + period
                time3 = (16 * 4) + period
                times.append(time)
                times.append(time2)
                times.append(time3)
                chromosome[0][i]['assigned_classroom'] = classroom
                chromosome[0][i]['assigned_time'] = times
            # reserve 2 times for the lecture classes with a Length of 2 hours
            elif chromosome[0][i]['Duration'] == "2" and chromosome[0][i]['Type'] == 'P':
                times = []
                time = 16 * 0 + period
                time2 = 16 * 4 + period
                times.append(time)
                times.append(time2)
                chromosome[0][i]['assigned_classroom'] = classroom
                chromosome[0][i]['assigned_time'] = times
            # reserve 1 time for a lecture class that is one hour only
            elif chromosome[0][i]['Duration'] == "1" and chromosome[0][i]['Type'] == 'P':
                times = []
                time = 16 * day + period
                times.append(time)
                chromosome[0][i]['assigned_classroom'] = classroom
                chromosome[0][i]['assigned_time'] = times
        # Sunday and Thursday classes
        elif day == 1 or day == 3:
            # reserve 1 time for the lab classes
            if chromosome[0][i]['Duration'] == "2" and chromosome[0][i]['Type'] == 'V':
                times = []
                time = 16 * day + period
                times.append(time)
                chromosome[0][i]['assigned_classroom'] = classroom
                chromosome[0][i]['assigned_time'] = times
            # reserve multiple times (2 times) for a lecture classes
            elif chromosome[0][i]['Duration'] in ("2", "3") and chromosome[0][i]['Type'] == 'P':
                time = 16 * 1 + period
                time2 = 16 * 3 + period
                if time == 16 or 19 or 25 or 28:
                    times = []
                    times.append(time)
                    times.append(time2)
                    chromosome[0][i]['assigned_classroom'] = classroom
                    chromosome[0][i]['assigned_time'] = times
            # reserve 1 time for a lecture class that is one hour only
            elif chromosome[0][i]['Duration'] == "1" and chromosome[0][i]['Type'] == 'P':
                times = []
                time = 16 * day + period
                times.append(time)
                chromosome[0][i]['assigned_classroom'] = classroom
                chromosome[0][i]['assigned_time'] = times

    # Set that class to a new time and place
    if found:
        # get a random pair from pairs and store it in the chromosome
        # print(pairs)
        novo = random.choice(pairs)
        chromosome[0][i]['assigned_classroom'] = novo[1]
        chromosome[0][i]['assigned_time'] = novo[0]
        # add the reserved pair to the rest gens in the chromosome
    for t in chromosome[0][i]['assigned_time']:
        for j in range(t, (t + length)):
            for L in chromosome[0][i]['Lecturer']:
                chromosome[1][L][j] += 1
            chromosome[2][chromosome[0][i]['assigned_classroom']][j] += 1

            if chromosome[0][i]['Type'] == "V":
                for group in chromosome[0][i]['for']:
                    chromosome[4][f"{group} {chromosome[0][i]['Group']}"][j] += 1
            elif chromosome[0][i]['Type'] == "P":
                for group in chromosome[0][i]['For_Group']:
                    chromosome[4][group][j] += 1

    for t in range(len(chromosome[0][i]['assigned_time'])):
        chromosome[5][chromosome[0][i]['Subject']][chromosome[0][i]['Type']].append(
            ([chromosome[0][i]['assigned_time'][t], chromosome[0][i]['for'], chromosome[0][i]['Group']]))
    return chromosome


def load_data2(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)
    return data


"""

Soft Constrains

"""


def neighbour2(chromosome):
    """
    Returns a mutated chromosome. pick two classes at random and swap their places and assigned times. Besides this,
    check if the two classes are compatible for swapping (if they use the same type of classrooms).
    :param: chromosome: Current timetable
    :return: Mutated timetable
    """
    first_index = random.randrange(0, len(chromosome[0]))

    first = chromosome[0][first_index]
    satisfied = False

    if first['Type'] == "V":
        first_length = 4
    elif (first['Type']) == "P" and (first['Duration']) == "3" and (first['assigned_time'][0]) <= 15:
        first_length = 2
    elif (first['Type']) == "P" and (first['Duration']) == "3" and (first['assigned_time'][0]) > 15:
        first_length = 3
    elif (first['Type']) == "P" and ((first['Duration']) == "2" or (first['Duration']) == "1"):
        first_length = 2

    c = 0
    # Find two candidates that can be swapped (constraints are type of classroom and length, because of overlapping days)
    while not satisfied:
        # Return the same chromosome after 100 failed attempts
        if c == 100:
            return chromosome
        second_index = random.randrange(0, len(chromosome[0]))

        second = chromosome[0][second_index]

        if second['Type'] == "V":
            second_length = 4
        elif (second['Type']) == "P" and (second['Duration']) == "3" and (second['assigned_time'][0]) <= 15:
            second_length = 2
        elif (second['Type']) == "P" and (second['Duration']) == "3" and (second['assigned_time'][0]) > 15:
            second_length = 3
        elif (second['Type']) == "P" and ((second['Duration']) == "2" or (second['Duration']) == "1"):
            second_length = 2

        if first['assigned_classroom'] in second['Classroom'] and second['assigned_classroom'] in first['Classroom'] \
                and first['assigned_time'][0] % 16 + second_length <= 16 \
                and second['assigned_time'][0] % 16 + first_length <= 16:
            if first['assigned_time'][-1] + second_length != 80 \
                    and second['assigned_time'][-1] + first_length != 80 \
                    and first != second:
                satisfied = True
        c += 1

    """
    Store the first and second classes in a temp values then swap the values and then store them in the chromosome
    """

    """
    
    """
    # Remove the two classes from their time frames and classrooms
    for t in chromosome[0][i]['assigned_time']:
        for j in range(t, (t + first_length)):
            for Lecturer in first['Lecturer']:
                if chromosome[1][Lecturer][j] != 0:
                    chromosome[1][Lecturer][j] -= 1
            if chromosome[2][first['assigned_classroom']][j] != 0:
                chromosome[2][first['assigned_classroom']][j] -= 1
            # i added an if below to prevent him from accessing the 0 item and decrease it
            if first['Type'] == "V":
                for group in first['for']:
                    if chromosome[4][f"{group} {first['Group']}"][j] != 0:
                        chromosome[4][f"{group} {first['Group']}"][j] -= 1
            elif first['Type'] == "P":
                for group in first['For_Group']:
                    if chromosome[4][group][j] != 0:
                        chromosome[4][group][j] -= 1

    for t in range(len(first['assigned_time'])):
        chromosome[5][first['Subject']][first['Type']].remove(
            ([first['assigned_time'][t], first['for'], first['Group']]))

    for t in chromosome[0][i]['assigned_time']:
        for j in range(t, (t + second_length)):
            for Lecturer in second['Lecturer']:
                if chromosome[1][Lecturer][j] != 0:
                    chromosome[1][Lecturer][j] -= 1
            if chromosome[2][second['assigned_classroom']][j] != 0:
                chromosome[2][second['assigned_classroom']][j] -= 1
            # i added an if below to prevent him from accessing the 0 item and decrease it
            if second['Type'] == "V":
                for group in second['for']:
                    if chromosome[4][f"{group} {second['Group']}"][j] != 0:
                        chromosome[4][f"{group} {second['Group']}"][j] -= 1
            elif second['Type'] == "P":
                for group in second['For_Group']:
                    if chromosome[4][group][j] != 0:
                        chromosome[4][group][j] -= 1

    for t in range(len(second['assigned_time'])):
        chromosome[5][second['Subject']][second['Type']].remove(
            ([second['assigned_time'][t], second['for'], second['Group']]))
    #
    #
    #
    # Swap the times and classrooms
    tmp = first['assigned_time']
    first['assigned_time'] = second['assigned_time']
    second['assigned_time'] = tmp

    tmp_classroom = first['assigned_classroom']
    first['assigned_classroom'] = second['assigned_classroom']
    second['assigned_classroom'] = tmp_classroom

    # Set the classes to new timse and places
    for t in first['assigned_time']:
        for j in range(t, (t + first_length)):
            for L in first['Lecturer']:
                chromosome[1][L][j] += 1
            chromosome[2][first['assigned_classroom']][j] += 1
            if first['Type'] == "V":
                for group in first['for']:
                    chromosome[4][f"{group} {first['Group']}"][j] += 1
            elif first['Type'] == "P":
                for group in first['For_Group']:
                    chromosome[4][group][j] += 1
    for t in range(len(first['assigned_time'])):
        chromosome[5][first['Subject']][first['Type']].append(
            ([first['assigned_time'][t], first['for'], first['Group']]))

    for t in second['assigned_time']:
        for j in range(t, (t + second_length)):
            for Lecturer in second['Lecturer']:
                chromosome[1][Lecturer][j] += 1
            chromosome[2][second['assigned_classroom']][j] += 1
            if second['Type'] == "V":
                for group in second['for']:
                    chromosome[4][f"{group} {second['Group']}"][j] += 1
            elif second['Type'] == "P":
                for group in second['For_Group']:
                    chromosome[4][group][j] += 1
    for t in range(len(second['assigned_time'])):
        chromosome[5][second['Subject']][second['Type']].append(
            ([second['assigned_time'][t], second['for'], second['Group']]))
    return chromosome


if __name__ == "__main__":
    # input_file = 'iug_input2.json'
    output_file = 'classes/outputs/v3/chromosome final 5.json'
    chromosome_file = 'classes/chromosome new input data 31.json'
    best_timetable = None
    chromosome = load_data2(chromosome_file)
    for i in range(num_runs):
        # chromosome = dt.generate_chromosome(data)
        for j in range(max_generations):
            new_chromosome = neighbour(deepcopy(chromosome))
            ft = cost_function(chromosome)
            if j % 1000 == 0 or j == max_generations:
                print("1: At Iteration " + str(j) + " = " + str(ft))
            if ft == 0:
                break
            ftn = cost_function(new_chromosome)
            if ftn <= ft:
                chromosome = new_chromosome
        print("1: At Iteration 10000 = " + str(ft))
        if best_timetable is None or cost_function(chromosome) <= cost_function(best_timetable):
            best_timetable = deepcopy(chromosome)
        chromosome = best_timetable
        for j in range(2*max_generations):
            new_chromosome = neighbour2(deepcopy(chromosome))
            ft = cost_function2(chromosome)
            ftn = cost_function2(new_chromosome)
            if j % 1000 == 0 or j == max_generations:
                print("2: At Iteration " + str(j) + " = " + str(ft))
            if ftn <= ft:
                chromosome = new_chromosome
        print("2: At Iteration 30000 = " + str(ft))
        chromosome
        for j in range(max_generations):
            new_chromosome = neighbour(deepcopy(chromosome))
            ft = cost_function(chromosome)
            if j % 1000 == 0 or j == max_generations:
                print("3: At Iteration " + str(j) + " = " + str(ft))
            if ft == 0:
                break
            ftn = cost_function(new_chromosome)
            if ftn <= ft:
                chromosome = new_chromosome
        print("3: At Iteration 10000 = " + str(ft))
        if best_timetable is None or cost_function(chromosome) <= cost_function(best_timetable):
            best_timetable = deepcopy(chromosome)
        chromosome = best_timetable
    write_data2(chromosome, output_file)
    print("done")
    # ft = cost_function(chromosome)
    # print("cost")
    # print(ft)
