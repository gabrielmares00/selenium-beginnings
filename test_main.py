from definitions import driver

from qa_tests.text_box_tests import text_box_tests_entry_point as test_box_tests
from qa_tests.check_box_tests import check_box_tests_entry_point as check_box_tests
from qa_tests.radio_button_tests import radio_button_tests_entry_point as radio_button_tests

import os

def start_tests(mainDriver: driver.MainDriver, mainActioner: driver.MainActioner):
    print('Starting tests...')

    options = [1, 2, 3]
    try:
        specificTest = int(
            input(
                "Run specific test:\n" +
                "1) Text Box\n" +
                "2) Check Box\n" +
                "3) Radio Button\n"
                "Input: "
            )
        )

        if specificTest not in options:
            raise AttributeError
    except AttributeError as exception:
        print("Input one of the following: {}".format([option for option in options]))
        os._exit(1)
    finally:
        match specificTest:
            case 1:
                mainDriver.go_to_url('https://demoqa.com/text-box')
                test_box_tests(mainDriver)
            case 2:
                mainDriver.go_to_url('https://demoqa.com/checkbox')
                check_box_tests(mainDriver, mainActioner)
            case 3:
                mainDriver.go_to_url('https://demoqa.com/radio-button')
                radio_button_tests(mainDriver)
            case _:
                pass

    print('All tests done!')
