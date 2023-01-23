from bs4 import BeautifulSoup
from html_utils import find_link_in_table, read_table
import requests
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

    def get_programs(self):
        with console.status(f"Loading programs..."):
            res = self.session.get(urls.bos_page())
            soup = BeautifulSoup(res.text, PARSER)
            table = soup.select('select[name="course"] option')
            data = [it.get_text(strip=True) for it in table]

        return list(dict.fromkeys(data))
