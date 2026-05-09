"""
docker-compose exec pipelines python landing_zone/yellow_tripdata/pipeline.py
"""

import os

def incremental():
    print('incremental')

def backfill():
    print('backfill')

def main():
    print('pipeline here!')

if __name__ == '__main__':
    main()