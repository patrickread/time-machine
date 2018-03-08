#!/usr/bin/env python
# Retrieves alarms from Firebase DB when called, and stores in a local file at data/alarms.json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import json

cred = credentials.Certificate("credentials/firebase.json")
default_app = firebase_admin.initialize_app(cred, {
  'databaseURL': os.environ['TM_FIREBASE_DB_URL']
})

# Read alarms from Firebase DB
ref = db.reference('/alarms')
user_id = os.environ['TM_USER_ID']
alarms = list(ref.get()[user_id].values())

# Write out to file
file_handler = open("data/alarms.json", "w")
file_handler.write(json.dumps(alarms))
file_handler.close()
