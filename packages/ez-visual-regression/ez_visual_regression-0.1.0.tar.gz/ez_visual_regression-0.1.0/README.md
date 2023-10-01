# ez_visual_regression

*Used to take screenshots with selenium (pages or elements) and compare to baseline*

## Table of contents
- [What does ez\_visual\_regression do?](#what-does-ez_visual_regression-do)
- [Feature Overview](#feature-overview)
- [Why should I use ez\_visual\_regression?](#why-should-i-use-ez_visual_regression)
- [Quick-start](#quick-start)
- [Installation](#installation)
    - [From source](#from-source)
    - [From PyPi](#from-pypi)
    - [Examples](#examples)
    - [Create baseline images for testing an element](#create-baseline-images-for-testing-an-element)
    - [Test against baseline image for an element](#test-against-baseline-image-for-an-element)
    - [Test a whole page while ignoring h2's and elements with id of myChart](#test-a-whole-page-while-ignoring-h2s-and-elements-with-id-of-mychart)
- [Additional Documentation](#additional-documentation)


## What does ez_visual_regression do?

`ez_visual_regression` is a library for helping do visual regression testing. This is a fancy name for taking a screenshot of a known-good version of your app, then every time you make changes you can compare your current app to those screenshots to make sure things don't break.

![](docs/images/comparison.png)

(larger images here ![](https://github.com/Descent098/ez-visual-regression/tree/master/docs/images/example))

For example `baseline` here is the "correct" version, we accidentally removed the pricing table in `current`, and we can see the difference in `diff` (and in higher contrast in `thresh`). This process is typically quite annoying and needs custom code. `ez_visual_regression` makes this much easier, and integrates natively with selenium, along with nice features (like ignoring elements).

## Feature overview

On top of just normal visual regression ez_visual_regression supports:

- Element ignoring; Using [query selectors (CSS Selectors)](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors) you can select elements who's changes you want to ignore (i.e. hero's with changing images, or the text for commonly changing elements)
- Full page **or** element based; Allows you to decide if you want to make your tests by full page, or by element
- Warning and error thresholds; If you don't want to raise complete red flags you can set error thresholds to say if there "might" be a problem. This logs to `stderr`, which means you can be more liberal with your measurements without full pipeline failures
- Plug-n-play api; The API takes in any [non-headless (standard)](https://en.wikipedia.org/wiki/Headless_browser#:~:text=A%20headless%20browser%20is%20a,interface%20or%20using%20network%20communication.) webdriver. This means you can do **any selenium configuration** you want on the driver and then pass it into the api. It does no more and no less than what each of the functions say.
- Configuration based testing; You can always use the API if you want a code-based approach, or you can setup a config file and run from the cli

## Why should I use ez_visual_regression?

There are a ton of great and more robust tools out there for this analysis, or for visual regression testing, but I found each of them had their own problems, here's a list:

|Package|Issue|
|-------|-----|
|[needle](https://github.com/python-needle/needle)| Requires a Nose test runner, and had out of date dependencies|
|[pytest-needle](https://github.com/jlane9/pytest-needle) | Works well, but cannot use [webdiver_manager](https://pypi.org/project/webdriver-manager/) with it | 
|[dpxdt](https://github.com/bslatkin/dpxdt) | Didn't test, but was 7 years old and mostly focused on CI/CD usage|
|[Visual Regression Tracker](https://github.com/Visual-Regression-Tracker/Visual-Regression-Tracker) | Works great, but for some of my use cases I need an API not a full application|
|[hermione](https://github.com/gemini-testing/hermione)|Could not use javascript/nodeJS for my use case|
|[specter](https://github.com/letsgetrandy/specter)|Could not use javascript/nodeJS for my use case|
|[Cypress-image-screenshot](https://github.com/jaredpalmer/cypress-image-snapshot)|Could not use javascript/nodeJS for my use case|

So I build ez_visual_regression to fill in the gaps I saw in the available solutions. Namely being plug-n-play with any selenium driver to do whatever configurations I need!

## Quick-start

### Installation

#### From source

1. Clone this repo: (put github/source code link here)
2. Run ```pip install .``` or ```sudo pip3 install .```in the root directory

#### From PyPi

1. Run ```pip install ez-visual-regression```

#### Examples

Normally instantiating a browser takes a few steps, for example:

```python
from selenium import webdriver                                         # Instantiates a browser
from selenium.webdriver.chrome.options import Options                  # Allows webdriver config
from webdriver_manager.chrome import ChromeDriverManager               # Manages webdriver install
from selenium.webdriver.chrome.service import Service as ChromeService # Helps instantiate browser

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()))
```

There is an included method to shorten this:

```python
from ez_visual_regression.api import instantiate_driver

driver_name = "chrome" # Can be "chrome", "edge", or "firefox"
driver = instantiate_driver(driver_name)
```

Which is what I will use from here on out, but you can use any method to instantiate a driver and pass it to the functions

##### Create baseline images for testing an element

```python
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

##### Test against baseline image for an element

```python
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

##### Test a whole page while ignoring h2's and elements with id of myChart

```python
# Setup driver
from ez_visual_regression.api import instantiate_driver

driver_name = "chrome"
driver = instantiate_driver(driver_name)

# import functions needed for testing
from ez_visual_regression.api import assert_image_similarity_to_baseline

url = "tests/example_sites/no_difference/index.html" # File in this case
folder = "tests/example_sites/no_difference" # Where to store output images
ignored_elements = ["h2", "#myChart"] # Queryselector for elements to ignore

assert_image_similarity_to_baseline(driver, url, folder=folder, ignored_elements=ignored_elements)
```

## Additional Documentation

For more details check out our:

- [User Documentation](https://ez-visual-regression.readthedocs.io/en/latest/)
- [API Documentation](https://kieranwood.ca/ez_visual_regression)
