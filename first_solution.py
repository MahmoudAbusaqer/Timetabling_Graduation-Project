import json
import random
import cost_functionsNEW

def load_data(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)

    classes = data['Classes']
    departments = data['departments']
    depart_groups = data['department_groups']

    return classes, departments, depart_groups


def generate_chromosome(data, departments, depart_groups):
    professors = {}
    classrooms = {}
    groups = {}
    department_groups = {}
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
    for single_depart_groups in depart_groups:
        department_groups[single_depart_groups] = [0] * 80

    for single_class in data:
        new_single_class = single_class.copy()
        class_type = single_class['Type']
        class_length = single_class['Duration']
        classroom = random.choice(single_class['Classroom'])  # get a random classroom from the classrooms
        new_single_class['assigned_classroom'] = classroom
        day = random.randrange(0, 5)  # get a random day for this class
        period = choose_period(day, class_type, class_length)  # get a random period (time) for a class
        lecturer = new_single_class['Lecturer']
        reserve_group = []
        reserve_department_groups = []
        for single_lecture in lecturer:
            reserve_professor = professors[single_lecture]
        reserve_classroom = classrooms[classroom]
        for single_for in new_single_class['for']:
            reserve_group.append(groups[single_for])
        # print("reserve_group: " + str(reserve_group))
        if new_single_class['Type'] == "V":
            for single_dep in new_single_class["for"]:
                reserve_department_groups.append(department_groups[f"{single_dep} {new_single_class['Group']}"])
        elif new_single_class['Type'] == "P":
            for single_dep in new_single_class["For_Group"]:
                reserve_department_groups.append(department_groups[single_dep])
            # print("reserve_department_groups: " + str(reserve_department_groups))
        assign_time(day, period, class_length, class_type, new_single_class, reserve_professor,
                    reserve_classroom, reserve_group, reserve_department_groups, subjects)
        new_data.append(new_single_class)
        # For testing output only need to be removed later
        # print(new_single_class)
        # number_of_runs += 1
        # print(str(number_of_runs))

    return new_data, professors, classrooms, groups, department_groups, subjects


def choose_period(day, class_type, class_length):
    class_length = int(class_length)
    lap_periods = [0, 2, 4, 6, 8, 10, 12]
    sat_mon_wed = [0, 2, 4, 6, 8, 10, 12, 14]
    sun_tue = [0, 3, 9, 12]
    new_period = None
    if class_type == "V":  # lap class
        new_period = random.choice(lap_periods)
    elif day in (0, 2, 4) and class_type == "P":  # lecture class
        new_period = random.choice(sat_mon_wed)
    elif day in (1, 3) and class_type == "P":  # lecture class
        if class_length == 1 or class_length == 2:
            new_period = random.choice(sat_mon_wed)
        elif class_length == 3:
            new_period = random.choice(sun_tue)

    return new_period


def assign_time(day, period, class_length, class_type, new_single_class, reserve_professor, reserve_classroom,
                reserve_group, reserve_department_groups, subjects):
    group = new_single_class['Group']
    # Saturday, Monday and Wednesday classes
    if day == 0 or day == 2 or day == 4:
        # reserve 1 time for the lab classes
        if class_length == "2" and class_type == 'V':
            print("***state 1***")
            time = 16 * day + period
            new_single_class['assigned_time'] = [time]
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 1,
                         group, reserve_department_groups)
        # reserve 3 times for the lecture classes with a Length of 3 hours
        elif class_length == "3" and class_type == 'P':
            print("***state 2***")
            time = 16 * 0 + period
            time2 = 16 * 2 + period
            time3 = (16 * 4) + period
            new_single_class['assigned_time'] = time, time2, time3
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 2,
                         group, reserve_department_groups)
            reserve_time(time2, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 2,
                         group, reserve_department_groups)
            reserve_time(time3, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 2,
                         group, reserve_department_groups)
        # reserve 2 times for the lecture classes with a Length of 2 hours
        elif class_length == "2" and class_type == 'P':
            print("***state 3***")
            time = 16 * 0 + period
            time2 = 16 * 4 + period
            new_single_class['assigned_time'] = time, time2
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 3,
                         group, reserve_department_groups)
            reserve_time(time2, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 3,
                         group, reserve_department_groups)
        # reserve 1 time for a lecture class that is one hour only
        elif class_length == "1" and class_type == 'P':
            print("***state 6***")
            time = 16 * day + period
            new_single_class['assigned_time'] = [time]
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 6,
                         group, reserve_department_groups)

    # Sunday and Thursday classes
    elif day == 1 or day == 3:
        # reserve 1 time for the lab classes
        if class_length == "2" and class_type == 'V':
            print("***state 4***")
            time = 16 * day + period
            new_single_class['assigned_time'] = [time]
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 1,
                         group, reserve_department_groups)
        # reserve multiple times (2 times) for a lecture classes
        elif class_length in ("2", "3") and class_type == 'P':
            print("***state 5***")
            time = 16 * 1 + period
            time2 = 16 * 3 + period
            new_single_class['assigned_time'] = time, time2
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 5,
                         group, reserve_department_groups)
            reserve_time(time2, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 5,
                         group, reserve_department_groups)
        # reserve 1 time for a lecture class that is one hour only
        elif class_length == "1" and class_type == 'P':
            print("***state 6***")
            time = 16 * day + period
            new_single_class['assigned_time'] = [time]
            reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects, 6,
                         group, reserve_department_groups)


# reserve the time chosen for all other chromosomes like professors, classrooms, and groups
def reserve_time(time, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                 subjects, state, group, reserve_department_groups):
    if state == 1:
        # print("time= " + str(time))
        for i in range(time, time + 4):
            reserve_professor[i] += 1
            reserve_classroom[i] += 1
            for single_group in reserve_group:
                single_group[i] += 1
            for single_department_groups in reserve_department_groups:
                single_department_groups[i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['for'], group))
    elif state == 2 or state == 3 or state == 6:
        for i in range(time, time + 2):
            reserve_professor[i] += 1
            reserve_classroom[i] += 1
            for single_group in reserve_group:
                single_group[i] += 1
            for single_department_groups in reserve_department_groups:
                single_department_groups[i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['for'], group))
    elif state == 5:
        for i in range(time, time + 3):
            reserve_professor[i] += 1
            reserve_classroom[i] += 1
            for single_group in reserve_group:
                single_group[i] += 1
            for single_department_groups in reserve_department_groups:
                single_department_groups[i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['for'], group))


def write_data(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)


def write_data2(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file)

if __name__ == "__main__":
    input_file = 'classes/2nd iug_input v4 first_solution v12.json'
    # output_file = 'classes/iug_output v11.json'
    chromosome_file = 'classes/chromosome new input data 31.json'
    da = load_data(input_file)
    chromosome = generate_chromosome(da[0], da[1], da[2])
    # write_data(chromosome[0], output_file)
    write_data2(chromosome, chromosome_file)

    # cost_function = cost_functionsNEW.cost
    # ft = cost_function(chromosome)
