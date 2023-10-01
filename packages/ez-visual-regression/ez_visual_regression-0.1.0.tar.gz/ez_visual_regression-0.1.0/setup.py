"""Contains all the configuration for the package on pip"""
import setuptools
from ez_visual_regression import __version__

def get_content(*filename:str) -> str:
    """ Gets the content of a file or files and returns
    it/them as a string

    Parameters
    ----------
    filename : (str)
        Name of file or set of files to pull content from 
        (comma delimited)
    
    Returns
    -------
    str:
        Content from the file or files
    """
    content = ""
    for file in filename:
        with open(file, "r") as full_description:
            content += full_description.read()
    return content

setuptools.setup(
    name = "ez_visual_regression",
    version = __version__,
    author = "Kieran Wood",
    author_email = "kieran@canadiancoding.ca",
    description = "Used to take screenshots with selenium (pages or elements) and compare to baseline",
    long_description = get_content("README.md", "CHANGELOG.md"),
    long_description_content_type = "text/markdown",
    project_urls = {
        "User Docs" :      "https://kieranwood.ca/ez-visual-regression",
        "API Docs"  :      "https://ez-visual-regression.readthedocs.io",
        "Source" :         "https://github.com/Descent098/ez-visual-regression",
        "Bug Report":      "https://github.com/Descent098/ez-visual-regression/issues/new?assignees=Descent098&labels=bug&template=bug_report.md&title=%5BBUG%5D",
        "Feature Request": "https://github.com/Descent098/ez-visual-regression/issues/new?labels=enhancement&template=feature_request.md&title=%5BFeature%5D",
        "Roadmap":         "https://github.com/Descent098/ez-visual-regression/projects"
    },
    include_package_data = True,
    packages = setuptools.find_packages(),
    entry_points = { 
           'console_scripts': ['ezvr = ez_visual_regression.cli:main']
       },
    install_requires = [
    "docopt",
    "ez_img_diff",
    "selenium",
    "webdriver_manager",
    "pyyaml",
        ],
    extras_require = {
        "dev" : ["nox",    # Used to run automated processes
                "pytest",  # Used to run the test code in the tests directory
                "mkdocs",  # Used to create HTML versions of the markdown docs in the docs directory
                "mkdocs-material",
                ], 
        "CI": [
            "pytest",  # Used to run the test code in the tests directory
            "pyvirtualdisplay"
        ]

    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta"
    ],
)