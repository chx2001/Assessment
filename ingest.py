import os
from llama_index.core import (
    VectorStoreIndex, 
    SimpleDirectoryReader, 
    StorageContext,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from fastapi import HTTPException
from fastapi import UploadFile
import config

class DocumentIndexer:
    def __init__(self):
        self.documents_directory = config.DOCUMENTS_DIRECTORY
        self.persist_dir = config.PERSIST_DIR

    # check if the file extension is valid
    def is_valid_file(self, filename: str) -> bool:
        valid_extensions = {'.txt'}
        return os.path.splitext(filename)[1].lower() in valid_extensions

    # save the uploaded file to disk
    def save_file(self, files: UploadFile) -> str:
        file_path = os.path.join(self.documents_directory, files.filename)
        with open(file_path, "wb") as f:
            content = files.file.read()
            f.write(content)
        return file_path

    # create and store index
    def create_and_store_index(self) -> str:
        documents = SimpleDirectoryReader(self.documents_directory).load_data()
        index = VectorStoreIndex.from_documents(documents, show_progress=True)
        index.storage_context.persist(persist_dir=self.persist_dir)
        return self.persist_dir

    # function to get content length of an async file
    def get_content_length(self, file):
        length = 0
        for chunk in file:
            length += len(chunk)
        return length