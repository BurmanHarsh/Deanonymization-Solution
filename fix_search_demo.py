import os
import gzip
import requests
from hashlib import sha256

# Configuration
AIL_HOME = os.getcwd()
PASTES_DIR = os.path.join(AIL_HOME, 'PASTES')
M_URL = 'http://127.0.0.1:7700'
M_KEY = 'ailmeilisearchpassword'

def setup_demo():
    item_id = 'sample_item_debug'
    content = "This is a debug sample containing a credit card 4111111111111111 and keyword debug"
    
    # 1. Create the file on disk (what Item.get_filename() expects)
    if not os.path.exists(PASTES_DIR):
        os.makedirs(PASTES_DIR)
    
    file_path = os.path.join(PASTES_DIR, item_id + '.gz')
    with gzip.open(file_path, 'wb') as f:
        f.write(content.encode('utf-8'))
    print(f"Created file: {file_path}")

    # 2. Inject into Meilisearch
    # The search engine uses 'uuid' as primary key and 'content' for searching
    # The uuid is typically uuid5(NAMESPACE_URL, global_id)
    import uuid
    global_id = f"item:{item_id}"
    doc_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, global_id))
    
    doc = {
        "uuid": doc_uuid,
        "id": global_id,
        "content": content,
        "last": 1600000000
    }
    
    r = requests.post(f"{M_URL}/indexes/onion/documents", 
                     json=[doc], 
                     headers={"Authorization": f"Bearer {M_KEY}"})
    
    if r.status_code == 200 or r.status_code == 201:
        print("Successfully injected into Meilisearch")
    else:
        print(f"Meilisearch error: {r.text}")

if __name__ == "__main__":
    setup_demo()
