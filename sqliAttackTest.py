import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pprint import pprint
from threading import Thread

# initialize an HTTP session & set the browser
response = requests.Session()

class sqliAttackTest(Thread):
    def __init__(self, pageList):
        Thread.__init__(self)
        self.pageList = pageList
        self.vulnerablepages = []

    def join(self):
        Thread.join(self)
        return self.vulnerablepages
    def run(self):
        for link in self.pageList:
            self.test_sql_injection(link)

    def get_soup(self,url):
        """"""
        return BeautifulSoup(response.get(url).content, "html.parser")

    def get_all_forms(self,url):
        """On lui rentre un lien et ça nous resort tous les formulaire qui existe sur la page web"""
        return self.get_soup(url).find_all("form")


    def get_form_details(self,form):
        """
        This function extracts all possible useful information about an HTML `form`
        """
        details = {}
        # get the form action (target url)
        try:
            action = form.attrs.get("action").lower()
        except:
            action = None
        # get the form method (POST, GET, etc.)
        method = form.attrs.get("method", "get").lower()
        # get all the input details such as type and name
        inputs = []
        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type", "text")
            input_name = input_tag.attrs.get("name")
            input_value = input_tag.attrs.get("value", "")
            inputs.append({"type": input_type, "name": input_name, "value": input_value})
        # put everything to the resulting dictionary
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details

    def is_vulnerable(self,response):
        """A simple boolean function that determines whether a page
        is SQL Injection vulnerable from its `response`"""
        errors = {
            # MySQL
            "you have an error in your sql syntax;",
            "warning: mysql",
            # SQL Server
            "unclosed quotation mark after the character string",
            # Oracle
            "quoted string not properly terminated",
            #
            "mysqli",
        }
        for error in errors:
            # if you find one of these errors, return True
            if error in response.content.decode().lower():
                return True
        # no error detected
        return False

    def test_sql_injection(self,url):
        # test on URL
        for c in "\"'":
            # add quote/double quote character to the URL
            new_url = url + c
            print("[!] Trying", new_url)
            # make the HTTP request
            res = response.get(new_url)
            if self.is_vulnerable(res):
                # SQL Injection detected on the URL itself,
                # no need to preceed for extracting forms and submitting them
                print("[+] SQL Injection vulnerability detected, link:", new_url)
                return
        # test on HTML forms
        forms = self.get_all_forms(url)
        print(f"[+] Detected {len(forms)} forms on {url}.")
        for form in forms:
            form_details = self.get_form_details(form)
            for c in "\"'":
                # the data body we want to submit
                data = {}
                for input_tag in form_details["inputs"]:
                    if input_tag["type"] == "hidden" or input_tag["value"]:
                        # any input form that is hidden or has some value,
                        # just use it in the form body
                        try:
                            data[input_tag["name"]] = input_tag["value"] + c
                        except:
                            pass
                    elif input_tag["type"] != "submit":
                        # all others except submit, use some junk data with special character
                        data[input_tag["name"]] = f"test{c}"
                # join the url with the action (form request URL)
                url = urljoin(url, form_details["action"])
                if form_details["method"] == "post":
                    res = response.post(url, data=data)
                elif form_details["method"] == "get":
                    res = response.get(url, params=data)
                # test whether the resulting page is vulnerable
                if self.is_vulnerable(res):
                    print("[+] SQL Injection vulnerability detected, link:", url)
                    print("[+] Form:")
                    pprint(form_details)
                    self.vulnerablepages.append(url)
                    break