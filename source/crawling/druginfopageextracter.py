from bs4 import BeautifulSoup
import requests

# # info body name: 
# 9 glob-content-header-wrapper phone-content-header-openclose-wrapper
# 12 glob-floatNone glob-content-header-wrapper phone-content-header-openclose-wrapper
# 22 glob-floatLeft
# # info body:
# glob-floatNone glob-content-section-text phone-content-section-openclose-text 


# Input: Soup object.
# Output: The name of the drug.
def _get_pill_name(soup):
    return soup.head.title.text 


# Input: Soup object.
# Output: The headline of the information area.
def _get_information_area_headline(soup):
    classname = 'glob-floatLeft'
    for informationarea in soup.find_all('h3', attrs={'class': classname}):
        headline = informationarea.text
        print(headline)


# Input: soup object.
# Output: One of the information area bodies.
def _get_information_area_body(soup):
    classname = 'glob-floatNone glob-content-section-text phone-content-section-openclose-text'
    for informationareabody in soup.find_all('div', attrs={'class': classname}):
        _traverse_children(informationareabody)


# Input: div body
# Output: a list with strings
def _traverse_children(informationareabody):
    #  asd = []
    for child in informationareabody.recursiveChildGenerator():
        name = getattr(child, "name", None)
        if name is not None:
            pass
            # print(name)
        elif not child.isspace(): # leaf node, don't print spaces
            print(child)
            # asd.append(child)
    print("--------------------")
    # print(asd)


def _process_data(soup):
    classname = 'glob-content-header-wrapper phone-content-header-openclose-wrapper'
    asd = soup.find_all('div', attrs={'class': classname}).h3
    print(asd)


# Gets a url and sends it to processedata() 
def getdata(url):
    try:
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'html.parser')
    except expression as identifier:
        pass
        print(url)
        print("somthing went wrong")
    finally:
        # _process_data(soup)
        #_get_information_area_body(soup)
        _get_information_area_headline(soup)
        # _get_pill_name(soup)
        # _whattosearchfor(soup)
        # print(soup)


getdata('http://pro.medicin.dk/Medicin/Praeparater/536')