import apache_beam as beam
import pandas as pd
import logging
import threading
import io
from sklearn.preprocessing import StandardScaler


class FilterRows(beam.DoFn):
  
  def setup(self):
      logging.info(f'FilterRows setup: {threading.current_thread().name}')

  def process(self, data):

    logging.info(f"\tFiltering rows for patient {data[0]}. Thread: [{threading.current_thread().name}]")

    df = pd.read_json(io.StringIO(data[1]))

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