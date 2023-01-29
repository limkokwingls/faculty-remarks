from dataclasses import dataclass
from model import Course, CourseGrades
from test_three import remove_failed_passed_courses
from rich import print

one = CourseGrades(Course("1", "Web Design in JavaScript"), "A", None, None)
two = CourseGrades(Course("2", "PHP"), "PP", None, None)
three = CourseGrades(Course("3", "php"), "B", None, None)
# four = CourseGrades(Course("4", "C++"), "B", None, None)
# five = CourseGrades(
#     Course("x", "Web Design with java Script"), "D", None, None)

grades = [
    one, two, three,
]


new_list = remove_failed_passed_courses(grades)
# new_list = [x for x in grades if x not in delete]
print(new_list)
