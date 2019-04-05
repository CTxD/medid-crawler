# pylint:disable=protected-access
import bs4
from source.crawling import druginfopageextracter

imprintimagehtml = """
<tbody><tr>
  <td class="glob-ident-row-data-col-row-mark" valign="top" nowrap="">Præg:</td>
  <td class="glob-alignRight glob-ident-second-size" valign="top">
    <div class="glob-floatRight"><img class="glob-ident-praeg DisplayInline" src="/resource/media/15fb56d9-856a-4352-bb83-bca96eea9d09"></div>
  </td>
</tr>
</tbody>
""" 

'''
imprintonetexthtml = """
<tbody><tr>
  <td class="glob-ident-row-data-col-row-mark" valign="top" nowrap="">Præg:</td>
  <td class="glob-alignRight glob-ident-second-size" valign="top">
    <div class="glob-floatRight">VS2</div>
  </td>
</tr>
</tbody>
""" 
'''

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
  <h1 class="ptitle" title="Actiq®">Actiq<sup>®</sup><span class="glob-h1mini"> </span></h1>
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

soup = bs4.BeautifulSoup(imagehtml, 'html.parser')
plastersoup = bs4.BeautifulSoup(plasterhtml, 'html.parser')
headersoup = bs4.BeautifulSoup(headerhtml, 'html.parser')
imprintsoup = bs4.BeautifulSoup(imprintimagehtml, 'html.parser')
kindsoup = bs4.BeautifulSoup(kindhtml, 'html.parser')


def test_extractimagesourcefrombs4():
    result = druginfopageextracter._getpillimage(soup)
    assert result == ['/resource/media/NP4W2MUH?ptype=1']


def test_extractkindandstrengthfrombs4():
    result = druginfopageextracter._getpillkindandstrength(soup)
    assert result == ['Tabletter', '5 mg']


def test__getpillkindandstrength_nokindorstrength():
    result = druginfopageextracter._getpillkindandstrength(kindsoup)
    assert result == [None, None]


def test__getpillimprint_manytextelements():
    result = druginfopageextracter._getpillimprint(soup)
    assert result == ['A-007', ' 5']


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
    assert result == ['Hvid', ' Black']


def test__getphotoidentification_nopillorcapsule():
    result = druginfopageextracter._getphotoidentification(plastersoup)
    assert result == []


def test__getphotoidentification_withpillorcapsule():
    result = druginfopageextracter._getphotoidentification(soup)
    assert result == [{'kind': 'Tabletter', 'strength': '5 mg', 'imprint': ['A-007', ' 5'], 
                       'score': 'Ingen kærv', 'colour': ['Blå'], 'sizeDimensions': '4,6 x 8,2', 
                       'imageUrl': ['/resource/media/NP4W2MUH?ptype=1']}]


def test__getpillname():
    result = druginfopageextracter._getpillname(headersoup)
    assert result == 'Actiq® '


def test__getpillsubstance():
    result = druginfopageextracter._getpillsubstance(headersoup)
    assert result == 'Fentanyl'