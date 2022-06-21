import json
import random
import cost_functions


def load_data(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)

    for university_class in data['Classes']:
        classroom = university_class['Classroom']
        university_class['Classroom'] = data['Classrooms'][classroom]

    data = data['Classes']

    return data


def generate_chromosome(data):
    professors = {}
    classrooms = {}
    groups = {}
    subjects = {}

    new_data = []

    number_of_runs = 0

    # create the chromosome which will reserve 80 places (Genes) for the whole timetable to put the randomly generated
    # value in it, every place consists of a half-hour (Gene)
    for single_class in data:
        professors[single_class['Lecturer']] = [0] * 80
        for classroom in single_class['Classroom']:
            classrooms[classroom] = [0] * 80
        for group in single_class['Group']:
            groups[group] = [0] * 80
        subjects[single_class['Subject']] = {'P': [], 'V': [], 'L': []}  # need edit (2 needed)

    for single_class in data:
        new_single_class = single_class.copy()
        classroom = random.choice(
            single_class['Classroom'])  # get a random classroom from the classrooms for this class
        day = random.randrange(0, 5)  # get a random day for this class
        period = random.randrange(0, 17 - int(single_class['Duration']))  # get a random period (time) for this class

        # create a new variable called assigned_classroom (zadata_ucionica) to store the initial assigned classroom to the class
        new_single_class['assigned_classroom'] = classroom
        all_times = []  # To store the times reserved for this class
        class_length = single_class['Duration']

        reserve_professor = professors[new_single_class['Lecturer']]
        reserve_classroom = classrooms[classroom]
        reserve_group = groups

        # Saturday, Monday and Wednesday classes
        if day == 0 or day == 2 or day == 4:
            # reserve 1 time for the lab classes
            if single_class['Duration'] == "2" and single_class['Type'] == 'V':
                print("***state 1***")
                time = 16 * day + period
                new_single_class['assigned_time'] = time
                reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                             subjects)

            # reserve 3 times for the lecture classes with a Length of 3 hours
            elif class_length == "3" and single_class['Type'] == 'P':
                print("***state 2***")

                time = 16 * 0 + period
                time2 = 16 * 2 + period
                time3 = (16 * 4) + period
                all_times.append(time)
                all_times.append(time2)
                all_times.append(time3)
                new_single_class['assigned_time'] = all_times

                reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                             subjects)
                reserve_time(time2, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                             subjects)
                reserve_time(time3, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                             subjects)

            # reserve 2 times for the lecture classes with a Length of 2 hours
            elif single_class['Duration'] == "2" and single_class['Type'] == 'P':
                print("***state 3***")

                time = 16 * 0 + period
                time2 = 16 * 4 + period

                all_times.append(time)
                all_times.append(time2)
                new_single_class['assigned_time'] = all_times

                reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                             subjects)
                reserve_time(time2, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                             subjects)

            # reserve 1 time for a lecture class that is one hour only
            elif class_length == "1" and single_class['Type'] == 'P':
                print("***state 6***")
                time = 16 * day + period
                new_single_class['assigned_time'] = time
                reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                             subjects)

        # Sunday and Thursday classes
        elif day == 1 or day == 3:
            # reserve 1 time for the lab classes
            if class_length == "2" and single_class['Type'] == 'V':
                print("***state 4***")
                time = 16 * day + period
                new_single_class['assigned_time'] = time
                reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                             subjects)

            # reserve multiple times (2 times) for a lecture classes
            elif class_length in ("2", "3") and single_class['Type'] == 'P':
                print("***state 5***")

                time = 16 * 1 + period
                time2 = 16 * 3 + period
                all_times.append(time)
                all_times.append(time2)
                new_single_class['assigned_time'] = all_times

                reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                             subjects)
                reserve_time(time2, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                             subjects)

            # reserve 1 time for a lecture class that is one hour only
            elif class_length == "1" and single_class['Type'] == 'P':
                print("***state 6***")
                time = 16 * day + period
                new_single_class['assigned_time'] = time
                reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                             subjects)

        new_data.append(new_single_class)
        # print(str(new_single_class))
        number_of_runs += 1
        print(str(number_of_runs))
    return new_data, professors, classrooms, groups, subjects


# reserve the time chosen for all other chromosomes like professors, classrooms, and groups
def reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects):
    for i in range(time, time + int(class_length)):
        reserve_professor[i] += 1
        reserve_classroom[i] += 1
        for group in reserve_group:
            reserve_group[group][i] += 1
    subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['Group']))


def write_data(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)


if __name__ == "__main__":
    input_file = 'classes/iug_input1.json'
    output_file = 'classes/iug_output.json'
    da = load_data(input_file)
    chromosome = generate_chromosome(da)
    # cost = cost_functions.cost(chromosome)
    # print("Cost = " + str(cost))
    write_data(chromosome[0], output_file)
