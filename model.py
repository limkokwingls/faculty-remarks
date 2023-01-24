from dataclasses import dataclass


@dataclass
class Result:
    course: str
    points: float


@dataclass
class BorderlineObject:
    percent_covered = 0.0
    internal_std_no: str
    student_no: str
    names: str
    final_exam_marks: float
    total: float

    def is_borderline(self):
        if self.total >= 44:
            s = str(self.total)
            if "." in s:
                s = s.split(".")[0]
            return s == '48' or s.endswith("9") or s.endswith("4")
        return False
