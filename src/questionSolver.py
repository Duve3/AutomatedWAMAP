from time import sleep
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.chrome.webdriver as cwebdriver
import selenium.common.exceptions as exceptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from aiHandler import AiHandler


PROMPT = """
Solve the following question. 
give EACH required answer (according to the input's) only, do not show work, do not write any other text.
Respond in LATEX format
If a question requires more than one response, separate each response by semicolon
"""


def iterateOverQuestions(driver: cwebdriver.WebDriver):
    ai = AiHandler()

    while True:
        sleep(2)
        if QuestionCompleted(driver):
            if NextQuestion(driver):
                continue
            return

        ScreenshotCurrentQuestion(driver)

        print("Question screenshotted, asking AI")

        answers = ai.askQuestion("./question.png", PROMPT)

        print("Answer: " + answers.text)

        if not NextQuestion(driver):
            return


def QuestionCompleted(driver: cwebdriver.WebDriver):
    # questions are only considered completed if the div of scoreresult correct exists
    try:
        label = driver.find_element(By.CSS_SELECTOR, 'div[class="scoreresult correct"]')

        if label.text == "":
            # just incase
            return False
        return True
    except exceptions.NoSuchElementException:
        return False


def ScreenshotCurrentQuestion(driver: cwebdriver.WebDriver):
    div = driver.find_element(By.CSS_SELECTOR, 'div[class="home"]')
    div.screenshot("./question.png")


def NextQuestion(driver: cwebdriver.WebDriver):
    button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next"]')

    if button.is_enabled():
        button.click()
        return True

    return False
