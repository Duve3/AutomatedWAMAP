from time import sleep

import selenium.webdriver as webdriver
from google import genai
from selenium.webdriver.common.by import By
import selenium.webdriver.chrome.webdriver as cwebdriver
import selenium.common.exceptions as exceptions
from selenium.webdriver.common.keys import Keys

from questionSolver import QuestionSolver


def listModels():
    with open("./login.env", "r") as f:
        data = f.read().splitlines()
        API_KEY = data[2]

    client = genai.Client(api_key=API_KEY)

    print(client.models.list().page)


def main():
    #listModels()
    print("Welcome to the WAMAP assignment solver")

    print("Loading ENV file")

    with open("./login.env", "r") as file:
        data = file.read().splitlines()

        if len(data) != 3:
            print("ENV file not setup correctly!")

            print("Ensure line 1 is WAMAP Username\nline 2 is WAMAP Password\nline 3 is Google GenAI api key")
            return

        print("Data is setup correctly ; if you have issues with logging in verify login info")

    seleniumSetup()


def seleniumSetup():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless")
    driver: cwebdriver.WebDriver = webdriver.Chrome(options=opts)
    print("Enter URL for selenium to fetch!")
    url = input("> ")

    if not url:
        url = "https://www.wamap.org/assess2/?cid=41964&aid=2438932#/"

    driver.get(url)

    driver.implicitly_wait(5)

    if LoggedIn(driver):
        print("We are logged in")
    else:
        Login(driver)

        # wait for the login to go through
        sleep(1.5)

    StartAssignment(driver)

    # wait for start to go through
    sleep(1.5)

    QuestionSolver(driver).iterateOverQuestions()

    print("assignment completed.")

    driver.quit()


def LoggedIn(driver: cwebdriver.WebDriver):
    try:
        driver.find_element(By.CSS_SELECTOR, 'label[for="username"]')
    except exceptions.NoSuchElementException:
        # login element doesn't exist, we are logged in already
        return True

    # login element exists, we are not logged in currently
    return False


def Login(driver: cwebdriver.WebDriver):
    with open("./login.env", "r") as file:
        data = file.read().splitlines()
        username = data[0]
        password = data[1]

    usernameInput = driver.find_element(By.CSS_SELECTOR, 'input[id="username"]')
    passwordInput = driver.find_element(By.CSS_SELECTOR, 'input[id="password"]')

    usernameInput.clear()
    usernameInput.send_keys(username)

    passwordInput.clear()
    passwordInput.send_keys(password)

    # automatically login via return key
    passwordInput.send_keys(Keys.RETURN)


def StartAssignment(driver: cwebdriver.WebDriver):
    try:
        # first we try resume element
        driver.find_element(By.XPATH, '//button[text()="Resume"]').click()
    except exceptions.NoSuchElementException:
        try:
            # then we try start element
            driver.find_element(By.XPATH, '//button[text()="Start"]').click()
        except exceptions.NoSuchElementException as e:
            print("FAILED TO FIND ANY START/RESUME BUTTON ON THE PAGE!!!!")
            raise e


if __name__ == "__main__":
    main()
