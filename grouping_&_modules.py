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
    new_data = []
    departments = {}
    for single_department in departments_data:
        department = departments_data[single_department]
        department_groups = math.ceil(department / 20)
        dep_group = {}
        for i in range(1, department_groups + 1):
            if single_department[-1] == "m":
                dep_group[f"10{i}"] = []
            elif single_department[-1] == "f":
                dep_group[f'20{i}'] = []
        departments[single_department] = dep_group

    for single_class in classes_data:
        if single_class['Type'] == "P":
            class_capacity = single_class['Capacity']
            class_for = single_class["for"]
            total_number_of_students = 0
            groups_to_sections = {}
            dept_groups = []
            for single_class_for in class_for:
                total_number_of_students += departments_data[single_class_for]
                keys = departments[single_class_for]
                for key in keys:
                    dept_groups.append(f"{single_class_for} {key}")
            num_of_sec = math.ceil(total_number_of_students / class_capacity)
            num_incre = 1
            total_number_of_students2 = 0
            students_number_in_group = 0
            for i in range(1, num_of_sec+1):
                groups_to_sections[i] = []
            group_y = []
            for y in dept_groups:
                group_y.append(y)
                groups_to_sections[num_incre] = group_y
                students_number_in_group += 20
                total_number_of_students2 += 20
                if students_number_in_group == class_capacity or (students_number_in_group + 20) > class_capacity \
                        or (((total_number_of_students - total_number_of_students2) < class_capacity)
                            and dept_groups[-1] == y):
                    num_incre += 1
                    students_number_in_group = 0
                    group_y = []

            for i in range(1, num_of_sec+1):
                new_single_class = single_class.copy()
                new_single_class['For_Group'] = groups_to_sections[i]
                if new_single_class['Subject'][-1] == "M":
                    new_single_class['Group'] = f"10{i}"
                elif new_single_class['Subject'][-1] == "F":
                    new_single_class['Group'] = f"20{i}"

                lecturer = new_single_class['Lecturer']
                number_of_lecturer = random.randrange(0, len(lecturer))
                new_single_class['Lecturer'] = [lecturer[number_of_lecturer]]
                for j in groups_to_sections[i]:
                    new_pair = j.rsplit(" ")
                    departments[new_pair[0]][new_pair[1]].append(new_single_class)
                new_data.append(new_single_class)

        elif single_class['Type'] == "V":
            class_for = single_class["for"]
            for single_class_for in class_for:
                for keys, values in departments.items():
                    for single_value in values:
                        if single_class_for == keys:
                            new_single_class = single_class.copy()
                            lecturer = new_single_class['Lecturer']
                            number_of_lecturer = random.randrange(0, len(lecturer))
                            new_single_class['Lecturer'] = [lecturer[number_of_lecturer]]
                            new_single_class["for"] = [single_class_for]
                            if new_single_class['Subject'][-1] == "M":
                                new_single_class['Group'] = single_value
                            elif new_single_class['Subject'][-1] == "F":
                                new_single_class['Group'] = single_value
                            departments[keys][single_value].append(new_single_class)
                            new_data.append(new_single_class)

    return departments, new_data


def write_data(data, path):
    with open(path, 'w') as write_file:
        json.dump(data, write_file, indent=4)


def write_data2(data, departments, path):
    new_data = {'departments': departments, 'Classes': data}
    with open(path, 'w') as write_file:
        json.dump(new_data, write_file, indent=4)


if __name__ == "__main__":
    input_file = 'classes/1st iug_input v4 grouping_modules.json'
    output_file = 'classes/department groups with modules.json'
    output_file2 = 'classes/2nd iug_input v4 first_solution.json'
    da = load_data(input_file)
    departments_groups = generate_department_groups(da[0], da[1])
    write_data(departments_groups[0], output_file)
    write_data2(departments_groups[1], da[1],  output_file2)
