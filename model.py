from dataclasses import dataclass


@dataclass
class Faculty:
    id: str
    name: str
    link_to_courses: str

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


@dataclass
class Program:
    id: str
    name: str

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
