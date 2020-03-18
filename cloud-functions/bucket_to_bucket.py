from google.cloud import storage
from google.cloud.exceptions import NotFound
import os

BUCKET_DEST = os.environ['BUCKET_DEST']

storage_client = storage.Client()

def copy_object(event, context):

    bucket_name = event['bucket']
    object_name_src = event['name']
    object_name_dest = object_name_src

    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(object_name_src)
    destination_bucket = storage_client.bucket(BUCKET_DEST)

    blob_copy = source_bucket.copy_blob(
        source_blob, destination_bucket, object_name_dest
    )

    print(
        "Blob {} in bucket {} copied to blob {} in bucket {}.".format(
            source_blob.name,
            source_bucket.name,
            blob_copy.name,
            destination_bucket.name,
        )
    )

def delete_object(event, context):
    bucket_name = event['bucket']
    object_name_src = event['name']

    destination_bucket = storage_client.bucket(BUCKET_DEST)

    try:
        destination_bucket.delete_blob(object_name_src)
    except NotFound:
        print("Sync deletion of object {} from bucket {} to bucket {} Not Found".format(
                object_name_src,
                bucket_name,
                destination_bucket.name,
            )
        )