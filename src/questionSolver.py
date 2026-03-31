import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.chrome.webdriver as cwebdriver
import selenium.common.exceptions as exceptions
from selenium.webdriver.common.keys import Keys

from aiHandler import AiHandler


PROMPT = """
Solve the following question. 
give EACH required answer (according to the input's) only, do not show work, do not write any other text.
"""


def iterateOverQuestions(driver: cwebdriver.WebDriver):
    ai = AiHandler()

    # WARN: this actually goes to question 2 immediately, idk how to avoid
    while True:
        if QuestionCompleted(driver):
            continue

        ScreenshotCurrentQuestion(driver)

        print("Question screenshoted, asking AI")

        answers = ai.askQuestion("./question.png", PROMPT)

        print(answers)

        if not NextQuestion(driver):
            return


def QuestionCompleted(driver: cwebdriver.WebDriver):
    # questions are only considered completed if the div of scoreresult correct exists
    try:
        driver.find_element(By.CSS_SELECTOR, 'div[class="scoreresult correct"][tabindex="-1"]')
    except exceptions.NoSuchElementException:
        return False

    return True


def ScreenshotCurrentQuestion(driver: cwebdriver.WebDriver):
    div = driver.find_element(By.CSS_SELECTOR, 'div[class="home"]')
    div.screenshot("./question.png")


def NextQuestion(driver: cwebdriver.WebDriver):
    button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next"]')

    if button.is_enabled():
        button.click()
        return True

    return False
