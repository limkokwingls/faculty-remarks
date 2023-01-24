from dataclasses import dataclass


@dataclass
class Result:
    course: str
    points: float


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
