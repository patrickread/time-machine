#!/usr/bin/env python

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

cred = credentials.Certificate("credentials/firebase.json")
default_app = firebase_admin.initialize_app(cred, {
  'databaseURL': os.environ['TM_FIREBASE_DB_URL']
})

ref = db.reference('/alarms')
user_id = os.environ['TM_USER_ID']
alarms = list(ref.get()[user_id].values())
print(alarms)
