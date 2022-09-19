from definitions.exceptions import WebElementIsNotInput, WebElementIsNotButton, WebElementIsNotDiv
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class Div():
    def __init__(self, web_element: WebElement) -> None:
        try:
            if web_element.tag_name not in ['div']:
                raise WebElementIsNotDiv

            self.div = web_element
        except WebElementIsNotDiv as exception:
            exception.print()

    def get_attribute(self, attribute) -> None:
        return self.div.get_attribute(attribute)
    
    def find_element(self, method: str, tag_name: str, class_name: str=None, id: str=None):
        match method:
            case 'xpath':
                try:
                    if class_name:
                        element = self.div.find_element(
                            By.XPATH,
                            "//./{}[contains(@class, '{}')]".format(tag_name, class_name)
                        )
                    elif id:
                        element = self.div.find_element(
                            By.XPATH,
                            "//./{}[@id='{}']".format(tag_name, id)
                        )
                    else:
                        raise AttributeError
                except AttributeError as exception:
                    exception.print()
            case 'tag_name':
               element = self.div.find_element(
                    By.TAG_NAME,
                    tag_name
                )

        return element
    
    #TODO: Find a better method to find elements, reduce duplicate code
    def find_elements(self, method: str, tag_name: str, class_name: str=None, id: str=None):
        match method:
            case 'xpath':
                try:
                    if class_name:
                        elements = self.div.find_elements(
                            By.XPATH,
                            "//./{}[contains(@class, '{}')]".format(tag_name, class_name)
                        )
                    elif id:
                        elements = self.div.find_elements(
                            By.XPATH,
                            "//./{}[@id='{}']".format(tag_name, id)
                        )
                    else:
                        raise AttributeError
                except AttributeError as exception:
                    exception.print()
            case 'tag_name':
               elements = self.div.find_elements(
                    By.TAG_NAME,
                    tag_name
                )

        return elements

class TextBox():
    def __init__(self, web_element: WebElement) -> None:
        try: 
            if web_element.tag_name not in ['input', 'textarea']:
                raise WebElementIsNotInput
            
            self.text_box = web_element
        except WebElementIsNotInput as exception:
            exception.print()

    def clear_text(self) -> None:
        self.text_box.clear()
    
    def get_text(self) -> None:
        return self.text_box.get_attribute('value')
    
    def set_text(self, text) -> None:
        self.text_box.send_keys(text)
    
    def get_attribute(self, attribute) -> None:
        return self.text_box.get_attribute(attribute)


class Button():
    def __init__(self, webElement: WebElement) -> None:
        try:
            if webElement.tag_name not in ['input', 'button']:
                raise WebElementIsNotButton
            
            self.button = webElement
        except WebElementIsNotButton as exception:
            exception.print()
    
    def get_attribute(self, attribute) -> None:
        return self.button.get_attribute(attribute)
    
    def click(self) -> None:
        self.button.click()