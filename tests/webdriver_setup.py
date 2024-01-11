
import pytest
import time

from selenium.webdriver.chrome.service import Service

from utils import config_setup
from config.TestData import TestData
from selenium import webdriver
from utils import data_helpers
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from typing import List
from typing import Optional
from selenium import webdriver
import os
import re


class Browser:
    """Browser ENUMS"""
    CHROME = 'chrome'
    FIREFOX = 'firefox'
    EDGE = 'edge'

def build_browser(browser, experimental_options: Optional[List[dict]],
                  browser_options: List[str], version: str, driver_manager: bool, path=None):
    global options
    if browser == Browser.CHROME:
        options = build_browser_options(Browser.CHROME, browser_options, experimental_options)

        if driver_manager:
            try:
                if not os.path.exists(path):
                    os.makedirs(path, exist_ok=True)
                time.sleep(1)
                service = Service()
                options = webdriver.ChromeOptions()
                if browser_options:
                    options.headless = True
                preferences = experimental_options[0]
                options.add_experimental_option("prefs", preferences)
                return webdriver.Chrome(options=options,service=service)
            except FileNotFoundError or OSError:
                if not os.path.exists(path):
                    time.sleep(3)
                    os.makedirs(path, exist_ok=True)
                options = webdriver.ChromeOptions()
                if browser_options:
                    options.headless = True
                service = Service()
                preferences = experimental_options[0]
                options.add_experimental_option("prefs", preferences)
                return webdriver.Chrome(options=options, service=service)
        else:
            options = webdriver.ChromeOptions()
            if browser_options:
                options.headless = True
            service = Service()
            preferences = experimental_options[0]
            options.add_experimental_option("prefs", preferences)
            return webdriver.Chrome(options=options, service=service)

    elif browser == Browser.FIREFOX:
        options = build_browser_options(Browser.FIREFOX, browser_options, experimental_options)

        if driver_manager:
            service = Service()
            options = webdriver.FirefoxOptions()
            if browser_options:
                options.headless = True

            return webdriver.Firefox(options=options, service=service)
        else:
            service = Service()
            options = webdriver.FirefoxOptions()
            if browser_options:
                options.headless = True

            return webdriver.Firefox(options=options, service=service)

def build_browser_options(browser, browser_options: List[str], experimental_options: Optional[List[dict]]):
    browser = browser.lower()
    if browser == Browser.CHROME:
        options = webdriver.ChromeOptions()
        if experimental_options:
            for exp_option in experimental_options:
                options.add_experimental_option("prefs", exp_option)

        if "mobile" in config_setup.master_config()['options']:
            mobile_setup(browser, options)
    elif browser == Browser.FIREFOX:
        options = webdriver.FirefoxOptions()
        if experimental_options:
            for index, exp_option in enumerate(experimental_options):
                key = list(exp_option.keys())[index]
                value = list(exp_option.values())[index]
                options.set_preference(key, value)
        if "mobile" in config_setup.master_config()['options']:
            mobile_setup(browser, options)
    else:
        raise ValueError(f'{browser} is not supported')

    for option in browser_options:
        options.add_argument(f'--{option}')

    return options

def mobile_setup(browser, options):
    if browser == Browser.CHROME or browser == Browser.EDGE:
        options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})
    if browser == Browser.FIREFOX:
        user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
        mobile_options = webdriver.FirefoxProfile()
        mobile_options.set_preference("general.useragent.override", user_agent)

