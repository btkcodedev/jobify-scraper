import firebase_admin
from datetime import datetime
from firebase_admin import credentials, firestore
from jobify.config import COMPANIES

cred = credentials.Certificate("jobify/secrets/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def write_companies():
    print("Starting to write companies to firebase")
    doc = {str(i + 1): company for i, company in enumerate(COMPANIES)}
    db.collection("companies").add(doc)
    print("Data written to Firebase successfully.")

def write_to_firebase(data, company):
    # Schema - Role, Category, URL
    print("Starting to write to firebase")
    roles = data["role"]
    categories = data["category"]
    urls = data["url"]
    unique_entries = set()

    for role, category, url in zip(roles, categories, urls):
        entry = (role, category, url)
        if entry not in unique_entries:
            unique_entries.add(entry)

            # Prepare data to be written
            doc_data = {
                "company": company,
                "title": role,
                "category": category,
                "url": url,
                "createdAt": datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            }

            # Write to Firestore
            db.collection(company).add(doc_data)

    print("Data written to Firebase successfully.")


