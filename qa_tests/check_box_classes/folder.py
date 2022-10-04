from typing import List
from selenium.webdriver.remote.webelement import WebElement
from qa_tests.check_box_classes.file import File

class Folder:
    def __init__(
            self,
            name: str=None,
            web_element: WebElement=None,
            folders: List['Folder']=None,
            files: List['File']=None) -> None:
        self.name = name

        if web_element:
            self.__web_element = web_element

        if folders:
            self.folders = folders
        else:
            self.folders = []

        if files:
            self.files = files
        else:
            self.files = []
    
    def append_folder(self, folder: 'Folder') -> None:
        self.folders.append(folder)
    
    def append_file(self, file: 'File') -> None:
        self.files.append(file)
    
    def get_folder_name(self) -> None:
        return self.name
    
    def get_folders(self) -> None:
        return self.folders
    
    def get_files(self) -> None:
        return self.files

    def __eq__(self, other: 'Folder') -> None:
        if self.name != other.name:
            return False

        for (self_folder, other_folder) in zip(self.folders, other.folders):
            if self_folder.name != other_folder.name:
                return False

        for (self_file, other_file) in zip(self.files, other.files):
            if self_file.name != other_file.name:
                return False
        
        return (self.folders == other.folders) and True
