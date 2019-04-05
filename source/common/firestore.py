import os
import logging

from firebase_admin import credentials, firestore, initialize_app

from source.crawling import pill
from source.config import CONFIG


logger = logging.getLogger(__name__)


class FBManager():
    def __init__(self):
        certificate = credentials.Certificate(
            os.path.join(os.getcwd(), CONFIG["CERT"])
        )
        self.db = firestore.client(initialize_app(certificate))

    def _convert_obj_to_dict(self, obj):
        class_dict = {}
        for attr in dir(obj):
            if attr.startswith('__'):
                continue

            attrvalue = getattr(obj, attr)

            if callable(attrvalue):
                continue

            if isinstance(attrvalue, list):
                newattrvalue = []
                for oldvalue in attrvalue:
                    newattrvalue.append(self._convert_obj_to_dict(oldvalue))

                attrvalue = newattrvalue

            class_dict[attr] = attrvalue

        return class_dict

    def add_or_update(self, collection_id: str, pill_object: pill.PillData):
        temp = self._convert_obj_to_dict(pill_object)
        self.db.collection(collection_id).document(pill_object.pillname).set(temp)

    def get(self, collection_id: str, document_id: str):
        return self.db.collection(collection_id).document(document_id).get()

    def get_all(self, collection_id: str):
        return self.db.collection(collection_id).get()