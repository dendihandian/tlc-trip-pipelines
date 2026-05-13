"""
docker-compose exec tlc_pipelines python pipelines/transformed/yellow_tripdata_detail/pipeline.py init
docker-compose exec tlc_pipelines python pipelines/transformed/yellow_tripdata_detail/pipeline.py incremental
docker-compose exec tlc_pipelines python pipelines/transformed/yellow_tripdata_detail/pipeline.py backfill --start-date 2026-03-01 --end-date 2026-03-01
"""

import sys
import os
sys.path.append(os.getcwd())

from pathlib import Path
PARENT_PATH = Path(__file__).parent

from utils.cli import Annotated, Argument, Option
from utils.cli import run, validate_parameter
from utils.cli import VALIDATION_ERROR_DATE, VALIDATION_ERROR_CASE
from utils.common import DATE_FORMAT
from utils.common import time_it, get_current_datetime, is_valid_date, sub_days, generate_dates_range
from utils.db import execute_query

DATABASE = 'datalake'
SCHEMA   = 'transformed'
TABLE    = 'yellow_tripdata_detail'

def process_by_date(date: str):
    print(f'processing {date}...')

    query = ''
    with open(f'{PARENT_PATH}/query.sql', 'r') as file:
        query = file.read()

    query = query.replace('{query_filter}', f"DATE(_date) = DATE('{date}')")
    execute_query(query, database=DATABASE)

@time_it
def backfill(start_date: str, end_date: str):
    dates_range = sorted(generate_dates_range(start_date, end_date), reverse=True)
    for date in dates_range:
        process_by_date(date)

@time_it
def incremental():
    start_date  = sub_days(get_current_datetime(), 60).strftime(DATE_FORMAT)
    end_date    = get_current_datetime().strftime(DATE_FORMAT)
    backfill(start_date, end_date)

@time_it
def init():
    query_ddl = ''
    with open(f'{PARENT_PATH}/ddl.sql', 'r') as file:
        query_ddl = file.read()

    execute_query(query_ddl, database=DATABASE)

    query_index = ''
    with open(f'{PARENT_PATH}/index.sql', 'r') as file:
        query_index = file.read()
    execute_query(query_index, database=DATABASE)

@time_it
def main(
    mode:       Annotated[str, Argument(help="ddl/incremental/backfill", callback=lambda mode: validate_parameter(mode, (lambda m: mode in m), VALIDATION_ERROR_CASE) if mode is not None else None)],
    start_date: Annotated[str, Option(help="start date", callback=lambda date: validate_parameter(date, is_valid_date, VALIDATION_ERROR_DATE) if date is not None else None)] = None,
    end_date:   Annotated[str, Option(help="end date", callback=lambda date: validate_parameter(date, is_valid_date, VALIDATION_ERROR_DATE) if date is not None else None)] = None,
):
    if mode == 'init':
        init()
    elif mode == 'incremental':
        incremental()
    elif mode == 'backfill':
        backfill(start_date, end_date)
    else:
        print('mode not recognized')

if __name__ == '__main__':
    run(main)