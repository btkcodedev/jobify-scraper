import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from jobify.sources import Browser


class Spotify(Browser):
    def __init__(self, url) -> None:
        super().__init__(url=url)
        self.job_info = {"role": [], "location": [], "category": [], "url": []}

    def load_all_jobs(self):
        WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//button")))
        all_buttons = {button.text: button for button in self.browser.find_elements(By.XPATH, "//button")}
        print("loading all jobs...")
        while True:
            try:
                load_more_button = self.browser.find_element(By.XPATH, '//button[text()="Load more jobs"]')
                self.browser.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                load_more_button.click()
                WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, '//button[text()="Load more jobs"]')))
            except WebDriverException:
                print("all jobs loaded...")
                break
            except Exception as e:
                print("page crashed")
                print("Error: ", e)
                time.sleep(3)

    def scrape_all_jobs(self):
        job_entries = self.browser.find_elements(By.CLASS_NAME, "entry_container__eT9IU")
        for job_entry in job_entries:
            job_title = job_entry.find_element(By.CLASS_NAME, "entry_title__Q0z3u").text.strip()
            location_element = job_entry.find_element(By.XPATH, ".//div[contains(@class, 'entry_locationCommitment__')]//span")
            location = location_element.text.strip()
            category_element = job_entry.find_element(By.XPATH, ".//div[contains(@class, 'tags_container__')]//p")
            category = category_element.text.strip()
            link = job_entry.find_element(By.CSS_SELECTOR, "a.entry_title__Q0z3u").get_attribute("href")

            self.job_info["role"].append(job_title)
            self.job_info["location"].append(location)
            self.job_info["category"].append(category)
            self.job_info["url"].append(link)
        return self.job_info
