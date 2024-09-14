from fastapi import FastAPI, UploadFile, Request, status
from fastapi.responses import Response, FileResponse
import pymongo, os, logging, datetime
import pandas as pd

# logging setup
if not os.path.exists('./logs'):
    os.makedirs('./logs')
logging.basicConfig(filename=f'./logs/{str(datetime.date.today())}.log', format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.info("---------- STARTING API ----------")

app = FastAPI()

mClient = pymongo.MongoClient(os.environ.get("MONGO_CONNECTION_STRING"))
mDatabase = mClient['cluster0']
mCollection = mDatabase['data_api']

@app.get('/')
async def root():
    return {"Status": "Ok"}


@app.post("/upload")
def upload(response: Response, file: UploadFile):
    try:
        fileDF = pd.read_csv(file.file)
        mongoDict = fileDF.to_dict('records')

        for item in mongoDict: # probably a better way to do this, I just couldn't figure one out with pandas
            item['metadata'] = {'filename': file.filename}

        mCollection.insert_many(mongoDict)

        response.status_code = 201
        return {'message': f'Success uploading {file.filename} to Mongo'}

    except Exception as e:
        logger.error('Error uploading or processing file.', exc_info=e)

        response.status_code = 500
        return {'message': 'Error uploading or processing file.'}

# download endpoint
@app.get("/download")
def download(response: Response, request: Request):
    try:
        if not 'filename' in request.headers:
            return {'message': 'Request missing `filename` in headers.'}

        query = {'metadata.filename': request.headers['filename']}
        df = pd.DataFrame(list(mCollection.find(query)))

        # The given media_type will force browsers to automatically download the file with the filename defined in the headers, however this is not
        # the case for any "code based" solutions. If you want to see how to download files from this API directly, please reference `examples/example_download.py`
        return Response(content=df.to_csv().encode('utf-8'), media_type='application/octet-stream', headers={'filename': request.headers['filename']}) 
    
    except Exception as e:
        logger.error('Error processing file for download.', exc_info=e)

        response.status_code = 500
        return {'message': 'Error processing file for download.'}