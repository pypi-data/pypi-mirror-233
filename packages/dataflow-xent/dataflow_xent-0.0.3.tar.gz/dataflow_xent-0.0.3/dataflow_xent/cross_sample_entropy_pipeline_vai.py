import argparse
import logging
import sys
import threading
import os
import json
import pandas as pd
import numpy as np

import apache_beam as beam
from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.bigquery.client import Client
from google.oauth2.service_account import Credentials

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io import ReadFromBigQuery, WriteToText
from sklearn.preprocessing import StandardScaler

import EntropyHub as EH

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
  
class FilterRows(beam.DoFn):
  
  def setup(self):
      logging.info(f'FilterRows setup: {threading.current_thread().name}')

  def process(self, data):

    logging.info(f"\tFiltering rows for patient {data[0]}. Thread: [{threading.current_thread().name}]")

    df = pd.read_json(data[1])

    # Sort the DataFrame based on 'OBR_DATE'
    df.sort_values(by='OBR_DATE', inplace=True)
    
    # Drop NaN values
    df.dropna(inplace=True)
    
    # Drop duplicate rows based on 'OBR_DATE'
    df.drop_duplicates(subset='OBR_DATE', keep='first', inplace=True)
    
    # Conver DataFrame to NumPy array
    arr = df[['HR', 'SPO2']].to_numpy()
    
    # Standardize the data
    normalize = StandardScaler()
    normalized_arr = normalize.fit_transform(arr)
    
    # Convert the NumPy array back to DataFrame
    normalized_df = pd.DataFrame(normalized_arr, columns=['HR', 'SPO2'])
  
    yield (data[0], normalized_df.to_json())

  def start_bundle(self):
    logging.info(f'FilterRows start_bundle: {threading.current_thread().name}')

  def finish_bundle(self):
      logging.info(f'FilterRows finish_bundle: {threading.current_thread().name}')

class ComputeEntropy(beam.DoFn):

  def setup(self):
      logging.info(f'ComputeEntropy setup: {threading.current_thread().name}')

  def process(self, data):

    arr = pd.read_json(data[1]).to_numpy()
    logging.info(f"\tComputing entropy for patient {data[0]}. Thread: [{threading.current_thread().name}]")
    # windowing
    # Parameters
    hours_of_data = 2
    overlap = 0.5
    m = 2
    r = 0.2
    window_size = hours_of_data * 120
    step_size = int(window_size * (1 - overlap))
    Logx = np.exp(1)
    tau = 1
    xsamp_values = []
    for index in range(0, arr.shape[0] - window_size + 1, step_size):
        window = arr[index:index+window_size]
        if len(window) == window_size:
            xsamp_en, _, _ = EH.XSampEn(window, m=m, tau=tau, r=r, Logx=Logx)
            xsamp_values.append({'index': index, 'xsamp_en': xsamp_en[-1]})
    yield (data[0], xsamp_values)


  def start_bundle(self):
    logging.info(f'ComputeEntropy start_bundle: {threading.current_thread().name}')

  def finish_bundle(self):
      logging.info(f'ComputeEntropy finish_bundle: {threading.current_thread().name}')

def run(argv=None, save_main_session=True):
  """
  Main entry point; defines and runs the cross sample entropy pipeline.
  """
  parser = argparse.ArgumentParser()

  # Adding input and output parameters to the parser
  parser.add_argument(
    '--input',
    dest='input',
    required=False,
    default='',
    help='The query to be executed'
    )
  
  parser.add_argument(
    '--output',
    dest='output',
    required=True,
    help='Output directory to write results to.')
  
  known_args, pipeline_args = parser.parse_known_args(argv)

  # We use the save_main_session option because one or more DoFn's in this
  # workflow rely on global context (e.g., a module imported at module level).
  pipeline_options = PipelineOptions(pipeline_args)
  pipeline_options.view_as(SetupOptions).save_main_session = save_main_session


  # The pipeline will be run on exiting the with block.
  with beam.Pipeline(options=pipeline_options) as p:

    query: str = \
    '''
       WITH patients AS (
                SELECT EMTEK_ID, TOTAL
                FROM (
                    SELECT EMTEK_ID, COUNT(EMTEK_ID) AS TOTAL
                    FROM `cross-sample-entropy.emtek.patient`
                    WHERE EMTEK_ID IS NOT NULL AND HR IS NOT NULL AND SPO2 IS NOT NULL
                    GROUP BY EMTEK_ID
                )
                WHERE TOTAL > 24*120
            )
            SELECT patients.EMTEK_ID FROM patients        

            ORDER BY EMTEK_ID
            LIMIT 10
    '''

    collection_emteks =  ( p 
                         | 'QueryForPatientEmtek' >> ReadFromBigQuery(query=query, use_standard_sql=True) 
                         | 'get emteks' >> beam.Map(lambda element: (element['EMTEK_ID'], None)) | 'group by key' >> beam.GroupByKey())

    # Computes the entropies in sub transformations
    x_entropies = ( collection_emteks | "get patient data" >> beam.ParDo(PatientData()) | 'filter vital signs' >> beam.ParDo(FilterRows()) | 'compute entropy' >> beam.ParDo(ComputeEntropy()) | beam.Map(lambda x: {'emtek_id': x[0], 'entropies': x[1]}))

    # Saves the output
    x_entropies | 'Write' >> WriteToText(file_path_prefix=known_args.output)
    

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run(argv=sys.argv)