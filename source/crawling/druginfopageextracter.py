from bs4 import BeautifulSoup
import requests


# Gets an soup object and returns a dictionary with active 
# categories 
def _whattosearchfor(soup):
    categories = {
        "Amning": "Active",
        "Andre anvendelsesområder": "Active",
        "Anvendelsesområder": "Active",
        "Bivirkninger": "Active",
        "Bloddonor": "Active",
        "Dispenseringsform": "Active",
        "Doping": "Active",
        "Doseringsforslag": "Active",
        "Egenskaber, håndtering og holdbarhed": "Active",
        "Farmakodynamik": "Active",
        "Farmakokinetik": "Active",
        "Firma": "Active",
        "Forgiftning": "Active",
        "Forsigtighedsregler": "Active",
        "Foto og identifikation": "Active",
        "Graviditet": "Active",
        "Hjælpestoffer": "Active",
        "Indholdsstoffer": "Active",
        "Instruktioner": "Active",
        "Interaktioner": "Active",
        "Kontraindikationer": "Active",
        "Nedsat leverfunktion": "Active",
        "Nedsat nyrefunktion": "Active",
        "Pakninger, priser, tilskud og udlevering": "Active",
        "Schengen-attest (pillepas)": "Active",
        "Substitution": "Active",
        "Tilskud": "Active",
        "Trafik": "Active",
        "Typiske alvorlige fejl": "Active"
    }
    # for k, v in categories.items():
    # print("Kay : {0}, Value : {1}".format(k, v))
    
    divs = soup.find('div', attrs={'class': 'pro-praeparat-quicklinks-div'})
    # divs = soup.find('span', attrs={'class': 'nolink'})
    print(divs)


# Gets a soupobject and processes it. The object is  sendt to
# senddata
def processedata():
    print("asd")
 

# Gets a url and sends it to processedata()
def getdata(url):
    try:
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'html.parser')
    except:
        print(url)
    finally:
        _whattosearchfor(soup)
        # print(soup)


# Gets a soup object and sends it to the backend
def senddata():
    print("asd")


getdata('http://pro.medicin.dk/Medicin/Praeparater/536')