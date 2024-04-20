from decouple import config

API_KEY = config("API_KEY")
DOCUMENTS_DIRECTORY = "./uploaded_documents"
PERSIST_DIR = "./storage"
MAX_FILE_SIZE_MB = 100