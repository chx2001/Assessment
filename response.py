from llama_index.core import (StorageContext, load_index_from_storage)
import config

class OutputRetriever:
    def __init__(self):
        self.persist_dir = config.PERSIST_DIR

    # query indexed documents
    def perform_query(self, query_string: str):
        # load the index from storage
        storage_context = StorageContext.from_defaults(persist_dir=self.persist_dir)
        index = load_index_from_storage(storage_context)

        # query
        query_engine = index.as_query_engine()
        response = query_engine.query(query_string)

        return response
