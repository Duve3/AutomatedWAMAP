import base64
from time import sleep
from typing import Self

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
    
        # Get the div's full dimensions and position (including overflow)
        rect = self.driver.execute_script("""
            const el = arguments[0];
            const rect = el.getBoundingClientRect();
            return {
                x: rect.left + window.scrollX,
                y: rect.top + window.scrollY,
                width: el.scrollWidth,      // full width including overflow
                height: el.scrollHeight     // full height including overflow
            };
        """, div)

        result = self.driver.execute_cdp_cmd("Page.captureScreenshot", {
            "format": "png",
            "clip": {
                "x": rect["x"],
                "y": rect["y"],
                "width": rect["width"],
                "height": rect["height"],
                "scale": 1
            },
            "captureBeyondViewport": True  # captures content outside the viewport
        })

        with open("./question.png", "wb") as f:
            f.write(base64.b64decode(result["data"]))

    def NextQuestion(self):
        button = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next"]')

        if button.is_enabled():
            button.click()
            self.questionCount += 1
            return True

        return False
