import firebase_admin
from datetime import datetime
from firebase_admin import credentials, firestore
from jobify.config import COMPANIES
from jobify.secrets.serviceAccountKey import SERVICE_ACCOUNT_JSON

cred = credentials.Certificate(SERVICE_ACCOUNT_JSON)
firebase_admin.initialize_app(cred)
db = firestore.client()

def write_companies():
    print("Starting to write companies to Firebase")
    
    existing_companies = set() 
    
    # Fetch existing companies from Firestore
    existing_docs = db.collection("companies").get()
    for doc in existing_docs:
        existing_companies.add(doc.id) 
    
    companies_to_write = []
    
    for i, company in enumerate(COMPANIES, start=1):
        if company not in existing_companies:
            companies_to_write.append((str(i), company))
        else:
            print(f"Company '{company}' already exists in Firestore, skipping.")
    
    # Write new companies to Firestore
    if companies_to_write:
        batch = db.batch()
        for idx, data in companies_to_write:
            new_doc_ref = db.collection("companies").document(idx)
            batch.set(new_doc_ref, {"name": data}) 
        
        batch.commit()
        print(f"{len(companies_to_write)} companies successfully written to Firestore.")
    else:
        print("All companies were already present in Firestore, nothing new to write.")


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

            existing_docs = db.collection(company).where("url", "==", url).stream()
            if any(existing_docs):
                print(f"URL {url} already exists in Firestore, skipping.")
                continue

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


