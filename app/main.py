from fastapi import FastAPI, UploadFile, Header
from fastapi.responses import JSONResponse
from .schema import statusSchema, exceptionSchema, uploadSchema, downloadSchema
from typing import List, Optional
import pymongo, os, logging, datetime
import pandas as pd

# logging setup
if not os.path.exists('./logs'):
    os.makedirs('./logs')
logging.basicConfig(filename=f'./logs/{str(datetime.date.today())}.log', format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.info("---------- STARTING API ----------")


# start of API code
app = FastAPI()

mClient = pymongo.MongoClient(os.environ.get("MONGO_CONNECTION_STRING"))
mDatabase = mClient['cluster0']
mCollection = mDatabase['data_api']


# root endpoint
@app.get('/', response_model=statusSchema)
async def root():
    """
    The `/` endpoint, also known as the root endpoint, is used for checking if an instance of the API is alive. If calling this endpoint does not return the below JSON snippet, then the API instance did not properly initialize.
    """

    return JSONResponse(content={"status": "ok", "version": "v0.1.0"}, status_code=200)


# upload endpoint
@app.post("/upload", responses={201: {'model': uploadSchema}, 500: {'model': exceptionSchema}}, status_code=201)
def upload(file: UploadFile):
    """
    The `/upload` endpoint should be called when attempting to upload a file to the API for processing/storage within the Mongo database.
    """

    try:
        fileDF = pd.read_csv(file.file)
        mongoDict = fileDF.to_dict('records')

        for item in mongoDict: # probably a better way to do this, I just couldn't figure one out with pandas
            item['metadata'] = {'filename': file.filename}

        mCollection.insert_many(mongoDict)

        return JSONResponse(content={'message': f'Success uploading {file.filename} to Mongo'}, status_code=201)

    except Exception as e:
        logger.error('Error uploading or processing file.', exc_info=e)

        return JSONResponse(content={'message': 'Error uploading or processing file.'}, status_code = 500)


# download endpoint
@app.get("/download", responses={200: {'model': downloadSchema}, 500: {'model': exceptionSchema}})
def download(filename: Optional[str] = Header(None)):
    """
    The `/download` endpoint should be called when a user wants to pull a specific dataset from the Mongo database. (It is planned to add future support for multiple filetypes, however, at the moment this endpoint will only return CSV data.)
    """

    try:
        df = pd.DataFrame(list(mCollection.find({'metadata.filename': filename}, {'_id': 0, 'metadata': 0})))

        return JSONResponse(content={'data': df.to_csv(index=False), 'format': 'csv'})
    
    except Exception as e:
        logger.error('Error processing file for download.', exc_info=e)

        return JSONResponse(content={'message': 'Error processing file for download.'}, status_code=500)