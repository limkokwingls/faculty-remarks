from bs4 import BeautifulSoup
from html_utils import find_link_in_table, read_table
import requests
from model import Result
import urls
from rich.console import Console
from rich import print

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
            res = self.session.post(urls.login, payload)
            page = BeautifulSoup(res.text, PARSER)
            tags = page.select("p")

            if tags:
                display_name = tags[0]
                display_name = display_name.get_text(strip=True)
                if "Students" in display_name:
                    self.logged_in = True
                    return True

    def read_transcript(self, student_number: int, semester: int, progress="1/1"):
        with console.status(f"{progress}) Reading transcript for {student_number}"):
            response = self.session.get(urls.transcript(student_number))
            page = BeautifulSoup(response.text, PARSER)
            table = page.select_one("table.ewReportTable")
            if not table:
                raise Exception("Table not found")
            table_data = read_table(table)[2:-1]

            data = []
            semester_val = -1
            for it in table_data:
                if it and len(it) > 1 and "Semester" in it[0]:
                    semester_val = it[1].split(" ")[-1]
                if int(semester_val) == semester:
                    data.append(it)

        return self.__get_results(data)

    def get_programs(self):
        with console.status(f"Loading programs..."):
            res = self.session.get(urls.bos_page())
            soup = BeautifulSoup(res.text, PARSER)
            table = soup.select('select[name="course"] option')
            data = [it.get_text(strip=True) for it in table]

        return list(dict.fromkeys(data))

    def __get_results(self, data: list):
        data = [it for it in data if it
                and ('Term:' not in it)
                and ('Term' not in it)
                and ('Semester:' not in it)
                and ('Semester' not in it)
                and ('Results:' not in it)
                and ('Results' not in it)
                and ('Code:' not in it)
                and ('Code' not in it)
                and ('Total:' not in it)
                and ('Total' not in it)]
        results = []
        for it in data:
            result = Result(course=it[0], points=float(it[7]))
            results.append(result)
        return results
