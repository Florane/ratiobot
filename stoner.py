from config import Config
from spammer import Spammer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from random import choice

class Stoner(Spammer):
    def generate(self):
            self.size = self.settings.get("ITER")
            self.iter = 0
            self.stone = []
            self.toss = []
            self.notsee = []

            with open(self.settings.get("SPAM_STONE")+self.settings.get("STONE_NAME")) as file:
                for line in file:
                    self.stone.append(line.strip())

            with open(self.settings.get("SPAM_STONE")+self.settings.get("TOSS_NAME")) as file:
                for line in file:
                    self.toss.append(line.strip())

            with open(self.settings.get("SPAM_STONE")+self.settings.get("FASH_NAME")) as file:
                for line in file:
                    self.notsee.append(line.strip())

    def length(self):
        return self.size

    def step(self):
        self.driver.find_element_by_xpath("//div[@data-testid='reply']").click()
        sleep(1.5)
        self.send_slash_n(self.driver.find_element_by_class_name("public-DraftEditor-content"),choice(self.stone)+choice(self.toss)+' is a '+choice(self.notsee))
        self.driver.find_element_by_xpath("//div[@data-testid='tweetButton']").click()
        #self.driver.find_element_by_xpath("//div[@aria-label='Закрыть']").click()
        self.iter += 1
        self.size += 1
        self.settings.set("ITER",self.size)
        self.settings.saveConfig(self.settings.get("CFG_NAME"))
        return self.iter
