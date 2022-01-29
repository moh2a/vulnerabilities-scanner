import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from threading import Thread

# Initiation de la session HTTP
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
            self.try_sql_injection(link)

    def get_soup(self,url):
        """
        Cette fonction nous permet d'obtenir le contenu qui se trouve dans un URL
        grâce notamment à la librairie BeautifuSoup
        :param: L’URL dont on veut avoir le contenu
        :return: Tout le contenu de l'URL grâce à la librairie BeautifulSoup
        """
        return BeautifulSoup(response.get(url).content, "html.parser")

    def get_all_forms(self,url):
        """
        Cette fonction nous resort tous les formulaire qui existe sur la page web
        :param: L’URL dont on veut avoir tous les formulaires
        :return: Tous les formulaires de l'URL en param
        """
        return self.get_soup(url).find_all("form")


    def get_informations_form(self,form):
        """
        Cette fonction nous permet d'extraire toutes les informations
        possibles et utiles sur un `formulaire` HTML
        :param: On lui donne un formulaire en paramètre (form)
        :return: La fonction nous retourne une liste avec les actions,
        méthodes et inputs d'une balise form
        """
        informationForm = {}
        # On va récupérer l'action du formulaire en param
        try:
            action = form.attrs.get("action").lower()
        except:
            action = None
        # On va récupérer la méthode du formulaire en param
        method = form.attrs.get("method", "get").lower()
        # On va récupérer les inputs du formulaire en param
        inputs = []
        for input in form.find_all("input"):
            type = input.attrs.get("type", "text")
            name = input.attrs.get("name")
            value = input.attrs.get("value", "")
            inputs.append({"type": type, "name": name, "value": value})
        # put everything to the resulting dictionary
        informationForm["action"] = action
        informationForm["method"] = method
        informationForm["inputs"] = inputs
        return informationForm

    def test_vulnerable(self,response):
        """
        Cette fonction booléenne permet de détermine si
        une page est vulnérable à une injection SQL à partir de sa "réponse".
        :param: On entre la réponse (response) lors de l'essai de l'injection SQL
        :return: Le booléen
        """
        errors = {
            # MySQL
            "you have an error in your sql syntax;",
            "mysqli",
            "warning: mysql",
            # SQL Server
            "unclosed quotation mark after the character string",
            # Oracle
            "quoted string not properly terminated",
            # PostgreSQL
            "PostgreSQL",
        }
        for error in errors:
            # Si on trouve l'une de ces erreurs (bien sur il y'en a beaucoup d'autres,
            # mais pour eviter de faire un trop gros code, alors on a choisi de vous en mettre
            # que quelques unes), ça retourne "True"
            if error in response.content.decode().lower():
                return True
        # Sinon ça retourne false (il n'y a pas eu d'erreurs détectées)
        return False

    def try_sql_injection(self,url):
        # On test l'injection SQL sur l'URL
        for injection in "\"'":
            # On ajoute une apostrophe/apostrophe double à l'URL
            new_url = url + injection
            print("*** Test sur : ", new_url, " ***")
            # On fait une requête HTTP avec le nouveau lien
            resp = response.get(new_url)
            if self.test_vulnerable(resp):
                # Si on rentre dans cette condition, cela veut dire que
                # c'est vulnérable à une injection SQL,
                # On a donc pas besoin d'extraire tous les formulaires et de faire le test sur eux
                print("")
                print("!!!!!!! Une vulnérabilité à été détectée de type injection SQL, voici le lien :")
                print("-->", new_url)
                print("")
                return
        # On test l'injection SQL sur les formulaires
        forms = self.get_all_forms(url)
        print("*** Nous avons detecté ", len(forms), " formulaire dans cet URL : ", url)
        for form in forms:
            form_informations = self.get_informations_form(form)
            for injection in "\"'":
                # On prépare la requête avec les données (dans le body) que nous voulons envoyer
                data = {}
                for input in form_informations["inputs"]:
                    if input["type"] == "hidden" or input["value"]:
                        # Quand un formulaire est caché ou bien à une certaine valeur,
                        # alors il suffit simplement de l'utiliser dans le body du formulaire
                        try:
                            data[input["name"]] = input["value"] + injection
                        except:
                            pass
                    elif input["type"] != "submit":
                        # On ajoute un caractère spécial à la fin de la donnée inutile
                        # sauf pour le submit
                        data[input["name"]] = "donnéeInutile" + injection
                # On join l'URL à l'action
                url = urljoin(url, form_informations["action"])
                if form_informations["method"] == "post":
                    resp = response.post(url, data=data)
                elif form_informations["method"] == "get":
                    resp = response.get(url, params=data)
                # On test maintenant si la page est vulnérable avec le formulaire
                if self.test_vulnerable(resp):
                    print("")
                    print("!!!!!!! Une vulnérabilité à été détectée de type injection SQL, voici le lien :")
                    print("-->", url)
                    print("--> Et voici le formulaire :")
                    print("Action : " ,form_informations["action"])
                    print("Methode : ", form_informations["method"])
                    print("Inputs :")
                    for input in form_informations["inputs"]:
                        print("       ",input)
                    print("")
                    self.vulnerablepages.append(url)
                    break