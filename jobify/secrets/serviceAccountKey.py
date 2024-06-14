## README: The service account json provided by firebase is converted to base64 format for ease of storage by command:
## cat path-to-your-service-account.json | base64 | xargs


from dotenv import load_dotenv, find_dotenv
import os
import json
import base64
load_dotenv(find_dotenv())

firebase_credentials = os.getenv("FIREBASE_SERVICE_ACCOUNT")
SERVICE_ACCOUNT_JSON = json.loads(base64.b64decode(firebase_credentials).decode('utf-8'))
