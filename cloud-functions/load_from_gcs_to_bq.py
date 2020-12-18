from google.cloud import storage
from google.cloud import bigquery
import os
import sys
import logging
from flask import abort

BQ_TABLE_IDS = os.environ['BQ_TABLE_IDS']
GCS_FILE_PREFIX = os.environ['GCS_FILE_PREFIX']

# Construct a BigQuery client object.
client = bigquery.Client()

def exit_abort():
    return abort(500)

def load_file(event, context):

    bq_table_ids = BQ_TABLE_IDS.split(',')
    gcs_file_prefix = GCS_FILE_PREFIX.split(',')

    if len(bq_table_ids) != len(gcs_file_prefix):
        error_msg = 'BQ_TABLE_IDS has different size ({}) than GCS_FILE_PREFIX ({})\n'.format(
            len(bq_table_ids), len(gcs_file_prefix))
        sys.stderr.write(error_msg)
        logging.error(RuntimeError(error_msg))
        exit_abort()

    bucket_name = event['bucket']
    object_name_src = event['name']

    i = 0
    for file_prefix in gcs_file_prefix:
        if file_prefix in object_name_src:
            print(object_name_src + " -- " + file_prefix + " -- " + bq_table_ids[i])
            import_to_bq(bucket_name, object_name_src, bq_table_ids[i])
            break
        i += 1


def import_to_bq(bucket_name, object_name_src, table_id):

    job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.ORC)

    destination_table = client.get_table(table_id)

    row_num_before_load = destination_table.num_rows

    # uri is like "gs://cloud-samples-data/bigquery/us-states/us-states.orc"
    uri = "gs://" + bucket_name + "/" + object_name_src

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)
    row_num_after_load = destination_table.num_rows
    print("Loaded {} rows.".format(row_num_after_load-row_num_before_load))
