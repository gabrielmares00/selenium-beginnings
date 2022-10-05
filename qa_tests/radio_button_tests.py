from definitions import driver
from selenium.webdriver.remote.webelement import WebElement
from typing import List
from utils import whole_document_element_finder as everywhere
from utils import under_current_node_element_finder as just_here


def _get_disabled_button(radio_list: List[WebElement]):
    for button in radio_list:
        if 'disabled' in button.get_attribute('innerHTML'):
            return button


def radio_button_tests_entry_point(driver: driver.MainDriver):
    radio_buttons = everywhere.find_elements(
        driver,
        'xpath',
        'div',
        class_name='custom-radio'
    )

    disabled_button = _get_disabled_button(radio_list=radio_buttons)

    print('Starting RADIO BUTTON tests')
    _check_if_radio_button_no_is_disabled(disabled_button)
    print('DONE')


#TODO: Check for mouse cursor type to change to disabled(?) when hovering over this button
def _check_if_radio_button_no_is_disabled(radio_button: WebElement):
    assert 'disabled' in radio_button.get_attribute('innerHTML')

    radio_input = just_here.find_element(
        radio_button,
        'xpath',
        'input',
        class_name='custom-control-input'
    )

    assert 'disabled' in radio_input.get_attribute('innerHTML')
    
    radio_label = just_here.find_element(
        radio_button,
        'xpath',
        'label',
        class_name='custom-control-input'
    )

    assert 'disabled' in radio_input.get_attribute('innerHTML')
