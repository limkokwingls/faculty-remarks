from dataclasses import dataclass
from model import Course, CourseGrades


@dataclass
class Data:
    name: str
    age: int = 0


obj = Data(name="Thabo")

print(Data.age)
