from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pathlib
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os

os.environ["DEBUSSY"] = "1"

c = Options()
c.add_argument("--headless")


tz_params = {'timezoneId': 'Europe/Berlin'}

match_url_list = list()
all_odds = list()


def get_match_urls(url):
    driver = webdriver.Chrome(
        executable_path=pathlib.Path(__file__).parent.resolve().joinpath("chromedriver.exe"), options=c)
    driver.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)
    try:
        driver.get(url)
    except:
        return get_match_urls(url)

    elements = driver.find_elements(By.CLASS_NAME, "table-participant")
    match_urls = list()
    for e in elements:
        links = e.find_elements(By.TAG_NAME, "a")
        for link in links:
            match_url = link.get_attribute("href")
            if match_url.startswith("https://"):
                match_urls.append(match_url)
    print(match_urls)
    return match_urls


def get_single_match_result(url):
    driver = webdriver.Chrome(
        executable_path=pathlib.Path(__file__).parent.resolve().joinpath("chromedriver.exe"), options=c)
    driver.execute_cdp_cmd('Emulation.setTimezoneOverride', tz_params)
    try:
        driver.get(url)

    except Exception as e:
        driver.close()
        return get_single_match_result(url)

    try:
        pinnacle_element = driver.find_element(By.XPATH,
                                               "//*[contains(text(), 'Pinnacle')]")
        parent_pinnacle = pinnacle_element.find_element(By.XPATH,
                                                        '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
    except NoSuchElementException:
        driver.close()
        return -1

    pinnacle_odds = parent_pinnacle.text.split(" ")
    try:
        odds = pinnacle_odds[3].split("\n")
    except:
        driver.close()
        return -1

    float_odds = [float(x) for x in odds[1:-1]]

    if not float_odds[0] > 2 or not float_odds[1] > 2 or not float_odds[2] > 2:
        driver.close()
        return -1

    minOdd = min(float_odds)
    minOdd_index = float_odds.index(minOdd)
    odd_web_element = parent_pinnacle.find_elements(
        By.CLASS_NAME, 'odds')[minOdd_index]
    isNotFound = True
    opening_odd = str()
    while isNotFound:
        try:
            ActionChains(driver).move_to_element(odd_web_element).perform()
            driver.execute_script(
                "arguments[0].scrollIntoView();", odd_web_element)
            opening_odd = WebDriverWait(driver, 5).until(
                ec.visibility_of_element_located((By.ID, "tooltipdiv")))
            opening_odds = opening_odd.find_element(
                By.XPATH, "//*[@id='tooltiptext']").find_elements(By.TAG_NAME, "strong")
            opening_odd = opening_odds[len(opening_odds)-1].text
            if opening_odd == "Click to BET NOW":
                opening_odd = opening_odds[len(opening_odds)-2].text

            isNotFound = False
        except Exception as e:
            pass
    try:
        match_score = driver.find_element(
            By.CLASS_NAME, "result").find_element(By.TAG_NAME, "strong").text
    except Exception as e:
        try:
            match_score = driver.find_element(
                By.CLASS_NAME, "live-score").find_element(By.TAG_NAME, "b").text
        except:
            match_score = "-"

    match_time = driver.find_element(By.CLASS_NAME, 'date').text[-5:]

    odds[0] = driver.find_element(By.TAG_NAME, "h1").text
    odds.append(opening_odd)
    odds.append(match_time)
    odds.append(match_score)

    print("odd: ", odds)
    if float(opening_odd) > 2:
        odds.append(True)
    else:
        odds.append(False)
    driver.close()
    return odds
