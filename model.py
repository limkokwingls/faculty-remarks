from dataclasses import dataclass


@dataclass
class Result:
    course: str
    points: float


@dataclass
class Course:
    code: str
    name: str


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
    def marks_from_points(points):
        # TODO: I don't think this formula is correct
        return (float(points) * 50) / 2

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
