import requests
from bs4 import BeautifulSoup
import re
import threading

domainUrl = "https://django-anuncios.solyd.com.br"
url_cars = "https://django-anuncios.solyd.com.br/automoveis/"

LINKS = []
PHONES = []

def searchCar(url):
    try:
        requestSearch = requests.get(url)

        if requestSearch.status_code == 200:
            return requestSearch.text

        else:
            print("Error in sending request")

    except Exception as error:
        print("Oops there was an error ! Please try again ")
        print(error)

def parsingRequest(requestSearch):
    try:
        soup = BeautifulSoup(requestSearch, "html.parser")
        return soup

    except Exception as error:
        print("Oops there was an error ! Please try again ")
        print(error)


def searchLinks(soup):
    try:
        cards_root = soup.find("div", class_="ui three doubling link cards")
        cards_item = cards_root.find_all("a")

    except Exception as error:
        print("Oops there was an error ! Please try again ")
        print(error)
        return None

    links = []

    for card in cards_item:
        try:
            link = card["href"]
            links.append(link)

        except:
            pass

    return links

def getPhone(soup):
    try:
        descriptionResponse = soup.find_all("div", class_="sixteen wide column")[2].p.get_text().strip()

    except Exception as error:
        print("Oops there was an error ! Please try again ")
        print(error)
        return None

    regx = re.findall(r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})", descriptionResponse)
    if regx:
        return regx

def discoverPhone():
    while True:
        try:
            advertisementLink = LINKS.pop(0)
        except:
            return None

        ResponseAdvertisement = searchCar(domainUrl + advertisementLink)

        if ResponseAdvertisement:
            soup = parsingRequest(ResponseAdvertisement)
            if soup:
                phones = getPhone(soup)
                if phones:
                    for phone in phones:
                        print("Phone found: ", phone)
                        PHONES.append(phone)
                        savePhone(phone)

def savePhone(phone):
    stringPhone = "{}{}{}\n".format(phone[0], phone[1], phone[2])
    try:
        with open("phones.csv", "a") as arquivo:
            arquivo.write(stringPhone)
    except Exception as error:
        print("Oops there was an error ! Please try again ")
        print(error)

if __name__ == "__main__":
    responseSearch = searchCar(url_cars)
    if responseSearch:
        soupSearch = parsingRequest(responseSearch)
        if soupSearch:
            LINKS = searchLinks(soupSearch)

            THREADS = []
            for i in range(10):
                t = threading.Thread(target=discoverPhone)
                THREADS.append(t)

            for t in THREADS:
                t.start()

            for t in THREADS:
                t.join()