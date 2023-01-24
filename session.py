import httpx
from bs4 import BeautifulSoup
import urls
from rich.console import Console

PARSER = "html5lib"
console = Console()


class Session:
    def __init__(self):
        transport = httpx.AsyncHTTPTransport(retries=5)
        # limits = httpx.Limits(
        #     max_keepalive_connections=None, max_connections=None)
        self.client = httpx.AsyncClient(
            follow_redirects=True, transport=transport, timeout=(90, 120))
        self.logged_in = False

    async def post(self, url, data):
        if not self.logged_in:
            raise RuntimeError("Not logged in")
        return await self.client.post(url, data=data)

    async def get(self, url):
        if not self.logged_in:
            raise RuntimeError("Not logged in")
        return await self.client.get(url)

    async def login(self, username: str, password: str):
        with console.status("Logging in..."):
            form = await self.client.get(urls.login)
            page = BeautifulSoup(form.text, PARSER)
            token = page.select("form table tr:last-child input")[0]
            payload = {
                "submit": "Login",
                "username": username,
                "password": password,
                token.attrs['name']: token.attrs["value"]
            }
            res = await self.client.post(urls.login, data=payload)
            page = BeautifulSoup(res.text, PARSER)
            tags = page.select("p")

            if tags:
                display_name = tags[0]
                display_name = display_name.get_text(strip=True)
                if "Students" in display_name:
                    self.logged_in = True
                    return True
