from typing import List


class PhotoIdentification:
    kind = ''
    imprint = ''
    score = ''
    colour = ''
    sizeDimensions = ''
    imageUrl = ''

    def __init__(self, kind, imprint, score, colour, sizeDimensions, imageUrl):
       self.kind = kind
       self.imprint = imprint
       self.score = score
       self.colour = colour
       self.sizeDimensions = sizeDimensions
       self.imageUrl = imageUrl


class PillData:
    def __init__(self, photofeatures: List[PhotoIdentification], pillname: str, substance: str):
        self.pillname = pillname
        self.substance = substance
        self.photofeatures: List[PhotoIdentification] = photofeatures
