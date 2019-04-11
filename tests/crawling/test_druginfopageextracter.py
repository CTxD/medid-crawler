# pylint:disable=protected-access
import collections
from urllib.parse import urlparse
import bs4
import httmock
import requests
from source.crawling import druginfopageextracter
from source.crawling.pill import PhotoIdentification, PillData


imprintimagehtml = """
<tbody><tr>
  <td class="glob-ident-row-data-col-row-mark" valign="top" nowrap="">Præg:</td>
  <td class="glob-alignRight glob-ident-second-size" valign="top">
    <div class="glob-floatRight"><img class="glob-ident-praeg DisplayInline" src="/resource/media/15fb56d9-856a-4352-bb83-bca96eea9d09"></div>
  </td>
</tr>
</tbody>
""" 

compatibilityhtml = """
<h1 class="ptitle" title="Actiq/asd">Actiq<sup>/</sup>asd<span class="glob-h1mini"> </span></h1>
  <div class="glob-floatLeft width75Procent">
    <div class="glob-praeparat-indholdsstofffer-header">
      <div class="SpaceBtm IndholdsstofferHeaderLinks"><a href="/Medicin/Indholdsstoffer/442"><b>Fentanyl</b></a></div>
    </div>
  </div>
<body>
<div class="glob-ident-row-openclose">
        <table class="thumbHeader">
          <tbody><tr>
            <td class="thumbarrow" valign="top">
                <img class="glob-floatLeft rotatearrow" src="/Content/Images
                /Pro/Topmenu/link_pro.gif" alt="" width="8" height="13">
            <h4 class="glob-floatLeft glob-main-color">Tabletter
              &nbsp;5 mg</h4>
            </td>
            <td class="thumbnail" valign="top"><img src="/resource/media
            /NP4W2MUH?ptype=1&amp;icon=true&amp;width=100&amp;height=50"></td>
          </tr>
        </tbody></table>
        <div class="identRowTable glob-col650 glob-floatLeft" style="display: none;">
          <div class="glob-floatLeft glob-col160 glob-marginRight20">
            <div class="glob-floatLeft glob-col160">
              <table class="glob-identRowTable" cellspacing="0" cellpadding="2" border="0">
                <colgroup>
                  <col style="width:30%;">
                  <col style="width:70%;">
                </colgroup>
                <tbody><tr>
                  <td class="glob-ident-row-data-col-row-mark" valign="top" nowrap="">Præg:</td>
                  <td class="glob-alignRight glob-ident-second-size" valign="top">
                    <div class="glob-floatRight">A-007, 5</div>
                  </td>
                </tr>
                <tr>
                  <td class="glob-ident-row-data-col-row-mark" valign="top">Kærv:</td>
                  <td class="glob-alignRight glob-ident-second-size" valign="top">Ingen kærv</td>
                </tr>
                <tr>
                  <td class="glob-ident-row-data-col-row-mark" valign="top">Farve:</td>
                  <td class="glob-alignRight glob-ident-second-size" valign="top">Blå</td>
                </tr>
                <tr>
                  <td class="glob-ident-row-data-col-row-mark" valign="top">Mål i mm:</td>
                  <td class="glob-alignRight glob-ident-second-size" valign="top">4,6 x 8,2</td>
                </tr>
              </tbody></table>
            </div>
          </div>
          <div class="glob-col430 glob-floatLeft glob-marginLeft9 vertAlignTop padtop15">
          <img class="glob-ident-row-image alignLeft vertAlignTop" src="/resource/media/NP4W2MUH?ptype=1" alt="tabletter 5 mg ">
          <div class="glob-floatNone"></div>
            <div class="glob-floatNone">&nbsp;</div>
            <div class="glob-floatNone">&nbsp;</div>
          </div>
        </div>
        <div class="glob-floatNone">&nbsp;</div>
      </div>
</body>
"""

