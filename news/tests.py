import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver

from webcw3.settings import BASE_DIR


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['db-data-1.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        url = str(BASE_DIR) + '/chromedriver.exe'
        cls.selenium = webdriver.Chrome(url)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_user_interaction(self):
        self.selenium.get(self.live_server_url + reverse('news:logging'))
        time.sleep(2)

        # navigate to signup
        signup_link = self.selenium.find_elements_by_css_selector("a")[3]
        time.sleep(2)

        signup_link.click()
        time.sleep(4)

        first_name = self.selenium.find_element_by_id("su-first-name")
        last_name = self.selenium.find_element_by_id("su-last-name")
        username = self.selenium.find_element_by_id("su-username")
        email = self.selenium.find_element_by_id("signup-email")
        dob = self.selenium.find_element_by_id("su-dob")
        password = self.selenium.find_element_by_id("password")
        password2 = self.selenium.find_element_by_id("password2")
        time.sleep(3)

        first_name.send_keys("testUser")
        last_name.send_keys("test")
        username.send_keys("testUser")
        email.send_keys("fakenewswebsite0@gmail.com")
        dob.send_keys("01/01/2000")
        password.send_keys("testPassword1")
        password2.send_keys("testPassword1")
        time.sleep(3)

        submit = self.selenium.find_element_by_id("su-submit")
        submit.click()
        time.sleep(3)

        # login new user
        self.selenium.find_element_by_name('username').send_keys('testUser')
        self.selenium.find_element_by_name('password').send_keys('testPassword1')
        self.selenium.find_element_by_class_name('btn-primary').click()
        time.sleep(3)

        # after login select article
        article = self.selenium.find_elements_by_class_name("article-header")[0]
        time.sleep(2)

        article.click()
        time.sleep(2)

        # add comment
        comment = self.selenium.find_element_by_id('comment-add-area')
        comment.send_keys("this is my comment")
        time.sleep(2)

        submit_comment = self.selenium.find_element_by_class_name("comment-add-button")
        submit_comment.click()
        time.sleep(3)

        # edit comment
        edit_comment = self.selenium.find_element_by_class_name("btn-warning")
        edit_comment.click()
        time.sleep(2)
        comment = self.selenium.find_element_by_id('comment-add-area')
        comment.send_keys(" with edits")
        time.sleep(2)

        submit_edit = self.selenium.find_element_by_class_name("comment-add-button")
        submit_edit.click()
        time.sleep(4)

        # delete comment
        delete_comment = self.selenium.find_element_by_class_name("btn-danger")
        time.sleep(2)
        delete_comment.click()
        time.sleep(3)

        comment_new = self.selenium.find_element_by_id('comment-add-area')
        comment_new.send_keys("please watch the like buttons")
        time.sleep(2)

        submit_comment = self.selenium.find_element_by_class_name("comment-add-button")
        submit_comment.click()
        time.sleep(3)

        # click like
        like_button = self.selenium.find_element_by_id("news-modal-like")
        like_button.click()
        time.sleep(3)

        exit_article = self.selenium.find_element_by_class_name("close")
        exit_article.click()
        time.sleep(3)
