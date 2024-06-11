import firebase_admin
from firebase_admin import credentials, firestore

def write_to_firebase(data, company):
    cred = credentials.Certificate("jobify/secrets/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

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
                "Role": role,
                "Category": category,
                "Url": url
            }

            # Write to Firestore
            db.collection('jobify').document(
                company).collection('jobs').add(doc_data)

    print("Data written to Firebase successfully.")


