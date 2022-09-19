from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


class MainDriver(webdriver.Chrome):
    def __init__(self) -> None:
        
        self.service = Service(executable_path=ChromeDriverManager().install())
        self.options = Options()
        # self.options.set_headless()
        self.options.add_experimental_option('detach', True)

        super().__init__(service=self.service, options=self.options)

    def go_to_url(self, url) -> None:
        self.get(url)

    def closeDriver(self) -> None:
        print('Finishing main loop...')
        self.quit()
    
    def checkDriverStatus(self) -> None:
        print("Is driver alive: {}".format(self.service.is_connectable()))

class MainActioner(ActionChains):
    def __init__(self, driver, duration=250):
        super().__init__(driver, duration)
