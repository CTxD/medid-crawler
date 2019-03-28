import os
import firebase_admin
from firebase_admin import credentials, firestore


credentials = credentials.Certificate(
    os.path.join(os.getcwd(), "medid-certificate.json")
)
medId = firebase_admin.initialize_app(credentials)
db = firestore.client()