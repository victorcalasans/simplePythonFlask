import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class AllTests(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless")  # roda sem interface gráfica
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Espera o Selenium subir
        for i in range(10):
            try:
                self.driver = webdriver.Remote(
                    command_executor="http://selenium:4444/wd/hub",
                    options=options
                )
                break
            except Exception as e:
                print("Esperando Selenium subir...", e)
                time.sleep(3)
        else:
            raise Exception("Selenium não respondeu")

        # Espera o Flask responder
        for i in range(10):
            try:
                self.driver.get("http://web:5000")
                return
            except Exception:
                print("Esperando aplicação web subir...")
                time.sleep(2)

        raise Exception("Aplicação web não respondeu")

    def test_user_can_register(self):
        self.driver.get("http://web:5000/register")

        self.driver.find_element(By.ID, "name").send_keys("devops")
        self.driver.find_element(By.ID, "email").send_keys("devops@email.com")
        self.driver.find_element(By.ID, "password").send_keys("qwe123qwe")
        self.driver.find_element(By.ID, "confirm").send_keys("qwe123qwe")
        self.driver.find_element(By.ID, "register").click()

        print(self.driver.current_url)

        self.assertIn("http://web:5000/", self.driver.current_url)
        assert "No results found." not in self.driver.page_source

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()