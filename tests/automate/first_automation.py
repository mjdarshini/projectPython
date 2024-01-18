import time

from pages.login_page import LoginPage
from tests.base_test import BaseTest


class TestAutomate(BaseTest):


    def test_automated_by_jaya(self):
        jaya = LoginPage(self.driver)
        jaya.goto()
        time.sleep(4)


