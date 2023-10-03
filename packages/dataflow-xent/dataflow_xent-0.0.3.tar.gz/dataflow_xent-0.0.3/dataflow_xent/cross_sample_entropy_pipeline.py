import argparse
import logging
import sys

import apache_beam as beam

from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io import ReadFromBigQuery, WriteToText

from dataflow_xent.patient_data import PatientData
from dataflow_xent.compute_entropy import ComputeEntropy
from dataflow_xent.filter_row import FilterRows

def run(argv=None, save_main_session=True):
  """
  Main entry point; defines and runs the cross sample entropy pipeline.
  """
  logging.info(sys.builtin_module_names)
  logging.info('====================================================================================================')
  logging.info(f'Arguments: {argv}')
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
  
  parser.add_argument(
    '--setup_file',
    dest='setup_file',
    required=False,
    help='Setup file to build the pipeline components with multiple Python files')
  
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