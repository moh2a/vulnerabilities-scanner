from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By

class ListPages(Thread):
    def __init__(self, ip, port):
        # Call the Thread class's init function
        Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        url = "http://" + self.ip + ":" + self.port
        driver = webdriver.Chrome()
        driver.get(url)
        delay = 5  # seconds
        driver.implicitly_wait(delay)
        url = driver.current_url
        linktable = []
        linktable.append(url)

        for link in linktable:
            for button in driver.find_elements(By.TAG_NAME, 'button'):
                link = button.get_attribute('routerlink')
                if (link and (link != "None")): linktable.append(url + link[1:])
            for button in driver.find_elements(By.TAG_NAME, 'a'):
                link = button.get_attribute('href')
                if (link and (link != "None")): linktable.append(link)
            linktable = list(dict.fromkeys(linktable))

        driver.quit()
        self.finaltable = []
        for link in linktable:
            if (url in link): self.finaltable.append(link)
        print("tableau : ")
        for link in self.finaltable:
            print(link + "\n")
    def join(self):
        Thread.join(self)
        return self.finaltable

