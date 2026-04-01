from time import sleep

import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.chrome.webdriver as cwebdriver
import selenium.common.exceptions as exceptions
from selenium.webdriver.common.keys import Keys

from questionSolver import iterateOverQuestions


def main():
    driver: cwebdriver.WebDriver = webdriver.Chrome()
    driver.get("https://www.wamap.org/assess2/?cid=41964&aid=2438852#/")

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

    iterateOverQuestions(driver)

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
    # assumes that you need to resume assignment
    driver.find_element(By.XPATH, '//button[text()="Resume"]').click()




if __name__ == "__main__":
    main()
