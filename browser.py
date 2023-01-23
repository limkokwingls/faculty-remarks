from bs4 import BeautifulSoup
from html_utils import find_link_in_table, read_table
import requests
from model import Faculty, Program
import urls
from rich.console import Console
import printer
from css import stylesheet

console = Console()

PARSER = "html5lib"


class Browser:
    def __init__(self):
        self.session = requests.Session()
        self.logged_in = False

    def login(self, username: str, password: str):
        with console.status("Logging in..."):
            form = self.session.get(urls.login)
            page = BeautifulSoup(form.text, PARSER)
            token = page.select("form table tr:last-child input")[0]
            payload = {
                "submit": "Login",
                "username": username,
                "password": password,
                token.attrs['name']: token.attrs["value"]
            }
            self.session.post(urls.login, payload)
            console.print("Login Successful", style="green")
            self.logged_in = True

    def program_students(self, faculty: Faculty, program: Program, semester: str, term: str):
        data = []
        with console.status(f"Loading student for {program} Semester {semester}..."):
            size = self.__get_size__(faculty, program, semester, term)
            if size.isnumeric():
                size = int(size)
            else:
                print(
                    f"Warning! contains too many records, may not extract them all {size}")
                size = 11
            pageNumber = 1
            for i in range(int(size)):
                res = self.session.get(
                    urls.program_students(faculty.id, program.id, semester, term, pageNumber))
                soup = BeautifulSoup(res.text, PARSER)
                students = read_table(soup.select_one("#ewlistmain"))
                pager = soup.select("#ewpagerform table a")
                pager = [it.text for it in pager][:-1]
                pageNumber = (i * 10) + 1
                data = data + students
        return data

    def get_faculties(self):
        with console.status(f"Loading faculties..."):
            res = self.session.get(urls.faculties())
            soup = BeautifulSoup(res.text, PARSER)
            table = soup.select_one("#ewlistmain")
            table_data = read_table(table)
            data = []
            for it in table_data:
                link = find_link_in_table(table, it[0], "Courses")
                id = link[link.find("SchoolID"):]
                if id:
                    id = id[id.find("=")+1:]
                faculty = Faculty(id=id, name=it[1], link_to_courses=link)
                data.append(faculty)
            return data

    def get_programs(self, faculty: Faculty):
        with console.status(f"Loading programs for {faculty.name}..."):
            res = self.session.get(urls.get_full_url(faculty.link_to_courses))
            soup = BeautifulSoup(res.text, PARSER)
            table = soup.select_one("#ewlistmain")
            table_data = read_table(table)
            data = []
            for it in table_data:
                link = find_link_in_table(table, it[0], "Versions")
                id = link[link.find("ProgramID"):]
                if id:
                    id = id[id.find("=")+1:]
                program = Program(name=it[0], id=id)
                data.append(program)
            return data

    def __get_size__(self, faculty: Faculty,  program: Program, semester: str, term: str):
        res = self.session.get(
            urls.program_students(faculty.id, program.id, semester, term, "1"))
        soup = BeautifulSoup(res.text, PARSER)
        pager = soup.select("#ewpagerform table a")
        pager = [it.text for it in pager]
        return pager[-2]

    def print_transcript(self, student_id: str):
        with console.status(f"Printing transcript for {student_id}..."):
            res = self.session.get(urls.transcript(student_id))
            soup = BeautifulSoup(res.text, PARSER)
            transcript = soup.select_one("table.ewReportTable")

            html = transcript.prettify()
            html = f"<style>{stylesheet}</style>{html}"

            printer.print_text(html)
