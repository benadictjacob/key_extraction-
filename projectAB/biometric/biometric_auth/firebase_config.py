# firebase_config.py
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate(r"biometric_auth\fingerscannner-firebase-adminsdk-fbsvc-d2ee995aaa.json")

# Avoid re-initializing if already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
