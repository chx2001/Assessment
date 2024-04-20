import os
import uvicorn
from fastapi import (FastAPI, File, UploadFile, HTTPException)
import config
from ingest import DocumentIndexer  
from response import OutputRetriever

os.environ["OPENAI_API_KEY"] = config.API_KEY

app = FastAPI()
document_indexer = DocumentIndexer()
output_retrieve = OutputRetriever()

# ingest
@app.post("/ingest")
async def upload_file(files: UploadFile = File(...)):
    try:
        content_length = document_indexer.get_content_length(files.file)

        # file size limit
        if content_length / (1024 * 1024) > config.MAX_FILE_SIZE_MB:
            raise HTTPException(status_code=400, detail=f"File size exceeds the maximum limit of {config.MAX_FILE_SIZE_MB} MB")

        # check file type
        if not document_indexer.is_valid_file(files.filename):
            raise HTTPException(status_code=400, detail="Only text files (.txt) are allowed.")

        # save file, create and store index
        file_path = document_indexer.save_file(files)
        persist_dir = document_indexer.create_and_store_index()

        # let user know the execution was successful
        return {"message": "Document successfully uploaded", "file store": file_path, "index store": persist_dir}
    
    except HTTPException as e:
        # debug purpose
        print(str(e))
        # return execution fail error
        return {"Error Code": e.status_code, "detail": "Execution request fail. Please try again"}
    
    except Exception as e:
        print(str(e))
        error_message = str(e)
        if "exceeded your current quota" in error_message:
            return {"Error Code": 429, "detail": "OpenAI: Rate limit exceeded. Please try again later."}
        else:
            return {"Error Code": 500, "detail": "Internal server error. Please contact customer service."}

# query 
@app.get("/query")
async def query(prompt: str):
    try:
        output = output_retrieve.perform_query(prompt)
        return {"message": output}

    except HTTPException as e:
        print(str(e))
        return {"Error Code": e.status_code, "detail": "Execution request fail. Please try again"}

    except Exception as e:
        print(str(e))
        error_message = str(e)
        if "exceeded your current quota" in error_message:
            return {"Error Code": 429, "detail": "OpenAI: Rate limit exceeded. Please try again later."}
        else:
            return {"Error Code": 500, "detail": "Internal server error. Please contact customer service."}



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
