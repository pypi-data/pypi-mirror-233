import os
import shutup
from asyncio import sleep
from typing import Dict, List, Union
from selenium.webdriver.common.by import By
from tttorrent.utils.driver import get_driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from tttorrent.exceptions.common import AuthError, TTTorrent
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, UnexpectedAlertPresentException

shutup.please()

_BASE_URL = "https://tt-torrent.com"


class NewClient:
    """Create a new instance to handle requests."""

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.driver = get_driver()

    async def auth(self) -> Union[List[Dict], None]:
        """Authentication handler."""
        self.driver.get(f"{_BASE_URL}/login.php")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "loginID")))
        self.driver.find_element(By.NAME, "loginID").send_keys(self.email)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.NAME, "submit").click()
        try:
            await sleep(2)
            self.driver.execute_script(
                "window.localStorage.setItem('__fb_chat_plugin', {'v':1,'path':2,'chatState':1,'visibility':'hidden','showUpgradePrompt':'not_shown','greetingVisibility':'hidden','shouldShowLoginPage':false})"
            )
        except UnexpectedAlertPresentException:
            alert = self.driver.switch_to.alert
            alert.accept()
            await sleep(2)
            self.driver.get(f"{_BASE_URL}/index.php")
        self.cookies = self.driver.get_cookies()
        err = self.driver.find_element(By.CLASS_NAME, "callout.alert")
        if err.is_displayed() and self.password in err.text:
            raise AuthError("wrong password")
        if err.is_displayed():
            raise AuthError("email not found")
        if "PHPSESSID" in str(self.cookies):
            return self.cookies
        return None

    async def _exec_report_action(self, action: str, tr=1):
        if action == "block" or action == "skip":
            self.driver.execute_script(
                """
            var elements = document.querySelectorAll("input.button");
                elements.forEach(element => {
                    element.removeAttribute('disabled')
            }) 
            """
            )
            if action == "block":
                self.driver.find_element(
                    By.XPATH, f"//body/div[@class='expanded row']/table/tbody/tr[{tr}]/td[5]/input[1]"
                ).click()
                await sleep(2)
                self.driver.find_element(
                    By.XPATH, f"//body/div[@class='expanded row']/table/tbody/tr[{tr}]/td[5]/input[3]"
                ).click()
                return
            elif action == "skip":
                self.driver.find_element(
                    By.XPATH, f"//body/div[@class='expanded row']/table/tbody/tr[{tr}]/td[5]/input[2]"
                ).click()
                await sleep(2)
                self.driver.find_element(
                    By.XPATH, f"//body/div[@class='expanded row']/table/tbody/tr[{tr}]/td[5]/input[3]"
                ).click()
                return
            raise ValueError(f"'block' or 'skip' are expected not {action}")

    async def reports(self, action="block", tr=1, show=False) -> Union[Dict, bool]:
        try:
            self.driver.get(f"{_BASE_URL}/report_staff.php")
        except UnexpectedAlertPresentException:
            alert = self.driver.switch_to.alert
            alert.accept()
            await sleep(2)
            self.driver.get(f"{_BASE_URL}/report_staff.php")
        try:
            self.driver.find_element(By.XPATH, "//body/div[@class='expanded row']/h2")
        except NoSuchElementException:
            try:
                self.driver.find_element(By.XPATH, "//body/div[@class='expanded row']/h2/font/font")
            except NoSuchElementException:
                raise TTTorrent("you are not admin")
        try:
            if self.driver.find_element(By.XPATH, "//body/div[@class='expanded row']/table/thead/tr/th[1]"):
                pass
        except NoSuchElementException:
            return False
        if show:
            qt = 0
            attemps = 100
            tabulate = {"reports": 0, "type": [], "fileName": [], "category": []}
            reports = self.driver.find_element(By.XPATH, "//body/div[@class='expanded row']/div[2]/ul/li[1]/a").text
            tabulate["reports"] = int(reports.replace("(", "").replace(")", ""))
            for table in range(attemps):
                try:
                    tp = self.driver.find_element(
                        By.XPATH, f"//body/div[@class='expanded row']/table/tbody/tr[{table}]/td[1]"
                    ).text
                    fn = self.driver.find_element(
                        By.XPATH, f"//body/div[@class='expanded row']/table/tbody/tr[{table}]/td[2]/a"
                    ).text
                    ct = self.driver.find_element(
                        By.XPATH, f"//body/div[@class='expanded row']/table/tbody/tr[{table}]/td[3]"
                    ).text
                    tabulate["type"].append(tp)
                    tabulate["fileName"].append(fn)
                    tabulate["category"].append(ct)
                except NoSuchElementException:
                    try:
                        tp = self.driver.find_element(
                            By.XPATH, f"//body/div[@class='expanded row']/table/tbody/tr[{table}]/td[1]/a/font/font"
                        ).text
                        fn = self.driver.find_element(
                            By.XPATH, f"//body/div[@class='expanded row']/table/tbody/tr[{table}]/td[2]/a/font/font"
                        ).text
                        ct = self.driver.find_element(
                            By.XPATH, f"//body/div[@class='expanded row']/table/tbody/tr[{table}]/td[3]/font/font"
                        ).text
                        tabulate["type"].append(tp)
                        tabulate["fileName"].append(fn)
                        tabulate["category"].append(ct)
                    except NoSuchElementException:
                        pass
            return tabulate
        await self._exec_report_action(action, tr=tr)
        await sleep(2)
        try:
            if self.driver.find_element(By.XPATH, "//body/div[@class='expanded row']/table/thead/tr/th[1]"):
                return True
        except NoSuchElementException:
            return False

    async def upload(
        self, name: str, category: int, torrent_path: str, image: str, description: str
    ) -> Union[str, None]:
        """Upload torrent handler."""
        self.driver.get(f"{_BASE_URL}/upload.php?category={category}")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "name")))
        self.driver.find_element(By.NAME, "name").send_keys(name)
        self.driver.find_element(By.ID, "file").send_keys(torrent_path)
        self.driver.find_element(
            By.XPATH,
            "//*[@id='poster']",
        ).send_keys(image)
        self.driver.find_element(By.NAME, "descr").send_keys(description)
        self.driver.execute_script("document.getElementById('submit').removeAttribute('disabled')")
        self.driver.find_element(By.ID, "submit").click()
        await sleep(2)
        try:
            if not self.driver.find_element(By.XPATH, "//body/div[3]/div[3]/div/fieldset/u[1]").text:
                raise ValueError("bad tracker, check it and try again")
        except NoSuchElementException:
            try:
                if not self.driver.find_element(By.XPATH, "//body/div[3]/div[3]/div/fieldset/u[1]/font/font").text:
                    raise ValueError("bad tracker, check it and try again")
            except NoSuchElementException:
                pass
        if "details.php" not in self.driver.current_url:
            return None
        return self.driver.current_url

    def close(self):
        return self.driver.quit()
