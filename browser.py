from bs4 import BeautifulSoup
from rich import print
from rich.console import Console

import urls
from html_utils import read_table
from model import Course, CourseGrades
from session import Session

console = Console()

PARSER = "html5lib"


class Browser:
    def __init__(self):
        self.session = Session()
        self.logged_in = False

    async def login(self):
        if await self.session.login():
            console.print("\nLogin Successful", style="green")
            self.logged_in = True
        return self.logged_in

    async def read_transcript(self, student_number: int | str, semester: int):
        response = await self.session.get(urls.transcript(student_number))
        page = BeautifulSoup(response.text, PARSER)
        table = page.select_one("table.ewReportTable")
        if not table:
            print(f"Error student {student_number} has no transcript")
            return []
        table_data = read_table(table)[2:-1]

        data = []
        semester_val = -1
        for it in table_data:
            if it and len(it) > 1 and "Semester" in it[0]:
                semester_val = it[1].split(" ")[-1]
            if int(semester_val) == semester:
                data.append(it)
        return self.__get_results(data)

    async def get_programs(self):
        res = await self.session.get(urls.bos_page())
        soup = BeautifulSoup(res.text, PARSER)
        table = soup.select('select[name="course"] option')
        data = [it.get_text(strip=True) for it in table]

        return list(dict.fromkeys(data))

    def __get_results(self, data: list):
        data = [
            it
            for it in data
            if it
            and ("Term:" not in it)
            and ("Term" not in it)
            and ("Semester:" not in it)
            and ("Semester" not in it)
            and ("Results:" not in it)
            and ("Results" not in it)
            and ("Code:" not in it)
            and ("Code" not in it)
            and ("Total:" not in it)
            and ("Total" not in it)
        ]
        results = []
        for it in data:
            try:
                course_grade = CourseGrades(
                    course=Course(code=it[0], name=it[1]),
                    grade=it[2],
                    marks=CourseGrades.marks_from_grade(it[2]),
                    points=it[-2],
                )
                results.append(course_grade)
            except Exception as ex:
                print(f"{it} caused an error: ", ex)
        return results
