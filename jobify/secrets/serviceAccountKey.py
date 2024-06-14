## README: The service account json provided by firebase is converted to base64 format for ease of storage by command:
## cat path-to-your-service-account.json | base64 | xargs


from dotenv import load_dotenv, find_dotenv
import os
import json
import base64
load_dotenv(find_dotenv())

firebase_credentials = os.getenv("FIREBASE_SERVICE_ACCOUNT")
SERVICE_ACCOUNT_JSON = json.loads(base64.b64decode(firebase_credentials).decode('utf-8'))

# firebase_credentials = {
#   "type": os.getenv("FIREBASE_TYPE"),
#   "project_id": os.getenv("FIREBASE_PROJECT_ID"),
#   "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
#   "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),
#   "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
#   "client_id": os.getenv("FIREBASE_CLIENT_ID"),
#   "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
#   "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
#   "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
#   "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
#   "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN"),
# }