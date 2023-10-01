# Standard library dependencies
import os 
from typing import Union, List, Dict


# Third party dependencies
import yaml
from selenium.webdriver.remote.webdriver import WebDriver              # Used for type hinting

from ez_visual_regression.api import *

def parse_config(config_path: str) -> Dict[str, Union[str, List[List[Union[bool,None,int,str]]]]]:
    """Takes in a path to a config file and parses it for use with execute_config()

    Parameters
    ----------
    config_path : str
        The path to a file

    Returns
    -------
    Dict[str, Union[str, List[List[Union[bool,None,int,str]]]]]
        A dictionary with 3 keys, driver (a WebDriver object), tests (all arguments for for assert_image_similarity_to_baseline() calls), screenshots (all arguments for get_screenshot() calls)

    Raises
    ------
    FileNotFoundError
        If a config path does not exist
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config path {config_path} does not exist")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    driver = config.get("driver", "chrome").lower()
    tests = []
    screenshots = []

    if config.get("tests", False):
        for test in config["tests"]:
            url = config["tests"][test]["url"]
            locator = config["tests"][test].get("locator", False)
            warning_threshold = config["tests"][test].get("warning_threshold", 10)
            error_threshold = config["tests"][test].get("error_threshold", 30)
            ignored_elements = config["tests"][test].get("ignored_elements", None)
            folder = config["tests"][test].get("folder", test)
            multielements = config["tests"][test].get("multielements", False)
            tests.append([url, folder, locator, warning_threshold, error_threshold, ignored_elements, multielements])
    if config.get("screenshots", False):
        for screenshot in config["screenshots"]:
            url = config["screenshots"][screenshot]["url"]
            locator = config["screenshots"][screenshot].get("locator", False)
            ignored_elements = config["screenshots"][screenshot].get("ignored_elements", None)
            folder = config["screenshots"][screenshot].get("folder", screenshot)
            filename = os.path.join(folder, "screenshot.png")
            screenshots.append([url,filename,locator,ignored_elements])
    return {"driver":driver, "tests":tests, "screenshots": screenshots}

def execute_config(config: Dict[str, Union[str, List[List[Union[bool,None,int,str]]]]]):
    config["driver"] = instantiate_driver(config["driver"])
    print("Executing tests")
    for test in config["tests"]:
        assert_image_similarity_to_baseline(config["driver"], *test)

    print("Executing screenshots")
    for screenshot in config["screenshots"]:
        get_screenshot(config["driver"], *screenshot)
    