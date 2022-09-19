from definitions import driver
from selenium.webdriver.common.by import By

def tools_qa_text_box_get_container(driver: driver.MainDriver):
    container = driver.find_element(
        By.XPATH,
        "//./div[contains(@class, 'text-field-container')]"
    )

    return container