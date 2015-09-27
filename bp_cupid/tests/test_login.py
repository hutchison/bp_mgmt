from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.contrib.auth.models import User

class TestLogin(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.username = 'alice'
        self.email = 'alice@example.org'
        self.password = 'test'
        User.objects.create_user(self.username, self.email, self.password)

    def tearDown(self):
        self.browser.quit()

    def test_successful_login(self):
        self.browser.get(self.live_server_url)

        self.browser.find_element_by_link_text('Login').click()

        input_username = self.browser.find_element_by_id('id_username')
        input_username.send_keys(self.username)
        input_password = self.browser.find_element_by_id('id_password')
        input_password.send_keys(self.password)

        self.browser.find_element_by_css_selector('[type=submit]').click()

        self.assertIsNotNone(self.browser.find_element_by_id('logout'))

    def test_failing_login(self):
        self.browser.get(self.live_server_url)

        self.browser.find_element_by_link_text('Login').click()

        input_username = self.browser.find_element_by_id('id_username')
        input_username.send_keys(self.username)
        input_password = self.browser.find_element_by_id('id_password')
        input_password.send_keys('foobar')

        self.browser.find_element_by_css_selector('[type=submit]').click()

        alert = self.browser.find_element_by_class_name('alert-danger')
        self.assertEqual(
            alert.text,
            'Benutzerdaten oder Passwort nicht gefunden.'
        )
