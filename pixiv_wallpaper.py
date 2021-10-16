import os
import time
import ctypes
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
from plyer import notification


RANKING_PAGE_URL = "https://www.pixiv.net/ranking.php?mode=monthly&content=illust"
FIREFOX_PROFILE_PATH = r""


def get_illust_page(driver):
    driver.get(RANKING_PAGE_URL)
    section = driver.find_element_by_id("1")
    a = section.find_element_by_class_name("title")
    driver.get(a.get_attribute("href"))


def dl_illust(driver):
    time.sleep(1)
    try:
        div = driver.find_element_by_xpath("//div[text()='すべて見る']")
        button = div.find_element_by_xpath("..")
        button.click()
    except Exception:
        pass

    a = driver.find_element_by_class_name("gtm-expand-full-size-illust")
    url = a.get_attribute("href")
    extension = url.split(".")[-1]
    filename = f"illust.{extension}"

    file_list = os.listdir()
    for i in file_list:
        if "illust." in i:
            os.remove(i)

    headers = {"Referer": "https://www.pixiv.net/"}
    r = requests.get(url, headers=headers)
    with open(filename, "wb") as f:
        f.write(r.content)

    return filename


def set_wallpaper(filename):
    path = os.path.abspath(filename)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)


if __name__ == "__main__":
    options = Options()
    options.add_argument("--headless")
    profile = webdriver.FirefoxProfile(FIREFOX_PROFILE_PATH)
    driver = webdriver.Firefox(options=options, firefox_profile=profile)

    try:
        get_illust_page(driver)
        filename = dl_illust(driver)
        set_wallpaper(filename)
    except Exception as e:
        notification.notify(title="pixiv-wallpaper", message="エラーが発生しました")
        print(e)
    finally:
        pass
        driver.quit()
