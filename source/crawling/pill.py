# photo identifiction
# pill name (handels navn)
# aktive indeholdstof

from typing import List

# class PillExtended:

#     pillname = None
#     breastFeeding = ['']
#     otherFieldsOfApplication = ['']
#     fieldsOfApplication = ['']
#     commonSideEffects = ['']
#     uncommonSideEffects = ['']
#     unknownSideEffects = ['']
#     bloodDonor = ['']
#     dispensingForms = ['']
#     doping = ['']
#     dosageProposals = ['']
#     featuresHandlingDurability = ['']
#     pharmacodynamics = ['']
#     pharmacokinetics = ['']
#     company = ['']
#     poisoning = ['']
#     precautions = ['']
#     photoIdentifications = ['']
#     pregnancy = ['']
#     exipients = ['']
#     substances = ['']
#     instructions = ['']
#     interactions = ['']
#     contraIndications = ['']
#     hepaticImpairment = ['']
#     renalImpairment = ['']
#     marketRepresentations = ['']
#     schengenCertificates = ['']
#     substitutions = ['']
#     subsidies = ['']
#     traffic = ''
#     crucialErrors = ['']

#     def _init_(
#         self, 
#         pillname, 
#         breastFeeding, 
#         otherFieldsOfApplication, fieldsOfApplication,
#                 commonSideEffects, uncommonSideEffects, unknownSideEffects, bloodDonor,
#                 dispensingForms, doping, dosageProposals, featuresHandlingDurability,
#                 pharmacodynamics, pharmacokinetics, company, poisoning, precautions,
#                 photoIdentifications, pregnancy, exipients, substances, instructions,
#                 interactions, contraIndications, hepaticImpairment, renalImpairment,
#                 marketRepresentations, schengenCertificates, substitutions, subsidies,
#                 traffic, crucialErrors):

#         self.pillname = pillname
#         self.breastFeeding = breastFeeding
#         self.otherFieldsOfApplication = otherFieldsOfApplication
#         self.fieldsOfApplication = fieldsOfApplication
#         self.commonSideEffects = commonSideEffects
#         self.uncommonSideEffects = uncommonSideEffects
#         self.unknownSideEffects = unknownSideEffects
#         self.bloodDonor = bloodDonor
#         self.dispensingForms = dispensingForms
#         self.doping = doping
#         self.dosageProposals = dosageProposals 
#         self.featuresHandlingDurability = featuresHandlingDurability
#         self.pharmacodynamics = pharmacodynamics
#         self.pharmacokinetics = pharmacokinetics
#         self.company = company
#         self.poisoning = poisoning 
#         self.precautions = precautions
#         self.photoIdentifications = photoIdentifications
#         self.pregnancy = pregnancy
#         self.exipients = exipients
#         self.substances = substances 
#         self.instructions = instructions
#         self.interactions = interactions
#         self.contraIndications = contraIndications
#         self.hepaticImpairment = hepaticImpairment
#         self.renalImpairment = renalImpairment
#         self.marketRepresentations = marketRepresentations
#         self.schengenCertificates = schengenCertificates
#         self.substitutions = substitutions
#         self.subsidies = subsidies
#         self.traffic = traffic
#         self.crucialErrors = crucialErrors 


# class CommonError:
#     description = ''
#     consequence = ''
    
#     def _init_(self, description, consequence):
#         self.description = description
#         self.consequence = consequence


# class MarketRepresentation:
#     subsidy = ''
#     delivery = ''
#     dispensingForm = ''
#     vNumber = ''
#     packaging = ''
#     priceInDkk = ''
#     dddPrice = ''

#     def _init_(self, subsidy, delivery, dispensingForm, vNumber, packaging, priceInDkk, dddPrice):
#         self.subsidy = subsidy
#         self.delivery = delivery
#         self.dispensingForm = dispensingForm
#         self.vNumber = vNumber
#         self.packaging = packaging
#         self.priceInDkk = priceInDkk
#         self.dddPrice = dddPrice


class PhotoIdentification:
    def __init__(self, kind, strength, imprint, score, colour, sizeDimensions, imageUrl):  # noqa
        self.kind = kind
        self.strength = strength
        self.imprint: List[str] = imprint
        self.score = score
        self.colour: List[str] = colour
        self.sizeDimensions = sizeDimensions
        self.imageUrl: List[str] = imageUrl


class PillData:
    def __init__(self, pillname: str, substance: str, photofeatures: List[PhotoIdentification]):
        self.pillname = pillname
        self.substance = substance
        self.photofeatures: List[PhotoIdentification] = photofeatures
