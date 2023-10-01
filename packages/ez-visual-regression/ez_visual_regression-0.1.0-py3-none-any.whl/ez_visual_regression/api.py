# Standard lib dependencies
import os                                                              # Path verification & modification
import time                                                            # Allows for pauses
import logging                                                         # Enables logging
import webbrowser
from typing import Union, List

# Third Party Dependencies
## Image comparison
from ez_img_diff.api import compare_images

## Browser automation
from selenium import webdriver                                         # Instantiates a browser
from selenium.webdriver.common.by import By                            # Specify find_element type
from selenium.webdriver.chrome.options import Options                  # Allows webdriver config
from selenium.webdriver.remote.webdriver import WebDriver              # Used for type hinting
from selenium.common.exceptions import NoSuchElementException          # Allows for error catching

### Used to manage driver installation
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

### Services needed for instantiating browsers
from selenium.webdriver.chrome.service import Service as ChromeService # Helps instantiate browser
from selenium.webdriver.edge.service import Service as EdgeService     # Helps instantiate browser
from selenium.webdriver.firefox.service import Service as FirefoxService


def get_screenshot(driver:WebDriver, url:str, filename:str, locator:Union[str, None]=None, ignored_elements: List[str]= None):
    """Takes a screenshot of a page or element

    Parameters
    ----------
    driver : WebDriver
        The browser to use for capturing screenshots

    url : str
        The URl you want to get a screenshot from (or filepath)

    filename : str, optional
        The file to export the screenshot to, by default None

    locator : Union[str, None], optional
        The CSS selector to search the element with (i.e. #myChart, .rows etc.)
        
    ignored_elements: List[str], option
        Use a query selector to specify elements to ignore

    Notes
    -----
    - If locator is not specified a full page screenshot is used
    
    
    References
    ----------
    - How to use by if you've never seen it https://selenium-python.readthedocs.io/locating-elements.html
    
    Raises
    ------
    FileNotFoundError
        If the URL is a file path and it does not exist
        
    Examples
    --------
    ### Create a screenshot of full page
    ```
    from ez_visual_regression.api import get_screenshot, get_installed_driver, instantiate_driver

    # Configuration variables
    URL = "https://canadiancoding.ca"
    filename = "screenshot.png"

    driver_name = "chrome"
    driver = instantiate_driver(driver_name)

    get_screenshot(driver, URL, filename=filename)
    ```
    
    ### Create a screenshot of an element
    ```
    from ez_visual_regression.api import get_screenshot, get_installed_driver, instantiate_driver

    # Configuration variables
    URL = "https://canadiancoding.ca"
    filename = "screenshot.png"

    driver_name = "chrome"
    driver = instantiate_driver(driver_name)
    locator = "#myChart"

    get_screenshot(driver, URL, filename=filename, locator=locator)
    ```
    
    ### Create a screenshot of full page while ignoring elements with the card class and nav element(s)
    ```
    from ez_visual_regression.api import get_screenshot, get_installed_driver, instantiate_driver

    # Configuration variables
    URL = "https://canadiancoding.ca"
    filename = "screenshot.png"

    driver_name = "chrome"
    driver = instantiate_driver(driver_name)
    ignored_elements = ["nav", ".card"]

    get_screenshot(driver, URL, filename=filename, ignored_elements=ignored_elements)
    ```
    """
    if not url.startswith("http"):
        if (url.endswith(".html") or url.endswith(".pdf")) and not url.startswith("file:///"): # Assume file path
            logging.debug("URL provided does not have protocol, defaulting to file")
            abs_fp = os.path.abspath(url).replace("\\","/")
            if not os.path.exists(abs_fp):
                raise FileNotFoundError(f"File path {abs_fp} does not exist")
            url = f"file:///{abs_fp}"
        else:
            url = "http://" + url
    if not os.path.exists(os.path.dirname(filename)):
        os.mkdir(os.path.dirname(filename))
    print(f"{filename=} {locator=}")
    driver.get(url)

    
    # Wait for page to load and run all animations
    time.sleep(3) # TODO: Be better
    if ignored_elements:
        for selector in ignored_elements:
            driver.execute_script(f'document.querySelectorAll("{selector}").forEach((el)=>{{el.style.opacity=0}})')
    if locator: # Screenshot element
        try:
            driver.find_elements(By.CSS_SELECTOR, locator)[0].screenshot(filename)
        except NoSuchElementException:
            logging.error(f"\033[0;m Element does not exist when looking for css selector: {locator} confirm spelling and capitalization\033[1;37m")
            exit(1)
    else: # Screenshot page
        driver.save_screenshot(filename)

