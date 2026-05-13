"""
docker-compose exec tlc_pipelines python pipelines/master/taxi_zone_lookup/pipeline.py incremental
"""

import sys
import os
sys.path.append(os.getcwd())

from utils.cli import Annotated, Argument
from utils.common import time_it, get_current_datetime
from utils.dataframe import read_csv_from_url
from utils.db import save_to_postgresql
from utils.cli import run

DATABASE = 'datalake'
SCHEMA   = 'master'
TABLE    = 'taxi_zone_lookup'

@time_it
def preprocess_data(df):
    print('casting all columns to string ...')
    df = df.astype(str)

    print('generating _ingested_at ...')
    df['_ingested_at'] = str(get_current_datetime())

    return df

@time_it
def incremental():
    url_parquet = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv'
    df = read_csv_from_url(url_parquet)

    if df is not None:
        df = preprocess_data(df)
        save_to_postgresql(df, DATABASE, SCHEMA, TABLE)
    else:
        print(f'data is not available for {url_parquet}')

@time_it
def main(
    mode: Annotated[str, Argument(help="incremental or backfill")],
):
    if mode == 'incremental':
        incremental()

if __name__ == '__main__':
    run(main)