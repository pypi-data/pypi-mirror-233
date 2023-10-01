import os

from ez_visual_regression import __version__
from ez_visual_regression.api import *
from ez_visual_regression.configuration import parse_config, execute_config

from docopt import docopt                                              # Handles CLI parsing


usage = """ez visual regression

Usage:
ezvr [<config_file>] [-h] [-v]
ezvr screenshot <url> [-l locator] [-i ignored_elements] [-f folder] [-m]
ezvr test <url> [-l locator] [-i ignored_elements] [-f folder] [-w warning_threshold] [-e error_threshold] [-m]

Options:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit
    -m, --multielement    Whether the test should be in multielement mode
    -i ignored_elements, --ignore ignored_elements 
                        a list of ignored elements
    -l locator, --locator locator 
                        The locator to use to look for element(s) (leave blank for full-page)
    -f folder, --folder folder
                        The folder to put images in, if you leave it blank images will be put in cwd
    -w warning_threshold, --warning warning_threshold
                        The threshold as a float before a warning is logged
    -e error_threshold, --error error_threshold
                        The threshold as a float before an error is raised
"""

def main():
    args = docopt(usage, version=__version__)
    
    if args["<config_file>"] or (not args["screenshot"] and not args["test"]):
        if not args["<config_file>"]:
            args["<config_file>"] = "config.yml"
        config = parse_config(args["<config_file>"])
        execute_config(config)

    elif args["screenshot"]:
        driver_name = "chrome"
        driver = instantiate_driver(driver_name)
        # Preprocess arguments
        if not args["--folder"]:
            args["--folder"] = "."
        get_screenshot(driver, args["<url>"],os.path.join(args["--folder"], "screenshot.png"), args["--locator"], args["--ignore"])
        print(f"Screenshot saved to {os.path.join(args['--folder'], 'screenshot.png')}")
    elif args["test"]:
        driver_name = "chrome"
        driver = instantiate_driver(driver_name)
        # Preprocess arguments
        if not args["--folder"]:
            args["--folder"] = "."
        if not args["--warning"]:
            args["--warning"] = 10
        else:
            args["--warning"] = float(args["--warning"])
        if not args["--error"]:
            args["--error"] = 30
        else:
            args["--error"] = float(args["--error"])

        diff = assert_image_similarity_to_baseline(driver, args["<url>"], args["--folder"], args["--locator"], args["--warning"], args["--error"], args["--ignore"], args["--multielement"])
        print(f"Difference was: {diff}")

