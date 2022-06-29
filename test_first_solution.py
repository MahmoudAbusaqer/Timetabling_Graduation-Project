import json
import random
import math


def load_data(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)

    for university_class in data['Classes']:
        classroom = university_class['Classroom']
        university_class['Classroom'] = data['Classrooms'][classroom]

    classes = data['Classes']
    departments = data['departments']

    return classes, departments


def generate_department_groups(classes_data, departments_data):
    departments = {}
    for single_department in departments_data:
        department = departments_data[single_department]
        department_groups = math.ceil(department / 20)
        dep_group = {}
        for i in range(1, department_groups + 1):
            modules = []
            for single_class in classes_data:
                if single_class['Type'] == "V":
                    for f in single_class["for"]:
                        if f.__contains__(single_department):
                            new_single_class = single_class.copy()
                            new_single_class['for'] = [single_department]
                            modules.append(new_single_class)
                            break
            if single_department[-1] == "m":
                dep_group[f"10{i}"] = modules
            elif single_department[-1] == "f":
                dep_group[f'20{i}'] = modules
        departments[single_department] = dep_group

    return departments


def generate_chromosome(data, departments_data, departments):
    professors = {}
    classrooms = {}
    groups = {}
    subjects = {}
    new_data = []

    number_of_runs = 0

    # department_groups = departments

    # create the chromosome which will reserve 80 places (Genes) for the whole timetable to put the randomly generated
    # value in it, every place consists of a half-hour (Gene)
    for single_class in data:
        if isinstance(single_class['Lecturer'], str):
            professors[single_class['Lecturer']] = [0] * 80
        else:
            for lecturer in single_class['Lecturer']:
                professors[lecturer] = [0] * 80
        for classroom in single_class['Classroom']:
            classrooms[classroom] = [0] * 80
        subjects[single_class['Subject']] = {'P': [], 'V': []}
    for single_group in departments:
        # for single_group in departments.get(single_dep):
        # print(single_group)
        groups[single_group] = [0] * 80

    # theoretical classes
    for single_class in data:
        # new_single_class = single_class.copy()
        class_type = single_class['Type']
        class_length = single_class['Duration']
        number_of_section = 0
        if class_type == "P":
            number_of_students = 0
            for f in single_class["for"]:
                number_of_students += departments_data.get(f)
                # print(departments_data.get(f))
            class_capacity = single_class['Capacity']
            if number_of_students >= class_capacity:
                number_of_section = math.ceil(number_of_students / class_capacity)

                for_group = []
                section_groups = []
                total_number_students = 0
                # for single_depart in single_class["for"]:
                #     for single_group in departments[single_depart]:
                #         for_group.append(f"{single_depart} {single_group}")   # neeeeeed edit
                #         total_number_students += 20
                #         if total_number_students == class_capacity:
                #             section_groups = for_group
                #             for_group = []

                for i in range(1, number_of_section + 1):
                    new_single_class = single_class.copy()
                    print("number_of_section: " + str(i))
                    if new_single_class['Subject'][-1] == "M":
                        new_single_class['Group'] = f"10{i}"
                    elif new_single_class['Subject'][-1] == "F":
                        new_single_class['Group'] = f"20{i}"

                    # new_single_class['For_Group'] = section_groups[i]  # neeeeeed edit

                    classroom = random.choice(single_class['Classroom'])  # get a random classroom from the classrooms
                    new_single_class['assigned_classroom'] = classroom
                    day = random.randrange(0, 5)  # get a random day for this class
                    period = choose_period(day, class_type, class_length)  # get a random period (time) for a class
                    lecturer = new_single_class['Lecturer']
                    if isinstance(lecturer, str):
                        reserve_professor = professors[lecturer]
                    else:
                        try:
                            reserve_professor = professors[lecturer[i - 1]]
                            new_single_class['Lecturer'] = lecturer[i - 1]
                        except:
                            number_of_lecturer = random.randrange(0, len(lecturer))
                            new_single_class['Lecturer'] = lecturer[number_of_lecturer]
                            reserve_professor = professors[lecturer[number_of_lecturer]]

                    reserve_classroom = classrooms[classroom]
                    for single_dep in new_single_class["for"]:
                        reserve_group = groups[single_dep]
                    assign_time(day, period, class_length, class_type, new_single_class, reserve_professor,
                                reserve_classroom, reserve_group, subjects)
                    new_data.append(new_single_class)
                    # For testing output only need to be removed later
                    print(new_single_class)
                    number_of_runs += 1
                    print(str(number_of_runs))
            else:
                new_single_class = single_class.copy()
                for_group = []
                for single_depart in new_single_class["for"]:
                    for single_group in departments[single_depart]:
                        for_group.append(f"{single_depart} {single_group}")
                new_single_class['For_Group'] = for_group
                classroom = random.choice(single_class['Classroom'])  # get a random classroom from the classrooms
                new_single_class['assigned_classroom'] = classroom
                day = random.randrange(0, 5)  # get a random day for this class
                period = choose_period(day, class_type, class_length)  # get a random period (time) for a class
                reserve_professor = professors[new_single_class["Lecturer"]]
                reserve_classroom = classrooms[classroom]
                for single_dep in new_single_class["for"]:
                    reserve_group = groups[single_dep]
                assign_time(day, period, class_length, class_type, new_single_class, reserve_professor,
                            reserve_classroom, reserve_group, subjects)
                if new_single_class['Subject'][-1] == "M":
                    new_single_class['Group'] = "101"
                elif new_single_class['Subject'][-1] == "F":
                    new_single_class['Group'] = "201"

                new_data.append(new_single_class)
                # For testing output only need to be removed later
                print(new_single_class)
                number_of_runs += 1
                print(str(number_of_runs))

    # lap classes
    for single_department in departments:
        for single_group in departments[single_department]:
            for single_class in departments[single_department][single_group]:
                new_single_class = single_class.copy()
                class_type = single_class['Type']
                class_length = single_class['Duration']
                number_of_section = 0
                classroom = random.choice(single_class['Classroom'])  # get a random classroom from the classrooms
                new_single_class['assigned_classroom'] = classroom
                day = random.randrange(0, 5)  # get a random day for this class
                period = choose_period(day, class_type, class_length)  # get a random period (time) for a class
                lecturer = single_class['Lecturer']
                if isinstance(lecturer, str):
                    reserve_professor = professors[lecturer]
                else:
                    try:
                        number_of_lecturer = int(single_group[-1]) - 1
                        reserve_professor = professors[lecturer[number_of_lecturer]]
                        new_single_class['Lecturer'] = lecturer[number_of_lecturer]
                    except:
                        number_of_lecturer = random.randrange(0, len(lecturer))
                        new_single_class['Lecturer'] = lecturer[number_of_lecturer]
                        reserve_professor = professors[lecturer[number_of_lecturer]]

                reserve_classroom = classrooms[classroom]
                # for single_dep in single_class["for"]:
                reserve_group = groups[single_department]
                assign_time(day, period, class_length, class_type, new_single_class, reserve_professor,
                            reserve_classroom, reserve_group, subjects)
                new_single_class['Group'] = single_group

                new_data.append(new_single_class)
                # For testing output only need to be removed later
                print(new_single_class)
                number_of_runs += 1
                print(str(number_of_runs))

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
    # Saturday, Monday and Wednesday classes
    if day == 0 or day == 2 or day == 4:
        # reserve 1 time for the lab classes
        if class_length == "2" and class_type == 'V':
            print("***state 1***")
            time = 16 * day + period
            new_single_class['assigned_time'] = time
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 1)
        # reserve 3 times for the lecture classes with a Length of 3 hours
        elif class_length == "3" and class_type == 'P':
            print("***state 2***")
            time = 16 * 0 + period
            time2 = 16 * 2 + period
            time3 = (16 * 4) + period
            new_single_class['assigned_time'] = time, time2, time3
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 2)
            reserve_time(time2, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 2)
            reserve_time(time3, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 2)
        # reserve 2 times for the lecture classes with a Length of 2 hours
        elif class_length == "2" and class_type == 'P':
            print("***state 3***")
            time = 16 * 0 + period
            time2 = 16 * 4 + period
            new_single_class['assigned_time'] = time, time2
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 3)
            reserve_time(time2, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 3)
        # reserve 1 time for a lecture class that is one hour only
        elif class_length == "1" and class_type == 'P':
            print("***state 6***")
            time = 16 * day + period
            new_single_class['assigned_time'] = time
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 6)

    # Sunday and Thursday classes
    elif day == 1 or day == 3:
        # reserve 1 time for the lab classes
        if class_length == "2" and class_type == 'V':
            print("***state 4***")
            time = 16 * day + period
            new_single_class['assigned_time'] = time
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 1)
        # reserve multiple times (2 times) for a lecture classes
        elif class_length in ("2", "3") and class_type == 'P':
            print("***state 5***")
            time = 16 * 1 + period
            time2 = 16 * 3 + period
            new_single_class['assigned_time'] = time, time2
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 5)
            reserve_time(time2, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 5)
        # reserve 1 time for a lecture class that is one hour only
        elif class_length == "1" and class_type == 'P':
            print("***state 6***")
            time = 16 * day + period
            new_single_class['assigned_time'] = time
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 6)


