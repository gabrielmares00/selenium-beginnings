import time
from typing import List

from definitions import driver, elements
from selenium.webdriver.common.by import By

from utils import whole_document_element_finder as everywhere


def reset_fields(text_fields: List[elements.TextBox]):
    for field in text_fields:
        field.clear_text()


def text_box_tests_entry_point(mainDriver: driver.MainDriver):
    container = elements.Div(everywhere.tools_qa_get_container(mainDriver, 'text-field-container'))

    input_elements = everywhere.find_elements(container.get_inner_element(), 'tag_name', 'input')
    # print([element.get_attribute('placeholder') for element in input_elements])

    name_field = elements.TextBox(input_elements[0])
    email_field = elements.TextBox(input_elements[1])

    text_area_elements = everywhere.find_elements(container.get_inner_element(), 'tag_name', 'textarea')
    # print([element.get_attribute('placeholder') for element in text_area_elements])

    current_adress_field = elements.TextBox(text_area_elements[0])
    permanent_adress_field = elements.TextBox(text_area_elements[1])

    text_fields = [name_field, email_field, current_adress_field, permanent_adress_field]

    text_field_tests = [
        check_if_text_box_has_been_filled,
        check_if_text_box_has_been_filled_and_emptyd,
        check_if_text_box_is_empty,
    ]

    print('Starting text boxes validation tests...')
    for default_field_test in text_field_tests:
        for default_field in text_fields:
            default_field_test(default_field)
        
        reset_fields(text_fields)
    print('Done!')

    submit_button = elements.Button(
        everywhere.find_element(container.get_inner_element(), 'xpath', 'button', id='submit'))
    output_div = elements.Div(
        everywhere.find_element(container.get_inner_element(), 'xpath', 'div', id='output'))

    # https://gist.github.com/cjaoude/fd9910626629b53c4d25
    valid_emails = [
        "firstname.lastname@example.com",
        "email@subdomain.example.com",
        # "firstname+lastname@example.com", - Should have been valid
        "email@123.123.123.123",
        # "email@[123.123.123.123]", - Should have been valid
        "email@example.com",
        "1234567890@example.com",
        "email@example-one.com",
        "_______@example.com",
        #"email@example.name", - Should have been valid
        # "email@example.museum", - Should have been valid
        "email@example.co.jp",
        "firstname-lastname@example.com"
    ]

    print('Starting email field validation tests with VALID emails...')
    for valid_email in valid_emails:
        email_field_valid_input(output_div, email_field, submit_button, valid_email)
        
        reset_fields(text_fields)
    print('Done!')

    invalid_emails = [
        "plainaddress",
        "@example.com",
        "Joe Smith <email@example.com>",
        "email.example.com",
        "email@example@example.com",
        ".email@example.com",
        "email.@example.com",
        "email..email@example.com",
        "あいうえお@example.com",
        "email@example.com (Joe Smith)",
        "email@example",
        "email@-example.com",
        # "email@example.web", - Should have been invalid
        "email@111.222.333.44444",
        "email@example..com",
        "Abc..123@example.com",
    ]

    # This should be fine, field keeps the 'form-error' class attribute if another invalid email is given
    print('Starting email field validation tests with INVALID emails...')
    for invalid_email in invalid_emails:
        email_field_invalid_input(email_field, submit_button, invalid_email)
        
        reset_fields(text_fields)
    print('Done!')


def check_if_text_box_is_empty(text_field: elements.TextBox):
    assert text_field.get_text() == ""


def check_if_text_box_has_been_filled(text_field: elements.TextBox):
    assert text_field.get_text() == ""

    text_field.set_text('PogChamp')
    assert text_field.get_text() == 'PogChamp'


def check_if_text_box_has_been_filled_and_emptyd(text_field: elements.TextBox):
    assert text_field.get_text() == ""

    text_field.set_text('PogChamp')
    assert text_field.get_text() == 'PogChamp'

    text_field.clear_text()
    assert text_field.get_text() == ''


def email_field_valid_input(
        output_div: elements.Div,
        email_field: elements.TextBox,
        submit_button: elements.Button,
        email_to_validate: str):
    email_field.set_text(email_to_validate)
    submit_button.click()

    email_result = everywhere.find_element(output_div.get_inner_element(), 'tag_name', 'p')
    assert email_result.get_attribute('innerHTML') == "Email:{}".format(email_to_validate)


def email_field_invalid_input(
        email_field: elements.TextBox,
        submit_button: elements.Button,
        email_to_validate: str):
    email_field.set_text(email_to_validate)
    submit_button.click()

    assert 'field-error' in email_field.get_attribute('class')
