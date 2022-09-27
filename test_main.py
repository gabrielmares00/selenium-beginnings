from definitions import driver

from qa_tests.text_box_tests import text_box_tests_entry_point as test_box_tests
from qa_tests.check_box_tests import check_box_tests_entry_point as check_box_tests

def start_tests(mainDriver: driver.MainDriver, mainActioner: driver.MainActioner):
    print('Starting tests...')

    mainDriver.go_to_url('https://demoqa.com/text-box')
    test_box_tests(mainDriver)

    mainDriver.go_to_url('https://demoqa.com/checkbox')
    check_box_tests(mainDriver, mainActioner)

    print('All tests done!')