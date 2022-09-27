from definitions import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def _generate_Xpath_single_element(
        base_element: WebElement,
        tag_name: str,
        class_name: str=None,
        id: str=None):
    try:
        if class_name:
            return base_element.find_element(
                By.XPATH,
                ".//{}[contains(@class, '{}')]".format(tag_name, class_name)
            )
        elif id:
            return base_element.find_element(
                By.XPATH,
                ".//{}[@id='{}']".format(tag_name, id)
            )
        else:
            raise AttributeError
    except AttributeError as exception:
        print(exception)


def _generate_Xpath_list_element(
        base_element: WebElement,
        tag_name: str,
        class_name: str=None,
        id: str=None):
    try:
        if class_name:
            return base_element.find_elements(
                By.XPATH,
                ".//{}[contains(@class, '{}')]".format(tag_name, class_name)
            )
        elif id:
            return base_element.find_elements(
                By.XPATH,
                ".//{}[@id='{}']".format(tag_name, id)
            )
        else:
            raise AttributeError
    except AttributeError as exception:
        print(exception)


def find_element(
        element: WebElement,
        method: str,
        tag_name: str,
        class_name: str=None,
        id: str=None):
    match method:
        case 'xpath':
            found_element = _generate_Xpath_single_element(element, tag_name, class_name, id)
        case 'tag_name':
           found_element = element.find_element(
                By.TAG_NAME,
                tag_name
            )
        case _:
            raise AttributeError

    return found_element


def find_elements(
        element: WebElement,
        method: str,
        tag_name: str,
        class_name: str=None,
        id: str=None):
    match method:
        case 'xpath':
            found_elements = _generate_Xpath_list_element(element, tag_name, class_name, id)
        case 'tag_name':
           found_elements = element.find_elements(
                By.TAG_NAME,
                tag_name
            )
        case _:
            raise AttributeError

    return found_elements or []

def tools_qa_get_container(driver: driver.MainDriver, container_name: str):
    container = driver.find_element(
        By.XPATH,
        "//./div[contains(@class, '{}')]".format(container_name)
    )

    return container
