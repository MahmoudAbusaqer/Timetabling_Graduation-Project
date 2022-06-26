import json
import random
import cost_functions
from colorama import Fore
from colorama import Style

cost_function_try = cost_functions.cost


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
    level = {}
    # for_specialty = {}
    # print("professors: " + str(professors))
    # print("classrooms: " + str(classrooms))
    # print("groups: " + str(groups))
    # print("subjects: " + str(subjects))
    # print("level: " + str(level))

    new_data = []
    not_assigned_data = []

    number_of_runs = 0

    # create the chromosome which will reserve 80 places (Genes) for the whole timetable to put the randomly generated
    # value in it, every place consists of a half-hour (Gene)
    for single_class in data:
        professors[single_class['Lecturer']] = [0] * 80
        level[single_class['Level']] = [0] * 80
        for classroom in single_class['Classroom']:
            classrooms[classroom] = [0] * 80
        for group in single_class['Group']:
            groups[group] = [0] * 80
        # for single_specialty in single_class['for']:
        #     for_specialty[single_specialty] = [0] * 80
        subjects[single_class['Subject']] = {'P': [], 'V': []}  # need edit (2 needed)

    copy_data = data.copy()
    for single_class in copy_data:
        new_single_class = single_class.copy()
        classroom = random.choice(
            single_class['Classroom'])  # get a random classroom from the classrooms for this class
        day = random.randrange(0, 5)  # get a random day for this class
        class_type = new_single_class['Type']
        class_length = new_single_class['Duration']
        period = choose_period(day, class_type, class_length)  # get a random period (time) for this class

        # create a new variable called assigned_classroom (assigned_classroom) to store the initial assigned classroom
        # to the class
        # new_single_class['assigned_classroom'] = classroom

        reserve_professor = professors[new_single_class['Lecturer']]
        reserve_classroom = classrooms[classroom]
        reserve_level = level[new_single_class['Level']]
        # reserve_for = for_specialty[new_single_class['for']]
        reserve_group = groups

        # belong = False
        print_int(number_of_runs)
        # Saturday, Monday and Wednesday classes
        if day == 0 or day == 2 or day == 4:
            # reserve 1 time for the lab classes
            if class_length == "2" and new_single_class['Type'] == 'V':
                print("***state 1***")
                check_time_bool = True
                time = state_1(day, period)

                class_level = new_single_class['Level']
                class_for = new_single_class['for']
                lecturer = new_single_class['Lecturer']
                search_data = slice_data(new_data, class_level, class_for, lecturer)

                for i in range(len(search_data)):
                    print_int(number_of_runs)
                    check_time = []
                    genes_times = []
                    data_class_for = search_data[i]['for']
                    class_for = new_single_class['for']
                    # belong = belong_to_speciality(class_for, data_class_for)
                    # for f in new_data[i]['for']:
                    #     if new_single_class['Level'].__contains__(f):
                    #         print("yes")
                    #         belong_to_speciality = True
                    #         break
                    #     else:
                    #         print("no")

                    # if search_data[i]['Level'] == new_single_class['Level']:
                    # \
                    #     and new_data[i]['for'] == new_single_class['for'] \
                    #     and new_data[i]['Duration'] == new_single_class['Duration'] \
                    #     and new_data[i]['assigned_classroom'] == new_single_class['assigned_classroom']:

                    duration = search_data[i]['Duration']
                    class_type = search_data[i]['Type']
                    assigned_genes = search_data[i]['assigned_time']
                    genes_times = object_assigned_time(duration, class_type, assigned_genes)

                    # print(genes_times)

                    for g in range(0, 4):
                        check_time.append(time + g)

                    # if search_data[i]['Lecturer'] == new_single_class['Lecturer']:
                    #     pass

                    for w in check_time:
                        if genes_times.__contains__(w):
                            if search_data[i]['assigned_classroom'] == classroom:
                                print(f"{Fore.RED}The newly assigned time does violate another class "
                                      f"time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break
                            elif search_data[i]['assigned_classroom'] != classroom and \
                                    search_data[i]['Lecturer'] == new_single_class['Lecturer']:

                                print(f"{Fore.RED}violate the Lecturer class time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break

                if check_time_bool:
                    new_single_class['assigned_classroom'] = classroom
                    new_single_class['assigned_time'] = time
                    reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group,
                                 new_single_class, subjects, reserve_level, 1)
                    new_data.append(new_single_class)
                    print(str(new_single_class))
                    number_of_runs += 1
                    print("number_of_runs = " + str(number_of_runs))
                else:
                    not_assigned_data.append(new_single_class)
                    copy_data.append(new_single_class)
                    print(
                        f"{Fore.RED}There is a violating of a hard constraints, so no assigment done here{Style.RESET_ALL}")
                    # print("not_assigned_data: " + str(not_assigned_data))
                    # print("professors: " + str(professors))
                    # print("classrooms: " + str(classrooms))
                    # print("groups: " + str(groups))
                    # print("subjects: " + str(subjects))
                    # print("level: " + str(level))
                # print("end")

            # reserve 3 times for the lecture classes with a Length of 3 hours
            elif class_length == "3" and new_single_class['Type'] == 'P':
                # print("***state 2***")
                check_time_bool = True
                time = state_2(period)
                class_level = new_single_class['Level']
                class_for = new_single_class['for']
                lecturer = new_single_class['Lecturer']
                search_data = slice_data(new_data, class_level, class_for, lecturer)

                for i in range(len(search_data)):
                    print_int(number_of_runs)
                    check_time = []
                    genes_times = []
                    data_class_for = search_data[i]['for']
                    class_for = new_single_class['for']
                    # belong = belong_to_speciality(class_for, data_class_for)
                    # if search_data[i]['Level'] == new_single_class['Level']:
                    # \
                    #     and new_data[i]['for'] == new_single_class['for'] \
                    #     and new_data[i]['Duration'] == new_single_class['Duration']\
                    #     and new_data[i]['assigned_classroom'] == new_single_class['assigned_classroom']\
                    #     and len(new_data[i]['assigned_time']) == 3:

                    duration = search_data[i]['Duration']
                    class_type = search_data[i]['Type']
                    assigned_genes = search_data[i]['assigned_time']
                    # print("new_data[i] = " + str(new_data[i]))
                    genes_times = object_assigned_time(duration, class_type, assigned_genes, "state 2")

                    for g in range(0, 3):
                        check_time.append(time[g])
                        check_time.append(time[g] + 1)
                        # genes_times.append(assigned_genes[g])
                        # genes_times.append(assigned_genes[g] + 1)

                    for w in check_time:
                        if genes_times.__contains__(w):
                            if search_data[i]['assigned_classroom'] == classroom:
                                print(f"{Fore.RED}The newly assigned time does violate another class "
                                      f"time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break
                            elif search_data[i]['assigned_classroom'] != classroom and \
                                    search_data[i]['Lecturer'] == new_single_class['Lecturer']:
                                print(f"{Fore.RED}violate the Lecturer class time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break

                if check_time_bool:
                    new_single_class['assigned_classroom'] = classroom
                    new_single_class['assigned_time'] = time
                    for t in time:
                        reserve_time(t, class_length, reserve_professor, reserve_classroom, reserve_group,
                                     new_single_class, subjects, reserve_level, 2)
                    new_data.append(new_single_class)
                    print(str(new_single_class))
                    number_of_runs += 1
                    print("number_of_runs = " + str(number_of_runs))
                else:
                    not_assigned_data.append(new_single_class)
                    copy_data.append(new_single_class)
                    print(
                        f"{Fore.RED}There is a violating of a hard constraints, so no assigment done here{Style.RESET_ALL}")
                    # print("not_assigned_data: " + str(not_assigned_data))
                    # print("professors: " + str(professors))
                    # print("classrooms: " + str(classrooms))
                    # print("groups: " + str(groups))
                    # print("subjects: " + str(subjects))
                    # print("level: " + str(level))
            # reserve 2 times for the lecture classes with a Length of 2 hours
            elif class_length == "2" and new_single_class['Type'] == 'P':
                # print("***state 3***")
                check_time_bool = True
                time = state_3(period)
                class_level = new_single_class['Level']
                class_for = new_single_class['for']
                lecturer = new_single_class['Lecturer']
                search_data = slice_data(new_data, class_level, class_for, lecturer)

                for i in range(len(search_data)):
                    print_int(number_of_runs)
                    check_time = []
                    genes_times = []
                    data_class_for = search_data[i]['for']
                    class_for = new_single_class['for']
                    # belong = belong_to_speciality(class_for, data_class_for)
                    # if search_data[i]['Level'] == new_single_class['Level']:
                    # \
                    #     and new_data[i]['for'] == new_single_class['for'] \
                    #     and new_data[i]['Duration'] == new_single_class['Duration']\
                    #     and new_data[i]['assigned_classroom'] == new_single_class['assigned_classroom']:

                    duration = search_data[i]['Duration']
                    class_type = search_data[i]['Type']
                    assigned_genes = search_data[i]['assigned_time']
                    genes_times = object_assigned_time(duration, class_type, assigned_genes)

                    for g in range(0, 2):
                        check_time.append(time[g])
                        check_time.append(time[g] + 1)
                        # genes_times.append(assigned_genes[g])
                        # genes_times.append(assigned_genes[g] + 1)

                    for w in check_time:
                        if genes_times.__contains__(w):
                            if search_data[i]['assigned_classroom'] == classroom:
                                print(f"{Fore.RED}The newly assigned time does violate another class "
                                      f"time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break
                            elif search_data[i]['assigned_classroom'] != classroom and \
                                    search_data[i]['Lecturer'] == new_single_class['Lecturer']:
                                print(f"{Fore.RED}violate the Lecturer class time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break

                if check_time_bool:
                    new_single_class['assigned_classroom'] = classroom
                    new_single_class['assigned_time'] = time
                    for t in time:
                        reserve_time(t, class_length, reserve_professor, reserve_classroom, reserve_group,
                                     new_single_class, subjects, reserve_level, 3)
                    new_data.append(new_single_class)
                    print(str(new_single_class))
                    number_of_runs += 1
                    print("number_of_runs = " + str(number_of_runs))
                else:
                    not_assigned_data.append(new_single_class)
                    copy_data.append(new_single_class)
                    print(
                        f"{Fore.RED}There is a violating of a hard constraints, so no assigment done here{Style.RESET_ALL}")
                    # print("not_assigned_data: " + str(not_assigned_data))
                    # print("professors: " + str(professors))
                    # print("classrooms: " + str(classrooms))
                    # print("groups: " + str(groups))
                    # print("subjects: " + str(subjects))
                    # print("level: " + str(level))

            # reserve 1 time for a lecture class that is one hour only
            elif class_length == "1" and new_single_class['Type'] == 'P':
                print("***state 6***")
                check_time_bool = True
                time = state_1(day, period)
                class_level = new_single_class['Level']
                class_for = new_single_class['for']
                lecturer = new_single_class['Lecturer']
                search_data = slice_data(new_data, class_level, class_for, lecturer)

                for i in range(len(search_data)):
                    print_int(number_of_runs)
                    check_time = []
                    genes_times = []
                    data_class_for = search_data[i]['for']
                    class_for = new_single_class['for']
                    # belong = belong_to_speciality(class_for, data_class_for)
                    # if search_data[i]['Level'] == new_single_class['Level']:
                    # \
                    #     and new_data[i]['for'] == new_single_class['for'] \
                    #     and new_data[i]['Duration'] == new_single_class['Duration']\
                    #     and new_data[i]['assigned_classroom'] == new_single_class['assigned_classroom']:

                    duration = search_data[i]['Duration']
                    class_type = search_data[i]['Type']
                    assigned_genes = search_data[i]['assigned_time']
                    genes_times = object_assigned_time(duration, class_type, assigned_genes)

                    for g in range(0, 2):
                        check_time.append(time + g)
                        # genes_times.append(assigned_genes + g)

                    for w in check_time:
                        if genes_times.__contains__(w):
                            if search_data[i]['assigned_classroom'] == classroom:
                                print(f"{Fore.RED}The newly assigned time does violate another class "
                                      f"time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break
                            elif search_data[i]['assigned_classroom'] != classroom and \
                                    search_data[i]['Lecturer'] == new_single_class['Lecturer']:
                                print(f"{Fore.RED}violate the Lecturer class time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break

                if check_time_bool:
                    new_single_class['assigned_classroom'] = classroom
                    new_single_class['assigned_time'] = time
                    reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group,
                                 new_single_class, subjects, reserve_level, 6)
                    new_data.append(new_single_class)
                    print(str(new_single_class))
                    number_of_runs += 1
                    print("number_of_runs = " + str(number_of_runs))
                else:
                    not_assigned_data.append(new_single_class)
                    copy_data.append(new_single_class)
                    print(
                        f"{Fore.RED}There is a violating of a hard constraints, so no assigment done here{Style.RESET_ALL}")
                    # print("not_assigned_data: " + str(not_assigned_data))
                    # print("professors: " + str(professors))
                    # print("classrooms: " + str(classrooms))
                    # print("groups: " + str(groups))
                    # print("subjects: " + str(subjects))
                    # print("level: " + str(level))
        # Sunday and Thursday classes
        elif day == 1 or day == 3:
            # reserve 1 time for the lab classes
            if class_length == "2" and new_single_class['Type'] == 'V':
                print("***state 4***")
                check_time_bool = True
                time = state_1(day, period)
                class_level = new_single_class['Level']
                class_for = new_single_class['for']
                lecturer = new_single_class['Lecturer']
                search_data = slice_data(new_data, class_level, class_for, lecturer)

                for i in range(len(search_data)):
                    print_int(number_of_runs)
                    check_time = []
                    genes_times = []
                    data_class_for = search_data[i]['for']
                    class_for = new_single_class['for']
                    # belong = belong_to_speciality(class_for, data_class_for)
                    # if search_data[i]['Level'] == new_single_class['Level']:
                    # \
                    #     and new_data[i]['for'] == new_single_class['for'] \
                    #     and new_data[i]['Duration'] == new_single_class['Duration']\
                    #     and new_data[i]['assigned_classroom'] == new_single_class['assigned_classroom']:

                    duration = search_data[i]['Duration']
                    class_type = search_data[i]['Type']
                    assigned_genes = search_data[i]['assigned_time']
                    genes_times = object_assigned_time(duration, class_type, assigned_genes)

                    for g in range(0, 4):
                        check_time.append(time + g)
                        # genes_times.append(assigned_genes + g)

                    for w in check_time:
                        if genes_times.__contains__(w):
                            if search_data[i]['assigned_classroom'] == classroom:
                                print(f"{Fore.RED}The newly assigned time does violate another class "
                                      f"time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break
                            elif search_data[i]['assigned_classroom'] != classroom and \
                                    search_data[i]['Lecturer'] == new_single_class['Lecturer']:
                                print(f"{Fore.RED}violate the Lecturer class time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break

                if check_time_bool:
                    new_single_class['assigned_classroom'] = classroom
                    new_single_class['assigned_time'] = time
                    reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group,
                                 new_single_class, subjects, reserve_level, 1)
                    new_data.append(new_single_class)
                    print(str(new_single_class))
                    number_of_runs += 1
                    print("number_of_runs = " + str(number_of_runs))
                else:
                    not_assigned_data.append(new_single_class)
                    copy_data.append(new_single_class)
                    print(
                        f"{Fore.RED}There is a violating of a hard constraints, so no assigment done here{Style.RESET_ALL}")
                    # print("not_assigned_data: " + str(not_assigned_data))
                    # print("professors: " + str(professors))
                    # print("classrooms: " + str(classrooms))
                    # print("groups: " + str(groups))
                    # print("subjects: " + str(subjects))
                    # print("level: " + str(level))

            # reserve multiple times (2 times) for a lecture classes
            elif class_length in ("2", "3") and new_single_class['Type'] == 'P':
                # print("***state 5***")
                check_time_bool = True
                time = state_5(period)
                class_level = new_single_class['Level']
                class_for = new_single_class['for']
                lecturer = new_single_class['Lecturer']
                search_data = slice_data(new_data, class_level, class_for, lecturer)

                for i in range(len(search_data)):
                    print_int(number_of_runs)
                    check_time = []
                    genes_times = []
                    data_class_for = search_data[i]['for']
                    class_for = new_single_class['for']
                    # belong = belong_to_speciality(class_for, data_class_for)
                    # if search_data[i]['Level'] == new_single_class['Level']:
                    # \
                    #     and new_data[i]['for'] == new_single_class['for'] \
                    #     and new_data[i]['Duration'] == new_single_class['Duration']\
                    #     and new_data[i]['assigned_classroom'] == new_single_class['assigned_classroom']\
                    #     and len(new_data[i]['assigned_time']) == 2:

                    duration = search_data[i]['Duration']
                    class_type = search_data[i]['Type']
                    assigned_genes = search_data[i]['assigned_time']
                    # print("new_data[i] = " + str(new_data[i]))
                    genes_times = object_assigned_time(duration, class_type, assigned_genes, "state 5")

                    for g in range(0, 2):
                        check_time.append(time[g])
                        check_time.append(time[g] + 1)
                        check_time.append(time[g] + 2)
                        # genes_times.append(assigned_genes[g])
                        # genes_times.append(assigned_genes[g] + 1)
                        # genes_times.append(assigned_genes[g] + 2)

                    for w in check_time:
                        if genes_times.__contains__(w):
                            if search_data[i]['assigned_classroom'] == classroom:
                                print(f"{Fore.RED}The newly assigned time does violate another class "
                                      f"time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break
                            elif search_data[i]['assigned_classroom'] != classroom and \
                                    search_data[i]['Lecturer'] == new_single_class['Lecturer']:
                                print(f"{Fore.RED}violate the Lecturer class time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break

                if check_time_bool:
                    new_single_class['assigned_classroom'] = classroom
                    new_single_class['assigned_time'] = time
                    for t in time:
                        reserve_time(t, class_length, reserve_professor, reserve_classroom, reserve_group,
                                     new_single_class, subjects, reserve_level, 5)
                    new_data.append(new_single_class)
                    print(str(new_single_class))
                    number_of_runs += 1
                    print("number_of_runs = " + str(number_of_runs))
                else:
                    not_assigned_data.append(new_single_class)
                    copy_data.append(new_single_class)
                    print(
                        f"{Fore.RED}There is a violating of a hard constraints, so no assigment done here{Style.RESET_ALL}")
                    # print("not_assigned_data: " + str(not_assigned_data))
                    # print("professors: " + str(professors))
                    # print("classrooms: " + str(classrooms))
                    # print("groups: " + str(groups))
                    # print("subjects: " + str(subjects))
                    # print("level: " + str(level))

            # reserve 1 time for a lecture class that is one hour only
            elif class_length == "1" and new_single_class['Type'] == 'P':
                print("***state 6***")
                check_time_bool = True
                time = state_1(day, period)
                class_level = new_single_class['Level']
                class_for = new_single_class['for']
                lecturer = new_single_class['Lecturer']
                search_data = slice_data(new_data, class_level, class_for, lecturer)

                for i in range(len(search_data)):
                    print_int(number_of_runs)
                    check_time = []
                    genes_times = []
                    data_class_for = search_data[i]['for']
                    class_for = new_single_class['for']
                    # belong = belong_to_speciality(class_for, data_class_for)
                    # if search_data[i]['Level'] == new_single_class['Level']:
                    # \
                    #     and new_data[i]['for'] == new_single_class['for'] \
                    #     and new_data[i]['Duration'] == new_single_class['Duration']\
                    #     and new_data[i]['assigned_classroom'] == new_single_class['assigned_classroom']:

                    duration = search_data[i]['Duration']
                    class_type = search_data[i]['Type']
                    assigned_genes = search_data[i]['assigned_time']
                    genes_times = object_assigned_time(duration, class_type, assigned_genes)

                    for g in range(0, 2):
                        check_time.append(time + g)
                        # genes_times.append(assigned_genes + g)

                    for w in check_time:
                        if genes_times.__contains__(w):
                            if search_data[i]['assigned_classroom'] == classroom:
                                print(f"{Fore.RED}The newly assigned time does violate another class "
                                      f"time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break
                            elif search_data[i]['assigned_classroom'] != classroom and \
                                    search_data[i]['Lecturer'] == new_single_class['Lecturer']:
                                print(f"{Fore.RED}violate the Lecturer class time{Style.RESET_ALL}")
                                check_time_bool = False
                                # break

                if check_time_bool:
                    new_single_class['assigned_classroom'] = classroom
                    new_single_class['assigned_time'] = time
                    reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group,
                                 new_single_class, subjects, reserve_level, 6)
                    new_data.append(new_single_class)
                    print(str(new_single_class))
                    number_of_runs += 1
                    print("number_of_runs = " + str(number_of_runs))
                else:
                    not_assigned_data.append(new_single_class)
                    copy_data.append(new_single_class)
                    print(
                        f"{Fore.RED}There is a violating of a hard constraints, so no assigment done here{Style.RESET_ALL}")
                    # print("not_assigned_data: " + str(not_assigned_data))
                    # print("professors: " + str(professors))
                    # print("classrooms: " + str(classrooms))
                    # print("groups: " + str(groups))
                    # print("subjects: " + str(subjects))
                    # print("level: " + str(level))

    print("not_assigned_data = " + str(len(not_assigned_data)))
    return new_data, professors, classrooms, groups, level, subjects


def print_int(number_of_runs):
    print("number_of_runs = " + str(number_of_runs))


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


def slice_data(data, class_level, class_for, lecturer):
    new_data = []
    belong = False
    for i in range(len(data)):
        for f in data[i]["for"]:
            if class_for.__contains__(f):
                belong = True
                break
            else:
                belong = False
        if data[i]["Level"] == class_level and belong:
            new_data.append(data[i])
        if data[i]["Lecturer"] == lecturer:
            new_data.append(data[i])
    return new_data


def object_assigned_time(duration, class_type, assigned_genes, state="no need"):
    genes_times = []
    if duration == "1":
        for g in range(0, 2):
            genes_times.append(assigned_genes + g)
    elif duration == "2" and class_type == "P":
        for g in range(0, 2):
            genes_times.append(assigned_genes[g])
            genes_times.append(assigned_genes[g] + 1)
    elif duration == "2" and class_type == "V":
        for g in range(0, 4):
            genes_times.append(assigned_genes + g)
    elif duration == "3" and len(assigned_genes) == 3:
        # print("duration = " + str(duration))
        # print("len = " + str(len(assigned_genes)))
        for g in range(0, 3):
            genes_times.append(assigned_genes[g])
            genes_times.append(assigned_genes[g] + 1)
    elif duration == "3" and len(assigned_genes) == 2:
        # print("len = " + str(len(assigned_genes)))
        for g in range(0, 2):
            genes_times.append(assigned_genes[g])
            genes_times.append(assigned_genes[g] + 1)
            genes_times.append(assigned_genes[g] + 2)
        # print("genes_times for state 5 = " + str(genes_times))

    return genes_times


def state_1(day, period):
    # reserve 1 time for the  class
    time = 16 * day + period
    return time


def state_2(period):
    # reserve 3 times for the lecture classes with a Length of 3 hours
    print("***state 2***")
    all_times = []  # To store the times reserved for this class
    time = 16 * 0 + period
    time2 = 16 * 2 + period
    time3 = (16 * 4) + period
    all_times.append(time)
    all_times.append(time2)
    all_times.append(time3)
    return all_times


def state_3(period):
    # reserve 2 times for the lecture classes with a Length of 2 hours
    print("***state 3***")
    all_times = []  # To store the times reserved for this class
    time = 16 * 0 + period
    time2 = 16 * 4 + period
    all_times.append(time)
    all_times.append(time2)
    return all_times


def state_5(period):
    # reserve 2 times for the lecture classes with a Length of 2 hours
    print("***state 5***")
    all_times = []  # To store the times reserved for this class
    time = 16 * 1 + period
    time2 = 16 * 3 + period
    all_times.append(time)
    all_times.append(time2)
    return all_times


# reserve the time chosen for all other chromosomes like professors, classrooms, and groups
def reserve_time(time, class_length, reserve_professor, reserve_classroom, reserve_group, new_single_class,
                 subjects, reserve_level, state):
    if state == 1:
        # print("time= " + str(time))
        for i in range(time, time + 4):
            print("i = " + str(i))
            reserve_professor[i] += 1
            reserve_classroom[i] += 1
            reserve_level[i] += 1
            for group in reserve_group:
                reserve_group[group][i] += 1
            # for single_specialty in reserve_for:
            #     reserve_for[single_specialty][i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['Group']))
    elif state == 2 or state == 3 or state == 6:
        for i in range(time, time + 2):
            reserve_professor[i] += 1
            reserve_classroom[i] += 1
            reserve_level[i] += 1
            for group in reserve_group:
                reserve_group[group][i] += 1
            # for single_specialty in reserve_for:
            #     reserve_for[single_specialty][i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['Group']))
    elif state == 5:
        for i in range(time, time + 3):
            reserve_professor[i] += 1
            reserve_classroom[i] += 1
            reserve_level[i] += 1
            for group in reserve_group:
                reserve_group[group][i] += 1
            # for single_specialty in reserve_for:
            #     reserve_for[single_specialty][i] += 1
        subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['Group']))

    # for i in range(time, time + int(class_length)):
    #     reserve_professor[i] += 1
    #     reserve_classroom[i] += 1
    #     reserve_level[i] += 1
    #     for group in reserve_group:
    #         reserve_group[group][i] += 1
    #     # for single_specialty in reserve_for:
    #     #     reserve_for[single_specialty][i] += 1
    # subjects[new_single_class['Subject']][new_single_class['Type']].append((time, new_single_class['Group']))


def write_data(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)


def write_data2(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file)


if __name__ == "__main__":
    input_file = 'classes/iug_input3.json'
    output_file = 'classes/iug_output_test5.json'
    output_file2 = 'classes/chromosome5.json'
    da = load_data(input_file)

    chromosome = generate_chromosome(da)

    write_data(chromosome[0], output_file)
    write_data2(chromosome, output_file2)

