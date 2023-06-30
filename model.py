from dataclasses import dataclass


@dataclass
class Result:
    course: str
    points: float


@dataclass
class Course:
    code: str
    name: str

    def __hash__(self) -> int:
        return hash(self.clean_name())

    def __eq__(self, obj) -> bool:
        if type(obj) != type(self):
            raise Exception(
                f"Cannot compare {type(obj)} and {type(self)}")
        if self.code.upper() == obj.code.upper():
            return True
        if self.clean_name() == obj.clean_name():
            return True
        return False

    def clean_name(self):
        new_name = self.name.upper()
        new_name = new_name.replace(" I ", " 1 ")
        new_name = new_name.replace(" II ", " 2 ")
        new_name = new_name.replace(" III ", " 3 ")
        new_name = new_name.replace(" & ", " AND ")
        new_name = new_name.replace(
            "with Java Script".upper(), "in JavaScript".upper())
        if new_name.endswith("III"):
            new_name = new_name[:-3] + "3"
        if new_name.endswith("II"):
            new_name = new_name[:-2] + "2"
        if new_name.endswith("I"):
            new_name = new_name[:-1] + "1"

        

        return new_name.upper().replace(" ", "")


@dataclass
class CourseGrades:
    course: Course
    grade: str
    marks: float | None
    points: float | None

    def __post_init__(self):
        self.marks = float(self.marks) if self.marks else None
        self.points = float(self.points) if self.points else None

    @staticmethod
    def marks_from_grade(grade):
        switch = {
            'A+': 90,
            'A': 85,
            'A-': 80,
            'B+': 75,
            'B': 70,
            'B-': 65,
            'C+': 60,
            'C': 55,
            'C-': 50,
            'PX': 50,
            'PP': 45,
        }
        return switch.get(grade, 0)

    def is_borderline(self):
        if not self.marks:
            return False
        if self.marks >= 44:
            s = str(self.marks)
            if "." in s:
                s = s.split(".")[0]
            if s == '48' or s.endswith("9") or s.endswith("4"):
                return True
            if self.marks >= 45 and self.marks <= 49:
                return self.grade.lower() != 'pp'
        return False


@dataclass
class Student:
    std_no: str
    name: str
    grades: list[CourseGrades]
    remarks: str = ""


@dataclass
class BorderlineObject:
    std_no: str | int
    std_class: str
    course: str
    marks: float
    grade: str

    def is_borderline(self):
        if self.marks >= 44:
            s = str(self.marks)
            if "." in s:
                s = s.split(".")[0]
            if s == '48' or s.endswith("9") or s.endswith("4"):
                return True
            if self.marks >= 45 and self.marks <= 49:
                return self.grade.lower() != 'pp'
        return False
