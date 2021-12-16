from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By

class ListPages(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        urlBase = "http://" + self.ip + ":" + self.port
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(urlBase)
        delay = 3 # seconds
        driver.implicitly_wait(delay)
        url = driver.current_url
        linktable = []
        linktable_ = []
        self.finaltable = []
        linktable.append(url)
        while linktable:
            url = linktable.pop()
            self.finaltable.append(url)
            driver.get(url)
            #driver.implicitly_wait(delay)
            for button in driver.find_elements(By.TAG_NAME, 'a'):
                link = button.get_attribute('href')
                if (link and (link != "None")):

                    if link not in self.finaltable:
                        linktable.append(link)
            linktable = list(dict.fromkeys(linktable))

        driver.quit()
        print("tableau : ")
        for link in self.finaltable:
            print(link + "\n")
    def join(self):
        Thread.join(self)
        return self.finaltable

