import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('firebase-adminsdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://research-paper-finder-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
ref = db.reference('/')
import json
with open("Research_Paper_JSON_master.json", "r") as f:
	file_contents = json.load(f)
ref.set(file_contents)