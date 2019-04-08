import logging
from . import pill, crawler
import re

logger = logging.getLogger(__name__)


# Input: soup object
# Output: object with pill name, activ substanc, and a list of photo elements
def _getpilldata(soup):
    if _ismedicincompatible(soup):
        print("IM MAKING AN PILL OBJ")
        pillname = _getpillname(soup)
        substance = _getpillsubstance(soup)
        photoinfo = _getphotoidentification(soup)
       
        return pill.PillData(pillname, substance, photoinfo)
    return None
    

def _ismedicincompatible(soup):
    try:
        headerclassname = 'thumbarrow'
        isitapill = soup.find('td', attrs={'class': headerclassname})
        isitapill = isitapill.h4.text.lower()
        # Checks if it is a tablet or a kapsle
        if 'tablet' in isitapill or 'kapsle' in isitapill:
            print("it is a tablet or a kapsle")
            try:
                substanceclassname = 'SpaceBtm IndholdsstofferHeaderLinks'
                substance = soup.find('div', attrs={'class': substanceclassname}).b.text
                if substance is not None:
                    print("in substance if")
                    return True
            except Exception as e:
                print("in exception")
                e = False
                return e
    except Exception:
        print("it is not a tablet or a kapsle")
        return False
    return False


def _isphotoandidentification(soup):
    try:
        headerclassname = 'thumbarrow'
        isitapill = soup.find('td', attrs={'class': headerclassname})
        isitapill = isitapill.h4.text.lower()
        # Checks if it is a tablet or a kapsle
        if 'tablet' in isitapill or 'kapsle' in isitapill:
            print("it is a tablet or a kapsle")
            return True
    except Exception:
        print("it is not a tablet or a kapsle")
        return False
    return False
   
    # headclassname = 'glob-floatLeft'
    # categorie = "foto og identifikation"
    # categories = ''
    
    # for head in soup.find_all('h3', attrs={headclassname}):
    #     head = head.text.lower()
    #     categories += head
    # if categories == categorie:
    #     print("there is a categorie")
    #     return True
    # print("there is not a categorie")  
    # return False


def _getpillsubstance(soup):
    classname = 'SpaceBtm IndholdsstofferHeaderLinks'
    substance = soup.find('div', attrs={'class': classname})
    return substance.b.text.strip()


# Input: Soup object.
# Output: The name of the drug.
def _getpillname(soup):
    rawname = soup.h1.text.strip()
    if '/' in rawname:
        print('####################', rawname, '#############################')
        rawname = rawname.replace('/', '\\')
        print('####################', rawname, '#############################')

    return rawname
 

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
    except Exception as e:
        logger.error(
            'Something went wrong parsing the soup from the url. '
            f'The following exceptins was raised: {type(e)} :: {str(e)}'
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
            imprintarr.append(imprintphoto['src'].strip())
    else:
        imprintarr = [imp.strip() for imp in isimprinttext.text.split(',')]
    return imprintarr


def _getpillcolour(tablevalue):
    return [color.strip() for color in tablevalue.text.split(',')]


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
                tablekey = tablerow.find(
                    'td', 
                    attrs={'class': 'glob-ident-row-data-col-row-mark'}
                ).text
                tablekey = tablekey.lower().split()[0].split(':')[0]
                tablevalue = tablerow.find(
                    'td', 
                    attrs={'class': 'glob-alignRight glob-ident-second-size'}
                )

                if tablekey == "præg":
                    tempfeaturedict["imprint"] = _getpillimprint(photoinfo)
                elif tablekey == "farve":
                    tempfeaturedict["colour"] = _getpillcolour(tablevalue)
                else:
                    tempfeaturedict[keymapping[tablekey]] = tablevalue.text
            
            # Gets the image of the pill
            image = _getpillimage(photoinfo)
            tempfeaturedict["imageUrl"] = image
            imageinfoarr.append(pill.PhotoIdentification(**tempfeaturedict))
            
    return imageinfoarr


# Gets a url and sends it to processedata() 
def getdata(urls):
    #featureobjarr = []
    for url in urls:
        try:
            print("---------start---------")
            logger.info('Extracting drug info from url %s', url)
            soup = crawler.crawl(url)
            pilldata = _getpilldata(soup)
            if pilldata is None:
                logger.warning('Drug not pill or tablet')
                print("---------stop---------")
                continue
            yield pilldata
            # featureobjarr.append(pilldata)
            print("---------append---------")
        except Exception as e:
            logger.error(
                'Something went wrong parsing the soup from the url. '
                f'The following exceptins was raised: {type(e)} :: {str(e)}'
                f' ON URL: {url}'
            )
    # return featureobjarr

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