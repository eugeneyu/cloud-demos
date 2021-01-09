from google.auth import compute_engine
import google.auth.transport.requests
import os
import requests
import logging
from flask import abort

PROJECT_ID = os.environ['PROJECT_ID']
PROJECT_LOCATION = os.environ['PROJECT_LOCATION']
DEST_LOCATION = os.environ['DEST_LOCATION']
TEMPLATE_ID = os.environ['TEMPLATE_ID']

def exit_abort():
    return abort(500)

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

def start_transcode(event, context):

    bucket_name_input = event['bucket']
    object_name_input = event['name']
    file_name = os.path.split(object_name_input)[1]
    file_name_wo_extension = os.path.splitext(file_name)[0]

    cred = compute_engine.credentials.Credentials()

    auth_req = google.auth.transport.requests.Request()
    cred.refresh(auth_req)
    #print(cred.token)

    api_url = "https://transcoder.googleapis.com/v1beta1/projects/{}/locations/{}/jobs".format(PROJECT_ID, PROJECT_LOCATION)

    headers = {
        "Authorization": "Bearer {}".format(cred.token),
        "Content-Type": "application/json"
    }

    test = "gs://{}/{}".format(bucket_name_input, object_name_input)
    print("Bucket: {}, inputUri: {}\n".format(bucket_name_input, test))

    data = {
        "inputUri": "gs://{}/{}".format(bucket_name_input, object_name_input),
        "outputUri": "{}/{}/".format(DEST_LOCATION, file_name_wo_extension),
        "templateId": "{}".format(TEMPLATE_ID)
    }

    req = requests.Request('POST',api_url,headers=headers,json=data)
    prepared = req.prepare()
    pretty_print_POST(prepared)

    response = requests.post(url = api_url, headers=headers, json = data)

    if not response.ok or "error" in response.text:
        logging.error(RuntimeError(response.text))
        exit_abort()

    response_json = response.json()
    print("New job started - Job Name: {}".format(response_json['name']))