imagehtml = """
<body>
<div class="glob-ident-row-openclose">
        <table class="thumbHeader">
          <tbody><tr>
            <td class="thumbarrow" valign="top">
                <img class="glob-floatLeft rotatearrow" src="/Content/Images
                /Pro/Topmenu/link_pro.gif" alt="" width="8" height="13">
            <h4 class="glob-floatLeft glob-main-color">Tabletter
              &nbsp;5 mg</h4>
            </td>
            <td class="thumbnail" valign="top"><img src="/resource/media
            /NP4W2MUH?ptype=1&amp;icon=true&amp;width=100&amp;height=50"></td>
          </tr>
        </tbody></table>
        <div class="identRowTable glob-col650 glob-floatLeft" style="display: none;">
          <div class="glob-floatLeft glob-col160 glob-marginRight20">
            <div class="glob-floatLeft glob-col160">
              <table class="glob-identRowTable" cellspacing="0" cellpadding="2" border="0">
                <colgroup>
                  <col style="width:30%;">
                  <col style="width:70%;">
                </colgroup>
                <tbody><tr>
                  <td class="glob-ident-row-data-col-row-mark" valign="top" nowrap="">Præg:</td>
                  <td class="glob-alignRight glob-ident-second-size" valign="top">
                    <div class="glob-floatRight">A-007, 5</div>
                  </td>
                </tr>
                <tr>
                  <td class="glob-ident-row-data-col-row-mark" valign="top">Kærv:</td>
                  <td class="glob-alignRight glob-ident-second-size" valign="top">Ingen kærv</td>
                </tr>
                <tr>
                  <td class="glob-ident-row-data-col-row-mark" valign="top">Farve:</td>
                  <td class="glob-alignRight glob-ident-second-size" valign="top">Blå</td>
                </tr>
                <tr>
                  <td class="glob-ident-row-data-col-row-mark" valign="top">Mål i mm:</td>
                  <td class="glob-alignRight glob-ident-second-size" valign="top">4,6 x 8,2</td>
                </tr>
              </tbody></table>
            </div>
          </div>
          <div class="glob-col430 glob-floatLeft glob-marginLeft9 vertAlignTop padtop15">
          <img class="glob-ident-row-image alignLeft vertAlignTop" src="/resource/media/NP4W2MUH?ptype=1" alt="tabletter 5 mg ">
          <div class="glob-floatNone"></div>
            <div class="glob-floatNone">&nbsp;</div>
            <div class="glob-floatNone">&nbsp;</div>
          </div>
        </div>
        <div class="glob-floatNone">&nbsp;</div>
      </div>
</body>
"""

plasterhtml = """
<body>
<div class="glob-ident-row-openclose">
        <table class="thumbHeader">
          <tbody><tr>
            <td class="thumbarrow" valign="top">
                <img class="glob-floatLeft rotatearrow" src="/Content/Images
                /Pro/Topmenu/link_pro.gif" alt="" width="8" height="13">
            <h4 class="glob-floatLeft glob-main-color">Plaster
              &nbsp;5 mg</h4>
            </td>
            </tr>
          </tbody>
        </table>
</div>
</body>
"""


headerhtml = """
<div>
  <h1 class="ptitle" title="Actiq/asd">Actiq<sup>/</sup>asd<span class="glob-h1mini"> </span></h1>
  <div class="glob-floatLeft width75Procent">
    <div class="glob-praeparat-indholdsstofffer-header">
      <div class="SpaceBtm IndholdsstofferHeaderLinks"><a href="/Medicin/Indholdsstoffer/442"><b>Fentanyl</b></a></div>
    </div>
  </div>
  <div class="glob-floatRight width25Procent glob-alignRight">
    <div class="glob-padbtm20 glob-padTop12"><a class="displayBlock" name="ATCkode"></a><div><b>N02AB03</b></div>
    </div>
  </div>
  <div class="glob-floatNone"></div>
</div>
"""

