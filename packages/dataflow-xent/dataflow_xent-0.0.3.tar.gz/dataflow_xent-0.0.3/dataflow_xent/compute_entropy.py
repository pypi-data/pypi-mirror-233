import apache_beam as beam
import pandas as pd
import numpy as np
import logging
import threading
import io

from google.cloud import bigquery
from google.oauth2 import service_account
from google.cloud.bigquery.client import Client
from google.oauth2.service_account import Credentials

from dataflow_xent.xent.xsampent import XSampEn

class ComputeEntropy(beam.DoFn):

  def setup(self):
      logging.info(f'ComputeEntropy setup: {threading.current_thread().name}')

  def process(self, data):

    arr = pd.read_json(io.StringIO(data[1])).to_numpy()
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
            xsamp_en, _, _ = XSampEn(window, m=m, tau=tau, r=r, Logx=Logx)
            xsamp_values.append({'index': index, 'xsamp_en': xsamp_en[-1]})
    yield (data[0], xsamp_values)


  def start_bundle(self):
    logging.info(f'ComputeEntropy start_bundle: {threading.current_thread().name}')

  def finish_bundle(self):
      logging.info(f'ComputeEntropy finish_bundle: {threading.current_thread().name}')