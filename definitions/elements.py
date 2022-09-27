from definitions.exceptions import WebElementIsNotInput, WebElementIsNotButton, WebElementIsNotDiv
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class Div():
    def __init__(self, web_element: WebElement) -> None:
        try:
            if web_element.tag_name not in ['div']:
                raise WebElementIsNotDiv

            self.__div = web_element
        except WebElementIsNotDiv as exception:
            exception.print()
    
    def get_attribute(self, attribute) -> None:
        return self.__div.get_attribute(attribute)
    
    def get_inner_element(self) -> None:
        return self.__div


class TextBox():
    def __init__(self, web_element: WebElement) -> None:
        try: 
            if web_element.tag_name not in ['input', 'textarea']:
                raise WebElementIsNotInput
            
            self.__text_box = web_element
        except WebElementIsNotInput as exception:
            exception.print()

    def clear_text(self) -> None:
        self.__text_box.clear()
    
    def get_text(self) -> None:
        return self.__text_box.get_attribute('value')
    
    def set_text(self, text) -> None:
        self.__text_box.send_keys(text)
    
    def get_attribute(self, attribute) -> None:
        return self.__text_box.get_attribute(attribute)


class Button():
    def __init__(self, webElement: WebElement) -> None:
        try:
            if webElement.tag_name not in ['input', 'button']:
                raise WebElementIsNotButton
            
            self.__button = webElement
        except WebElementIsNotButton as exception:
            exception.print()
    
    def get_attribute(self, attribute) -> None:
        return self.__button.get_attribute(attribute)
    
    def click(self) -> None:
        self.__button.click()