kindhtml = """
<td class="thumbarrow" valign="top">
                <img class="glob-floatLeft rotatearrow" src="/Content/Images
                /Pro/Topmenu/link_pro.gif" alt="" width="8" height="13">
            </td>
"""


invalidimagehtml = """
<img class="glob-ident-row-image alignLeft vertAlignTop" src="/resource/media/NP4W2MUH?ptype=1" alt="Vi har desværre pt. ikke et foto af denne dispenseringsform og styrke">
"""


VALIDSCHEME, VALIDNETLOC, VALIDPATH, _, VALIDQUERY, _ = urlparse('http://mockurl.valid/')


@httmock.urlmatch(scheme=VALIDSCHEME, netloc=VALIDNETLOC, path=VALIDPATH, query=VALIDQUERY)
def valid_url_mock_returns_invalid_content(url: str, request: requests.Request):
    return {'status_code': 200, 'content': '<p>Invalid content</p>'}


@httmock.urlmatch(scheme=VALIDSCHEME, netloc=VALIDNETLOC, path=VALIDPATH, query=VALIDQUERY)
def valid_url_mock_returns_valid_content(url: str, request: requests.Request):
    return {'status_code': 200, 'content': compatibilityhtml}


VALIDSCHEMEIMG, VALIDNETLOCIMG, VALIDPATHIMG, _, VALIDQUERYIMG, _ = urlparse('http://pro.medicin.dk/resource/media/NP4W2MUH?ptype=1')
@httmock.urlmatch(scheme=VALIDSCHEMEIMG, netloc=VALIDNETLOCIMG, path=VALIDPATHIMG, query=VALIDQUERYIMG)
def valid_image_url(url: str, request: requests.Request):
    return {'status_code': 200, 'content': 'something'}


soup = bs4.BeautifulSoup(imagehtml, 'html.parser')
plastersoup = bs4.BeautifulSoup(plasterhtml, 'html.parser')
headersoup = bs4.BeautifulSoup(headerhtml, 'html.parser')
imprintsoup = bs4.BeautifulSoup(imprintimagehtml, 'html.parser')
kindsoup = bs4.BeautifulSoup(kindhtml, 'html.parser')
compatibilitysoup = bs4.BeautifulSoup(compatibilityhtml, 'html.parser')
invalidimagesoup = bs4.BeautifulSoup(invalidimagehtml, 'html.parser')


def test__getpillimage_with_valid_image():
    with httmock.HTTMock(valid_image_url):
        result = druginfopageextracter._getpillimage(soup)
    assert result == [b'c29tZXRoaW5n']


def test__getpillimage_with_invalid_image():
    result = druginfopageextracter._getpillimage(invalidimagesoup)
    assert result == [None]


def test_extractkindandstrengthfrombs4():
    result = druginfopageextracter._getpillkindandstrength(soup)
    assert result == ['Tabletter', '5 mg']


def test__getpillkindandstrength_nokindorstrength():
    result = druginfopageextracter._getpillkindandstrength(kindsoup)
    assert result == [None, None]


def test__getpillimprint_manytextelements():
    result = druginfopageextracter._getpillimprint(soup)
    assert result == ['A-007', '5']


def test__getpillimprint_image():
    result = druginfopageextracter._getpillimprint(imprintsoup)
    assert result == ['/resource/media/15fb56d9-856a-4352-bb83-bca96eea9d09']


def test__getpillcolour_onecolour():
    colourhtml = '<td class="glob-alignRight glob-ident-second-size" valign="top">Hvid</td>'
    coloursoup = bs4.BeautifulSoup(colourhtml, 'html.parser')
    result = druginfopageextracter._getpillcolour(coloursoup)
    assert result == ['Hvid']


def test__getpillcolour_manycolours():
    colourhtml = '<td class="glob-alignRight glob-ident-second-size" valign="top">Hvid, Black</td>'
    coloursoup = bs4.BeautifulSoup(colourhtml, 'html.parser')
    result = druginfopageextracter._getpillcolour(coloursoup)
    assert result == ['Hvid', 'Black']


