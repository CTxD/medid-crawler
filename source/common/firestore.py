import os
import logging
import time 
from typing import Dict

from firebase_admin import credentials, firestore, initialize_app

from source.crawling import pill
from source.config import CONFIG


logger = logging.getLogger(__name__)


class FBManager:
    def __init__(self):
        certificate = credentials.Certificate(
            os.path.join(os.getcwd(), CONFIG["CERT"])
        )
        self.db = firestore.client(initialize_app(certificate))

    def _convert_obj_to_dict(self, obj):
        class_dict = {}

        def parsekeyvalue(key, value):
            if key.startswith('__'):
                return None

            if callable(value):
                return None

            if isinstance(value, list):
                newattrvalue = []
                for oldvalue in value:
                    if isinstance(oldvalue, (str, int, float, bool, bytes)):
                        newattrvalue.append(oldvalue)
                    else:
                        newattrvalue.append(self._convert_obj_to_dict(oldvalue))

                value = newattrvalue

            return value
        
        for attr in dir(obj):
            value = parsekeyvalue(attr, getattr(obj, attr))
            if value is None:
                continue

            class_dict[attr] = value

        return class_dict

    def add_or_update(self, collection_id: str, pill_object: pill.PillData):
        temp = self._convert_obj_to_dict(pill_object)
        self.db.collection(collection_id).document(pill_object.pillname).set(temp)

    def get(self, collection_id: str, document_id: str):
        return self.db.collection(collection_id).document(document_id).get()

    def get_all(self, collection_id: str):
        return self.db.collection(collection_id).get()

    def update_crawling_meta(self, obj: Dict):
        self.db.collection('crawls').document(str(int(time.time()))).set(obj)