from typing import Union
from asyncio import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

_BASE_URL = "https://filebin.net"


async def image_uploader(driver, image_path) -> Union[str, None]:
    driver.get(_BASE_URL)
    driver.find_element(By.ID, "fileField").send_keys(image_path)
    await sleep(2)
    url = driver.find_element(By.XPATH, "//body/table/tbody/tr/td[1]/a").get_attribute("href")
    if url == None:
        return None
    return url
