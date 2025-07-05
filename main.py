class Student:
    """Класс 'Студент обыкновенный'"""

    def __init__(self, name, surname, sex):
        self.name = name
        self.surname = surname
        self.sex = sex
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecture(self, lecturer, course, rate):
        if (
            isinstance(lecturer, Lecturer) and
            course in lecturer.courses_attached and
            course in self.courses_in_progress and
            0 <= rate <= 10
        ):
            lecturer.rating.setdefault(course, []).append(rate)
        else:
            print('Ошибка. Рейтинг не добавлен')
            return False

    def average_grade(self):
        all_grades = []
        for list_grades in self.grades.values():
            all_grades.extend(list_grades)
        if len(all_grades) == 0:
            return 0
        result = sum(all_grades) / len(all_grades)
        return round(result, 1)

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {self.average_grade()}\n"
                f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
                f"Завершенные курсы: {', '.join(self.finished_courses)}\n"
                )

    def __eq__(self, other):
        return self.average_grade() == other.average_grade()

    def __gt__(self, other):
        return self.average_grade() > other.average_grade()


class Mentor:
    """Родительский класс для преподавателей"""

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    """Класс преподавателей читающих лекции"""

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.rating = {}

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {self.average_rating()}"
                )

    def average_rating(self):
        all_rating = []
        for list_rating in self.rating.values():
            all_rating.extend(list_rating)
        if len(all_rating) == 0:
            return 0
        result = sum(all_rating) / len(all_rating)
        return result

    def __eq__(self, other):
        return self.average_rating() == other.average_rating()

    def __gt__(self, other):
        return self.average_rating() > other.average_rating()


class Reviewer(Mentor):
    """Класс экспертов проверяющих задания"""

    def rate_hw(self, student, course, grade):
        if (
            isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
        ):
            student.grades.setdefault(course, []).append(grade)
            print('Оценка добавлена')
            return True
        else:
            print('Ошибка. Невозможно добавить оценку')
            return False

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                )


def average_grade_students(students:list, course_name):
    students = students
    course = course_name
    total_grades = []
    for student in students:
        if course in student.courses_in_progress and student.grades.get(course) != None:
            total_grades += student.grades[course]
    if len(total_grades) == 0:
        return 0
    else:
        average = sum(total_grades) / len(total_grades)
    return round(average,1)


def average_rating_lecturers(lecturers: list, course_name):
    lecturer = lecturers
    course = course_name
    total_grades = []
    for lecturer in lecturers:
        if course in lecturer.courses_attached and lecturer.rating.get(course) != None:
            total_grades += lecturer.rating[course]
    if len(total_grades) == 0:
        return 0
    else:
        average = sum(total_grades) / len(total_grades)
    return round(average, 1)

student_1 = Student('Гарри', 'Поттер', 'М')
student_2 = Student('Гермиона', 'Грейнджер', 'Ж')

lecturer_1 = Lecturer('Альбус', 'Дамблдор')
lecturer_2 = Lecturer('Северус', 'Снейп')

reviewer_1 = Reviewer('Рубеус', 'Хагрид')
reviewer_2 = Reviewer('Распределяющая', 'Шляпа')

student_1.courses_in_progress += ['Python', 'Java']
student_2.courses_in_progress += ['Python', 'С++', 'JavaScript']
student_1.add_courses('Git')
student_2.add_courses('Magical botany')

lecturer_1.courses_attached += ['Python', 'С++']
lecturer_2.courses_attached += ['Java', 'JavaScript']

reviewer_1.courses_attached += ['Python', 'С++']
reviewer_2.courses_attached += ['Java', 'JavaScript']

reviewer_2.rate_hw(student_2, 'Python', 3)  # Ошибка
reviewer_1.rate_hw(student_1, 'Python', 9)  # Успех
reviewer_1.rate_hw(student_1, 'Python', 8)  # Успех
reviewer_2.rate_hw(student_1, 'Java', 3)  # Успех
reviewer_1.rate_hw(student_2, 'Python', 10) # Успех
reviewer_1.rate_hw(student_2, 'С++', 9)
reviewer_2.rate_hw(student_2, 'JavaScript', 10)
reviewer_1.rate_hw(student_2, 'Python', 10)

student_1.rate_lecture(lecturer_1, 'Python', 12)    # Ошибка
student_1.rate_lecture(lecturer_1, 'Python', 10)    # Успех
student_2.rate_lecture(lecturer_2, 'JavaScript', 9)    # Успех
student_2.rate_lecture(lecturer_1, 'Python', 7)

print()
print(student_1)
print()
print(student_2)

print(lecturer_1)
print()
print(lecturer_2)

print()
print(reviewer_1)
print()
print(reviewer_2)

print(student_1 == student_2) # False
print(lecturer_1 > lecturer_2)  # True
print(lecturer_1 < lecturer_2)  # False

print(student_1.grades)
print(student_2.grades)
print()
print(lecturer_1.rating)
print(lecturer_2.rating)

print(average_grade_students([student_1, student_2], 'Python'))
print(average_rating_lecturers([lecturer_1, lecturer_2], 'Python'))
