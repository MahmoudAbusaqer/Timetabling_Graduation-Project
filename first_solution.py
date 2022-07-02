import json
import random


def load_data(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)

    classes = data['Classes']
    departments = data['departments']

    return classes, departments


def generate_chromosome(data, departments):
    professors = {}
    classrooms = {}
    groups = {}
    subjects = {}
    new_data = []

    number_of_runs = 0

    # create the chromosome which will reserve 80 places (Genes) for the whole timetable to put the randomly generated
    # value in it, every place consists of a half-hour (Gene)
    for single_class in data:
        for single_lecture in single_class['Lecturer']:
            professors[single_lecture] = [0] * 80
        for classroom in single_class['Classroom']:
            classrooms[classroom] = [0] * 80
        subjects[single_class['Subject']] = {'P': [], 'V': []}
    for single_group in departments:
        groups[single_group] = [0] * 80

    for single_class in data:
        new_single_class = single_class.copy()
        class_type = single_class['Type']
        class_length = single_class['Duration']
        classroom = random.choice(single_class['Classroom'])  # get a random classroom from the classrooms
        new_single_class['assigned_classroom'] = classroom
        day = random.randrange(0, 5)  # get a random day for this class
        period = choose_period(day, class_type, class_length)  # get a random period (time) for a class
        lecturer = new_single_class['Lecturer']
        for single_lecture in lecturer:
            reserve_professor = professors[single_lecture]
        reserve_classroom = classrooms[classroom]
        for single_dep in new_single_class["for"]:
            reserve_group = groups[single_dep]
        assign_time(day, period, class_length, class_type, new_single_class, reserve_professor,
                    reserve_classroom, reserve_group, subjects)
        new_data.append(new_single_class)
        # For testing output only need to be removed later
        # print(new_single_class)
        # number_of_runs += 1
        # print(str(number_of_runs))

    return new_data, professors, classrooms, groups, subjects


def choose_period(day, class_type, class_length):
    class_length = int(class_length)
    new_period = None
    if day in (0, 2, 4) and class_type == "V":  # lap class
        new_period = random.randrange(0, 15 - class_length)
    elif day in (0, 2, 4) and class_type == "P":  # lecture class
        if class_length == 1:
            new_period = random.randrange(0, 16 - class_length)
        elif class_length == 2:
            new_period = random.randrange(0, 17 - class_length)
        elif class_length == 3:
            new_period = random.randrange(0, 18 - class_length)
    elif day in (1, 3) and class_type == "V":  # lap class
        new_period = random.randrange(0, 15 - class_length)
    elif day in (1, 3) and class_type == "P":  # lecture class
        if class_length == 1:
            new_period = random.randrange(0, 16 - class_length)
        elif class_length == 2 or class_length == 3:
            new_period = random.randrange(0, 17 - class_length)

    return new_period


def assign_time(day, period, class_length, class_type, new_single_class, reserve_professor, reserve_classroom,
                reserve_group, subjects):
    group = new_single_class['Group']
    # Saturday, Monday and Wednesday classes
    if day == 0 or day == 2 or day == 4:
        # reserve 1 time for the lab classes
        if class_length == "2" and class_type == 'V':
            print("***state 1***")
            time = 16 * day + period
            new_single_class['assigned_time'] = [time]
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 1,
                         group)
        # reserve 3 times for the lecture classes with a Length of 3 hours
        elif class_length == "3" and class_type == 'P':
            print("***state 2***")
            time = 16 * 0 + period
            time2 = 16 * 2 + period
            time3 = (16 * 4) + period
            new_single_class['assigned_time'] = time, time2, time3
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 2,
                         group)
            reserve_time(time2, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 2,
                         group)
            reserve_time(time3, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 2,
                         group)
        # reserve 2 times for the lecture classes with a Length of 2 hours
        elif class_length == "2" and class_type == 'P':
            print("***state 3***")
            time = 16 * 0 + period
            time2 = 16 * 4 + period
            new_single_class['assigned_time'] = time, time2
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 3,
                         group)
            reserve_time(time2, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 3,
                         group)
        # reserve 1 time for a lecture class that is one hour only
        elif class_length == "1" and class_type == 'P':
            print("***state 6***")
            time = 16 * day + period
            new_single_class['assigned_time'] = [time]
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 6,
                         group)

    # Sunday and Thursday classes
    elif day == 1 or day == 3:
        # reserve 1 time for the lab classes
        if class_length == "2" and class_type == 'V':
            print("***state 4***")
            time = 16 * day + period
            new_single_class['assigned_time'] = [time]
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 1,
                         group)
        # reserve multiple times (2 times) for a lecture classes
        elif class_length in ("2", "3") and class_type == 'P':
            print("***state 5***")
            time = 16 * 1 + period
            time2 = 16 * 3 + period
            new_single_class['assigned_time'] = time, time2
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 5,
                         group)
            reserve_time(time2, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 5,
                         group)
        # reserve 1 time for a lecture class that is one hour only
        elif class_length == "1" and class_type == 'P':
            print("***state 6***")
            time = 16 * day + period
            new_single_class['assigned_time'] = [time]
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 6,
                         group)


# reserve the time chosen for all other chromosomes like professors, classrooms, and groups
def reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                 subjects, state, group):
    if state == 1:
        # print("time= " + str(time))
        for i in range(time, time + 4):
            reserve_professor[i] += 1
            reserve_classroom[i] += 1
            reserve_group[i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['for'], group))
    elif state == 2 or state == 3 or state == 6:
        for i in range(time, time + 2):
            reserve_professor[i] += 1
            reserve_classroom[i] += 1
            reserve_group[i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['for'], group))
    elif state == 5:
        for i in range(time, time + 3):
            reserve_professor[i] += 1
            reserve_classroom[i] += 1
            reserve_group[i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['for'], group))


def write_data(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)


def write_data2(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file)


if __name__ == "__main__":
    input_file = 'classes/2nd iug_input v4 first_solution.json'
    output_file = 'classes/iug_output v4.json'
    chromosome_file = 'classes/chromosome v4.json'
    da = load_data(input_file)
    chromosome = generate_chromosome(da[0], da[1])
    write_data(chromosome[0], output_file)
    write_data2(chromosome, chromosome_file)
