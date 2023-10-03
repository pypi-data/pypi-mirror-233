import apache_beam as beam
import pandas as pd
import logging
import threading
import json
import os

from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.bigquery.client import Client
from google.oauth2.service_account import Credentials
from google.cloud import storage

class PatientData(beam.DoFn):

  def setup(self):
      logging.info(f'PatientData setup: {threading.current_thread().name}')

      logging.info(f'Current directory: {os.getcwd()}')

      service_account_info = '''
              {
                "type": "service_account",
                "project_id": "cross-sample-entropy",
                "private_key_id": "1ee365442b9f454e38faf6054accbe289445c999",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC4+0rePXBNJ5OB\nw9LYUw0UN+tSozfBYWSLfxd00Fr8Y2dnO2Pa5MONvHGjmUyHtkiOMeZ900YaZ2xQ\nFl7FaEwgqRswkSTWsPLMa/RcIuFSbUmIR7YA9kptHWu8c3UiEtV95LPDAIqsAx+2\nX7BehWCdb0WLdqIJ7AL6Xn2Q2lA+2xWX6HaQzm5JEcw7tPA2yaR7XJxw3vvITT8S\nFGdMgtVBRxHuP87tjNqlGoWeKTrnHI2VIhmaZMrS3bP9czGIfqd4anOfFtjHNJv+\n6R6L/6qodURQUBnaK9dY8S3n6sGrlhCl9+rM4QF+9z6i5qnsGjQu3F94QXgEMros\necNCNCPhAgMBAAECggEAAoGlKg27D9CRdxioKrY1XyjCz4PWpZAkRJ+cOcD4+qJ+\nLC/p0nV3ENyUzZquJsiZgxO6A8pxELqGBS/IaPRY07h23dmZni8Xmx17WiQ+2VcR\nv/74wFqV95SGeS83TxbiPapzpRjEyD/ilh4FzcIQ5RE06Abbezbvc2UEXooWvENF\nyZZDVhA+JoZbfnaPPnyECI0wzkD9L2EwtXplWKJ8irAOZelZnK/c49HcTa7dg867\nFrL74DphJkZdwNxy9BBM0iYghHcQBjEicFBazbrIhERqFDFjaNsBlHT1yqeT2s/p\nUZSeyOuQbj8ZNmdpreJzq7XZe99HSkKaczJmuVaaAQKBgQDeYPK1rN7IugTEe4ud\nZgi3K80usg4eQJLb6u9j+JgvIUi3rsjN73caHv9O30wkuWGKWc/4+oQrRLc6FRo1\ngwyppwgqFUKGJX7beIk/HJRAUPIhC9l2pjt0+j9JTYXC85oSlWpZ9bB107zIjhL7\nxEBpHvG5O7vezPaWwsa/3AhCmQKBgQDU8ujNex7dQ/MUMuJ9LjpvTzUXa0V+3Yef\ngDIJX38RB5reSxGp6zWV8tzodnRhhCVrwaRpgBeT1ckQCk6o2LABuXiU5jPkuHBh\njHz0voeYvd/d5zYs7zTfELONExS0Oluqm4aKoXem0pJBwZ6ce/4+6EVneEQcO007\nHDFObdyAiQKBgQCo76eSorhAbyiOB3kh4tC+LnVagwO8sbuffBPOs50ROMzgVdTQ\ntZmaa2/zACn9QCO8kcwvzki4AiTb6AoYGu10uKK4LZxzAmsj2acSHej2D0hSGIlk\n3JYQoMeRLWZvmtYyRfYcT0x1xpwFFAGR6B4yfcKOwLVRZg3yrBeGy2YvCQKBgAnQ\n7LRUIZcXg8QBmHkmwWDSKONceYaglZjfou7VrRjO3e+zTCwmAIFaAZ7hnvnDyqnN\n8lM+qVeSOkN4Bio4WtypfQp4FhpL+jo07Kmngr6iuggTmWa23BwQPAabw4+PRRx3\nMNuBF+/jswQ+9Z3HBXBG6rQbUiBvB19bLFauL8TpAoGBANDjvw6bfnqW0Q9U8y2G\nDBmBDzsWPbl1QRTHf8O0lGFemJgnUJJcckwmN/yDIgBOVshMKbMbIQIBIB8wpkHI\nIn4A1+9+AjrGZaCubJZGt31ZKx7GeGY3OL8EdU7OrnorWHWC9LjmWh4uzgj+pbjK\nWZuN99HVwDaM4g6iZ/vL0v0x\n-----END PRIVATE KEY-----\n",
                "client_email": "data-science-vertex-ai@cross-sample-entropy.iam.gserviceaccount.com",
                "client_id": "108211620347938946278",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/data-science-vertex-ai%40cross-sample-entropy.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
              }
'''
      service_account_json = json.loads(service_account_info, strict=False)
      self.credentials: Credentials = service_account.Credentials.from_service_account_info(service_account_json)
      # self.credentials: Credentials = service_account.Credentials.from_service_account_file('config/sa.json', scopes=["https://www.googleapis.com/auth/cloud-platform"])

      # Initialize Bigquery client with the above obtained credentials
      self.bigquery_client: Client = bigquery.Client(credentials=self.credentials, project=self.credentials.project_id)

  def process(self, data):

    logging.info(f"\tExecuting query for patient {data[0]}. Thread: [{threading.current_thread().name}]")

    query: str = \
    f'''
        SELECT EMTEK_ID, OBR_DATE, HR, SPO2 FROM `cross-sample-entropy.emtek.patient`
        WHERE EMTEK_ID = {data[0]} AND HR IS NOT NULL AND SPO2 IS NOT NULL
        ORDER BY OBR_DATE
    '''   

    # Executes query against BigQuery
    df_patients: pd.DataFrame = self.bigquery_client.query(query).to_dataframe()

    yield (data[0], df_patients.to_json())


  def start_bundle(self):
    logging.info(f'PatientData start_bundle: {threading.current_thread().name}')

  def finish_bundle(self):
      logging.info(f'PatientData finish_bundle: {threading.current_thread().name}')

  def teardown(self):
     logging.info(f'PatientData tearing down: {threading.current_thread().name}')
     self.bigquery_client.close()
     return super().teardown()
  
