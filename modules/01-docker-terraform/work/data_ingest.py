#IMPORT
import os
import argparse
import pandas as pd
from sqlalchemy import create_engine

#FUNCTIONS
##MAIN
def main(params):
    ###SET VARIABLES
    user = params.user
    pasw = params.pasw
    host = params.host
    port = params.port
    db = params.db
    tble = params.tble
    url = params.url

    csv_file = 'yellow_tripdata_2021-01.csv'

    os.system(f"wget {url} -O {csv_file}.gz && gunzip {csv_file}.gz")

    ###SET ENGINE
    engine = create_engine(f'postgresql://{user}:{pasw}@{host}:{port}/{db}')

    ###EXTRACT DATA
    df_iter = pd.read_csv(csv_file, iterator=True, chunksize=100000)
    df = next(df_iter)

    ###PREPARE LOOP
    df.head(n=0).to_sql(tble, con=engine, if_exists='replace')

    ###LOAD DATA
    i = 0
    while True:
        i += 1
        try:
            df = next(df_iter)
            
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.to_sql(name=tble, con=engine, if_exists='append')
            print(f'Inserted chunk {i}')
        except StopIteration:
            print(f'All {i} chunks inserted : )')
            break

#RUN
if __name__ == '__main__':
    ##ARGPARSE
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='username for Postgres')
    parser.add_argument('--pasw', help='password for Postgres')
    parser.add_argument('--host', help='host for Postgres')
    parser.add_argument('--port', help='port for Postgres')
    parser.add_argument('--db', help='database name for Postgres')
    parser.add_argument('--tble', help='destination table name')
    parser.add_argument('--url', help='url to CSV data file')

    args = parser.parse_args()
    
    ##MAIN
    main(args)