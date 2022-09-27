import os
from ast import main

from definitions import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import test_main


def main():
    options = [1, 2, 3]
    try:
        testExercise = int(
            input(
                "Select test:\n" +
                "1) Show maintaned python versions\n" +
                "2) Verify decorators example count\n" +
                "3) Run tests on ToolsQA\n"
                "Input: "
            )
        )

        if testExercise not in options:
            raise AttributeError
    except AttributeError as exception:
        print("Input one of the following: {}".format([option for option in options]))
        os._exit(1)
    finally:
        mainDriver = driver.MainDriver()

        mainDriver.implicitly_wait(20)

        mainActioner = driver.MainActioner(mainDriver)

        match testExercise:
            case 1:
                mainDriver.go_to_url('https://www.python.org/')
                maintained_versions(mainDriver=mainDriver, mainActioner=mainActioner)
            case 2:
                mainDriver.go_to_url('https://www.python.org/')
                check_decorators_examples_count(mainDriver=mainDriver)
            case 3:
                tests_demoqa(mainDriver=mainDriver, mainActioner=mainActioner)
            case _:
                pass


def maintained_versions(mainDriver: driver.MainDriver, mainActioner: driver.MainActioner):
    '''
    Initial attempt -> cannot interact with the release a element, need to use other search method?

        # downloadsHeader = mainDriver.find_element(By.ID, 'downloads')
        # # print(downloadsHeader.get_attribute('innerHTML'))

        # downloadsTable = downloadsHeader.find_element(By.CLASS_NAME, 'subnav')
        # # print(downloadsTable.get_attribute('innerHTML'))

        # downloadsCells = downloadsTable.find_elements(By.CLASS_NAME, 'tier-2')
        # # print([element for element in downloadsCells])

        # allReleasesCell = downloadsCells[0]
        # # print(allReleasesCell.get_attribute('innerHTML'))
        # allReleasesCell.click()

    '''

    '''
        Second attempt -> Still couldn't get over the hidden restriction Selenium has
        Discovered ActionChains

            mainNavBar = mainDriver.find_element(
                By.XPATH,
                "//./div[contains(@class, 'container')]/nav[@id='mainnav']/ul[contains(@class, 'navigation menu')]")
            # print(mainNavBar.get_attribute('innerHTML'))

            downloadsTab = mainNavBar.find_element(By.XPATH, ".//li[@id='downloads']")
            # print(downloadsTab.get_attribute('aria-hidden'))
            # print(downloadsTab.get_attribute('aria-haspopup'))
            # print(downloadsTab.is_displayed())
            # print(downloadsTab.get_attribute('innerHTML'))

            # downloadsListCells = downloadsTab.find_elements(By.XPATH, ".//li[contains(@class, 'tier-2')]")
            # print(downloadsListCells.is_displayed())
            # print([element.get_attribute('innerHTML') and element.is_displayed() for element in downloadsListCells])
            # mainDriver.execute_script("arguments[0].click()", downloadsListCells[0])
            print(mainDriver.current_url)
        '''

    mainNavBar = mainDriver.find_element(
        By.XPATH,
        "//./div[contains(@class, 'container')]/nav[@id='mainnav']/ul[contains(@class, 'navigation menu')]")

    downloadsTab = mainNavBar.find_element(By.XPATH, ".//li[@id='downloads']")
    allReleasesCell = downloadsTab.find_element(
        By.XPATH, ".//li[contains(@class, 'tier-2')]")

    mainActioner.move_to_element(downloadsTab).click(allReleasesCell).perform()
    # print(mainDriver.current_url)

    releasesSection = mainDriver.find_element(
        By.XPATH,
        "//./div[@id='touchnav-wrapper']/div[@id='content']/div[contains(@class, 'container')]/section[contains(@class, 'main-content')]"
    )
    # print(releasesSection.get_attribute('innerHTML'))

    pythonVers = releasesSection.find_element(
        By.XPATH,
        ".//div[contains(@class, 'active-release-list-widget')]/ol"
    )
    # print(pythonVers.get_attribute('innerHTML'))

    print("Maintained versions:")
    for element in pythonVers.find_elements(By.XPATH, ".//li"):
        # print(element.get_attribute('innerHTML'))

        elementVersion = element.find_element(
            By.XPATH, ".//span[1]").get_attribute('innerHTML')
        elementStatus = element.find_element(
            By.XPATH, ".//span[2]").get_attribute('innerHTML')
        print(
            f'Python ver {elementVersion}, with release status: {elementStatus}')
    
    mainDriver.closeDriver()
    mainDriver.checkDriverStatus()


def check_decorators_examples_count(mainDriver: driver.MainDriver):
    searchBar = mainDriver.find_element(By.XPATH, "//*[@id='id-search-field']")

    # Fun fact: La un moment dat cand scriam la exercitiul asta, o picat search-ul de la python :D
    searchBar.clear()
    searchBar.send_keys('decorator')
    searchBar.send_keys(Keys.RETURN)

    searchResultsList = mainDriver.find_element(
        By.XPATH, "//*[@id='content']/div/section/form/ul")
    decoratorsDocsLink = searchResultsList.find_element(By.XPATH, ".//li/h3/a")
    decoratorsDocsLink.click()

    examplesLink = mainDriver.find_element(
        By.XPATH, "/html/body/section/nav/ul/li[10]/a")
    examplesLink.click()

    examplesSection = mainDriver.find_element(By.XPATH, "//*[@id='examples']")
    examplesTable = examplesSection.find_element(By.XPATH, ".//ol")

    examplesList = examplesTable.find_elements(By.XPATH, './/li')
    print(len(examplesList) == 5)

    mainDriver.closeDriver()
    mainDriver.checkDriverStatus()


def tests_demoqa(mainDriver: driver.MainDriver, mainActioner: driver.MainActioner):
    test_main.start_tests(mainDriver, mainActioner)

    mainDriver.closeDriver()
    mainDriver.checkDriverStatus()


if __name__ == "__main__":
    main()
