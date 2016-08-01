from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

class TestStartseite(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_check_title(self):
        self.browser.get(self.live_server_url)

        self.assertIn('BP Setup', self.browser.title)
