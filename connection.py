import os.path
from PyPDF2 import PdfReader
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def process_file_in_memory(service, file_id, file_name):
    """Downloads a file from Google Drive and processes it in memory."""
    request = service.files().get_media(fileId=file_id)
    file_stream = io.BytesIO()  # Create an in-memory file-like object
    downloader = MediaIoBaseDownload(file_stream, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Downloading {file_name}: {int(status.progress() * 100)}% complete.")

    # Reset the stream position to the beginning
    file_stream.seek(0)

    # Process the file based on its type
    if file_name.endswith(".pdf"):
        print(f"Processing PDF file: {file_name}")

        reader = PdfReader(file_stream)
        for page in reader.pages:
            print(page.extract_text())  # Extract and print text from each page
    elif file_name.lower().endswith((".jpg", ".jpeg", ".png")):
        print(f"Processing image file: {file_name}")
        # Example: Use PIL to process the image
        from PIL import Image

        image = Image.open(file_stream)
        image.show()  # Display the image (or process it as needed)
    else:
        print(f"Unsupported file type: {file_name}")


def load_folders(file_path):
    """Reads folder IDs from a text file."""
    folder_ids = []
    with open(file_path, "r") as file:
        for line in file:
            folder_id = line.strip()
            folder_ids.append(folder_id)
    return folder_ids


if __name__ == "__main__":
    # Load folder IDs from folders_id.txt
    file_path = "pages/folders_id.txt"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    folder_ids = load_folders(file_path)
    print("Loaded folder IDs:", folder_ids)

    # Authenticate Google API
    creds = None
    if os.path.exists("pages/credential_admin/token.json"):
        creds = Credentials.from_authorized_user_file(
            "pages/credential_admin/token.json", SCOPES
        )
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "pages/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("pages/token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        for folder_id in folder_ids:
            print(f"Listing files in folder: {folder_id}")
            results = (
                service.files()
                .list(q=f"'{folder_id}' in parents", fields="files(id, name)")
                .execute()
            )
            items = results.get("files", [])
            if not items:
                print(f"No files found in folder {folder_id}.")
            else:
                print("Files:")
                for item in items:
                    print(f"{item['name']} ({item['id']})")
                    process_file_in_memory(service, item["id"], item["name"])
    except HttpError as error:
        print(f"An error occurred: {error}")
