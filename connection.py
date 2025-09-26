import os

from PIL import Image
from PyPDF2 import PdfReader
from langchain_google_community import GoogleDriveLoader
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def read_txt_file(file_path):
    """Reads the clients folders list"""
    folder_ids = []
    with open(file_path, "r") as file:
        for line in file:
            # Strip whitespace and append folder ID
            folder_id = line.strip()
            folder_ids.append(folder_id)

    return folder_ids


def process_document(doc):
    """Process a document based on its type (e.g., image, PDF)"""
    print(doc)
    if doc.metadata["mimeType"].startswith("image/"):
        # Process image
        print(f"Processing image: {doc.metadata['name']}")
        # Example: Load image using PIL
        image = Image.open(doc.file_path)
        image.show()  # Display the image (or save/process as needed)

    elif doc.metadata["mimeType"] == "application/pdf":
        # Process PDF
        print(f"Processing PDF: {doc.metadata['name']}")
        reader = PdfReader(doc.file_path)
        for page in reader.pages:
            print(page.extract_text())  # Extract text from each page

    else:
        print(f"Unsupported file type: {doc.metadata['mimeType']}")


# Authenticate and get credentials
def authenticate_google():
    creds = None
    token_path = "./pages/token.json"
    credentials_path = "./pages/credentials.json"

    # Check if token already exists
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path)

    # If no valid token, authenticate using credentials.json
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.flies(
                credentials_path, ["https://www.googleapis.com/auth/drive"]
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return creds


# Read txt file for all the clients and update the dataset
if __name__ == "__main__":
    """This script reads the clients list and updates the database with the new documents"""

    # Authenticate Google API
    credentials = authenticate_google()

    # Path to the clients list file
    file_path = "./pages/folders_id.txt"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    folders = read_txt_file(file_path)

    print(folders)

    for folder in folders:
        # Load documents from Google Drive folder
        loader = GoogleDriveLoader(folder_id=folder, credentials=credentials)
        docs = loader.load()

        for doc in docs:
            print(docs)
            # process_document(doc)  # Process each document
