'''
Test Ideas:
1) Check if checkbox is enabled/disabled properly on click
2) Check if checkbox is enabled/disabled and selected field is shown in result div
3) Check if clicking on expand buttons shows the parent directory's children - DONE
4) Check if clicking on expand buttons when already toggled hides the children - DONE
5) Check if clicking on child FOLDER checkbox also adds parent folder(s) in result
6) Check if clicking on documents adds ONLY the document in result
7) Check if expand all button functions - DONE
8) Check if collapse all button functions - DONE
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


from utils import under_current_node_element_finder as just_here
from utils import whole_document_element_finder as everywhere
from typing import Dict
from definitions import driver, elements
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
from qa_tests.check_box_classes.file import File
from qa_tests.check_box_classes.folder import Folder


def reset_context_collapse_all(collapse_all_button: elements.Button):
    collapse_all_button.click()


def _generate_initial_folder(context: elements.Div):
    initial_folder = everywhere.find_element(
        context.get_inner_element(),
        'xpath',
        'li',
        class_name='rct-node-parent')
    initial_folder_span = everywhere.find_element(
        initial_folder, 'xpath', 'span', class_name='rct-title')
    root_name = initial_folder_span.get_attribute('innerHTML')

    return initial_folder, root_name


def _append_current_folder(
        folders: Dict,
        index: int,
        root_name: str,
        hierarchy: Dict):
    children_span = everywhere.find_element(
        folders[index],
        'xpath',
        'span',
        class_name='rct-title'
    )
    children_name = children_span.get_attribute('innerHTML')
    temp_dict = {children_name: []}
    hierarchy[root_name].append(temp_dict)


def _get_folder_children(folder: WebElement):
    return just_here.find_elements(folder, 'xpath', 'ol/li')


def _get_element_title(element: WebElement):
    element_span = everywhere.find_element(
        element, 'xpath', 'span', class_name='rct-title')
    return element_span.get_attribute('innerHTML')


def _generate_documents_special_case(root_folder: WebElement, node_name: str):
    documents_obj_folders = Folder(node_name)
    documents_folders = _get_folder_children(root_folder)

    for document_content in documents_folders:
        document_node_name = _get_element_title(document_content)
        if 'rct-node-parent' in document_content.get_attribute('class'):
            documents_obj_folders.append_folder(Folder(document_node_name))
        elif 'rct-node-leaf' in document_content.get_attribute('class'):
            documents_obj_folders.append_file(File(document_node_name))

    return documents_obj_folders


def _extract_result_text(context: WebElement):
    result_context = everywhere.find_element(context.get_inner_element(), 'xpath', 'div', id='result')
    result_text_elements = just_here.find_elements(result_context, 'xpath', 'span', class_name='text-success')
    result_text_extracted = [result.get_attribute('innerHTML') for result in result_text_elements]

    result_text = ' '.join(result_text_extracted)
    return result_text


def _reset_home_selection(context: WebElement):
    initial_folder_entry = _generate_initial_folder(context)[0]

    initial_folder_entry_checkbox = initial_folder_entry.find_element(
        By.XPATH,
        ".//span[contains(@class, 'rct-checkbox')]/*[name()='svg']"
    )
    folder_checkbox_status = initial_folder_entry_checkbox.get_attribute('class')

    if 'rct-icon-check' in folder_checkbox_status:
        initial_folder_entry.click()
    elif 'rct-icon-half-check' in folder_checkbox_status:
        initial_folder_entry.click()
        sleep(1)
        initial_folder_entry.click()


def check_box_tests_entry_point(driver: driver.MainDriver, actioner: driver.MainActioner):
    container = elements.Div(everywhere.tools_qa_get_container(
        driver, 'check-box-tree-wrapper'))
    # print(container.get_attribute('innerHTML'))

    expand_all_button = elements.Button(
        everywhere.find_element(
            container.get_inner_element(),
            'xpath',
            'button',
            class_name='rct-option-expand-all'))
    collapse_all_button = elements.Button(
        everywhere.find_element(
            container.get_inner_element(),
            'xpath',
            'button',
            class_name='rct-option-collapse-all'))

    print('Starting regular CHECK BOX tests...')
    check_if_root_is_collapsed(context=container)
    click_expand_all_button(
        context=container, expand_all_button=expand_all_button)
    expand_and_collapse_n_times(
        context=container,
        expand_all_button=expand_all_button,
        collapse_all_button=collapse_all_button,
        times=10
    )
    check_root_folder(context=container)

    check_parsing_root_folder(
        actioner=actioner,
        context=container)
    reset_context_collapse_all(collapse_all_button)

    check_parsing_expanded_tree(
        expand_all_button=expand_all_button,
        context=container
    )
    reset_context_collapse_all(collapse_all_button)

    check_selected_just_root(context=container)
    _reset_home_selection(context=container)

    check_selected_subfolderfolder_selected(context=container)
    reset_context_collapse_all(collapse_all_button)
    _reset_home_selection(context=container)

    check_selected_file_selected(context=container)
    print('Done!')


def check_if_root_is_collapsed(context: elements.Div):
    root_directory = everywhere.find_elements(
        context.get_inner_element(),
        'xpath',
        'li',
        class_name='rct-node-collapsed')

    assert len(root_directory) == 1


def click_expand_all_button(
        context: elements.Div,
        expand_all_button: elements.Button):
    expand_all_button.click()

    expanded_directories = everywhere.find_elements(
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
        expanded_directories = everywhere.find_elements(
            context.get_inner_element(),
            'xpath',
            'li',
            class_name='rct-node-expanded')
        assert len(expanded_directories) != 0

        collapse_all_button.click()
        collapsed_directories = everywhere.find_elements(
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

    initial_folder = everywhere.find_element(
        context.get_inner_element(), 'xpath', 'li', class_name='rct-node-parent')
    initial_folder_name = everywhere.find_element(
        initial_folder, 'xpath', 'span', class_name='rct-title')
    hierarchy_obtained[initial_folder_name.get_attribute('innerHTML')] = []

    assert hierarchy_to_test == hierarchy_obtained


def check_parsing_root_folder(
        actioner: driver.MainActioner,
        context: elements.Div):
    hierarchy_to_obtain = {
        'Home': [
            {'Desktop': []},
            {'Documents': []},
            {'Downloads': []}
        ]
    }

    hierarchy_tested = {}

    initial_folder_entry, root_name = _generate_initial_folder(context)
    hierarchy_tested[root_name] = []

    root_toggle_button = everywhere.find_element(
        initial_folder_entry,
        'xpath',
        'button',
        class_name='rct-collapse-btn')
    actioner.move_to_element(root_toggle_button).click().perform()

    folders_under_root = just_here.find_elements(
        initial_folder_entry, 'xpath', 'ol/li')

    for title_index in range(0, len(folders_under_root)):
        _append_current_folder(
            folders_under_root, title_index, root_name, hierarchy_tested)

    # print(hierarchy_to_obtain)
    # print(hierarchy_tested)

    assert hierarchy_tested == hierarchy_to_obtain


# TODO: THIS IS REALLY BAD AND ASSUMES 3 FOLDER LEVELS AND IS HARDCODED IN (PROBABLY) THE WORST WAY POSSIBLE
# TODO: FIX THIS ASAP
def check_parsing_expanded_tree(
        expand_all_button: elements.Button,
        context: elements.Div):
    expand_all_button.click()

    desktop_folder = Folder('Desktop', files=[File('Notes'), File('Commands')])

    workspace_folder = Folder(
        'WorkSpace', files=[File('React'), File('Angular'), File('Veu')])
    office_folder = Folder('Office', files=[File('Public'), File(
        'Private'), File('Classified'), File('General')])
    documents_folder = Folder('Documents', folders=[
                              workspace_folder, office_folder])

    downloads_folder = Folder(
        'Downloads', files=[File('Word File.doc'), File('Excel File.doc')])
    hierarchy_to_obtain = Folder(
        'Home', folders=[desktop_folder, documents_folder, downloads_folder])

    initial_folder_entry, root_name = _generate_initial_folder(context)
    hierarchy_to_test = Folder(root_name)

    folders_under_root = _get_folder_children(initial_folder_entry)

    for folder in folders_under_root:
        folder_name = _get_element_title(folder)
        obj_folder = Folder(folder_name)

        new_folders = _get_folder_children(folder)
        for new_folder in new_folders:
            node_name = _get_element_title(new_folder)

            if 'rct-node-parent' in new_folder.get_attribute('class'):
                if node_name == 'Documents':
                    obj_folder.append_folder(
                        _generate_documents_special_case(
                            root_folder=new_folder,
                            node_name=node_name
                        )
                    )
                else:
                    obj_folder.append_folder(Folder(node_name))
            elif 'rct-node-leaf' in new_folder.get_attribute('class'):
                obj_folder.append_file(File(node_name))

        hierarchy_to_test.append_folder(obj_folder)

    # print([folder.get_folder_name() for folder in hierarchy_to_obtain.get_folders()])
    # print([folder.get_folder_name() for folder in hierarchy_to_test.get_folders()])

    # for subfolder in hierarchy_to_obtain.get_folders():
    #     print([folder.get_folder_name() for folder in subfolder.get_folders()])
    #     print([file.get_file_name() for file in subfolder.get_files()])

    # for subfolder in hierarchy_to_test.get_folders():
    #     print([folder.get_folder_name() for folder in subfolder.get_folders()])
    #     print([file.get_file_name() for file in subfolder.get_files()])

    # print(hierarchy_to_test.folders)
    # print(hierarchy_to_obtain.folders)
    assert hierarchy_to_obtain == hierarchy_to_test


def check_selected_just_root(context: elements.Div):
    initial_folder_entry = _generate_initial_folder(context)[0]
    initial_folder_entry.click()

    initial_folder_entry_checkbox = initial_folder_entry.find_element(
        By.XPATH,
        ".//span[contains(@class, 'rct-checkbox')]/*[name()='svg']"
    )

    assert 'rct-icon-check' in initial_folder_entry_checkbox.get_attribute('class')

    expected_result = 'home desktop notes commands documents workspace react angular veu office public private classified general downloads wordFile excelFile'
    result = _extract_result_text(context=context)

    assert expected_result == result


def check_selected_subfolderfolder_selected(context: elements.Div):
    initial_folder_entry = _generate_initial_folder(context)[0]
    initial_folder_toggle = everywhere.find_element(initial_folder_entry, 'xpath', 'button', class_name='rct-collapse')
    initial_folder_toggle.click()

    root_subfolders = _get_folder_children(initial_folder_entry)
    downloads_folder = root_subfolders[2]
    downloads_folder.click()

    downloads_folder_checkbox = downloads_folder.find_element(
        By.XPATH,
        ".//span[contains(@class, 'rct-checkbox')]/*[name()='svg']"
    )

    assert 'rct-icon-check' in downloads_folder_checkbox.get_attribute('class')

    downloads_folder_files = _get_folder_children(downloads_folder)
    for file in downloads_folder_files:
        file_checkbox = file.find_element(
            By.XPATH,
            ".//span[contains(@class, 'rct-checkbox')]/*[name()='svg']"
        )

        assert 'rct-icon-check' in file_checkbox.get_attribute('class')

    initial_folder_entry_checkbox = initial_folder_entry.find_element(
        By.XPATH,
        ".//span[contains(@class, 'rct-checkbox')]/*[name()='svg']"
    )

    assert 'rct-icon-half-check' in initial_folder_entry_checkbox.get_attribute('class')

    expected_result = 'downloads wordFile excelFile'
    result = _extract_result_text(context=context)

    assert expected_result == result


def check_selected_file_selected(context: elements.Div):
    initial_folder_entry = _generate_initial_folder(context)[0]
    initial_folder_toggle = everywhere.find_element(initial_folder_entry, 'xpath', 'button', class_name='rct-collapse')
    initial_folder_toggle.click()

    root_subfolders = _get_folder_children(initial_folder_entry)
    downloads_folder = root_subfolders[2]
    downloads_folder_toggle = everywhere.find_element(downloads_folder, 'xpath', 'button', class_name='rct-collapse')
    downloads_folder_toggle.click()

    download_files = _get_folder_children(downloads_folder)
    excel_file = download_files[1]
    excel_file.click()

    excel_file_checkbox = excel_file.find_element(
        By.XPATH,
        ".//span[contains(@class, 'rct-checkbox')]/*[name()='svg']"
    )

    assert 'rct-icon-check' in excel_file_checkbox.get_attribute('class')
    
    downloads_folder_checkbox = downloads_folder.find_element(
        By.XPATH,
        ".//span[contains(@class, 'rct-checkbox')]/*[name()='svg']"
    )

    assert 'rct-icon-half-check' in downloads_folder_checkbox.get_attribute('class')

    initial_folder_entry_checkbox = initial_folder_entry.find_element(
        By.XPATH,
        ".//span[contains(@class, 'rct-checkbox')]/*[name()='svg']"
    )

    assert 'rct-icon-half-check' in initial_folder_entry_checkbox.get_attribute('class')

    expected_result = 'excelFile'
    result = _extract_result_text(context=context)

    assert expected_result == result
