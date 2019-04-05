from bs4 import BeautifulSoup
import requests
import logging
from . import pill
import re


# Input: soup object
# Output: object with pill name, activ substanc, and a list of photo elements
def _getpilldata(soup):
    pillname = _getpillname(soup)
    substance = _getpillsubstance(soup)
    photoinfo = _getphotoidentification(soup)

    pillobj = pill.PillData(pillname, substance, photoinfo)
    return pillobj
    

def _getpillsubstance(soup):
    classname = 'SpaceBtm IndholdsstofferHeaderLinks'
    substance = soup.find('div', attrs={'class': classname})
    return substance.b.text


# Input: Soup object.
# Output: The name of the drug.
def _getpillname(soup):
    return soup.h1.text 
 

def _getpillkindandstrength(photoinfo):
    temparr = []
    headerclassname = 'thumbarrow'
    try:
        pilltype = photoinfo.find('td', attrs={'class': headerclassname}).h4.text
        typetext = " ".join(pilltype.strip().split())
        if typetext:
            matches = re.match(r'(\D*)([\d,]* ?[\S]+)(\D*)', typetext)
            temparr.append(matches.group(1).strip())
            temparr.append(matches.group(2).strip())
        return temparr
    except Exception:
        logging.error('Something went wrong parsing the soup from the url. '
                      'The following exceptins was raised: {type(e)} :: {str(e)}'
                      )
        temparr.extend([None, None]) 
        return temparr


def _getpillimage(photoinfo):
    # iterates over all images and gets the images of the pills
    classname = 'glob-ident-row-image alignLeft vertAlignTop'
    imagearr = []
    for pillphoto in photoinfo.find_all('img', attrs={classname}):
        imagearr.append(pillphoto['src'])
    return imagearr


def _getpillimprint(photoinfo):
    isimprintphoto = photoinfo.find('img', attrs={'glob-ident-praeg DisplayInline'})
    isimprinttext = photoinfo.find('div', attrs={'glob-floatRight'})
    imprintarr = []

    if isimprintphoto is not None:                    
        # Gets the imprint image and stores it in the dictionary
        for imprintphoto in photoinfo.find_all('img', attrs={'glob-ident-praeg DisplayInline'}):
            imprintarr.append(imprintphoto['src'])
    else:
        imprintarr = isimprinttext.text.split(',')
    return imprintarr


def _getpillcolour(tablevalue):
    return tablevalue.text.split(',')


# Input: soup object
# Output: list of pill features for one or more pills
def _getphotoidentification(soup):
    headerclassname = 'thumbarrow'
    keymapping = {
        'præg': 'imprint',
        'kærv': 'score',
        'farve': 'colour',
        'mål': 'sizeDimensions'
    }
    imageinfoarr = []
    isitapill = soup.find('td', attrs={'class': headerclassname})
    isitapill = isitapill.h4.text.lower()
    # Checks if it is a tablet or a kapsle
    if 'tablet' in isitapill or 'kapsle' in isitapill:
        # Iterates over the amount of different types of pills there are for one kind
        for photoinfo in soup.find_all('div', attrs={'class': 'glob-ident-row-openclose'}):
            tempfeaturedict = {
                "kind": "",
                "strength": "",
                "imprint": "",
                "score": "",
                "colour": "",
                "sizeDimensions": "",
                "imageUrl": ""
            }

            # Gets the pill type and formats it
            pilltypeandstrength = _getpillkindandstrength(photoinfo) 
            tempfeaturedict["kind"] = pilltypeandstrength[0]
            tempfeaturedict["strength"] = pilltypeandstrength[1]

            # Iterates over the list of pill features and ekstrackts the key and value pairs
            table = photoinfo.find('table', attrs={'class': 'glob-identRowTable'})
            for tablerow in table.find_all('tr'):
                tablekey = tablerow.find('td', attrs={'class': 'glob-ident-row-data-col-row-mark'}).text
                tablekey = tablekey.lower().split()[0].split(':')[0]
                tablevalue = tablerow.find('td', attrs={'class': 'glob-alignRight glob-ident-second-size'})

                if tablekey == "præg":
                    tempfeaturedict["imprint"] = _getpillimprint(photoinfo)
                elif tablekey == "farve":
                    tempfeaturedict["colour"] = _getpillcolour(tablevalue)
                else:
                    tempfeaturedict[keymapping[tablekey]] = tablevalue.text
            
            # Gets the image of the pill
            image = _getpillimage(photoinfo)
            tempfeaturedict["imageUrl"] = image
            imageinfoarr.append(tempfeaturedict)
            
    return imageinfoarr


# Gets a url and sends it to processedata() 
def getdata(urls):
    featureobjarr = []
    for url in urls:
        try:
            source = requests.get(url).text
            soup = BeautifulSoup(source, 'html.parser')
            # _traverse_children(soup)
            featureobjarr.append(_getpilldata(soup))
            # _getphotoidentification(soup)
        except Exception:
            logging.error('Something went wrong parsing the soup from the url. '
                          'The following exceptins was raised: {type(e)} :: {str(e)}'
                          )


# # will be used for traversing thuge all categories for one pill
# def _traverse_children(soup):
#     keymapping = {
#         "Foto og identifikation": "photoandidentification"
#     }
#     categories = {
#         "photoandidentification": ""
#     }
#     classnameone = 'glob-floatNone glob-content-section-wrapper'
#     classnametwo = 'glob-floatNone glob-content-section-wrapper phone-content-section-wrapper'
#     headclassname = 'glob-floatLeft'
#     bodyclassname = 'glob-floatNone glob-content-section-text phone-content-section-openclose-text'
    
#     for categorieone in soup.find_all('div', attrs={classnameone}):
#         for head in categorieone.find_all('h3', attrs={headclassname}):
#             print(head.text)
#     print("------------------------------------------------------")
#     for categorietwo in soup.find_all('div', attrs={classnametwo}):
#         for head in categorietwo.find_all('h3', attrs={headclassname}):
#             print(head.text) 
# '''
