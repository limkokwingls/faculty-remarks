import httpx
from bs4 import BeautifulSoup
from rich.console import Console
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import urls

PARSER = "html5lib"
console = Console()


class Session:
    def __init__(self):
        transport = httpx.AsyncHTTPTransport(retries=5)
        limits = httpx.Limits(max_connections=5)
        self.client = httpx.AsyncClient(
            follow_redirects=True, transport=transport, timeout=(90, 120), limits=limits
        )
        self.logged_in = False

    async def post(self, url, data):
        if not self.logged_in:
            raise RuntimeError("Not logged in")
        return await self.client.post(url, data=data)

    async def get(self, url):
        if not self.logged_in:
            raise RuntimeError("Not logged in")
        return await self.client.get(url)

    async def login(self):
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )

        driver.get(urls.login)
        WebDriverWait(driver, 60 * 3).until(
            expected_conditions.presence_of_element_located(
                (By.LINK_TEXT, "[ Logout ]")
            )
        )

        cookies = driver.get_cookies()
        driver.quit()

        self.client.cookies.update({it["name"]: it["value"] for it in cookies})
        self.logged_in = True
        return self.logged_in
