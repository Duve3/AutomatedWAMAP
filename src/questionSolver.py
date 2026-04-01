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


class QuestionSolver:
    def __init__(self, driver: cwebdriver.WebDriver):
        self.ai = AiHandler()
        self.driver: cwebdriver.WebDriver = driver

        self.questionCount = 1

    def iterateOverQuestions(self):
        while True:
            sleep(2)
            if self.QuestionCompleted():
                if self.NextQuestion():
                    continue
                return

            self.ScreenshotCurrentQuestion()

            print(f"Question {self.questionCount} screenshotted, asking AI")

            answers = self.ai.askQuestion("./question.png", PROMPT)

            print(f"QUESTION {self.questionCount} ANSWER: " + answers.text)

            if not self.NextQuestion():
                return

    def QuestionCompleted(self):
        # questions are only considered completed if the div of scoreresult correct exists
        try:
            label = self.driver.find_element(By.CSS_SELECTOR, 'div[class="scoreresult correct"]')

            if label.text == "":
                # just incase
                return False
            return True
        except exceptions.NoSuchElementException:
            return False

    def ScreenshotCurrentQuestion(self):
        div = self.driver.find_element(By.CSS_SELECTOR, 'div[class="home"]')
        div.screenshot("./question.png")

    def NextQuestion(self):
        button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next"]')

        if button.is_enabled():
            button.click()
            self.questionCount += 1
            return True

        return False
