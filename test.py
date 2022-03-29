import json
import random


def load_data(path):
    with open(path, 'r') as read_file:
        data = json.load(read_file)

    for university_class in data['Casovi']:
        classroom = university_class['Ucionica']
        university_class['Ucionica'] = data['Ucionice'][classroom]

    data = data['Casovi']

    return data


def generate_chromosome(data):
    professors = {}
    classrooms = {}
    groups = {}
    subjects = {}

    new_data = []

    # reserve 60 place for the hole timetable to put the random generated value in it
    for single_class in data:
        professors[single_class['Nastavnik']] = [0] * 40
        for classroom in single_class['Ucionica']:
            classrooms[classroom] = [0] * 40
        for group in single_class['Grupe']:
            groups[group] = [0] * 40
        subjects[single_class['Predmet']] = {'P': [], 'V': [], 'L': []}  # need edit (2 needed)

    for single_class in data:
        new_single_class = single_class.copy()
        classroom = random.choice(single_class['Ucionica'])  # get a random classroom from the classrooms for this class
        day = random.randrange(0, 5)  # get a random day for this class
        period = random.randrange(0, 9 - int(single_class['Trajanje']))  # get a random period (time) for this class
        # create a new variable called zadata_ucionica to store the initial assigned classroom to the class
        new_single_class['Zadata_ucionica'] = classroom
        all_times = []  # To store the times reserved for this class
        class_length = single_class['Trajanje']

        # reserve_professor = professors[new_single_class['Nastavnik']]
        # reserve_classroom = classrooms[classroom]
        # reserve_group = groups

        # Saturday, Monday and Wednesday classes
        if day == 0 or day == 2 or day == 4:
            # reserve 1 time for the lab classes
            if single_class['Trajanje'] == "2" and single_class['Tip'] == 'L':
                print("***state 1***")
                time = 9 * day + period
                new_single_class['Zadato_vreme'] = time
                # reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects)
                for i in range(time, time + int(single_class['Trajanje'])):
                    professors[new_single_class['Nastavnik']][i] += 1
                    classrooms[classroom][i] += 1
                    for group in new_single_class['Grupe']:
                        groups[group][i] += 1
                subjects[new_single_class['Predmet']][new_single_class['Tip']].append((time, new_single_class['Grupe']))
            # reserve 3 times for the lecture classes with a Length of 3 hours
            elif class_length == "3" and single_class['Tip'] == 'P':
                print("***state 2***")
                # elif (single_class['Trajanje'] == 3 or single_class['Trajanje'] == 2) and single_class['Tip'] == 'P':
                # all_times = []
                time = 9 * 0 + period
                time2 = 9 * 2 + period
                time3 = (9 * 4) + period
                all_times.append(time)
                all_times.append(time2)
                all_times.append(time3)
                new_single_class['Zadato_vreme'] = all_times
                for i in range(time, time + int(single_class['Trajanje'])):
                    professors[new_single_class['Nastavnik']][i] += 1
                    classrooms[classroom][i] += 1
                    for group in new_single_class['Grupe']:
                        groups[group][i] += 1
                subjects[new_single_class['Predmet']][new_single_class['Tip']].append((time, new_single_class['Grupe']))
                for i in range(time2, time2 + int(single_class['Trajanje'])):
                    professors[new_single_class['Nastavnik']][i] += 1
                    classrooms[classroom][i] += 1
                    for group in new_single_class['Grupe']:
                        groups[group][i] += 1
                subjects[new_single_class['Predmet']][new_single_class['Tip']].append((time, new_single_class['Grupe']))
                for i in range(time3, time3 + int(single_class['Trajanje'])):
                    professors[new_single_class['Nastavnik']][i] += 1
                    classrooms[classroom][i] += 1
                    for group in new_single_class['Grupe']:
                        groups[group][i] += 1
                subjects[new_single_class['Predmet']][new_single_class['Tip']].append((time, new_single_class['Grupe']))
                # reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects)
                # reserve_time(time2, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects)
                # reserve_time(time3, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects)

            # reserve 2 times for the lecture classes with a Length of 2 hours
            elif single_class['Trajanje'] == "2" and single_class['Tip'] == 'P':
                print("***state 3***")

                # elif (single_class['Trajanje'] == 3 or single_class['Trajanje'] == 2) and single_class['Tip'] == 'P':
                # all_times = []
                time = 9 * 0 + period
                time2 = (9 * 4) + period
                print("1 - time = " + str(time))
                print("1- time + int(single_class['Trajanje']) = " + str(time + int(single_class['Trajanje'])))

                all_times.append(time)
                all_times.append(time2)
                new_single_class['Zadato_vreme'] = all_times
                for i in range(time, time + int(single_class['Trajanje'])):
                    increment = 0
                    print("i = " + str(i))
                    print("time2 + i = " + str(time2))
                    professors[new_single_class['Nastavnik']][i] += 1
                    print("before -> professors[new_single_class['Nastavnik']][time2 + i]")
                    x = time2 + increment
                    print("x" + str(x))
                    professors[new_single_class['Nastavnik']][x] += 1
                    print("after -> professors[new_single_class['Nastavnik']][time2 + i] ")
                    # المشكلة انه لما يجي يضيف بضيف في جين خارج حدود الكرموسوم
                    # حل المشكلة بانه لما يجي يختار الوقت ويضيف في الجين انه يضيف ايضا مجموع الساعات لهذا اليوم
                    # مثلا ليوم الاحد لازم نجمع الوقت + يوم السبت كله -> الوقت = 5 و اليوم الاحد -> 5 + 8 = 13
                    classrooms[classroom][i] += 1
                    classrooms[classroom][x] += 1
                    for group in new_single_class['Grupe']:
                        groups[group][i] += 1
                        groups[group][x] += 1

                    increment + 1
                subjects[new_single_class['Predmet']][new_single_class['Tip']].append((time, new_single_class['Grupe']))
                subjects[new_single_class['Predmet']][new_single_class['Tip']].append((time2, new_single_class['Grupe']))
                # print("time2 = " + str(time2))
                # print("time2 + int(single_class['Trajanje']) = " + str(time2 + int(single_class['Trajanje'])))
                # for j in range(time2, time2 + int(single_class['Trajanje'])):
                #     print("j = " + str(j))
                #     professors[new_single_class['Nastavnik']][j] += 1
                #     print("professors[new_single_class['Nastavnik']][time2 + j] = " + str(professors[new_single_class['Nastavnik']][j]))
                #     classrooms[classroom][j] += 1
                #     for group in new_single_class['Grupe']:
                #         groups[group][j] += 1
                # subjects[new_single_class['Predmet']][new_single_class['Tip']].append((time2, new_single_class['Grupe']))
                # reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects)
                # reserve_time(time2, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects)

        # Sunday and Thursday classes
        elif day == 1 or day == 3:
            # reserve 1 time for the lab classes
            if class_length == "2" and single_class['Tip'] == 'L':
                print("***state 4***")
                time = 9 * day + period
                new_single_class['Zadato_vreme'] = time
                for i in range(time, time + int(single_class['Trajanje'])):
                    professors[new_single_class['Nastavnik']][i] += 1
                    classrooms[classroom][i] += 1
                    for group in new_single_class['Grupe']:
                        groups[group][i] += 1
                subjects[new_single_class['Predmet']][new_single_class['Tip']].append((time, new_single_class['Grupe']))
                # reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects)

            # reserve multiple times (2 times) for a lecture classes
            elif class_length in ("2", "3") and single_class['Tip'] == 'P':
                print("***state 5***")
                # elif (single_class['Trajanje'] == 3 or single_class['Trajanje'] == 2) and single_class['Tip'] == 'P':
                # all_times = []
                time = 9 * 1 + period
                time2 = 9 * 3 + period
                all_times.append(time)
                all_times.append(time2)
                new_single_class['Zadato_vreme'] = all_times
                for i in range(time, time + int(single_class['Trajanje'])):
                    professors[new_single_class['Nastavnik']][i] += 1
                    classrooms[classroom][i] += 1
                    for group in new_single_class['Grupe']:
                        groups[group][i] += 1
                subjects[new_single_class['Predmet']][new_single_class['Tip']].append((time, new_single_class['Grupe']))
                for i in range(time2, time2 + int(single_class['Trajanje'])):
                    professors[new_single_class['Nastavnik']][i] += 1
                    classrooms[classroom][i] += 1
                    for group in new_single_class['Grupe']:
                        groups[group][i] += 1
                subjects[new_single_class['Predmet']][new_single_class['Tip']].append((time, new_single_class['Grupe']))
                # reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects)
                # reserve_time(time2, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects)

        new_data.append(new_single_class)

    return new_data, professors, classrooms, groups, subjects


# reserve the time chosen for all other chromosomes like professors, classrooms, and groups
# def reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class, subjects):
#     for i in range(time, time + int(single_class['Trajanje'])):
#         professors[new_single_class['Nastavnik']][i] += 1
#         classrooms[classroom][i] += 1
#         for group in new_single_class['Grupe']:
#             groups[group][i] += 1
#     subjects[new_single_class['Predmet']][new_single_class['Tip']].append((time, new_single_class['Grupe']))


def write_data(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)


if __name__ == "__main__":
    input_file = 'classes/input2.json'
    output_file = 'classes/output5.json'
    da = load_data(input_file)
    chromosome = generate_chromosome(da)
    write_data(chromosome[0], output_file)
