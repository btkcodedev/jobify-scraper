import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def setup_chromedriver():
    chromedriver_autoinstaller.install()


def verify_human(browser):
    WebDriverWait(browser, 20).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@value='Verify you are human']")))
    verify_button = browser.find_elements(By.XPATH, "//input[@value='Verify you are human']")
    verify_button[0].click()
    return
