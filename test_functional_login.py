import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class AllTests(unittest.TestCase):

    def setUp(self):
        for i in range(10):
            try:
                self.driver = webdriver.Remote(
                    command_executor="http://selenium:4444/wd/hub",
                    options=webdriver.ChromeOptions()
                )
                return
            except Exception as e:
                print("Esperando Selenium subir...", e)
                time.sleep(3)

        raise Exception("Selenium não respondeu")

    def test_user_can_login(self):
        self.driver.get("http://web:5000")
        self.driver.find_element(By.ID, "name").send_keys("devops")
        self.driver.find_element(By.ID, "password").send_keys("qwe123qwe")
        self.driver.find_element(By.ID, "loginbutton").click()

        self.assertIn("http://web:5000/courses", self.driver.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()