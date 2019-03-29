import os
import inspect
import firebase_admin
import logging
import json
from source.crawling import pill
from firebase_admin import credentials, firestore


logger = logging.getLogger(__name__)
credentials = credentials.Certificate(
    os.path.join(os.getcwd(), "medid-certificate.json")
)
medId = firebase_admin.initialize_app(credentials)
db = firestore.client()

def _convert_obj_to_dict(obj):
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
                newattrvalue.append(_convert_obj_to_dict(oldvalue))

            attrvalue = newattrvalue

        class_dict[attr] = attrvalue

    return class_dict

def add_or_update(collection_id: str, pill_object: pill.PillData):
        temp = _convert_obj_to_dict(pill_object)
        print(json.dumps(temp, indent=4))
        db.collection(collection_id).document(pill_object.pillname).set(temp)


def get(collection_id: str, document_id: str):
    return db.collection(collection_id).document(document_id).get()


def get_all(collection_id: str):
    return db.collection(collection_id).get()

