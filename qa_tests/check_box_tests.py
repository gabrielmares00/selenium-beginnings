'''
Test Ideas:
1) Check if checkbox is enabled/disabled properly on click
2) Check if checkbox is enabled/disabled and selected field is shown in result div
3) Check if clicking on expand buttons shows the parent directory's children
4) Check if clicking on expand buttons when already toggled hides the children
5) Check if clicking on child FOLDER checkbox also adds parent folder(s) in result
6) Check if clicking on documents adds ONLY the document in result
7) Check if expand all button functions
8) Check if collapse all button functions
'''

'''
{
    'Home':
    {
        'Desktop': [Notes, Command]
    }
    ...
}
'''

from definitions import driver, elements
from selenium.webdriver.common.by import By

import utils


def reset_context_collapse_all(collapse_all_button: elements.Button):
    collapse_all_button.click()


def check_box_tests_entry_point(driver: driver.MainDriver, actioner: driver.MainActioner):
    container = elements.Div(utils.tools_qa_get_container(driver, 'check-box-tree-wrapper'))
    # print(container.get_attribute('innerHTML'))

    expand_all_button = elements.Button(
        utils.find_element(container.get_inner_element(), 'xpath', 'button', class_name='rct-option-expand-all'))
    collapse_all_button = elements.Button(
        utils.find_element(container.get_inner_element(), 'xpath', 'button', class_name='rct-option-collapse-all'))

    print('Starting regular CHECK BOX tests...')
    check_if_root_is_collapsed(context=container)
    click_expand_all_button(context=container, expand_all_button=expand_all_button)
    expand_and_collapse_n_times(
        context=container,
        expand_all_button=expand_all_button,
        collapse_all_button=collapse_all_button,
        times=10
    )
    check_root_folder(context=container)
    check_parsing_root_folder(
        driver=driver,
        actioner=actioner,
        context=container)
    print('Done!')


def check_if_root_is_collapsed(context: elements.Div):
    root_directory = utils.find_elements(
        context.get_inner_element(),
        'xpath',
        'li',
        class_name='rct-node-collapsed')

    assert len(root_directory) == 1


def click_expand_all_button(
        context: elements.Div,
        expand_all_button: elements.Button):
    expand_all_button.click()

    expanded_directories = utils.find_elements(
        context.get_inner_element(),
        'xpath',
        'li',
        class_name='rct-node-expanded')
    assert len(expanded_directories) != 0


def expand_and_collapse_n_times(
        context: elements.Div,
        expand_all_button: elements.Button,
        collapse_all_button: elements.Button,
        times: int):
    for n in range(0, times):
        expand_all_button.click()
        expanded_directories = utils.find_elements(
            context.get_inner_element(),
            'xpath',
            'li',
            class_name='rct-node-expanded')
        assert len(expanded_directories) != 0

        collapse_all_button.click()
        collapsed_directories = utils.find_elements(
            context.get_inner_element(),
            'xpath',
            'li',
            class_name='rct-node-collapsed')
        assert len(collapsed_directories) != 0


def check_root_folder(
        context: elements.Div):
    hierarchy_to_test = {
        'Home': []
    }

    hierarchy_obtained = {}

    initial_folder = utils.find_element(context.get_inner_element(), 'xpath', 'li', class_name='rct-node-parent')
    initial_folder_name = utils.find_element(initial_folder, 'xpath', 'span', class_name='rct-title')
    hierarchy_obtained[initial_folder_name.get_attribute('innerHTML')] = []

    assert hierarchy_to_test == hierarchy_obtained


def check_parsing_root_folder(
        driver: driver.MainDriver,
        actioner: driver.MainActioner,
        context: elements.Div):
    hierarchy_to_test = {
        'Home': [
            {'Desktop': []},
            {'Documents': []},
            {'Downloads': []}
        ]
    }

    hierarchy_obtained = {}

    initial_folder = utils.find_element(context.get_inner_element(), 'xpath', 'li', class_name='rct-node-parent')
    initial_folder_span = utils.find_element(initial_folder, 'xpath', 'span', class_name='rct-title')
    root_name = initial_folder_span.get_attribute('innerHTML')
    hierarchy_obtained[root_name] = []

    root_toggle_button = utils.find_element(initial_folder, 'xpath', 'button', class_name='rct-collapse-btn')
    actioner.move_to_element(root_toggle_button).click().perform()

    #Find a way to better parse this
    #New function to get under element(IT'S NAMED THE SAME AS PARENT LIKE WHYYYYYYYYY)
    root_children = utils.find_elements(
        context.get_inner_element(),
        'xpath',
        'li/ol/li',
        class_name='rct-node-parent')
    
    for title_index in range(0, len(root_children)):
        children_span = utils.find_element(
            root_children[title_index],
            'xpath',
            'span',
            class_name='rct-title'
        )
        print(children_span.get_attribute('innerHTML'))
        children_name = children_span.get_attribute('innerHTML')
        temp_dict = {children_name: []}
        hierarchy_obtained[root_name].append(temp_dict)
    
    print(hierarchy_obtained)
    print(hierarchy_to_test)

    assert hierarchy_to_test == hierarchy_obtained