def compare_multiple_elements(driver:WebDriver, url:str, folder:str, locator:str, ignored_elements: List[str]= None) -> List[float]:
    """Regression test multiple elements

    Parameters
    ----------
    driver : WebDriver
        The browser to use for capturing screenshots

    url : str
        The URl you want to get a screenshot from (or filepath)

    folder : str
        The folder to export the screenshots to

    locator : str
        The CSS selector to search the element with (i.e. #myChart, .rows etc.)
        
    ignored_elements: List[str], option
        Use a query selector to specify elements to ignore

    Notes
    -----
    - If locator is not specified a full page screenshot is used
    
    
    References
    ----------
    - How to use by if you've never seen it https://selenium-python.readthedocs.io/locating-elements.html
    
    Raises
    ------
    FileNotFoundError
        If the URL is a file path and it does not exist
    
    Returns
    -------
    List[float]:
        The differences of each found element
    
    Examples
    --------
    ### Compare multiple elements
    ```
    from ez_visual_regression.api import compare_multiple_elements,instantiate_driver

    # Configuration variables
    URL = "https://canadiancoding.ca"
    folder = "canadiancoding"

    driver = instantiate_driver("chrome")
    locator = ".nav-item p"
    
    compare_multiple_elements(driver, URL,folder, locator) # Returns (assuming 3 total elements): [0.1, 19.8, 0.4]
    ```
    
    ### Compare multiple elements while ignoring divs and the red class
    ```
    from ez_visual_regression.api import compare_multiple_elements,nstantiate_driver

    # Configuration variables
    URL = "https://canadiancoding.ca"
    folder = "canadiancoding"

    driver = instantiate_driver("chrome")
    locator = ".nav-item p"
    ignored_elements= ["div", ".red"]

    compare_multiple_elements(driver, URL,folder, locator, ignored_elements) # Returns (assuming 3 total elements): [0.1, 0.0, 0.4]
    ```
    """
    
    if not url.startswith("http"):
        if (url.endswith(".html") or url.endswith(".pdf")) and not url.startswith("file:///"): # Assume file path
            logging.debug("URL provided does not have protocol, defaulting to file")
            abs_fp = os.path.abspath(url).replace("\\","/")
            if not os.path.exists(abs_fp):
                raise FileNotFoundError(f"File path {abs_fp} does not exist")
            url = f"file:///{abs_fp}"
        else:
            url = "http://" + url
    if not os.path.isdir(folder):
        os.mkdir(folder)
    
    driver.get(url)
    
    # Wait for page to load and run all animations
    time.sleep(3) # TODO: Be better
    if ignored_elements:
        for selector in ignored_elements:
            driver.execute_script(f'document.querySelectorAll("{selector}").forEach((el)=>{{el.style.opacity=0}})')

    try:
        elements = driver.find_elements(By.CSS_SELECTOR, locator)
        baseline_images = [(os.path.join(folder,f"baseline-{index}.png"), element) for index, element in enumerate(elements)]
        current_images = [element for element in elements]

        diffs = []
        
        for path, element in baseline_images:
            if not os.path.exists(path):
                element.screenshot(path)
                
        for index,element in enumerate(current_images):
            element.screenshot(os.path.join(folder,f"current-{index}.png"))
            diffs.append(compare_images(os.path.join(folder,f"current-{index}.png"), os.path.join(folder,f"baseline-{index}.png"), os.path.join(folder,f"diff-{index}.png"),os.path.join(folder,f"thresh-{index}.png")))
            
    except NoSuchElementException:
        logging.error(f"\033[0;m Element does not exist when looking for css selector: {locator} confirm spelling and capitalization\033[1;37m")
        exit(1)
    return diffs

