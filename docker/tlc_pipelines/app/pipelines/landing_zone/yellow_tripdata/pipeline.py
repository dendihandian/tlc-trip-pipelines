"""
docker-compose exec tlc_pipelines python pipelines/landing_zone/yellow_tripdata/pipeline.py incremental
docker-compose exec tlc_pipelines python pipelines/landing_zone/yellow_tripdata/pipeline.py backfill --start-date 2025-01-01 --end-date 2025-12-31
"""

import sys
import os
sys.path.append(os.getcwd())

from utils.cli import Annotated, Argument, Option, BadParameter
from utils.cli import run, validate_parameter
from utils.cli import VALIDATION_ERROR_DATE
from utils.common import DATE_FORMAT
from utils.common import time_it, get_current_datetime, is_valid_date, sub_days, generate_months_range
from utils.dataframe import read_parquet_from_url, generate_md5, split_dataframe
from utils.db import save_to_postgresql

DATABASE = 'landing_zone'
TABLE    = 'yellow_tripdata'

@time_it
def preprocess_data(df):
    print('casting all columns to string ...')
    df = df.astype(str)

    print('generating _md5 ...')
    df = generate_md5(df)

    print('generating _ingested_at ...')
    df['_ingested_at'] = str(get_current_datetime())

    return df

@time_it
def process_by_month(month: str):
    y = str(month).split('-')[0]
    m = str(month).split('-')[1]

    url_parquet = f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{y}-{m}.parquet"
    print(f'getting data from {url_parquet} ...')
    df = read_parquet_from_url(url_parquet)

    if df is not None:
        chunks = split_dataframe(df)
        for i, chunk in enumerate(chunks):
            print(f"🚀 Memproses chunk ke-{i+1} dari {len(chunks)} dengan {len(chunk)} baris...")
            if chunk 
            chunk = preprocess_data(chunk)
            save_to_postgresql(chunk, DATABASE, TABLE)

    else:
        print(f'data is not available for {url_parquet}')

@time_it
def backfill(start_date: str, end_date: str):
    months_range = sorted(generate_months_range(start_date, end_date), reverse=True)
    for month in months_range:
        process_by_month(month)

@time_it
def incremental():
    start_date  = sub_days(get_current_datetime(), 60).strftime(DATE_FORMAT)
    end_date    = get_current_datetime().strftime(DATE_FORMAT)
    backfill(start_date, end_date)

@time_it
def main(
    mode:       Annotated[str, Argument(help="incremental or backfill")],
    start_date: Annotated[str, Option(help="start date", callback=lambda date: validate_parameter(date, is_valid_date, VALIDATION_ERROR_DATE) if date is not None else None)] = None,
    end_date:   Annotated[str, Option(help="end date", callback=lambda date: validate_parameter(date, is_valid_date, VALIDATION_ERROR_DATE) if date is not None else None)] = None,
):
    if mode == 'incremental':
        incremental()
    elif mode == 'backfill':
        backfill(start_date, end_date)

if __name__ == '__main__':
    run(main)