def test__getphotoidentification_nopillorcapsule():
    result = druginfopageextracter._getphotoidentification(plastersoup)
    assert result == []


def test__getphotoidentification_withpillorcapsule():
    with httmock.HTTMock(valid_image_url):
        result = druginfopageextracter._getphotoidentification(soup)
    dataeq = PhotoIdentification(**{
        'kind': 'Tabletter', 'strength': '5 mg', 'imprint': ['A-007', '5'], 
        'score': 'Ingen kærv', 'colour': ['Blå'], 'sizeDimensions': '4,6 x 8,2', 
        'imageEncoding': [b'c29tZXRoaW5n']
    })
    
    assert len(result) == 1
    for prop in dir(result[0]):
        if prop.startswith('_'):
            continue
        assert hasattr(dataeq, prop)

        resattr = getattr(result[0], prop)
        dataattr = getattr(dataeq, prop)

        assert type(resattr) == type(dataattr) # noqa

        if isinstance(resattr, list):
            assert collections.Counter(dataattr) == collections.Counter(resattr)
        else:
            assert dataattr == resattr


def test__getpillname_withslash():
    result = druginfopageextracter._getpillname(headersoup)
    assert result == "Actiq\\asd"


def test__getpillsubstance():
    result = druginfopageextracter._getpillsubstance(headersoup)
    assert result == 'Fentanyl'


def test__ismedicincompatible_withinvalidinput():
    result = druginfopageextracter._ismedicincompatible(plastersoup)
    assert result is False


def test__ismedicincompatible_withvalidinput():
    result = druginfopageextracter._ismedicincompatible(compatibilitysoup)
    assert result is True


def test__getpilldata_withinvalidinput():
    result = druginfopageextracter._getpilldata("This is invalid data")
    assert result is None


def test__getpilldata_withvalidinput():
    result = druginfopageextracter._getpilldata(compatibilitysoup)
    dataeq = PillData("Actiq\\asd", "Fentanyl", PhotoIdentification(**{
        'kind': 'Tabletter', 'strength': '5 mg', 'imprint': ['A-007', '5'], 
        'score': 'Ingen kærv', 'colour': ['Blå'], 'sizeDimensions': '4,6 x 8,2', 
        'imageEncoding': ['/resource/media/NP4W2MUH?ptype=1']
    }))
    assert result.pillname == dataeq.pillname
    assert result.substance == dataeq.substance


def test_getdata_invalid_data(caplog):
    with httmock.HTTMock(valid_url_mock_returns_invalid_content):
        pills = list(druginfopageextracter.getdata(['http://mockurl.valid/']))
        assert len(caplog.records) == 2
        assert pills == []
        assert 'Extracting drug info from url http://mockurl.valid/' in caplog.text
        assert 'Drug not pill or tablet' in caplog.text


def test_getdata_exception(caplog):
    with httmock.HTTMock(valid_url_mock_returns_invalid_content):
        pills = list(druginfopageextracter.getdata([None]))
        assert len(caplog.records) == 2
        assert pills == []
        assert 'Extracting drug info from url' in caplog.text
        assert 'omething went wrong parsing the soup from the url.' in caplog.text


def test_getdata_valid_data(caplog):
    data = PillData("Actiq\\asd", "Fentanyl", PhotoIdentification(**{
        'kind': 'Tabletter', 'strength': '5 mg', 'imprint': ['A-007', '5'], 
        'score': 'Ingen kærv', 'colour': ['Blå'], 'sizeDimensions': '4,6 x 8,2', 
        'imageEncoding': ['/resource/media/NP4W2MUH?ptype=1']
    }))
    with httmock.HTTMock(valid_url_mock_returns_valid_content):
        result = list(druginfopageextracter.getdata(['http://mockurl.valid/']))
        assert len(caplog.records) == 1
        assert result is not None
        assert len(result) == 1
        assert result[0].pillname == data.pillname 
        assert result[0].substance == data.substance