def assert_image_similarity_to_baseline(driver:WebDriver, url:str, folder:str, locator:Union[str, None]=None, warning_threshold:float=10, error_threshold:float=30, ignored_elements: List[str]= None, multielements:bool=False) -> Union[float, List[float]]:
    """Asserts the current screenshot of a page is similar to `<folder>/baseline.png` within: 0 < diff < error_threshold

    Parameters
    ----------
    driver : WebDriver
        The browser to use for capturing screenshots

    url : str
        The URl you want to get a screenshot from (or filepath)

    folder : str
        The folder to save the baseline, threshold, current and difference images to

    locator : Union[str, None], optional
        The CSS selector to search the element with (i.e. #myChart, .rows etc.)

    warning_threshold : float, optional
        The threshold at which there will be a logged warning, by default 10

    error_threshold : float, optional
        The threshold at which an explicit error will be thrown, by default 30
    
    ignored_elements: List[str], option
        Use a query selector to specify elements to ignore
        
    multielements: bool, option
        Whether to screenshot all occurances of a css selector (True), or just the firs occurance (False), default False

    Raises
    ------
    AssertionError
        If diff > error_threshold
        
    Returns
    -------
    Union[float, List[float]]:
        The difference between the two images as a whole number percent (i.e. 1.313 is 1.313% or 15.928 is 15.928%), or list of floats if multielement is True
    
    Examples
    --------
    ### Create baseline images for a webpage
    ```
    # Setup driver
    from ez_visual_regression.api import instantiate_driver

    driver_name = "chrome"
    driver = instantiate_driver(driver_name)

    # import functions needed for testing
    from ez_visual_regression.api import assert_image_similarity_to_baseline

    url = "tests/example_sites/no_difference/index.html" # File in this case
    folder = "tests/example_sites/no_difference" # Where to store output images
    locator = "#myChart" # The queryselector to find an element with

    # Creates baseline if one isn't available
    assert_image_similarity_to_baseline(driver,url, locator=locator, folder=folder)
    ```
    
    ### Test against baseline image
    ```
    # Setup driver
    from ez_visual_regression.api import instantiate_driver

    driver_name = "chrome"
    driver = instantiate_driver(driver_name)

    # import functions needed for testing
    from ez_visual_regression.api import assert_image_similarity_to_baseline

    url = "tests/example_sites/no_difference/index.html" # File in this case
    folder = "tests/example_sites/no_difference" # Where to store output images
    locator = "#myChart" # The queryselector to find an element with

    try:
        assert_image_similarity_to_baseline(driver,url, locator=locator, folder=folder )
    except AssertionError:
        print("Image too far from baseline!")
    ```
    
    ### Take screenshot of whole page while ignoring h2's and elements with id of myChart
    ```
    # Setup driver
    from ez_visual_regression.api import instantiate_driver

    driver_name = "chrome"
    driver = instantiate_driver(driver_name)
    
    # import functions needed for testing
    from ez_visual_regression.api import assert_image_similarity_to_baseline

    url = "tests/example_sites/no_difference/index.html" # File in this case
    folder = "tests/example_sites/no_difference" # Where to store output images
    ignored_elements = ["h2", "#myChart"]

    assert_image_similarity_to_baseline(driver,url, folder=folder, ignored_elements=ignored_elements)
    ```
    
    ### Take screenshot of all nav elements (not just 1) on a page
    ```
    from ez_visual_regression.api import compare_multiple_elements, instantiate_driver

    # Configuration variables
    URL = "https://canadiancoding.ca"
    folder = "canadiancoding"

    driver = instantiate_driver("chrome")
    locator = ".nav-item p"
    ignored_elements= ["div", ".red"]

    assert_image_similarity_to_baseline(driver, URL, folder, locator, ignored_elements=ignored_elements, multielements=True) # Returns (assuming 3 total elements): [0.1, 0.0, 0.4]
    ```
    """
    if not os.path.isdir(folder):
        print(f"No directory was found called {folder}, creating...")
        os.mkdir(folder)
    if not os.path.exists(os.path.join(folder, "baseline.png")) and not multielements:
        print(f"No baseline image(s) found in {os.path.join(folder, 'baseline.png')}, creating...")
        get_screenshot(driver, url, os.path.join(folder, "baseline.png"), locator, ignored_elements)

    if multielements:
        diffs = compare_multiple_elements(driver, url, folder, locator, ignored_elements)
        return diffs
    else:
        get_screenshot(driver, url, os.path.join(folder, "current.png"), locator, ignored_elements)

        diff = compare_images(os.path.join(folder, "baseline.png"), os.path.join(folder, "current.png"), os.path.join(folder, "diff.png"), os.path.join(folder, "thresh.png"))

        if diff > error_threshold:
            logging.error(f"Difference {diff} is over error threshold {error_threshold}")
            raise AssertionError(f"Difference {diff} is over error threshold {error_threshold}")
        if error_threshold > diff > warning_threshold:
            logging.warning(f"Difference {diff} is over warning threshold {error_threshold}")
            
        return diff
    
def instantiate_driver(driver:str) -> WebDriver:
    """Creates a webdriver based on a driver name

    Parameters
    ----------
    driver : str
        The name of the driver to use (can be "edge", "chrome" or "firefox")

    Returns
    -------
    WebDriver
        The webdriver for the specified browser

    Raises
    ------
    ValueError
        If the driver does not exist
    
    Examples
    --------
    ### Get any supported browser, and instantiate it
    ```
    from ez_visual_regression.api import instantiate_driver

    driver_name = "chrome" # Either "chrome", "firefox","edge" or raises webbrowser.Error
    instantiate_driver(driver_name) # Returns a WebDriver of the correct browser type
    ```
    
    ### Check if person has chrome installed
    ```
    from ez_visual_regression.api import instantiate_driver

    get_installed_driver("chrome") # Either "chrome" or raises webbrowser.Error
    instantiate_driver(driver_name) # Returns a Chrome.WebDriver
    ```
    """
    if driver == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        return webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))
    elif driver == "edge":
        edge_options = Options()
        return webdriver.Edge(options=edge_options, service=EdgeService(EdgeChromiumDriverManager().install()))
    elif driver == "firefox":
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    else:
        raise ValueError(f"Driver not supported {driver}")
