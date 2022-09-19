from definitions import driver

from qa_tests.text_box_tests import text_box_tests_entry_point as test_box_tests

def start_tests(mainDriver: driver.MainDriver):
    print('Starting tests...')

    test_box_tests(mainDriver)

    print('All tests done!')