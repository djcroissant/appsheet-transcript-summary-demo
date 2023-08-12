import base64
import logging
import pprint
import io
import datetime

import google.auth

# import google.auth.transport.requests
from google.auth.transport.requests import AuthorizedSession
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build

creds, project = google.auth.default(
    scopes=[
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/drive.readonly",
    ]
)

def getDocSummary(doc_string):
    authed_session = AuthorizedSession(creds)

    a = datetime.datetime.now()
    prompt = "Summarize the following conversation. " + doc_string
    response = authed_session.post(
        url = "https://us-central1-aiplatform.googleapis.com/v1/projects/{project}/locations/us-central1/publishers/google/models/text-bison:predict".format(
            project=project
        ),
        json={
            "instances": [
                { "prompt": prompt}
            ],
            "parameters": {
                "temperature": 0.2,
                "maxOutputTokens": 256,
                "topK": 40,
                "topP": 0.95
            }
        },
    )
    b = datetime.datetime.now()
    c = b - a
    logging.error(
        "{s} ms to summarize with GenAI text-bison service.".format(
            s=c.total_seconds() * 1000
        )
    )

    return response.content.predictions[0].content


#def getDocFromDrive(name):
def getDocFromDrive(name):
    # name = "Transcript test1"
    service = build("drive", "v3", credentials=creds)
    page_token = None

    response = (
        service.files()
        .list(
            q="name='" + name + "'",
            spaces="drive",
            fields="nextPageToken, files(id, name, thumbnailLink)",
            pageToken=page_token,
        )
        .execute()
    )

    files = response.get("files", [])

    if len(files) > 0:
        for file in response.get("files", []):
            # Process change
            print("Found file: " + file.get("name") + " and id: " + file.get("id"))
            request = service.files().get_media(fileId=file.get("id"))
            # fh = io.BytesIO()
            fh = io.FileIO("doc.txt", "wb")
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download " + str(int(status.progress() * 100)))

            # output["formThumbnail"] = file["thumbnailLink"]
            break

        with open("doc.txt", "rb") as docFile:
            doc_string = docFile.read().decode("utf-8")
            print("doc string: " + doc_string)
    else:
        doc_string = "error"

    return doc_string
