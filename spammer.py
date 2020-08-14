#handles spammer body
from config import Config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
class Spammer():
    def __init__(self,settings,general):
        self.settings = settings
        self.general = general

    def begin(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.get("https://twitter.com/login")
        login = self.driver.find_element_by_name("session[username_or_email]")
        password = self.driver.find_element_by_name("session[password]")
        enter = self.driver.find_element_by_xpath("//div[@role='button']")
        login.send_keys(self.general.get("LOGIN"))
        password.send_keys(self.general.get("PASSWORD"))
        enter.click()
        self.driver.get("https://twitter.com/"+str(self.settings.get("TARGET_USER"))+"/status/"+str(self.settings.get("TARGET_TWEET")))

    def generate(self):
        self.iter = self.settings.get("ITER")
        self.spamList = []
        with open(self.settings.get("SPAM_NAME"),encoding="utf-8") as file:
            for line in file:
                self.spamList.append(line.strip())

    def length(self):
        return len(self.spamList)

    def send_slash_n(self,elem,text):
        for part in text.split('\\n'):
            elem.send_keys(part)
            ActionChains(self.driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        elem.send_keys(Keys.BACKSPACE)

    def step(self):
        self.driver.find_element_by_xpath("//div[@data-testid='reply']").click()
        sleep(1.5)
        self.send_slash_n(self.driver.find_element_by_class_name("public-DraftEditor-content"),self.spamList[self.iter])
        self.driver.find_element_by_xpath("//div[@data-testid='tweetButton']").click()
        #self.driver.find_element_by_xpath("//div[@aria-label='Закрыть']").click()
        self.iter += 1
        self.settings.set("ITER",self.iter)
        self.settings.saveConfig(self.settings.get("CFG_NAME"))
        return self.iter
