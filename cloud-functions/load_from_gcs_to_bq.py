from google.cloud import storage
from google.cloud import bigquery
import os

BQ_TABLE_ID = os.environ['BQ_TABLE_ID']

# Construct a BigQuery client object.
client = bigquery.Client()


def load_file(event, context):

    bucket_name = event['bucket']
    object_name_src = event['name']
    object_name_dest = object_name_src

    job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.ORC)

    table_id = BQ_TABLE_ID
    destination_table = client.get_table(table_id)

    row_num_before_load = destination_table.num_rows

    # uri = "gs://cloud-samples-data/bigquery/us-states/us-states.orc"
    uri = "gs://" + bucket_name + "/" + object_name_src

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Make an API request.

    load_job.result()  # Waits for the job to complete.

    destination_table = client.get_table(table_id)
    row_num_after_load = destination_table.num_rows
    print("Loaded {} rows.".format(row_num_after_load-row_num_before_load))