# reserve the time chosen for all other chromosomes like professors, classrooms, and groups
def reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                 subjects, state):
    if state == 1:
        # print("time= " + str(time))
        for i in range(time, time + 4):
            reserve_professor[i] += 1
            reserve_classroom[i] += 1
            reserve_group[i] += 1
            # if len(reserve_group) == 0:
            #     reserve_group[i] += 1
            # else:
            #     for group in reserve_group:
            #         reserve_group[group][i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['for']))
    elif state == 2 or state == 3 or state == 6:
        for i in range(time, time + 2):
            reserve_professor[i] += 1
            reserve_classroom[i] += 1
            reserve_group[i] += 1
            # if len(reserve_group) == 0:
            #     reserve_group[i] += 1
            # else:
            #     for group in reserve_group:
            #         reserve_group[group][i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['for']))
    elif state == 5:
        for i in range(time, time + 3):
            reserve_professor[i] += 1
            reserve_classroom[i] += 1
            # print(reserve_group)
            # if len(reserve_group) == 0:
            #     reserve_group[i] += 1
            # else:
            # for group in reserve_group:
            reserve_group[i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['for']))


def write_data(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)


def write_data2(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file)


if __name__ == "__main__":
    input_file = 'classes/iug_input v3.json'
    output_file = 'classes/iug_output v3.json'
    chromosome_file = 'classes/chromosome v3.json'
    da = load_data(input_file)
    departments_groups = generate_department_groups(da[0], da[1])
    chromosome = generate_chromosome(da[0], da[1], departments_groups)
    # print(departments_groups)
    # write_data(chromosome[0], output_file)
    # write_data2(chromosome, chromosome_file)
