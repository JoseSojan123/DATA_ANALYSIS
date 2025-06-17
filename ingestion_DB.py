import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time


logging.basicConfig(
   filename="logs/ingestion_db.log",
   level = logging.DEBUG,
   format = "%(asctime)s - %(levelname)s - %(message)s",
   filemode = "a"
)

engine = create_engine('sqlite:///inventory.db')



def ingest_db(df ,table_name ,engine):
    ''' This function will take a dataframe and a table name and ingest the dataframe into the database '''
    df.to_sql(table_name , con = engine , if_exists = 'replace' , index = False)


def load_raw_data():
  ''' This function will load the csvs as dataframes and ingest them into the database '''
  start = time.time()
  for file in os.listdir('data'):
    if '.csv' in file:
      df = pd.read_csv('data/' + file)
      logging.info(f'Ingesting {file} into the database')
      
      ingest_db(df , file[:-4], engine)

  end = time.time()
  total_time = (end - start)/60
  logging.info('All files ingested successfully!')
  logging.info(f'Total time taken to ingest all files: {total_time} minutes')


if __name__ == "__main__":
   load_raw_data()