from threading import Thread
import requests
from bs4 import BeautifulSoup as beautifulSoup
from urllib.parse import urljoin

class XSSTest(Thread):
    def __init__(self, pageList):
        Thread.__init__(self)
        self.pageList = pageList
        self.vulnerablepages = []

    def run(self):
        for url in self.pageList:
            print(self.xss_vulnerability_testing(url))
    def join(self):
        Thread.join(self)
        return self.vulnerablepages

    def get_all_forms_from_page(self, url):
        # BeautifulSoup is a Python library for pulling data out of HTML and XML files, it works with a parser.
        # the BeautifulSoup object allows us to represent the document as a nested data structure
        # then, we can easily navigate the data structure to retrieve the information we're looking for (forms)
        soup = beautifulSoup(requests.get(url).content, "html.parser")
        return soup.find_all("form")

    def get_form_details(self, form):
        # Once we have all the forms of the page, we need to extract the information that we need such as the
        # the action of the form, the method or other attributes

        inputs = []
        # in the next variable, we will gather all of the details of the HTML tags regarding the existing form
        form_details = {}

        action = form.attrs.get("action").lower()
        method = form.attrs.get("method", "get").lower()

        for one_input_tag in form.find_all("input"):
            type = one_input_tag.attrs.get("type", "text")
            name = one_input_tag.attrs.get("name")
            inputs.append({"type": type, "name": name})

        form_details["action"] = action
        form_details["method"] = method
        form_details["inputs"] = inputs
        return form_details

    def submit_js(self, url, js, form_details):
        print("icicici", form_details)
        input_tags = form_details["inputs"]
        form_action = form_details["action"]
        form_method = form_details["method"]

        url_params = {}  # data that will be sent in the request respecting the form : {'key': 'value'}
        for one_input in input_tags:
            one_input_type = one_input["type"]
            if one_input_type == "text" or one_input_type == "search":
                one_input["value"] = js

            # in order to add it to our key value parameters, we need to get the mapping of the name and the value, and
            # not their classic type (error example : "list indices must be integers or slices, not str")
            one_input_name = one_input.get("name")
            one_input_value = one_input.get("value")
            if one_input_name and one_input_value:
                url_params[one_input_name] = one_input_value
        complete_url = urljoin(url, form_action)
        if form_method == "post":
            return requests.post(complete_url, url_params)
        elif form_method == "get":
            return requests.get(complete_url, url_params)
        else:  # only 3 methods are possible for the action of a form : post get or dialog
            return "The request type DIALOG is not supported"

    def xss_vulnerability_testing(self, url):
        script = "<script>alert('XSS vulnerability detected')</script>"
        all_forms = self.get_all_forms_from_page(url)
        for one_form in all_forms:
            form_details = self.get_form_details(one_form)

            # our submit_js function returns either a Response object (server's response to an HTTP request) or a String
            response = self.submit_js(url, script, form_details)
            print("icicici2", response.url)
            if isinstance(response, str):
                return "The form isn't supported"
            else:
                response_content = response.content.decode()
                if script in response_content:
                    print(f"An XSS vulnerability was detected on this url : {url}")
                    print(f"Here is the vulnerable form: {form_details}")

                    print("page : ", url)
                    self.vulnerablepages.append(url)
                    return "XSS detected !"
        return "No XSS detected"

